# YouTube Downloader GUI

A simple graphical user interface (GUI) application built with Python and PyQt6 to download YouTube videos and audio using the powerful `yt-dlp` library.

<!-- Optional: Add a screenshot link here -->
<!-- ![Screenshot](link/to/your/screenshot.png) -->

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

1.  Download the latest `.exe` file from the [Releases](link/to/your/releases) page.
2.  Double-click the downloaded `.exe` file to run the application. No installation is required.

    **Note on Virus Detection:** Executables created with tools like PyInstaller are sometimes flagged as potentially unwanted programs (PUPs) or viruses by antivirus software. This can happen because the executable bundles Python and its libraries, which might trigger heuristic detection. The use of modules like `os` and `subprocess` for file system interaction (like opening the download folder) can also contribute. The code is open-source, so you can inspect it yourself. If you encounter a warning, you may need to add an exception in your antivirus software.

### Running from Source

1.  **Prerequisites:**

    - Python 3.8 or later.
    - `pip` (Python package installer).
    - `ffmpeg` (Required by `yt-dlp` for merging formats). Make sure it's installed and accessible in your system's PATH, or place the `ffmpeg.exe` (and related `.dll` files) in the `ffmpeg/bin` subdirectory alongside `downloader.py` if running from source, or ensure the PyInstaller build includes it correctly.

2.  **Clone the repository:**

    ```bash
    git clone https://github.com/SSujitX/Youtube-Downloader.git
    cd Youtube-Downloader

    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    _(You'll need to create a `requirements.txt` file. Based on your imports, it should contain at least:)_

    ```
    PyQt6>=6.0.0
    yt-dlp>=2023.0.0
    rich>=10.0.0
    ```

4.  **Run the application:**
    ```bash
    python youtube_gui.py
    ```

## Building the Executable (Optional)

If you want to build the executable yourself:

1.  Install PyInstaller: `pip install pyinstaller`
2.  Ensure `ffmpeg` binaries are correctly placed (e.g., in an `ffmpeg/bin` folder).
3.  Ensure the icon file (`yt.png`) is present.
4.  Run PyInstaller (adjust paths and options as needed):

    ```bash
    pyinstaller --onefile --windowed --icon=yt.png --add-data "ffmpeg;ffmpeg" --add-data "yt.png;." youtube_gui.py
    ```

    - `--onefile`: Creates a single executable file.
    - `--windowed`: Prevents the console window from appearing.
    - `--icon`: Sets the application icon.
    - `--add-data "ffmpeg;ffmpeg"`: Bundles the `ffmpeg` directory.
    - `--add-data "yt.png;."`: Bundles the icon file.

    The executable will be located in the `dist` folder.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgements

- **yt-dlp:** The core library used for interacting with YouTube and downloading videos. ([yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp))
- **PyQt6:** The GUI framework used to build the application interface. ([PyQt Website](https://www.riverbankcomputing.com/software/pyqt/))
- **Rich:** Used for enhanced logging in the backend. ([Rich GitHub](https://github.com/Textualize/rich))
