import os
import requests
import patoolib
import shutil
import tempfile
from rich.progress import Progress


def ffmpeg_dir_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg")


def ffmpeg_required_files():
    d = ffmpeg_dir_path()
    return [
        os.path.join(d, "bin", exe)
        for exe in ("ffmpeg.exe", "ffplay.exe", "ffprobe.exe")
    ]


def is_ffmpeg_ready():
    return all(os.path.isfile(f) for f in ffmpeg_required_files())


from rich.progress import (
    Progress,
    BarColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    TextColumn,
    FileSizeColumn,
)


import time


def download_with_progress(url, dest):
    with (
        requests.get(url, stream=True) as r,
        Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            DownloadColumn(),
            FileSizeColumn(),
            TextColumn("{task.fields[avg_speed]}"),
            TimeRemainingColumn(),
        ) as progress,
    ):
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        task = progress.add_task(
            f"{os.path.basename(dest)}", total=total, avg_speed="0 MB/s"
        )
        start_time = time.time()
        downloaded = 0
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    elapsed = time.time() - start_time
                    avg_speed = (
                        f"{downloaded / 1024 / 1024 / elapsed:.2f} MB/s"
                        if elapsed > 0
                        else "0 MB/s"
                    )
                    progress.update(task, advance=len(chunk), avg_speed=avg_speed)


import contextlib


import logging


def extract_and_move(archive, target_dir):
    with tempfile.TemporaryDirectory() as tmpdir:
        with (
            open(os.devnull, "w") as devnull,
            contextlib.redirect_stdout(devnull),
            contextlib.redirect_stderr(devnull),
        ):
            logging.getLogger("patoolib").setLevel(logging.WARNING)
            patoolib.extract_archive(archive, outdir=tmpdir)
        items = os.listdir(tmpdir)
        if len(items) != 1:
            raise RuntimeError(
                "Unexpected archive structure: more than one top-level item found."
            )
        src_dir = os.path.join(tmpdir, items[0])
        os.makedirs(target_dir, exist_ok=True)
        for item in os.listdir(src_dir):
            src, dst = os.path.join(src_dir, item), os.path.join(target_dir, item)
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.move(src, dst)
            else:
                shutil.move(src, dst)


def download_and_extract_ffmpeg():
    """
    Downloads and extracts ffmpeg if not already present. Returns the absolute ffmpeg directory path.
    """
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z"
    archive = "ffmpeg-git-essentials.7z"
    target_dir = ffmpeg_dir_path()
    if is_ffmpeg_ready():
        return target_dir
    download_with_progress(url, archive)
    extract_and_move(archive, target_dir)
    os.remove(archive)
    return target_dir


if __name__ == "__main__":
    print(download_and_extract_ffmpeg())
