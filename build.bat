@echo off
echo =======================================
echo Building Dynamic Theme Manager
echo =======================================

echo Installing required Python packages...
pip install -r requirements.txt
pip install pyinstaller pillow

echo Cleaning old build artifacts...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

python -m PyInstaller --noconfirm --clean DynamicThemeManager.spec

echo Build complete! The executable is located in dist/Dynamic Theme Manager/
pause
