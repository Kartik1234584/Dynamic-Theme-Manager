# Building Dynamic Theme Manager

This application can be converted into a standalone Windows `.exe` file using PyInstaller.
Follow these steps:

## Prerequisites
Ensure you have installed the requirements:
```bash
pip install -r requirements.txt
```

## Build Process
Run the following command in the terminal from the root directory of the project:

```bash
pyinstaller --noconfirm --onedir --windowed --add-data "assets;assets/" --name "DynamicThemeManager" main.py
```

### Explanation of flags:
- `--noconfirm`: Replace output directory without asking.
- `--onedir`: Create a one-folder bundle containing an executable (easier for debugging missing assets). You can use `--onefile` instead if you want a single exe.
- `--windowed`: Do not open a console window when the app runs (important for GUI apps).
- `--add-data`: Include the `assets` folder. Database and Settings folders will be created automatically in the runtime directory.
- `--name`: The name of the output executable.

## Output
After running the command, PyInstaller will create a `dist` folder.
Navigate to `dist/DynamicThemeManager/` and look for `DynamicThemeManager.exe`.

## Note
If you want a custom icon for your executable, use the `--icon` flag:
```bash
pyinstaller --noconfirm --onedir --windowed --add-data "assets;assets/" --icon "assets/icon.ico" --name "DynamicThemeManager" main.py
```
