# Dynamic Theme Manager

Dynamic Theme Manager is a professional, standalone Windows desktop application designed to automate and manage your desktop wallpapers and themes. It allows users to seamlessly import Microsoft Store themes, create custom categories, schedule wallpaper changes based on the time of day, and run quietly in the system tray.

---

## 🌟 Key Features

1. **Dashboard & Live Analytics**
   - View total imported themes, Microsoft Themes, and raw wallpapers at a glance.
   - See your current active wallpaper and resolution details.
   - Access a live activity log of recent changes.

2. **Microsoft Store Integration**
   - Automatically scans your PC's `AppData/Local/Microsoft/Windows/Themes` directory.
   - Extracts raw 4K wallpapers from installed Windows 10/11 themes.
   - **Refresh Button:** Instantly syncs any newly downloaded themes from the Microsoft Store without needing to restart the app.

3. **Time-of-Day Scheduler**
   - Allows you to set specific themes for different parts of the day.
   - **Morning (06:00 - 12:00)**
   - **Afternoon (12:00 - 18:00)**
   - **Evening (18:00 - 22:00)**
   - **Night (22:00 - 06:00)**
   - Automatically overrides the globally active theme when enabled.

4. **Background System Tray Execution**
   - Fully supports minimizing to the Windows System Tray (Taskbar).
   - Right-click context menu for quick actions: `Show`, `Next Wallpaper`, and `Quit`.
   - Continues rotating wallpapers silently in the background based on your chosen interval.

5. **Robust Database Architecture**
   - **100% Portable SQLite Database**: Uses a local `wallpapers.db` file instead of relying on heavy external SQL servers. 
   - Dynamically manages categories, wallpaper metadata, favorites, and history.

6. **Crash Logging & Error Handling**
   - Features a global exception hook. If the application encounters a fatal error, it safely logs the entire traceback to a `crash.log` file in the root directory for easy debugging.

---

## 🏗️ Technical Stack

- **Language:** Python 3.x
- **GUI Framework:** PyQt6
- **Database:** SQLite3 (Built-in)
- **Image Processing:** Pillow (PIL)
- **Packaging & Deployment:** PyInstaller & Inno Setup

---

## 📂 Project Structure

```text
Dynamic Theme Manager/
├── main.py                     # Entry point, AppCore logic, and Exception handlers
├── DynamicThemeManager.spec    # PyInstaller compilation instructions
├── build.bat                   # 1-Click script to build the executable
├── installer.iss               # Inno Setup script to create setup.exe
├── icon.ico / icon.png         # Custom application branding
├── splash.png                  # Loading splash screen image
├── core/
│   ├── database_manager.py     # SQLite connection and queries
│   ├── scheduler_manager.py    # Time-of-day logic (JSON backed)
│   ├── settings_manager.py     # Interacts with the DB settings table
│   ├── theme_scanner.py        # Scans Windows registry/AppData for themes
│   ├── thumbnail_manager.py    # Generates low-res previews for UI
│   └── wallpaper_manager.py    # Handles OS-level background changing
└── ui/
    ├── main_window.py          # Main PyQt6 Window & Sidebar layout
    ├── dashboard_tab.py        # Analytics, Live Preview, and Refresh actions
    ├── scheduler_tab.py        # UI for time-of-day rotation profiles
    └── ... (other tabs)
```

---

## 🚀 How to Build & Deploy

This project is fully configured for professional Windows distribution.

### Step 1: Compile the `.exe`
1. Navigate to the project root directory.
2. Double-click the **`build.bat`** file.
3. This script will automatically:
   - Install required packages (`pip install pyinstaller pillow PyQt6`).
   - Clean up any previous old builds.
   - Run PyInstaller using `DynamicThemeManager.spec`.
   - Output the compiled files into `dist/Dynamic Theme Manager/`.

### Step 2: Create the Windows Installer
1. Ensure you have **Inno Setup 6+** installed on your PC (Download from `jrsoftware.org`).
2. Open the **`installer.iss`** file in the Inno Setup Compiler.
3. Click **Build > Compile** (or the Green Play button).
4. Inno Setup will compress the `dist` folder and generate your final `DynamicThemeManager_Setup.exe` inside the newly created `Output` folder.

### Notes on Deployment
- The installer automatically requests proper write permissions for `cache`, `database`, `settings`, and `wallpapers` folders, ensuring the app won't crash when installed in `C:\Program Files\`.
- Because the database uses SQLite, users do not need Python or any external database engines installed on their PC. The installer is fully standalone!

---

## ⚙️ Developer Notes

- **Icons & Paths in PyInstaller:** When running as a PyInstaller executable, standard relative paths (like `os.path.abspath("icon.png")`) can break. The project handles this internally by detecting `sys.frozen` and dynamically adjusting paths to use `sys.executable`.
- **Modifying the Splash Screen:** The PyInstaller splash screen (`splash.png`) is automatically closed in `main.py` using `pyi_splash.close()` right before the main Qt window calls `.show()`.
- **Customizing Default Settings:** You can edit `core/scheduler_manager.py` to change the default hours for morning, afternoon, evening, and night.
