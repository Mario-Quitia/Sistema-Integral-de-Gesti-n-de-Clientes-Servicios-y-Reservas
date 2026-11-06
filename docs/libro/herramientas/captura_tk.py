"""
Capturas REALES de Software FJ con los controles (widgets) de Tkinter señalados.

Las imágenes de base son capturas reales en pantalla (docs/manual/capturas).
Para saber dónde está cada control se abre la misma ventana, con la misma
geometría, fuera del área visible y se leen las coordenadas de los widgets.
El archivo software_fj.log se respalda y se restaura.
Uso: python docs/libro/herramientas/captura_tk.py
"""
import ctypes
import os
import shutil
import sys
from ctypes import wintypes

ctypes.windll.shcore.SetProcessDpiAwareness(2)
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SALIDA = os.path.join(RAIZ, "docs", "libro", "img")
sys.path.insert(0, RAIZ)
os.chdir(RAIZ)
LOG = os.path.join(RAIZ, "software_fj.log")
shutil.copy2(LOG, LOG + ".respaldo_libro")

from PIL import Image, ImageDraw, ImageFont   # noqa: E402

from interfaz import VentanaPrincipal          # noqa: E402

user32, gdi32 = ctypes.windll.user32, ctypes.windll.gdi32
F = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 15)
ROJO, AZUL, VERDE, MORADO, NARANJA = (220, 38, 38), (37, 99, 235), (22, 163, 74), (124, 58, 237), (217, 119, 6)


class BMIH(ctypes.Structure):
    _fields_ = [("biSize", wintypes.DWORD), ("biWidth", wintypes.LONG), ("biHeight", wintypes.LONG),
                ("biPlanes", wintypes.WORD), ("biBitCount", wintypes.WORD), ("biCompression", wintypes.DWORD),
                ("biSizeImage", wintypes.DWORD), ("biXPelsPerMeter", wintypes.LONG),
                ("biYPelsPerMeter", wintypes.LONG), ("biClrUsed", wintypes.DWORD),
                ("biClrImportant", wintypes.DWORD)]


def foto(app):
    """Imagen del área de cliente de la ventana (sin barra de título) y su origen en pantalla."""
    app.update()
    h = int(app.wm_frame(), 16)
    wr = wintypes.RECT()
    user32.GetWindowRect(h, ctypes.byref(wr))
    w, hh = wr.right - wr.left, wr.bottom - wr.top
    hdc = user32.GetWindowDC(h)
    mem = gdi32.CreateCompatibleDC(hdc)
    bmp = gdi32.CreateCompatibleBitmap(hdc, w, hh)
    gdi32.SelectObject(mem, bmp)
    user32.PrintWindow(h, mem, 2)
    bi = BMIH(ctypes.sizeof(BMIH), w, -hh, 1, 32, 0, 0, 0, 0, 0, 0)
    buf = ctypes.create_string_buffer(w * hh * 4)
    gdi32.GetDIBits(mem, bmp, 0, hh, buf, ctypes.byref(bi), 0)
    img = Image.frombuffer("RGB", (w, hh), buf, "raw", "BGRX", 0, 1)
    gdi32.DeleteObject(bmp); gdi32.DeleteDC(mem); user32.ReleaseDC(h, hdc)
    # recorte al área de cliente (la parte que dibuja Tkinter)
    x0, y0 = app.winfo_rootx() - wr.left, app.winfo_rooty() - wr.top
    img = img.crop((x0, y0, x0 + app.winfo_width(), y0 + app.winfo_height()))
    return img, (app.winfo_rootx(), app.winfo_rooty())


MANUAL = os.path.join(RAIZ, "docs", "manual", "capturas")


def base(app, captura):
    """Captura real en pantalla tomada para el manual (misma geometría 1340x686).
    Su origen está desplazado (1, 31) píxeles por el borde y la barra de título."""
    app.update()
    img = Image.open(os.path.join(MANUAL, captura + ".png")).convert("RGB")
    return img, (app.winfo_rootx() - 1, app.winfo_rooty() - 31)


def marcar(img, origen, marcas, nombre, recorte=None):
    """marcas: lista de (widget, texto, color, posición de la etiqueta: 'arriba'|'abajo'|'derecha')."""
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    for w, texto, color, pos in marcas:
        w.update_idletasks()
        x, y = w.winfo_rootx() - origen[0], w.winfo_rooty() - origen[1]
        x1, y1 = x + w.winfo_width(), y + w.winfo_height()
        d.rectangle([x - 2, y - 2, x1 + 2, y1 + 2], outline=color + (255,), width=3)
        tw = d.textlength(texto, font=F) + 12
        if pos == "abajo":
            lx, ly = x, y1 + 4
        elif pos == "derecha":
            lx, ly = x1 + 6, y + (y1 - y) / 2 - 11
        else:
            lx, ly = x, y - 26
        d.rounded_rectangle([lx, ly, lx + tw, ly + 22], radius=5, fill=color + (255,))
        d.text((lx + 6, ly + 2), texto, font=F, fill="white")
    final = Image.alpha_composite(img.convert("RGBA"), capa).convert("RGB")
    if recorte:
        final = final.crop(recorte)
    final.save(os.path.join(SALIDA, nombre + ".png"))
    print("captura", nombre, final.size)


def main():
    app = VentanaPrincipal()
    app.geometry("1340x686+-3000+0")
    s = app.sistema
    for args in (("1032456789", "Laura Gómez", "laura.gomez@mail.com", "3104567890"),
                 ("80123456", "Andrés Pérez", "aperez@empresa.co", "6017654321"),
                 ("1019876543", "Camila Rodríguez", "camila.rodriguez@correo.com", "3125558899")):
        s.clientes.registrar(*args)
    s.servicios.registrar_sala("SAL-01", "Sala Ejecutiva", 50000, 12, 2)
    s.servicios.registrar_equipo("EQU-01", "Videobeam Epson", 35000, "Proyector", 1)
    app.update()

    # --- Clientes
    app.mostrar("clientes")
    c = app.vistas["clientes"]
    c.form.asignar({"identificacion": "79456123", "nombre": "Juan Martínez",
                    "correo": "jmartinez@outlook.com", "telefono": "3157771234"})
    app.update()
    img, o = base(app, "03_cliente_formulario")
    etiqueta_ident = c.form.controles["identificacion"].master.winfo_children()[0]
    marcar(img, o, [
        (c.form.master.master, "tk.Frame (Panel)", MORADO, "arriba"),
        (etiqueta_ident, "ttk.Label", VERDE, "derecha"),
        (c.form.controles["correo"], "ttk.Entry", AZUL, "abajo"),
        (c.botones["Guardar"], "ttk.Button", ROJO, "abajo"),
        (c.busqueda, "ttk.Entry", AZUL, "abajo"),
        (c.tabla.arbol, "ttk.Treeview (tabla)", NARANJA, "abajo"),
    ], "t_widgets_clientes")

    # --- Reservas
    app.mostrar("reservas")
    r = app.vistas["reservas"]
    r.form.asignar({"cliente": "1032456789 - Laura Gómez", "servicio": "SAL-01 - Sala Ejecutiva (Sala)",
                    "duracion": "3", "impuesto": "19", "descuento": "10"})
    import time
    fin = time.time() + 0.8
    while time.time() < fin:
        app.update()
    img, o = base(app, "28_reserva_cotizacion")
    marcar(img, o, [
        (r.form.controles["cliente"], "ttk.Combobox", MORADO, "arriba"),
        (r.form.controles["duracion"], "ttk.Entry", AZUL, "abajo"),
        (r._valores_costo["total"], "tk.Label", VERDE, "arriba"),
        (r.form.master.winfo_children()[-1], "ttk.Button (x2)", ROJO, "abajo"),
        (r.filtro, "ttk.Combobox", MORADO, "abajo"),
    ], "t_widgets_reservas")

    # --- Menú lateral
    app.mostrar("dashboard")
    img, o = base(app, "01_panel_vacio")
    lateral = app.botones_menu["dashboard"].master
    marcar(img, o, [
        (app.botones_menu["clientes"], "BotonMenu (tk.Label)", ROJO, "derecha"),
        (app.botones_menu["dashboard"], "activo", AZUL, "derecha"),
    ], "t_menu", recorte=(0, 31, lateral.winfo_width() + 232, lateral.winfo_height() + 31))
    app.destroy()


if __name__ == "__main__":
    try:
        main()
    finally:
        shutil.move(LOG + ".respaldo_libro", LOG)
