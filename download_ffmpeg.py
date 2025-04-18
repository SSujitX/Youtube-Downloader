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
    # Check for ffmpeg.exe directly in the ffmpeg folder
    return [os.path.join(d, "ffmpeg.exe")]


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
    # target_dir is the main 'ffmpeg' folder
    with tempfile.TemporaryDirectory() as tmpdir:
        # Suppress patoolib output
        with (
            open(os.devnull, "w") as devnull,
            contextlib.redirect_stdout(devnull),
            contextlib.redirect_stderr(devnull),
        ):
            logging.getLogger("patoolib").setLevel(logging.WARNING)
            patoolib.extract_archive(archive, outdir=tmpdir)

        # Find the extracted top-level folder
        items = os.listdir(tmpdir)
        if len(items) != 1 or not os.path.isdir(os.path.join(tmpdir, items[0])):
            raise RuntimeError(
                f"Unexpected archive structure: Expected one top-level directory, found: {items}"
            )
        extracted_root_dir = os.path.join(tmpdir, items[0])

        # Find the source 'bin' directory
        src_bin_dir = os.path.join(extracted_root_dir, "bin")
        if not os.path.isdir(src_bin_dir):
            raise RuntimeError(
                f"Could not find 'bin' directory within {extracted_root_dir}"
            )

        # Clean and ensure the final target directory exists
        if os.path.exists(target_dir):
            print(f"Cleaning existing target directory: {target_dir}")
            shutil.rmtree(target_dir)
        os.makedirs(target_dir)

        # Move all files from extracted 'bin' to the target directory
        print(f"Moving files from extracted 'bin' to {target_dir}")
        for item_name in os.listdir(src_bin_dir):
            src_item_path = os.path.join(src_bin_dir, item_name)
            dst_item_path = os.path.join(target_dir, item_name)
            if os.path.isfile(src_item_path):
                shutil.move(src_item_path, dst_item_path)
            # We ignore any subdirectories within bin, if they exist

        # The rest of tmpdir (including extracted_root_dir and its other contents)
        # will be deleted automatically.


def download_and_extract_ffmpeg():
    """
    Downloads and extracts ffmpeg if not already present. Removes ffplay and ffprobe.
    Returns the absolute ffmpeg directory path.
    """
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z"
    # Use a temporary filename for download to avoid conflict if script interrupted
    temp_archive = "ffmpeg-download.tmp.7z"
    target_dir = ffmpeg_dir_path()

    if is_ffmpeg_ready():
        print("FFmpeg already present.")
        return target_dir

    print("FFmpeg not found or incomplete. Downloading...")
    try:
        download_with_progress(url, temp_archive)
        print("Download complete. Extracting...")
        extract_and_move(temp_archive, target_dir)
        print("Extraction complete. Cleaning up executables...")

        # Delete ffplay.exe and ffprobe.exe from the target directory
        for exe_to_delete in ("ffplay.exe", "ffprobe.exe"):
            file_path = os.path.join(
                target_dir, exe_to_delete
            )  # Check in target_dir directly
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Removed {exe_to_delete}")
            except OSError as e:
                print(f"Warning: Could not remove {file_path}: {e}")

    except Exception as e:
        print(f"Error during download/extraction: {e}")
        # Attempt to clean up target dir if extraction failed partially
        if os.path.exists(target_dir):
            try:
                shutil.rmtree(target_dir)
                print(f"Cleaned up incomplete target directory: {target_dir}")
            except OSError as clean_e:
                print(
                    f"Warning: Could not clean up target directory {target_dir}: {clean_e}"
                )
        return None  # Indicate failure
    finally:
        # Ensure temporary archive is always removed
        if os.path.exists(temp_archive):
            try:
                os.remove(temp_archive)
                print(f"Removed temporary archive: {temp_archive}")
            except OSError as e:
                print(
                    f"Warning: Could not remove temporary archive {temp_archive}: {e}"
                )

    # Final check
    if is_ffmpeg_ready():
        print("FFmpeg setup complete.")
        return target_dir
    else:
        print("Error: FFmpeg setup failed. ffmpeg.exe not found after process.")
        return None


if __name__ == "__main__":
    print(download_and_extract_ffmpeg())
