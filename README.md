# Dynamic Theme Manager

> A focused Windows desktop app for turning your wallpaper collection into a living, automatically curated backdrop.

[![Platform](https://img.shields.io/badge/platform-Windows-0078D4?style=flat-square&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/UI-PyQt6-41CD52?style=flat-square&logo=qt&logoColor=white)](https://www.qt.io/qt-for-python)
[![SQLite](https://img.shields.io/badge/storage-SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

Dynamic Theme Manager scans wallpaper folders and installed Windows themes, organizes images into collections, and changes your desktop automatically. Choose a theme, set the rhythm, and let the app quietly handle the rest from the system tray.

## Highlights

| | Capability | What it does |
| --- | --- | --- |
| **01** | **Automatic rotation** | Change wallpapers on a fixed interval, from 30 seconds to a custom duration. |
| **02** | **Theme collections** | Organize wallpapers into collections such as Nature, Dark, Anime, Minimal, Cars, or Random. |
| **03** | **Microsoft theme sync** | Scan installed Windows themes and import their raw 4K wallpapers into the library. |
| **04** | **Time-of-day scheduling** | Assign different collections to morning, afternoon, evening, and night. |
| **05** | **Smart selection** | Shuffle wallpapers and avoid showing the same image repeatedly. |
| **06** | **Background operation** | Minimize to the system tray and use quick actions such as Show, Next Wallpaper, and Quit. |

## Preview

<p align="center">
   <img src="screenshots/Screenshot%202026-10-02%20023729.png" alt="Dynamic Theme Manager dashboard" width="850">
</p>

<p align="center">
   <img src="screenshots/Screenshot%202026-10-02%20023716.png" alt="Dynamic Theme Manager wallpaper library" width="420">
   <img src="screenshots/Screenshot%202026-10-02%20023703.png" alt="Dynamic Theme Manager themes view" width="420">
</p>

## Getting Started

### Requirements

- Windows 10 or later
- Python 3.x

### Run from source

```powershell
git clone <your-repository-url>
cd "theme changer"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

The application creates its local database and settings files as needed. Add wallpaper folders from the **Wallpapers** tab, then choose a collection and rotation interval from **Settings**.

## Build a Windows executable

The repository includes a PyInstaller configuration and a one-click build script:

```powershell
.\build.bat
```

The packaged application is written to `dist/Dynamic Theme Manager/`. For a distributable installer, open `installer.iss` with Inno Setup after building the application. More detail is available in [build_exe.md](build_exe.md).

## Project Structure

```text
.
├── core/                  # Database, scanning, scheduling, settings, and rotation logic
├── ui/                    # PyQt6 window, tabs, styles, and reusable components
├── utils/                 # Windows wallpaper and startup integration
├── wallpapers/            # Bundled wallpaper collections
├── settings/              # Local application preferences
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── build.bat              # PyInstaller build script
└── installer.iss          # Inno Setup installer definition
```

## Tech Stack

- **Python** for the application logic
- **PyQt6** for the desktop interface
- **SQLite** for portable local data storage
- **Pillow** for image processing and thumbnails
- **PyInstaller** and **Inno Setup** for Windows packaging

## Documentation

- [Build and packaging guide](build_exe.md)
- [Technical documentation](DOCUMENTATION.md)

## License

No license has been included yet.
