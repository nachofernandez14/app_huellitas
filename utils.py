import os 
import sys


def resource_path(relative_path):
    """Devuelve la ruta absoluta al recurso, compatible con PyInstaller"""
    try:
        # PyInstaller crea una carpeta temporal _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)