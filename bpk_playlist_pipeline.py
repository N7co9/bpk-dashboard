#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BPK Pipeline (MLX-Whisper + Pyannote Diarization)
- Resilient: SQLite state tracking, atomic writes, graceful shutdown, retry logic
- Scalable: Streaming playlist fetch, efficient memory management
- User-friendly: Rich progress UI, bundled logs, real-time stats
"""

import argparse
import contextlib
import datetime as dt
import gc
import inspect
import json
import logging
import os
os.environ.setdefault("TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD", "1")
import random
import re
import shutil
import signal
import sqlite3
import subprocess
import sys
import time
import warnings
from collections import deque
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

# -----------------------------
# Suppress noisy warnings
# -----------------------------
warnings.filterwarnings("ignore", category=UserWarning, module="pyannote")
warnings.filterwarnings("ignore", category=UserWarning, module="speechbrain")
warnings.filterwarnings("ignore", category=UserWarning, module="torchaudio")
warnings.filterwarnings("ignore", message=".*weights_only.*")

LOG = logging.getLogger("BPK_Pipeline")

# -----------------------------
# Graceful shutdown
# -----------------------------
class StopFlag:
    """Catches SIGINT/SIGTERM and sets a flag (no exception raised)."""
    def __init__(self):
        self.stop = False
        signal.signal(signal.SIGINT, self._handle)
        signal.signal(signal.SIGTERM, self._handle)

    def _handle(self, signum, frame):
        if not self.stop:
            LOG.warning("\n[STOP] Shutdown signal received. Finishing current video, then exiting...")
        self.stop = True


# -----------------------------
# Utilities
# -----------------------------
def now_utc_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()

def atomic_write_text(path: Path, text: str, encoding: str = "utf-8"):
    """Atomic write: tmp -> rename."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding=encoding)
    tmp.replace(path)

def append_jsonl(path: Path, obj: Dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def tail(s: str, max_chars: int = 4000) -> str:
    s = s or ""
    return s if len(s) <= max_chars else s[-max_chars:]

def normalize_url(url: str) -> str:
    url = url.replace("\\?", "?").replace("\\=", "=").replace("\\&", "&").replace("\\", "")
    return url.strip()

def word_count(text: str) -> int:
    return len([w for w in re.split(r"\s+", (text or "").strip()) if w])

def filter_hallucinations(segments: List[Dict]) -> List[Dict]:
    """Remove Whisper hallucinations (repetitive words > 60% of segment)."""
    clean = []
    for s in segments:
        text = (s.get("text") or "").strip()
        if not text:
            continue
        words = re.split(r"\s+", text)
        if len(words) > 5:
            most_common = max(set(words), key=words.count)
            if (words.count(most_common) / len(words)) > 0.6:
                continue
        clean.append(s)
    return clean

def is_likely_english_noise(text: str) -> bool:
    """Heuristic for outro/ad noise (high ASCII, sponsor keywords)."""
    t = (text or "").strip().lower()
    if not t:
        return False
    ascii_ratio = sum(1 for c in t if ord(c) < 128) / max(1, len(t))
    kws = ("support", "donate", "thanks", "producer", "produced", "music", "song",
           "lyrics", "watching", "subscribe")
    return ascii_ratio > 0.95 and any(k in t for k in kws)

def detect_outro_cutoff(segments: List[Dict], window_s: float) -> Optional[float]:
    """Detect outro by checking last N seconds for English noise."""
    if not segments:
        return None
    end_time = max(float(s.get("end", 0.0)) for s in segments)
    tail_start = max(0.0, end_time - float(window_s))
    tail_idx = [i for i, s in enumerate(segments) if float(s.get("start", 0.0)) >= tail_start]
    if not tail_idx:
        return None
    found_any = False
    for i in reversed(tail_idx):
        if is_likely_english_noise(segments[i].get("text", "")):
            found_any = True
            continue
        if found_any:
            return float(segments[i + 1].get("start", 0.0))
    return float(segments[tail_idx[0]].get("start", 0.0)) if found_any else None

def trim_segments_by_cutoff(segments: List[Dict], cutoff_s: Optional[float]) -> List[Dict]:
    if cutoff_s is None:
        return segments
    cutoff_s = float(cutoff_s)
    return [s for s in segments if float(s.get("end", 0.0)) <= cutoff_s]


# -----------------------------
# Tool resolution
# -----------------------------
def resolve_tool(explicit: Optional[str], stacher_default: Path, name: str) -> str:
    """Resolve tool path: explicit > Stacher dir > PATH."""
    if explicit:
        p = Path(explicit).expanduser()
        if p.exists():
            return str(p)
        raise FileNotFoundError(f"{name} not found at {p}")
    if stacher_default.exists():
        return str(stacher_default)
    which = shutil.which(name)
    if which:
        return which
    raise FileNotFoundError(f"{name} not found (neither {stacher_default} nor in PATH)")

def tool_env(stacher_dir: Path) -> Dict[str, str]:
    env = os.environ.copy()
    env["PATH"] = f"{stacher_dir}:{env.get('PATH','')}"
    env.setdefault("TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD", "1")
    return env


# -----------------------------
# Subprocess helpers
# -----------------------------
def run_cmd(
    cmd: List[str],
    *,
    env: Optional[Dict[str, str]] = None,
    timeout: Optional[int] = None,
) -> Tuple[int, str, str]:
    try:
        p = subprocess.run(
            cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, timeout=timeout,
        )
        return p.returncode, p.stdout or "", p.stderr or ""
    except subprocess.TimeoutExpired:
        return -1, "", "TimeoutExpired"
    except Exception as e:
        return -2, "", f"{type(e).__name__}: {e}"

def iter_cmd_stdout_lines(
    cmd: List[str],
    *,
    env: Optional[Dict[str, str]] = None,
    timeout: Optional[int] = None
) -> Iterable[str]:
    """Stream stdout line-by-line to avoid memory bloat."""
    start = time.time()
    with subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1) as p:
        assert p.stdout is not None
        for line in p.stdout:
            if timeout and (time.time() - start) > timeout:
                with contextlib.suppress(Exception):
                    p.kill()
                raise TimeoutError(f"Timeout while running: {' '.join(cmd)}")
            yield line.rstrip("\n")
        rc = p.wait()
        if rc != 0:
            err = ""
            if p.stderr:
                err = tail(p.stderr.read(), 4000)
            raise RuntimeError(f"Command failed rc={rc}: {' '.join(cmd)}\n{err}")


# -----------------------------
# SQLite state
# -----------------------------
class StateDB:
    """SQLite-based state tracker for videos (status, attempts, errors, timings)."""
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path), check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA synchronous=NORMAL;")
        self._init()

    def _init(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS videos (
          video_id TEXT PRIMARY KEY,
          status TEXT NOT NULL,
          last_stage TEXT,
          attempts INTEGER NOT NULL DEFAULT 0,
          last_error TEXT,
          started_ts TEXT,
          finished_ts TEXT,
          seconds REAL,
          words INTEGER
        );
        """)
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS meta (
          k TEXT PRIMARY KEY,
          v TEXT
        );
        """)
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()

    def get_total(self) -> Optional[int]:
        row = self.conn.execute("SELECT v FROM meta WHERE k='total'").fetchone()
        return int(row[0]) if row and row[0].isdigit() else None

    def set_total(self, n: int):
        self.conn.execute("INSERT OR REPLACE INTO meta(k,v) VALUES('total', ?)", (str(int(n)),))
        self.conn.commit()

    def status_of(self, vid: str) -> Optional[str]:
        row = self.conn.execute("SELECT status FROM videos WHERE video_id=?", (vid,)).fetchone()
        return row[0] if row else None

    def mark_in_progress(self, vid: str, stage: str):
        self.conn.execute("""
        INSERT INTO videos(video_id,status,last_stage,attempts,started_ts)
        VALUES(?, 'in_progress', ?, 1, ?)
        ON CONFLICT(video_id) DO UPDATE SET
          status='in_progress',
          last_stage=excluded.last_stage,
          attempts=videos.attempts+1,
          started_ts=excluded.started_ts;
        """, (vid, stage, now_utc_iso()))
        self.conn.commit()

    def mark_ok(self, vid: str, *, seconds: float, words: int):
        self.conn.execute("""
        UPDATE videos SET status='ok', finished_ts=?, seconds=?, words=?, last_error=NULL
        WHERE video_id=?;
        """, (now_utc_iso(), float(seconds), int(words), vid))
        self.conn.commit()

    def mark_failed(self, vid: str, *, stage: str, error: str):
        self.conn.execute("""
        INSERT INTO videos(video_id,status,last_stage,attempts,last_error,finished_ts)
        VALUES(?, 'failed', ?, 1, ?, ?)
        ON CONFLICT(video_id) DO UPDATE SET
          status='failed',
          last_stage=excluded.last_stage,
          attempts=videos.attempts+1,
          last_error=excluded.last_error,
          finished_ts=excluded.finished_ts;
        """, (vid, stage, tail(error, 8000), now_utc_iso()))
        self.conn.commit()


# -----------------------------
# yt-dlp helpers
# -----------------------------
def ytdlp_info(ytdlp: str, plugins_dir: Path, video_url: str, *, env: Dict[str, str]) -> Dict:
    cmd = [ytdlp, "--plugin-dirs", str(plugins_dir), "--no-playlist", "-J", video_url]
    rc, out, err = run_cmd(cmd, env=env, timeout=120)
    if rc != 0:
        LOG.warning("Metadata fetch failed (rc=%s): %s", rc, tail(err, 200))
        return {}
    try:
        return json.loads(out)
    except Exception:
        return {}

def download_best_audio(
    ytdlp: str,
    plugins_dir: Path,
    video_url: str,
    out_dir: Path,
    *,
    retries: int,
    socket_timeout: int,
    env: Dict[str, str],
) -> Path:
    """Download best audio; prefer --print after_move:filepath, fallback to directory scan."""
    out_dir.mkdir(parents=True, exist_ok=True)
    out_tmpl = str(out_dir / "%(id)s.%(ext)s")

    cmd = [
        ytdlp,
        "--plugin-dirs", str(plugins_dir),
        "--no-playlist",
        "-f", "bestaudio/best",
        "-o", out_tmpl,
        "--no-progress",
        "--no-warnings",
        "--retries", str(int(retries)),
        "--fragment-retries", str(int(retries)),
        "--socket-timeout", str(int(socket_timeout)),
        "--print", "after_move:filepath",
        video_url,
    ]

    rc, out, err = run_cmd(cmd, env=env, timeout=3600)
    if rc == 0:
        candidates = [ln.strip() for ln in out.splitlines() if ln.strip()]
        for c in reversed(candidates):
            p = Path(c)
            if p.exists() and p.is_file() and p.suffix not in (".part", ".ytdl"):
                return p

    if rc != 0:
        raise RuntimeError(f"yt-dlp download failed rc={rc}\n{tail(err, 4000)}")

    # Fallback: pick newest real file
    files = []
    for p in out_dir.glob("*.*"):
        if not p.is_file():
            continue
        if p.suffix in (".part", ".ytdl", ".json"):
            continue
        files.append(p)
    if not files:
        raise RuntimeError("Download finished but no usable audio file found.")
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0]


# -----------------------------
# ffmpeg
# -----------------------------
def to_16k_mono_wav(ffmpeg: str, in_path: Path, out_path: Path, *, env: Dict[str, str]):
    cmd = [
        ffmpeg, "-y", "-i", str(in_path),
        "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000",
        str(out_path),
    ]
    rc, out, err = run_cmd(cmd, env=env, timeout=3600)
    if rc != 0:
        raise RuntimeError(f"ffmpeg convert failed rc={rc}\n{tail(err, 4000)}")


# -----------------------------
# Diarization (pyannote)
# -----------------------------
def diarize_to_rttm(
    pipeline,
    wav_path: Path,
    out_rttm: Path,
    *,
    min_speakers: int,
    max_speakers: int,
):
    """Run pyannote diarization and write RTTM atomically."""
    diarization = pipeline(str(wav_path), min_speakers=min_speakers, max_speakers=max_speakers)
    out_rttm.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_rttm.with_suffix(out_rttm.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        diarization.write_rttm(f)
    tmp.replace(out_rttm)
    # Validate RTTM
    if not out_rttm.exists() or out_rttm.stat().st_size == 0:
        raise RuntimeError("Diarization produced empty or missing RTTM file.")


# -----------------------------
# Existing JSON validation
# -----------------------------
def is_valid_ok_json(path: Path) -> bool:
    """Check if JSON exists, is valid, and status='ok'."""
    if not path.exists():
        return False
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
        return (obj.get("metadata", {}).get("status") == "ok")
    except Exception:
        return False


# -----------------------------
# Retry wrapper
# -----------------------------
def with_retries(fn, *, attempts: int, base_sleep: float, jitter: float, retry_name: str):
    """Execute fn with exponential backoff on exceptions."""
    last_err = None
    for i in range(1, attempts + 1):
        try:
            return fn()
        except Exception as e:
            last_err = e
            if i >= attempts:
                raise
            sleep_s = base_sleep * (2 ** (i - 1)) + random.random() * jitter
            LOG.warning("%s failed (attempt %d/%d): %s | sleeping %.1fs",
                        retry_name, i, attempts, type(e).__name__, sleep_s)
            time.sleep(sleep_s)
    raise last_err  # pragma: no cover


# -----------------------------
# Main
# -----------------------------
def main():
    ap = argparse.ArgumentParser(
        description="BPK Pipeline: Resilient MLX-Whisper + Pyannote Diarization for massive playlists (macOS/Apple Silicon)"
    )
    ap.add_argument("--playlist-url", required=True, help="YouTube playlist URL")
    ap.add_argument("--out-dir", required=True, help="Output directory for JSON+RTTM")
    ap.add_argument("--tmp-dir", default="/tmp/bpk_pipeline", help="Temp directory for downloads")
    ap.add_argument("--state-dir", default=None, help="State directory (default: <out-dir>/.state)")

    ap.add_argument("--yt-dlp", dest="ytdlp_path", default=None, help="Explicit yt-dlp binary path")
    ap.add_argument("--ffmpeg", dest="ffmpeg_path", default=None, help="Explicit ffmpeg binary path")

    ap.add_argument("--whisper-model", default="mlx-community/whisper-large-v3-turbo", help="MLX Whisper model")
    ap.add_argument("--outro-window-s", type=int, default=180, help="Outro detection window (seconds)")

    ap.add_argument("--min-speakers", type=int, default=2, help="Minimum speakers for diarization")
    ap.add_argument("--max-speakers", type=int, default=12, help="Maximum speakers for diarization")
    ap.add_argument("--diarization-device", default="mps", help="Device for diarization (mps/cpu/cuda)")

    ap.add_argument("--retry-failed", action="store_true", help="Retry previously failed videos")
    ap.add_argument("--fail-fast", action="store_true", help="Exit on first video failure")
    ap.add_argument("--keep-temp", action="store_true", help="Keep temp files after processing")

    ap.add_argument("--ytdlp-retries", type=int, default=10, help="yt-dlp retry count")
    ap.add_argument("--ytdlp-socket-timeout", type=int, default=30, help="yt-dlp socket timeout (seconds)")

    ap.add_argument("--max-attempts-per-video", type=int, default=2, help="Max retry attempts per video")
    ap.add_argument("--sleep-s", type=float, default=0.3, help="Base sleep between videos (seconds)")
    ap.add_argument("--sleep-jitter-s", type=float, default=0.3, help="Random jitter added to sleep (seconds)")

    ap.add_argument("--manifest-refresh", action="store_true", help="Force rebuild of playlist manifest")
    ap.add_argument("--limit", type=int, default=0, help="Limit to first N videos (0=all)")
    args = ap.parse_args()

    # Logging: compact, suppress noisy libs
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("filelock").setLevel(logging.WARNING)

    stop = StopFlag()

    home = Path.home()
    stacher_dir = home / ".stacher"
    plugins_dir = stacher_dir / "yt_dlp_plugins"

    ytdlp = resolve_tool(args.ytdlp_path, stacher_dir / "yt-dlp", "yt-dlp")
    ffmpeg = resolve_tool(args.ffmpeg_path, stacher_dir / "ffmpeg", "ffmpeg")
    env = tool_env(stacher_dir)

    playlist_url = normalize_url(args.playlist_url)

    out_dir = Path(args.out_dir).expanduser().resolve()
    tmp_dir = Path(args.tmp_dir).expanduser().resolve()
    state_dir = Path(args.state_dir).expanduser().resolve() if args.state_dir else (out_dir / ".state")

    json_dir = out_dir / "json"
    rttm_dir = out_dir / "rttm"
    for d in (out_dir, tmp_dir, state_dir, json_dir, rttm_dir):
        d.mkdir(parents=True, exist_ok=True)

    events_jsonl = state_dir / "events.jsonl"
    errors_log = state_dir / "errors.log"
    manifest = state_dir / "playlist_ids.txt"
    db = StateDB(state_dir / "state.db")

    # Optional rich UI
    try:
        from rich.console import Console
        from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
        console = Console()
        use_rich = True
    except ImportError:
        console = None
        use_rich = False

    def log_event(level: str, msg: str, **fields):
        append_jsonl(events_jsonl, {"ts": now_utc_iso(), "level": level, "msg": msg, **fields})
        if level == "error":
            LOG.error(msg)
        elif level == "warn":
            LOG.warning(msg)
        else:
            LOG.info(msg)

    # 1) Build or reuse manifest (streaming)
    if args.manifest_refresh or not manifest.exists():
        log_event("info", "Building playlist manifest (streaming)...", playlist_url=playlist_url)
        cmd = [
            ytdlp,
            "--plugin-dirs", str(plugins_dir),
            "--flat-playlist",
            "--no-warnings",
            "--print", "id",
            playlist_url,
        ]
        seen = set()
        n = 0
        tmp_manifest = manifest.with_suffix(".txt.tmp")
        with tmp_manifest.open("w", encoding="utf-8") as f:
            for line in iter_cmd_stdout_lines(cmd, env=env, timeout=3600):
                vid = line.strip()
                if not vid or vid in seen:
                    continue
                seen.add(vid)
                f.write(vid + "\n")
                n += 1
                if args.limit and n >= args.limit:
                    break
        tmp_manifest.replace(manifest)
        db.set_total(n)
        log_event("info", f"Manifest ready: {n} videos.", total=n)

    # Load manifest total
    total = db.get_total()
    if total is None:
        total = sum(1 for _ in manifest.open("r", encoding="utf-8"))
        db.set_total(total)

    if args.limit and args.limit > 0:
        total = min(total, args.limit)

    # 2) Load models
    log_event("info", "Loading AI models (Whisper + Diarization)...", whisper_model=args.whisper_model)
    import mlx_whisper
    from pyannote.audio import Pipeline
    import torch

    diarization_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")
    diarization_pipeline.to(torch.device(args.diarization_device))
    log_event("info", "Models loaded.", device=args.diarization_device)

    # 3) Progress stats
    t_global = time.time()
    last_durations = deque(maxlen=30)
    ok_count = 0
    fail_count = 0
    skip_count = 0
    done_count = 0

    def eta_seconds(avg_s: float, remaining: int) -> Optional[float]:
        return (avg_s * remaining) if avg_s > 0 else None

    # 4) Processing loop
    def process_one(vid: str, idx: int):
        nonlocal ok_count, fail_count, skip_count, done_count

        out_json = json_dir / f"{vid}.json"
        out_rttm = rttm_dir / f"{vid}.rttm"
        video_url = f"https://www.youtube.com/watch?v={vid}"
        work = tmp_dir / vid

        # Skip logic: prefer JSON validity + RTTM existence
        if (is_valid_ok_json(out_json) and out_rttm.exists() and out_rttm.stat().st_size > 0
            and not args.retry_failed):
            skip_count += 1
            done_count += 1
            return

        st = db.status_of(vid)
        if st == "ok" and not args.retry_failed:
            skip_count += 1
            done_count += 1
            return
        if st == "failed" and not args.retry_failed:
            skip_count += 1
            done_count += 1
            return

        if stop.stop:
            raise SystemExit("Stop requested")

        if work.exists() and not args.keep_temp:
            shutil.rmtree(work, ignore_errors=True)
        work.mkdir(parents=True, exist_ok=True)

        stage = "start"
        t0 = time.time()
        db.mark_in_progress(vid, stage=stage)
        append_jsonl(events_jsonl, {"ts": now_utc_iso(), "video_id": vid, "event": "start", "i": idx, "n": total})

        try:
            # Stage: info
            stage = "info"
            info = ytdlp_info(ytdlp, plugins_dir, video_url, env=env)

            # Stage: download (with retry)
            stage = "download"
            def _dl():
                return download_best_audio(
                    ytdlp, plugins_dir, video_url, work,
                    retries=args.ytdlp_retries,
                    socket_timeout=args.ytdlp_socket_timeout,
                    env=env
                )
            audio_src = with_retries(
                _dl,
                attempts=max(1, args.max_attempts_per_video),
                base_sleep=1.0,
                jitter=0.5,
                retry_name="download"
            )

            # Stage: ffmpeg
            stage = "ffmpeg_16k"
            wav_16k = work / f"{vid}.16k.wav"
            to_16k_mono_wav(ffmpeg, audio_src, wav_16k, env=env)

            # Stage: asr
            stage = "asr_mlx"
            kwargs = {"path_or_hf_repo": args.whisper_model, "verbose": False}
            sig = None
            with contextlib.suppress(Exception):
                sig = inspect.signature(mlx_whisper.transcribe)
            if sig and "verbose" not in sig.parameters:
                kwargs.pop("verbose", None)

            transcribe_result = mlx_whisper.transcribe(str(wav_16k), **kwargs)

            segments = []
            for s in transcribe_result.get("segments", []) or []:
                start_s = float(s.get("start", 0.0) or 0.0)
                end_s = float(s.get("end", 0.0) or 0.0)
                if end_s < start_s:
                    continue
                text = (s.get("text", "") or "").strip()
                segments.append({"start": start_s, "end": end_s, "text": text})

            segments = filter_hallucinations(segments)
            cutoff = detect_outro_cutoff(segments, window_s=float(args.outro_window_s))
            kept = trim_segments_by_cutoff(segments, cutoff)
            transcript_text = "\n".join(s["text"] for s in kept if s.get("text")).strip()

            # Stage: diarization (with retry, REQUIRED)
            stage = "diarization"
            def _diarize():
                diarize_to_rttm(
                    diarization_pipeline,
                    wav_16k,
                    out_rttm,
                    min_speakers=args.min_speakers,
                    max_speakers=args.max_speakers,
                )
            with_retries(_diarize, attempts=3, base_sleep=2.0, jitter=1.0, retry_name="diarization")

            # Stage: write_json
            stage = "write_json"
            source_url = (info.get("webpage_url") if isinstance(info, dict) else None) or video_url
            diar_rel = str(out_rttm.relative_to(out_dir))
            payload = {
                "metadata": {
                    "source_url": source_url,
                    "video_id": vid,
                    "original_title": (info.get("title") if isinstance(info, dict) else "") or "",
                    "author": ((info.get("uploader") or info.get("channel")) if isinstance(info, dict) else "") or "",
                    "publish_date": None,
                    "video_length_seconds": (info.get("duration") if isinstance(info, dict) else 0) or 0,
                    "retrieval_timestamp_utc": now_utc_iso(),
                    "word_count": word_count(transcript_text),
                    "status": "ok",
                    "diarization_rttm_path": diar_rel,
                    "outro_cutoff_seconds": cutoff,
                    "whisper_model": args.whisper_model,
                },
                "transcript_text": transcript_text,
                "segments": kept,
            }
            atomic_write_text(out_json, json.dumps(payload, ensure_ascii=False, indent=2))

            seconds = time.time() - t0
            words = word_count(transcript_text)
            db.mark_ok(vid, seconds=seconds, words=words)
            append_jsonl(events_jsonl, {
                "ts": now_utc_iso(),
                "video_id": vid,
                "event": "ok",
                "seconds": round(seconds, 3),
                "words": words
            })
            ok_count += 1
            done_count += 1
            last_durations.append(seconds)

        except Exception as e:
            seconds = time.time() - t0
            msg = f"{type(e).__name__}: {e}"
            db.mark_failed(vid, stage=stage, error=msg)
            fail_payload = {
                "metadata": {
                    "video_id": vid,
                    "source_url": video_url,
                    "retrieval_timestamp_utc": now_utc_iso(),
                    "status": "failed",
                    "failure_stage": stage,
                },
                "failure": {"message": tail(msg, 2000)},
            }
            with contextlib.suppress(Exception):
                atomic_write_text(out_json, json.dumps(fail_payload, ensure_ascii=False, indent=2))
            with errors_log.open("a", encoding="utf-8") as f:
                f.write(f"[{now_utc_iso()}] {vid} {video_url}\nSTAGE={stage}\n{msg}\n\n")
            fail_count += 1
            done_count += 1
            last_durations.append(seconds)
            if args.fail_fast:
                raise

        finally:
            if not args.keep_temp:
                shutil.rmtree(work, ignore_errors=True)
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            if torch.backends.mps.is_available():
                torch.mps.empty_cache()
            time.sleep(max(0.05, args.sleep_s + random.random() * args.sleep_jitter_s))

    # Run with progress
    if use_rich and console:
        from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[cyan]{task.completed}/{task.total}"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            transient=False,
            console=console,
        ) as prog:
            task = prog.add_task("[green]Processing playlist", total=total)
            with manifest.open("r", encoding="utf-8") as f:
                for idx, line in enumerate(f, start=1):
                    if args.limit and idx > args.limit:
                        break
                    vid = line.strip()
                    if not vid:
                        prog.update(task, advance=1)
                        continue

                    avg = (sum(last_durations) / len(last_durations)) if last_durations else 0.0
                    remaining = max(0, total - done_count)
                    vpm = (ok_count / ((time.time() - t_global) / 60.0)) if (time.time() - t_global) > 0 else 0.0
                    prog.update(
                        task,
                        description=f"[green]✓{ok_count} [red]✗{fail_count} [yellow]↷{skip_count} [cyan]avg={avg:.1f}s [magenta]{vpm:.1f}vid/min",
                    )

                    try:
                        process_one(vid, idx)
                    except SystemExit:
                        log_event("warn", "Stop requested. Exiting after current progress.")
                        break
                    prog.update(task, advance=1)
                    if stop.stop:
                        log_event("warn", "Stop flag set. Stopping loop.")
                        break
    else:
        # plain mode
        with manifest.open("r", encoding="utf-8") as f:
            for idx, line in enumerate(f, start=1):
                if args.limit and idx > args.limit:
                    break
                vid = line.strip()
                if not vid:
                    continue
                avg = (sum(last_durations) / len(last_durations)) if last_durations else 0.0
                LOG.info("[%d/%d] vid=%s ok=%d fail=%d skip=%d avg=%.1fs",
                         idx, total, vid, ok_count, fail_count, skip_count, avg)
                try:
                    process_one(vid, idx)
                except SystemExit:
                    LOG.warning("Stop requested. Exiting.")
                    break
                if stop.stop:
                    LOG.warning("Stop flag set. Stopping loop.")
                    break

    elapsed = time.time() - t_global
    LOG.info("✅ Finished. ok=%d fail=%d skip=%d total_done=%d elapsed=%.1fs",
             ok_count, fail_count, skip_count, done_count, elapsed)
    db.close()


if __name__ == "__main__":
    main()

