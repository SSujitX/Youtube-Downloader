# YouTube Downloader GUI - Free & Open-Source Video/Audio Downloader

<p align="center">
  <a href="https://github.com/SSujitX/Youtube-Downloader/releases/latest"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/SSujitX/Youtube-Downloader"></a>
  <a href="https://opensource.org/licenses/MIT"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
  <img alt="Python Version" src="https://img.shields.io/badge/python-3.9%2B-blue.svg">
  <a href="https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2FSSujitX%2FYoutube-Downloader"><img src="https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2FSSujitX%2FYoutube-Downloader&label=Visitors&countColor=%23263759&style=flat" /></a>
</p>

Download YouTube videos and audio easily with this free, open-source graphical user interface (GUI) application. Built with Python and PyQt6, it leverages the powerful `yt-dlp` library to provide a simple way to save YouTube content directly to your computer (Windows, macOS, Linux).

<p align="center">
  <img alt="Screenshot" src="https://github.com/user-attachments/assets/efe0072d-d0ee-4eda-922b-f0b398e82c54">
</p>

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Using the Executable (Windows)](#using-the-executable-windows)
  - [Running from Source](#running-from-source)
- [Building the Executable (Optional)](#building-the-executable-optional)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- **Easy URL Input:** Paste YouTube video URLs directly.
- **Fetch Formats:** Retrieve available video and audio formats before downloading.
- **Format Selection:**
  - Choose to download the best available video quality (muxed with best audio).
  - Select specific video-only formats (will be muxed with best audio).
  - Choose to download the best available audio-only format.
  - Select specific audio-only formats.
- **Audio/Video Download:** Download either the full video or just the audio stream.
- **Cookie Support:** Option to use cookies from Firefox or Chrome to download age-restricted or private videos (requires browser login).
- **Custom Download Location:** Choose where to save your downloaded files.
- **Progress Display:** Real-time progress bar showing download percentage, speed, and size.
- **Open Download Folder:** Quickly open the folder containing your downloads.
- **Cross-Platform:** Should work on Windows, macOS, and Linux (executable provided for Windows).

## Getting Started

### Using the Executable (Windows)

1.  Download the latest `.exe` file from the [Releases](https://github.com/SSujitX/youtube-downloader/releases/tag/1.0) page.
2.  Double-click the downloaded `.exe` file to run the application. No installation is required.

    **Note on Virus Detection:** Executables created with tools like PyInstaller are sometimes flagged as potentially unwanted programs (PUPs) or viruses by antivirus software. This can happen because the executable bundles Python and its libraries, which might trigger heuristic detection. The use of modules like `os` and `subprocess` for file system interaction (like opening the download folder) can also contribute. The code is open-source, so you can inspect it yourself. If you encounter a warning, you may need to add an exception in your antivirus software.

### Running from Source

1.  **Prerequisites:**

    - Python 3.13 or later (as specified in `pyproject.toml`).
    - `uv` (Python package installer and virtual environment manager). You can install it following the instructions [here](https://github.com/astral-sh/uv#installation).
    - `ffmpeg` (Required by `yt-dlp` for merging formats). Make sure it's installed and accessible in your system's PATH, or place the `ffmpeg.exe` (and related `.dll` files) in the `ffmpeg/bin` subdirectory alongside `downloader.py` if running from source, or ensure the PyInstaller build includes it correctly.

2.  **Clone the repository:**

    ```bash
    git clone https://github.com/SSujitX/youtube-downloader.git
    cd youtube-downloader
    ```

3.  **Create a virtual environment and install dependencies:**

    It's recommended to use a virtual environment. `uv` can create one and sync dependencies from `pyproject.toml` and `uv.lock` in one step:

    ```bash
    # Create a virtual environment named .venv (if it doesn't exist)
    # and install dependencies from pyproject.toml/uv.lock
    uv sync
    ```

4.  **Run the application:**

    Activate the virtual environment first (the command depends on your shell, e.g., `.venv\\Scripts\\activate` on Windows Command Prompt/PowerShell, or `source .venv/bin/activate` on Linux/macOS/Git Bash). Then run:

    ```bash
    # Or, run directly using uv without activating the environment
    uv run python youtube_gui.py
    ```

## Building the Executable (Optional)

If you want to build the executable yourself:

1.  Ensure `uv` is installed and you have synced the environment (`uv sync`).
2.  Install PyInstaller into your environment: `uv run pip install pyinstaller`
3.  Ensure `ffmpeg` binaries are correctly placed (e.g., in an `ffmpeg/bin` folder).
4.  Ensure the icon file (`yt.ico` or `yt.png`) is present.
5.  Run PyInstaller using `uv run` (adjust paths and options as needed):

    ```bash
    # Example using yt.ico
    uv run pyinstaller --onefile --windowed --icon=yt.ico --add-data "ffmpeg;ffmpeg" --add-data "yt.ico;." youtube_gui.py

    # Example using yt.png
    # uv run pyinstaller --onefile --windowed --icon=yt.png --add-data "ffmpeg;ffmpeg" --add-data "yt.png;." youtube_gui.py
    ```

    - `--onefile`: Creates a single executable file.
    - `--windowed`: Prevents the console window from appearing.
    - `--icon`: Sets the application icon.
    - `--add-data "ffmpeg;ffmpeg"`: Bundles the `ffmpeg` directory.
    - `--add-data "yt.ico;."` or `--add-data "yt.png;."`: Bundles the icon file.

    The executable will be located in the `dist` folder.

## Contributing

Contributions are welcome! If you have suggestions for improvements or find any bugs, please feel free to open an issue or submit a pull request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgements

- **yt-dlp:** The core library used for interacting with YouTube and downloading videos. ([yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp))
- **PyQt6:** The GUI framework used to build the application interface. ([PyQt Website](https://www.riverbankcomputing.com/software/pyqt/))
- **Rich:** Used for enhanced logging in the backend. ([Rich GitHub](https://github.com/Textualize/rich))
