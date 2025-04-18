import os
import sys
import logging
import contextlib
import io
from yt_dlp import YoutubeDL
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import (
    Progress,
    BarColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
)

console = Console()


class YTVideoDownloader:
    def __init__(
        self, progress_hook=None, use_rich=True, browsers=None, download_dir=None
    ):
        # Resource path (ffmpeg, icons)
        if hasattr(sys, "_MEIPASS"):
            self.resource_path = sys._MEIPASS
        else:
            self.resource_path = os.path.dirname(os.path.abspath(sys.argv[0]))

        # Output path (downloads, logs) - always next to the executable
        if getattr(sys, "frozen", False):
            self.output_path = os.path.dirname(sys.executable)
        else:
            self.output_path = os.path.dirname(os.path.abspath(__file__))

        os.chdir(self.output_path)

        # Determine download directory
        if download_dir:
            self.download_dir = download_dir
        else:
            # Default download dir next to executable/script
            self.download_dir = os.path.join(self.output_path, "downloaded_videos")

        os.makedirs(self.download_dir, exist_ok=True)

        self.log_path = os.path.join(self.output_path, "yt_video_downloader.log")
        self.setup_logger()

        self.use_rich = use_rich
        self.external_hook = progress_hook
        self.progress = None
        self.browsers = browsers if browsers else []

        if self.use_rich:
            self.progress = Progress(
                "[progress.description]{task.description}",
                BarColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
                TimeRemainingColumn(),
                console=console,
                transient=True,
            )

    def setup_logger(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            handlers=[
                RichHandler(
                    console=console, show_time=False, show_level=False, show_path=False
                ),
                logging.FileHandler(self.log_path, mode="a", encoding="utf-8"),
            ],
        )
        self.logger = logging.getLogger("YTLogger")

    def get_formats(self, url: str) -> dict:
        self.logger.info(f"Attempting to fetch formats for: {url}")
        formats_list = []
        info = None
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "logger": self.logger,
            "socket_timeout": 30,
            "retries": 1,
            "extract_flat": "discard_in_playlist",
            "noplaylist": True,
            "geo_bypass": True,
            "age_limit": None,
            "cookiesfrombrowser": self.browsers if self.browsers else None,
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info and "formats" in info:
                    formats_list = info["formats"]
                    self.logger.info(
                        f"Successfully fetched {len(formats_list)} format entries."
                    )
                else:
                    self.logger.warning("No formats found in extracted info.")

            return {"status": True, "formats": formats_list, "info": info}
        except Exception as e:
            self.logger.error(f"Failed to fetch formats: {e}")
            return {"status": False, "message": f"Failed to fetch formats: {e}"}

    def download_video(self, url: str, format_string: str | None = None) -> dict:
        ffmpeg_path = os.path.join(self.resource_path, "ffmpeg", "ffmpeg.exe")
        final_path = {"file": None}
        task_id = [None]

        def default_progress(d):
            if d.get("status") == "downloading":
                if not self.use_rich:
                    if d.get("filename"):
                        final_path["file"] = d["filename"]
                    return

                if task_id[0] is None:
                    filename = os.path.basename(d.get("filename", "video"))
                    task_id[0] = self.progress.add_task(
                        f"Downloading: {filename}", total=d.get("total_bytes", 0)
                    )
                self.progress.update(task_id[0], completed=d.get("downloaded_bytes", 0))
                if d.get("filename"):
                    final_path["file"] = d["filename"]
            elif d.get("status") == "finished":
                if d.get("filename"):
                    final_path["file"] = d["filename"]
                elif d.get("filepath"):
                    final_path["file"] = d["filepath"]
                if self.use_rich and self.progress:
                    self.progress.stop()

        effective_format = (
            format_string or "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        )
        self.logger.info(f"Using format selection: {effective_format}")

        ydl_opts = {
            "format": effective_format,
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(self.download_dir, "%(title)s.%(ext)s"),
            "ffmpeg_location": ffmpeg_path,
            "progress_hooks": [self.external_hook or default_progress],
            "quiet": True,
            "no_warnings": True,
            "socket_timeout": 30,
            "retries": 3,
            "fragment_retries": 3,
            "extractor_retries": 3,
            "noplaylist": True,
            "geo_bypass": True,
            "age_limit": None,
            "logger": self.logger,
            "progress_with_newline": False,
            "consoletitle": False,
        }

        if self.browsers:
            self.logger.info(f"Attempting to use cookies from: {self.browsers}")
            ydl_opts["cookiesfrombrowser"] = self.browsers
        else:
            self.logger.info("Cookies not requested.")

        try:
            with YoutubeDL(ydl_opts) as ydl:
                if self.use_rich and self.progress:
                    with self.progress:
                        with contextlib.redirect_stdout(io.StringIO()):
                            ydl.download([url])
                else:
                    with contextlib.redirect_stdout(io.StringIO()):
                        ydl.download([url])

            if not final_path["file"]:
                files = sorted(
                    [f for f in os.listdir(self.download_dir) if f.endswith(".mp4")],
                    key=lambda f: os.path.getmtime(os.path.join(self.download_dir, f)),
                    reverse=True,
                )
                if files:
                    final_path["file"] = os.path.join(self.download_dir, files[0])

            return {
                "status": True,
                "message": "Download succeeded",
                "filepath": final_path["file"],
            }

        except Exception as e:
            self.logger.error(f">= Download failed: {e}")
            error_message = f"Download failed: {e}"
            if self.browsers:
                error_message += f" (Tried using cookies from: {self.browsers})"
            return {
                "status": False,
                "message": error_message,
                "filepath": None,
            }
