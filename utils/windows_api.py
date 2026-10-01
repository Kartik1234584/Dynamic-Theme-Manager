import ctypes
import os
import platform

SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDWININICHANGE = 0x02

def set_wallpaper(image_path):
    """Changes the Windows desktop wallpaper."""
    if not os.path.exists(image_path):
        return False
        
    try:
        if platform.system() == "Windows":
            # Using SystemParametersInfoW for Unicode paths (recommended)
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 
                0, 
                image_path, 
                SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
            )
            return True
        return False
    except Exception as e:
        print(f"Error setting wallpaper: {e}")
        return False

def add_to_startup(app_name, exe_path):
    """Adds the application to Windows startup registry."""
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Failed to add to startup: {e}")
        return False

def remove_from_startup(app_name):
    """Removes the application from Windows startup registry."""
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, app_name)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Failed to remove from startup: {e}")
        return False
