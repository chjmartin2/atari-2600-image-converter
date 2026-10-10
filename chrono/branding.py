"""Shared application artwork, resolved in source and frozen bundles."""
from pathlib import Path
from PIL import Image, ImageTk

ASSETS = Path(__file__).resolve().parent / "resources" / "branding"

def photo(name, size, master):
    with Image.open(ASSETS / name) as image:
        image = image.convert("RGBA")
        image.thumbnail(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image, master=master)

def install_window_icon(window):
    window._brand_icons = [photo("icon.png", (size, size), window) for size in (256, 48, 32, 16)]
    window.iconphoto(True, *window._brand_icons)
    if window.tk.call("tk", "windowingsystem") == "win32":
        window.iconbitmap(default=str(ASSETS / "app.ico"))
