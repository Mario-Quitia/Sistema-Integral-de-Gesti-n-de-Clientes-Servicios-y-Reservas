"""
Captura REAL de archivos del proyecto abiertos en Visual Studio Code.

Abre cada archivo en una ventana NUEVA de VS Code (no toca las ventanas que
ya estén abiertas), la fotografía y la cierra.
Uso: python docs/libro/herramientas/captura_vscode.py
"""
import ctypes
import os
import subprocess
import time
from ctypes import wintypes

from PIL import ImageGrab

ctypes.windll.shcore.SetProcessDpiAwareness(2)
user32 = ctypes.windll.user32
dwmapi = ctypes.windll.dwmapi
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SALIDA = os.path.join(RAIZ, "docs", "libro", "img")
os.makedirs(SALIDA, exist_ok=True)
CODE = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\bin\code.cmd")
WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

ARCHIVOS = [  # (nombre de salida, ruta, línea)
    ("vscode_main", "main.py", 1),
    ("vscode_cliente", "modelos/cliente.py", 1),
    ("vscode_servicios", "modelos/servicios.py", 180),
    ("vscode_ventana", "interfaz/ventana_principal.py", 40),
]


def titulo(h):
    n = user32.GetWindowTextLengthW(h)
    b = ctypes.create_unicode_buffer(n + 1)
    user32.GetWindowTextW(h, b, n + 1)
    return b.value


def ventanas_code():
    res = []

    def cb(h, _):
        if user32.IsWindowVisible(h) and titulo(h).endswith("Visual Studio Code"):
            res.append(h)
        return True
    user32.EnumWindows(WNDENUMPROC(cb), 0)
    return res


def foto_ventana(h):
    """Copia el contenido de la ventana aunque otra ventana la tape (PrintWindow)."""
    from PIL import Image
    gdi32 = ctypes.windll.gdi32
    l, t, r, b = rect(h)
    wr = wintypes.RECT()
    user32.GetWindowRect(h, ctypes.byref(wr))
    ancho, alto = wr.right - wr.left, wr.bottom - wr.top
    hdc = user32.GetWindowDC(h)
    mem = gdi32.CreateCompatibleDC(hdc)
    bmp = gdi32.CreateCompatibleBitmap(hdc, ancho, alto)
    gdi32.SelectObject(mem, bmp)
    user32.PrintWindow(h, mem, 2)               # PW_RENDERFULLCONTENT
    class BMIH(ctypes.Structure):
        _fields_ = [("biSize", wintypes.DWORD), ("biWidth", wintypes.LONG), ("biHeight", wintypes.LONG),
                    ("biPlanes", wintypes.WORD), ("biBitCount", wintypes.WORD),
                    ("biCompression", wintypes.DWORD), ("biSizeImage", wintypes.DWORD),
                    ("biXPelsPerMeter", wintypes.LONG), ("biYPelsPerMeter", wintypes.LONG),
                    ("biClrUsed", wintypes.DWORD), ("biClrImportant", wintypes.DWORD)]
    bi = BMIH(ctypes.sizeof(BMIH), ancho, -alto, 1, 32, 0, 0, 0, 0, 0, 0)
    buf = ctypes.create_string_buffer(ancho * alto * 4)
    gdi32.GetDIBits(mem, bmp, 0, alto, buf, ctypes.byref(bi), 0)
    img = Image.frombuffer("RGB", (ancho, alto), buf, "raw", "BGRX", 0, 1)
    gdi32.DeleteObject(bmp); gdi32.DeleteDC(mem); user32.ReleaseDC(h, hdc)
    # recorta el borde invisible para quedar igual que el marco visible
    return img.crop((l - wr.left, t - wr.top, r - wr.left, b - wr.top))


def rect(h):
    r = wintypes.RECT()
    dwmapi.DwmGetWindowAttribute(h, 9, ctypes.byref(r), ctypes.sizeof(r))
    return r.left, r.top, r.right, r.bottom


import sys
SOLO = set(sys.argv[1:])
for nombre, ruta, linea in ARCHIVOS:
    if SOLO and nombre not in SOLO:
        continue
    antes = set(ventanas_code())
    archivo = os.path.join(RAIZ, ruta)
    subprocess.Popen([CODE, "-n", "-g", f"{archivo}:{linea}"], shell=False)
    h, limite = None, time.time() + 40
    base = os.path.basename(ruta)
    while time.time() < limite:
        nuevas = [w for w in ventanas_code() if w not in antes and base in titulo(w)]
        nuevas = [w for w in nuevas if (lambda r: (r[2] - r[0]) > 600)(rect(w))]
        if nuevas:
            h = nuevas[0]
            break
        time.sleep(0.5)
    if not h:
        print("No se abrió la ventana para", ruta)
        continue
    user32.ShowWindow(h, 9)
    user32.MoveWindow(h, 0, 0, 1366, 728, True)
    user32.SetForegroundWindow(h)
    time.sleep(6)                       # resaltado de sintaxis y carga completa
    user32.SetForegroundWindow(h)
    time.sleep(1)
    for _intento in range(5):           # reintenta si la ventana aún no se dibujó
        img = foto_ventana(h)
        if img.convert("L").getextrema()[1] > 60:
            break
        time.sleep(3)
    img.save(os.path.join(SALIDA, nombre + ".png"))
    print("captura", nombre, titulo(h))
    user32.PostMessageW(h, 0x0010, 0, 0)   # WM_CLOSE
    time.sleep(3)
