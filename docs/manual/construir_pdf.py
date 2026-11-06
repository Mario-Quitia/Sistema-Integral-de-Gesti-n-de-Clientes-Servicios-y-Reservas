"""
Genera el PDF «Manual de Usuario y Funciones» de Software FJ.

Requiere las capturas reales creadas por captura.py (carpeta capturas/)
y los datos de la portada (datos_portada.json).

Uso:  python docs/manual/construir_pdf.py
Salida: docs/Manual_Usuario_Software_FJ.pdf
"""
import json
import os
import sys

from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame, Image, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate, Paragraph, Preformatted,
                                Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

AQUI = os.path.dirname(os.path.abspath(__file__))
PROYECTO = os.path.abspath(os.path.join(AQUI, "..", ".."))
CAPT = os.path.join(AQUI, "capturas")
ANOT = os.path.join(AQUI, "anotadas")
SALIDA = os.path.join(PROYECTO, "docs", "Manual_Usuario_Software_FJ.pdf")
os.makedirs(ANOT, exist_ok=True)
sys.path.insert(0, PROYECTO)

with open(os.path.join(AQUI, "datos_portada.json"), encoding="utf-8") as f:
    PORTADA = json.load(f)

# ------------------------------------------------------------------ fuentes y colores
FUENTES = "C:/Windows/Fonts/"
for nombre, archivo in (("Segoe", "segoeui.ttf"), ("Segoe-B", "segoeuib.ttf"), ("Segoe-I", "segoeuii.ttf"),
                        ("Segoe-BI", "segoeuiz.ttf"), ("Segoe-SB", "seguisb.ttf"), ("Segoe-L", "segoeuil.ttf"),
                        ("Consolas", "consola.ttf"), ("Consolas-B", "consolab.ttf")):
    pdfmetrics.registerFont(TTFont(nombre, FUENTES + archivo))
pdfmetrics.registerFontFamily("Segoe", normal="Segoe", bold="Segoe-B", italic="Segoe-I", boldItalic="Segoe-BI")
pdfmetrics.registerFontFamily("Consolas", normal="Consolas", bold="Consolas-B", italic="Consolas",
                              boldItalic="Consolas-B")

C = {k: colors.HexColor(v) for k, v in {
    "navy": "#0f172a", "navy2": "#1e293b", "azul": "#2563eb", "azul_osc": "#1d4ed8", "azul_cl": "#dbeafe",
    "azul_bg": "#eff6ff", "texto": "#1e293b", "suave": "#64748b", "borde": "#e2e8f0", "fondo": "#f8fafc",
    "verde": "#16a34a", "verde_bg": "#f0fdf4", "naranja": "#d97706", "naranja_bg": "#fffbeb",
    "rojo": "#dc2626", "rojo_bg": "#fef2f2", "turq": "#0891b2", "turq_bg": "#ecfeff", "morado": "#7c3aed",
    "teal": "#0d9488", "dorado": "#ca8a04", "gris": "#94a3b8"}.items()}

ANCHO, ALTO = A4
MARGEN = 20 * mm
ANCHO_UTIL = ANCHO - 2 * MARGEN

# ------------------------------------------------------------------ estilos
def estilo(nombre, **kw):
    base = dict(fontName="Segoe", fontSize=10, leading=14.5, textColor=C["texto"], spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(nombre, **base)


E = {
    "cuerpo": estilo("cuerpo", alignment=TA_LEFT),
    "h2": estilo("h2", fontName="Segoe-B", fontSize=14.5, leading=19, textColor=C["navy"],
                 spaceBefore=12, spaceAfter=6, keepWithNext=1),
    "h3": estilo("h3", fontName="Segoe-SB", fontSize=11.5, leading=15, textColor=C["azul_osc"],
                 spaceBefore=8, spaceAfter=4, keepWithNext=1),
    "vineta": estilo("vineta", leftIndent=14, bulletIndent=3, spaceAfter=3),
    "pie": estilo("pie", fontName="Segoe-I", fontSize=8.5, leading=11, textColor=C["suave"],
                  alignment=TA_CENTER, spaceBefore=4, spaceAfter=12),
    "celda": estilo("celda", fontSize=8.8, leading=11.8, spaceAfter=0),
    "celda_b": estilo("celda_b", fontName="Segoe-B", fontSize=8.8, leading=11.8, spaceAfter=0),
    "celda_h": estilo("celda_h", fontName="Segoe-B", fontSize=8.8, leading=11.8, spaceAfter=0,
                      textColor=colors.white),
    "paso": estilo("paso", spaceAfter=0, leading=14),
    "aviso": estilo("aviso", fontSize=9.4, leading=13.2, spaceAfter=0),
    "aviso_t": estilo("aviso_t", fontName="Segoe-B", fontSize=8.5, leading=11, spaceAfter=2),
    "toc0": estilo("toc0", fontName="Segoe-B", fontSize=10.5, leading=15, spaceBefore=6, spaceAfter=0),
    "toc1": estilo("toc1", fontSize=9.5, leading=13, leftIndent=18, spaceAfter=0, textColor=C["suave"]),
    "intro": estilo("intro", fontName="Segoe-L", fontSize=12, leading=17.5, textColor=C["suave"],
                    spaceAfter=10),
}


def P(texto, st="cuerpo"):
    return Paragraph(texto, E[st] if isinstance(st, str) else st)


def B(texto):
    """Nombre de un botón o elemento de la pantalla."""
    return f'<font name="Segoe-B" color="#1d4ed8">{texto}</font>'


def K(texto):
    """Texto que el usuario escribe o ve literalmente."""
    return f'<font name="Consolas" color="#0f172a" backColor="#f1f5f9">&nbsp;{texto}&nbsp;</font>'


def vinetas(items):
    return [Paragraph(t, E["vineta"], bulletText="•") for t in items]


# ------------------------------------------------------------------ flowables propios
class Capitulo(Flowable):
    """Encabezado de capítulo con número grande y franja de color."""

    def __init__(self, numero, titulo, resumen=""):
        super().__init__()
        self.numero, self.titulo, self.resumen = numero, titulo, resumen
        self.alto = 58 * mm

    def wrap(self, aw, ah):
        return aw, self.alto

    def draw(self, ):
        c = self.canv
        c.saveState()
        trazo = c.beginPath()
        trazo.roundRect(0, 0, ANCHO_UTIL, self.alto, 8)
        c.clipPath(trazo, stroke=0, fill=0)
        c.setFillColor(C["navy"])
        c.roundRect(0, 0, ANCHO_UTIL, self.alto, 8, stroke=0, fill=1)
        c.setFillColor(C["azul"])
        c.roundRect(0, 0, 9, self.alto, 4, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#1e3a8a"))
        c.circle(ANCHO_UTIL - 18 * mm, self.alto - 6 * mm, 30 * mm, stroke=0, fill=1)
        c.setFillColor(C["azul"])
        c.circle(ANCHO_UTIL - 4 * mm, 2 * mm, 16 * mm, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#93c5fd"))
        c.setFont("Segoe-B", 10)
        etiqueta = "ANEXO" if not str(self.numero).isdigit() else "CAPÍTULO"
        c.drawString(12 * mm, self.alto - 14 * mm, f"{etiqueta} {self.numero}")
        c.setFillColor(colors.white)
        c.setFont("Segoe-B", 25)
        c.drawString(12 * mm, self.alto - 27 * mm, self.titulo)
        if self.resumen:
            p = Paragraph(self.resumen, estilo("res", fontName="Segoe-L", fontSize=10.5, leading=14.5,
                                                textColor=colors.HexColor("#cbd5e1")))
            w, h = p.wrap(ANCHO_UTIL - 60 * mm, 40 * mm)
            p.drawOn(c, 12 * mm, self.alto - 33 * mm - h)
        c.restoreState()


def S(texto):
    return [CondPageBreak(55 * mm), Seccion(texto)]


def H3(texto):
    return [CondPageBreak(40 * mm), P(texto, "h3")]


class Seccion(Paragraph):
    """Subtítulo que se registra en el índice."""

    def __init__(self, texto):
        super().__init__(texto, E["h2"])
        self.texto_toc = texto


class NumeroPaso(Flowable):
    def __init__(self, n, color=None):
        super().__init__()
        self.n, self.color = n, color or C["azul"]

    def wrap(self, aw, ah):
        return 20, 20

    def draw(self):
        c = self.canv
        c.setFillColor(self.color)
        c.circle(10, 10, 9.5, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Segoe-B", 9.5)
        c.drawCentredString(10, 6.7, str(self.n))


def pasos(lista, titulo=None):
    filas = [[NumeroPaso(i), P(t, "paso")] for i, t in enumerate(lista, 1)]
    t = Table(filas, colWidths=[28, ANCHO_UTIL - 28])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 0)]))
    salida = []
    if titulo:
        salida.append(P(titulo, "h3"))
    salida += [t, Spacer(1, 4)]
    return salida


AVISOS = {
    "nota": ("NOTA", C["azul"], C["azul_bg"]),
    "importante": ("IMPORTANTE", C["naranja"], C["naranja_bg"]),
    "consejo": ("CONSEJO", C["verde"], C["verde_bg"]),
    "atencion": ("ATENCIÓN", C["rojo"], C["rojo_bg"]),
    "ejemplo": ("EJEMPLO PRÁCTICO", C["morado"], colors.HexColor("#f5f3ff")),
}


def aviso(tipo, texto, titulo=None):
    rotulo, color, fondo = AVISOS[tipo]
    contenido = [Paragraph(titulo or rotulo, estilo("at", parent=E["aviso_t"], textColor=color))]
    for parrafo in (texto if isinstance(texto, list) else [texto]):
        contenido.append(parrafo if isinstance(parrafo, Flowable) else P(parrafo, "aviso"))
    t = Table([[contenido]], colWidths=[ANCHO_UTIL])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), fondo),
                           ("LINEBEFORE", (0, 0), (0, -1), 3.5, color),
                           ("LEFTPADDING", (0, 0), (-1, -1), 11), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return KeepTogether([Spacer(1, 3), t, Spacer(1, 8)])


def tabla(encabezado, filas, anchos, color=None, negrita_col0=False, estilos_extra=None):
    datos = [[P(h, "celda_h") for h in encabezado]]
    for fila in filas:
        datos.append([c if isinstance(c, Flowable) else
                      P(str(c), "celda_b" if (negrita_col0 and i == 0) else "celda")
                      for i, c in enumerate(fila)])
    anchos = [ANCHO_UTIL * a for a in anchos]
    t = Table(datos, colWidths=anchos, repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), color or C["navy"]),
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LINEBELOW", (0, 0), (-1, -1), 0.5, C["borde"]),
          ("BOX", (0, 0), (-1, -1), 0.5, C["borde"]),
          ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
          ("TOPPADDING", (0, 0), (-1, -1), 4.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]
    for i in range(1, len(datos)):
        if i % 2 == 0:
            st.append(("BACKGROUND", (0, i), (-1, i), C["fondo"]))
    st += estilos_extra or []
    t.setStyle(TableStyle(st))
    return [t, Spacer(1, 10)]


# ------------------------------------------------------------------ figuras
CONTADOR = {"fig": 0}


def _imagen(ruta, ancho_max, alto_max=None):
    w, h = PILImage.open(ruta).size
    ancho = min(ancho_max, w * 0.75)
    alto = h * ancho / w
    if alto_max and alto > alto_max:
        alto = alto_max
        ancho = w * alto / h
    return Image(ruta, width=ancho, height=alto)


def _marco(img):
    t = Table([[img]])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#cbd5e1")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return t


def fig(nombre, pie, ancho=None, carpeta=CAPT, alto_max=None):
    CONTADOR["fig"] += 1
    ruta = os.path.join(carpeta, nombre + ".png")
    img = _imagen(ruta, ancho or ANCHO_UTIL, alto_max)
    return KeepTogether([Spacer(1, 4), _marco(img),
                         P(f'<font name="Segoe-B">Figura {CONTADOR["fig"]}.</font> {pie}', "pie")])


def fig_doble(n1, n2, pie, carpeta=CAPT):
    """Dos imágenes lado a lado (normalmente dos cuadros de diálogo)."""
    CONTADOR["fig"] += 1
    col = (ANCHO_UTIL - 10) / 2
    i1 = _marco(_imagen(os.path.join(carpeta, n1 + ".png"), col))
    i2 = _marco(_imagen(os.path.join(carpeta, n2 + ".png"), col))
    t = Table([[i1, i2]], colWidths=[col + 5, col + 5])
    t.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    return KeepTogether([Spacer(1, 4), t,
                         P(f'<font name="Segoe-B">Figura {CONTADOR["fig"]}.</font> {pie}', "pie")])


with open(os.path.join(CAPT, "coords.json"), encoding="utf-8") as f:
    COORDS = json.load(f)
FUENTE_PIL = ImageFont.truetype(FUENTES + "segoeuib.ttf", 17)
ROJO = (220, 38, 38)


def anotar(captura, origen, marcas, salida):
    """Dibuja recuadros numerados sobre una captura real usando las coordenadas guardadas."""
    im = PILImage.open(os.path.join(CAPT, captura + ".png")).convert("RGB")
    capa = PILImage.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    zonas = COORDS[origen]["zonas"]
    for numero, clave in enumerate(marcas, 1):
        x0, y0, x1, y1 = zonas[clave]
        d.rounded_rectangle([x0 - 1, y0 - 1, x1 + 1, y1 + 1], radius=7, outline=ROJO + (255,), width=3)
    for numero, clave in enumerate(marcas, 1):
        x0, y0, _x1, _y1 = zonas[clave]
        cx, cy = min(max(x0 + 2, 16), im.size[0] - 16), min(max(y0 + 2, 16), im.size[1] - 16)
        d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=ROJO + (255,), outline=(255, 255, 255, 255),
                  width=3)
        d.text((cx, cy - 1), str(numero), fill="white", font=FUENTE_PIL, anchor="mm")
    PILImage.alpha_composite(im.convert("RGBA"), capa).convert("RGB").save(os.path.join(ANOT, salida + ".png"))
    return salida


def leyenda(items):
    filas = []
    for i, (titulo, texto) in enumerate(items, 1):
        filas.append([NumeroPaso(i, C["rojo"]), P(f"<b>{titulo}.</b> {texto}", "celda")])
    t = Table(filas, colWidths=[26, ANCHO_UTIL - 26])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 1)]))
    return [t, Spacer(1, 8)]


def bloque_codigo(texto, tam=7.6):
    pre = Preformatted(texto, estilo("code", fontName="Consolas", fontSize=tam, leading=tam * 1.38,
                                     textColor=colors.HexColor("#e2e8f0")))
    t = Table([[pre]], colWidths=[ANCHO_UTIL])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), C["navy"]),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 8),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return [t, Spacer(1, 10)]


# ------------------------------------------------------------------ diagramas
def diagrama_estados():
    w, h = ANCHO_UTIL, 150
    d = Drawing(w, h)

    def caja(x, y, ancho, texto, color, sub):
        d.add(Rect(x, y, ancho, 46, rx=8, ry=8, fillColor=color, strokeColor=None))
        d.add(String(x + ancho / 2, y + 26, texto, fontName="Segoe-B", fontSize=11.5, fillColor=colors.white,
                     textAnchor="middle"))
        d.add(String(x + ancho / 2, y + 11, sub, fontName="Segoe", fontSize=7.8,
                     fillColor=colors.HexColor("#f8fafc"), textAnchor="middle"))

    def flecha(x1, y1, x2, y2, texto, dy=6, color=C["suave"], dx=0):
        d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=1.6))
        import math
        ang = math.atan2(y2 - y1, x2 - x1)
        a1, a2 = ang + 2.6, ang - 2.6
        d.add(Polygon([x2, y2, x2 + 8 * math.cos(a1), y2 + 8 * math.sin(a1), x2 + 8 * math.cos(a2),
                       y2 + 8 * math.sin(a2)], fillColor=color, strokeColor=None))
        d.add(String((x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy, texto, fontName="Segoe-SB", fontSize=8,
                     fillColor=color, textAnchor="middle"))

    bw = 108
    xs = [8, (w - bw) / 2, w - bw - 8]
    yt = 92
    caja(xs[0], yt, bw, "Pendiente", C["naranja"], "recién creada")
    caja(xs[1], yt, bw, "Confirmada", C["azul"], "aceptada")
    caja(xs[2], yt, bw, "Procesada", C["verde"], "facturada (final)")
    caja(xs[1], 6, bw, "Cancelada", C["rojo"], "sin cobro (final)")
    flecha(xs[0] + bw + 2, yt + 23, xs[1] - 2, yt + 23, "Confirmar")
    flecha(xs[1] + bw + 2, yt + 23, xs[2] - 2, yt + 23, "Procesar")
    flecha(xs[0] + bw / 2, yt - 2, xs[1] + 12, 54, "Cancelar", dy=-16, dx=12, color=C["rojo"])
    flecha(xs[1] + bw / 2, yt - 2, xs[1] + bw / 2, 54, "Cancelar", dy=-2, dx=26, color=C["rojo"])
    d.add(String(xs[0] + 4, yt + 54, "Crear reserva", fontName="Segoe-SB", fontSize=8, fillColor=C["suave"]))
    return d


def diagrama_costo():
    w, h = ANCHO_UTIL, 92
    d = Drawing(w, h)
    pasos_ = [("1. Subtotal", "tarifa × duración\n× regla del tipo", C["navy2"]),
              ("2. Descuento", "% sobre el subtotal", C["naranja"]),
              ("3. Neto", "subtotal − descuento", C["turq"]),
              ("4. Impuesto", "% sobre el neto", C["morado"]),
              ("5. TOTAL", "neto + impuesto", C["azul"])]
    gap = 12
    bw = (w - gap * 4) / 5
    for i, (t, sub, col) in enumerate(pasos_):
        x = i * (bw + gap)
        d.add(Rect(x, 14, bw, 66, rx=8, ry=8, fillColor=col, strokeColor=None))
        d.add(String(x + bw / 2, 56, t, fontName="Segoe-B", fontSize=11, fillColor=colors.white,
                     textAnchor="middle"))
        for j, linea in enumerate(sub.split("\n")):
            d.add(String(x + bw / 2, 38 - j * 10, linea, fontName="Segoe", fontSize=7.6,
                         fillColor=colors.HexColor("#f1f5f9"), textAnchor="middle"))
        if i < 4:
            xa = x + bw + 1
            d.add(Polygon([xa, 43, xa + gap - 2, 47, xa, 51], fillColor=C["gris"], strokeColor=None))
    return d


# ------------------------------------------------------------------ plantilla del documento
class Manual(BaseDocTemplate):
    def __init__(self, ruta):
        super().__init__(ruta, pagesize=A4, leftMargin=MARGEN, rightMargin=MARGEN, topMargin=24 * mm,
                         bottomMargin=20 * mm, title="Software FJ – Manual de Usuario y Funciones",
                         author="Equipo Software FJ – UNAD", subject="Manual de usuario",
                         creator="Software FJ")
        marco = Frame(MARGEN, 20 * mm, ANCHO_UTIL, ALTO - 44 * mm, id="cuerpo", leftPadding=0,
                      rightPadding=0, topPadding=0, bottomPadding=0)
        self.capitulo = ""
        self.addPageTemplates([
            PageTemplate("portada", [Frame(0, 0, ANCHO, ALTO, id="p")], onPage=dibujar_portada),
            PageTemplate("normal", [marco], onPageEnd=self.encabezado_pie),
        ])
        self._clave = 0

    def beforeDocument(self):
        self._clave = 0
        self.capitulo = ""

    def afterFlowable(self, fl):
        if isinstance(fl, Capitulo):
            self.capitulo = fl.titulo
            self._clave += 1
            clave = f"c{self._clave}"
            self.canv.bookmarkPage(clave)
            self.canv.addOutlineEntry(f"{fl.numero}. {fl.titulo}", clave, level=0)
            self.notify("TOCEntry", (0, f"{fl.numero}.&nbsp;&nbsp;{fl.titulo}", self.page, clave))
        elif isinstance(fl, Seccion):
            self._clave += 1
            clave = f"s{self._clave}"
            self.canv.bookmarkPage(clave)
            self.canv.addOutlineEntry(fl.texto_toc, clave, level=1)
            self.notify("TOCEntry", (1, fl.texto_toc, self.page, clave))

    def encabezado_pie(self, c, doc):
        c.saveState()
        c.setStrokeColor(C["borde"])
        c.setLineWidth(0.7)
        y = ALTO - 14 * mm
        c.setFillColor(C["azul"])
        c.roundRect(MARGEN, y - 1.5, 13, 11, 2, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Segoe-B", 6.2)
        c.drawCentredString(MARGEN + 6.5, y + 1.4, "FJ")
        c.setFillColor(C["navy"])
        c.setFont("Segoe-B", 8)
        c.drawString(MARGEN + 18, y + 1, "SOFTWARE FJ")
        c.setFillColor(C["suave"])
        c.setFont("Segoe", 8)
        c.drawString(MARGEN + 76, y + 1, "Manual de Usuario y Funciones")
        c.drawRightString(ANCHO - MARGEN, y + 1, self.capitulo)
        c.line(MARGEN, y - 5, ANCHO - MARGEN, y - 5)
        c.line(MARGEN, 13 * mm, ANCHO - MARGEN, 13 * mm)
        c.setFont("Segoe", 7.5)
        c.drawString(MARGEN, 9 * mm, f"{PORTADA['institucion']}  ·  {PORTADA['curso']}")
        c.setFont("Segoe-B", 8.5)
        c.setFillColor(C["navy"])
        c.drawRightString(ANCHO - MARGEN, 9 * mm, f"{doc.page}")
        c.restoreState()


def dibujar_portada(c, _doc):
    c.saveState()
    c.setFillColor(C["navy"])
    c.rect(0, 0, ANCHO, ALTO, stroke=0, fill=1)
    # formas decorativas
    c.setFillColor(colors.HexColor("#172554"))
    c.circle(ANCHO + 10 * mm, ALTO - 40 * mm, 95 * mm, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#1e3a8a"))
    c.circle(ANCHO + 5 * mm, ALTO - 45 * mm, 62 * mm, stroke=0, fill=1)
    c.setFillColor(C["azul"])
    c.circle(ANCHO - 12 * mm, ALTO - 70 * mm, 26 * mm, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#1e293b"))
    c.circle(-20 * mm, 30 * mm, 60 * mm, stroke=0, fill=1)
    c.setFillColor(C["azul"])
    c.rect(0, ALTO - 6 * mm, ANCHO, 6 * mm, stroke=0, fill=1)

    x = 22 * mm
    # logotipo (el mismo distintivo «FJ» que muestra la aplicación)
    c.setFillColor(C["azul"])
    c.roundRect(x, ALTO - 62 * mm, 26 * mm, 26 * mm, 4 * mm, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Segoe-B", 34)
    c.drawCentredString(x + 13 * mm, ALTO - 53 * mm, "FJ")
    c.setFont("Segoe-B", 15)
    c.drawString(x + 31 * mm, ALTO - 46 * mm, "SOFTWARE FJ")
    c.setFillColor(colors.HexColor("#94a3b8"))
    c.setFont("Segoe", 10)
    c.drawString(x + 31 * mm, ALTO - 53 * mm, "Sistema integral")

    c.setFillColor(colors.HexColor("#93c5fd"))
    c.setFont("Segoe-B", 11)
    c.drawString(x, ALTO - 100 * mm, "SOFTWARE FJ")
    c.setFillColor(colors.white)
    c.setFont("Segoe-B", 40)
    c.drawString(x, ALTO - 118 * mm, "Manual de Usuario")
    c.drawString(x, ALTO - 134 * mm, "y Funciones")
    c.setFillColor(C["azul"])
    c.rect(x, ALTO - 143 * mm, 30 * mm, 2.2 * mm, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#cbd5e1"))
    c.setFont("Segoe-L", 15)
    c.drawString(x, ALTO - 155 * mm, "Sistema Integral de Gestión de Clientes,")
    c.drawString(x, ALTO - 162.5 * mm, "Servicios y Reservas")

    # integrantes
    y = ALTO - 188 * mm
    c.setFillColor(colors.HexColor("#93c5fd"))
    c.setFont("Segoe-B", 9)
    c.drawString(x, y, "INTEGRANTES")
    c.setFillColor(colors.white)
    c.setFont("Segoe", 11)
    for i, nombre in enumerate(PORTADA["integrantes"]):
        c.drawString(x, y - 7 * mm - i * 6.3 * mm, nombre)

    # institución
    y = 46 * mm
    c.setStrokeColor(colors.HexColor("#334155"))
    c.line(x, y + 9 * mm, ANCHO - 22 * mm, y + 9 * mm)
    c.setFillColor(colors.white)
    c.setFont("Segoe-B", 11)
    c.drawString(x, y, PORTADA["institucion"])
    c.setFillColor(colors.HexColor("#cbd5e1"))
    c.setFont("Segoe", 10)
    lineas = [PORTADA["programa"], PORTADA["curso"]]
    if PORTADA.get("grupo"):
        lineas.append(PORTADA["grupo"])
    lineas.append(PORTADA["lugar_fecha"])
    for i, linea in enumerate(lineas):
        c.drawString(x, y - 6.2 * mm * (i + 1), linea)
    c.setFont("Segoe-B", 9)
    c.setFillColor(colors.HexColor("#93c5fd"))
    c.drawRightString(ANCHO - 22 * mm, y, f"Versión {PORTADA['version']}")
    c.restoreState()


# ------------------------------------------------------------------ datos calculados con el código real
def ejemplos_costos():
    from modelos.servicios import AlquilerEquipo, Asesoria, ReservaSala
    casos = [
        ("Sala Ejecutiva (12 personas)", ReservaSala("X1", "Sala Ejecutiva", 50000, 12), 3, 19, 10,
         "$ 50.000/hora × 3 horas"),
        ("Auditorio Principal (60 personas)", ReservaSala("X2", "Auditorio Principal", 80000, 60), 4, 19, 15,
         "$ 80.000 × 4 h × 1,10 (recargo sala grande)"),
        ("Videobeam Epson", AlquilerEquipo("X3", "Videobeam", 35000, "Proyector"), 2, 19, 0,
         "$ 35.000/día × 2 días × 1,05 (seguro)"),
        ("Asesoría en Ciberseguridad (Experto)",
         Asesoria("X4", "Ciberseguridad", 120000, "Seguridad", "Experto"), 2, 19, 5,
         "$ 120.000 × 2 h × 1,6 (nivel Experto)"),
    ]
    filas = []
    for nombre, servicio, dur, imp, desc, formula in casos:
        r = servicio.calcular_costo_detallado(dur, imp / 100, desc / 100 if desc else None)
        filas.append((nombre, formula, r, imp, desc))
    return filas


def m(valor):
    return f"$ {valor:,.0f}".replace(",", ".")


# ------------------------------------------------------------------ contenido
def contenido():
    h = []
    A = h.append

    def X(lista):
        h.extend(lista)

    # ---------------- portada
    A(NextPageTemplate("normal"))
    A(PageBreak())

    # ---------------- información del documento
    A(P("Acerca de este manual", estilo("t", parent=E["h2"], fontSize=20, leading=26, spaceBefore=0)))
    A(P("Este documento explica, paso a paso y con imágenes reales de la aplicación, cómo utilizar todas "
        "las funciones de <b>Software FJ</b>. Está escrito para cualquier persona, aunque no tenga "
        "conocimientos de informática ni de programación.", "intro"))
    X(tabla(["Dato", "Descripción"], [
        ("Producto", "SOFTWARE FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas"),
        ("Tipo de documento", "Manual de usuario y funciones"),
        ("Versión del manual", PORTADA["version"]),
        ("Fecha", PORTADA["lugar_fecha"]),
        ("Institución", PORTADA["institucion"]),
        ("Curso", PORTADA["curso"]),
        ("Dirigido a", "Personal de atención al cliente, recepción, administración y cualquier usuario del "
                       "programa"),
        ("Sistema operativo", "Windows (recomendado), macOS o Linux, con Python 3.8 o superior"),
    ], [0.27, 0.73], negrita_col0=True))
    X(H3("Cómo leer este manual"))
    A(P("A lo largo del documento encontrará recuadros de colores que destacan información útil:"))
    A(aviso("nota", "Información adicional que ayuda a entender una función."))
    A(aviso("consejo", "Recomendaciones para trabajar de forma más rápida y segura."))
    A(aviso("importante", "Datos que debe tener presentes para evitar errores o pérdidas de información."))
    A(aviso("atencion", "Acciones que no se pueden deshacer."))
    A(P(f"Los nombres de botones, menús y campos de la pantalla se escriben así: {B('Guardar')}. "
        f"Lo que usted debe escribir con el teclado aparece así: {K('python main.py')}. "
        "Todas las imágenes son capturas reales del programa en funcionamiento; los datos que aparecen "
        "(clientes, servicios y reservas) son ejemplos ficticios creados para este manual."))
    A(P("Las imágenes muestran recuadros rojos numerados para señalar partes de la pantalla. Debajo de "
        "cada imagen anotada se explica qué es cada número."))
    A(PageBreak())

    # ---------------- índice
    A(P("Contenido", estilo("t2", parent=E["h2"], fontSize=20, leading=26, spaceBefore=0, spaceAfter=10)))
    toc = TableOfContents(dotsMinLevel=0)
    toc.levelStyles = [E["toc0"], E["toc1"]]
    A(toc)
    A(PageBreak())

    # =============== 1. Bienvenida
    A(Capitulo(1, "Bienvenido a Software FJ",
               "Qué es el programa, para qué sirve y los conceptos básicos que necesita conocer."))
    A(Spacer(1, 10))
    X(S("1.1 ¿Qué es Software FJ?"))
    A(P("Software FJ es un programa de escritorio que ayuda a una empresa de servicios a llevar, en un solo "
        "lugar, el control de sus <b>clientes</b>, de los <b>servicios</b> que ofrece (salas, equipos y "
        "asesorías) y de las <b>reservas</b> que hacen los clientes sobre esos servicios."))
    A(P("El programa calcula automáticamente el valor de cada reserva (incluidos impuestos y descuentos), "
        "controla que no se reserve un servicio sin cupo, valida que los datos estén bien escritos y guarda "
        "un registro de todo lo que ocurre, para que siempre se pueda consultar qué se hizo y cuándo."))
    X(S("1.2 ¿Qué puede hacer con el programa?"))
    X(tabla(["Función", "¿Qué le permite hacer?", "Capítulo"], [
        ("Panel principal", "Ver de un vistazo cuántos clientes, servicios y reservas hay, y cuánto se ha "
                            "facturado.", "4"),
        ("Clientes", "Registrar clientes, buscarlos y actualizar sus datos de contacto.", "5"),
        ("Servicios", "Registrar salas, equipos y asesorías; consultar su disponibilidad; calcular tarifas; "
                      "habilitarlos o deshabilitarlos.", "6"),
        ("Costos", "Conocer cómo se calculan subtotal, descuento, impuesto y total.", "7"),
        ("Reservas", "Crear reservas con el costo calculado al instante; confirmarlas, procesarlas "
                     "(facturarlas) o cancelarlas; ver su historial.", "8"),
        ("Eventos y logs", "Consultar el registro de actividad y de errores de la sesión y del archivo "
                           "software_fj.log.", "9"),
        ("Herramientas", "Ejecutar una demostración automática de 15 operaciones, ver la información del "
                         "programa y salir.", "10"),
    ], [0.2, 0.68, 0.12], negrita_col0=True))
    X(S("1.3 Conceptos básicos"))
    A(P("Antes de empezar, conviene conocer las palabras que usa el programa:"))
    X(tabla(["Término", "Significado"], [
        ("Cliente", "Persona que solicita un servicio. Se identifica por su número de identificación "
                    "(por ejemplo, la cédula)."),
        ("Servicio", "Lo que la empresa ofrece. Hay tres tipos: <b>Sala</b> (se cobra por horas), "
                     "<b>Equipo</b> (se cobra por días) y <b>Asesoría</b> (se cobra por horas)."),
        ("Reserva", "Solicitud de un cliente para usar un servicio durante cierto tiempo. Tiene un código "
                    "automático (R-0001, R-0002...) y un estado."),
        ("Estado de la reserva", "Etapa en la que se encuentra: Pendiente, Confirmada, Procesada "
                                 "(facturada) o Cancelada."),
        ("Cupo", "Cantidad de reservas activas que un servicio puede atender al mismo tiempo. Por "
                 "ejemplo, un equipo con 1 unidad solo admite una reserva activa."),
        ("Tarifa", "Precio por hora o por día del servicio, en pesos."),
        ("Log o registro de eventos", "Lista de todo lo que ocurre en el programa (registros, cambios, "
                                      "errores) con su fecha y hora."),
    ], [0.24, 0.76], negrita_col0=True))
    A(aviso("importante", [
        "Software FJ guarda la información <b>en la memoria del computador mientras el programa está "
        "abierto</b>. Al cerrar el programa, los clientes, servicios y reservas registrados se borran y la "
        "próxima vez empezará vacío. Lo único que se conserva es el archivo de registro "
        "<b>software_fj.log</b>.",
        "Por eso, no cierre el programa hasta terminar su jornada de trabajo. El mismo programa se lo "
        "recuerda al momento de salir."]))
    A(PageBreak())

    # =============== 2. Instalación
    A(Capitulo(2, "Instalación y puesta en marcha",
               "Lo que necesita en su computador y cómo abrir Software FJ por primera vez."))
    A(Spacer(1, 10))
    X(S("2.1 Requisitos"))
    X(tabla(["Elemento", "Requisito"], [
        ("Computador", "Windows 10/11 (recomendado), macOS o Linux."),
        ("Pantalla", "Resolución mínima de 1024 × 700 píxeles. La ventana del programa no se puede reducir "
                     "por debajo de 1000 × 640."),
        ("Python", "Versión 3.8 o superior, que incluye la herramienta gráfica Tkinter. No se necesita "
                   "instalar nada más ni conexión a Internet."),
        ("Archivos del programa", "La carpeta de Software FJ completa (con main.py y las carpetas "
                                  "modelos, gestores e interfaz)."),
    ], [0.25, 0.75], negrita_col0=True))
    X(S("2.2 Instalar Python (solo la primera vez)"))
    X(pasos([
        "Abra su navegador e ingrese a <b>https://www.python.org/downloads/</b>.",
        f"Pulse el botón amarillo {B('Download Python')} para descargar el instalador.",
        "Abra el archivo descargado. En la primera pantalla del instalador <b>marque la casilla "
        f"{B('Add python.exe to PATH')}</b> (es muy importante).",
        f"Pulse {B('Install Now')} y espere a que termine. Al final pulse {B('Close')}.",
    ]))
    A(aviso("nota", "Tkinter, la herramienta con la que está construida la ventana del programa, viene "
                    "incluida en el instalador oficial de Python para Windows y macOS. En algunas "
                    "distribuciones de Linux debe instalarse aparte (por ejemplo, con el paquete "
                    "<b>python3-tk</b>)."))
    X(S("2.3 Comprobar que Python quedó instalado"))
    X(pasos([
        f"Pulse la tecla <b>Windows</b>, escriba {K('cmd')} y pulse <b>Enter</b>. Se abrirá una ventana "
        "negra llamada <i>Símbolo del sistema</i>.",
        f"Escriba {K('python --version')} y pulse <b>Enter</b>.",
        f"Debe aparecer un mensaje como {K('Python 3.12.4')}. Si aparece un error, consulte el "
        "capítulo 12, «Solución de problemas».",
    ]))
    X(S("2.4 Abrir Software FJ"))
    X(pasos([
        "Abra con el Explorador de archivos la carpeta donde guardó Software FJ (la que contiene el "
        "archivo <b>main.py</b>).",
        f"Haga clic en la barra de direcciones de la carpeta (la parte superior que muestra la ruta), "
        f"escriba {K('cmd')} y pulse <b>Enter</b>. Se abrirá el Símbolo del sistema ya ubicado en esa "
        "carpeta.",
        f"Escriba {K('python main.py')} y pulse <b>Enter</b>.",
        "En unos segundos se abrirá la ventana principal de Software FJ mostrando el "
        f"{B('Panel principal')} (vea la figura siguiente).",
    ]))
    A(fig("01_panel_vacio", "Software FJ recién abierto. Al iniciar no hay datos: todas las tarjetas "
                            "muestran 0."))
    A(aviso("consejo", "No cierre la ventana negra del Símbolo del sistema mientras usa el programa: "
                       "si la cierra, Software FJ también se cerrará."))
    X(S("2.5 Formas de iniciar el programa"))
    A(P("Además de la forma normal, el programa admite dos modos especiales que se escriben al final de la "
        "orden de inicio:"))
    X(tabla(["Orden que se escribe", "Qué hace"], [
        (K("python main.py"), "Abre la ventana del programa vacía, lista para trabajar. <b>Es la forma "
                              "habitual.</b>"),
        (K("python main.py --demo"), "Abre la ventana y, de inmediato, ofrece ejecutar la demostración "
                                     "automática de 15 operaciones (capítulo 10)."),
        (K("python main.py --consola"), "No abre ninguna ventana: ejecuta la demostración de 15 "
                                        "operaciones y muestra los resultados como texto en el Símbolo "
                                        "del sistema."),
    ], [0.38, 0.62]))
    X(S("2.6 Archivos del programa"))
    A(P("No es necesario abrir ni modificar ninguno de estos archivos. Se describen solo para que sepa qué "
        "contiene la carpeta:"))
    X(tabla(["Archivo o carpeta", "Contenido"], [
        ("main.py", "Archivo de inicio. Es el que se ejecuta para abrir el programa."),
        ("interfaz/", "Las pantallas del programa (panel, clientes, servicios, reservas, eventos)."),
        ("modelos/ y gestores/", "Las reglas del negocio: validaciones, cálculos y estados."),
        ("excepciones.py, registro.py, simulacion.py", "Manejo de errores, registro de eventos y "
                                                        "demostración."),
        ("software_fj.log", "Archivo de texto donde el programa anota toda su actividad. Se crea "
                            "automáticamente."),
        ("README.md", "Resumen técnico para desarrolladores."),
    ], [0.38, 0.62], negrita_col0=True))
    A(PageBreak())

    # =============== 3. Interfaz
    A(Capitulo(3, "Conociendo la interfaz",
               "Las partes de la ventana principal y los elementos que se repiten en todas las pantallas."))
    A(Spacer(1, 10))
    X(S("3.1 La ventana principal"))
    A(P("La ventana de Software FJ siempre tiene la misma organización: un menú oscuro a la izquierda y, a "
        "la derecha, el área de trabajo, que cambia según la opción elegida."))
    anotar("46_panel_con_datos", "01_panel_vacio",
           ["lateral", "encabezado", "reloj", "tarjetas", "actividad", "accesos", "estado"], "a_ventana")
    A(fig("a_ventana", "Partes de la ventana principal.", carpeta=ANOT))
    X(leyenda([
        ("Menú lateral", "Permite cambiar de pantalla. La opción en uso se resalta en azul. Abajo están las "
                         "herramientas Demostración, Acerca de y Salir."),
        ("Encabezado", "Muestra el nombre de la pantalla actual y una breve descripción de lo que se puede "
                       "hacer en ella."),
        ("Fecha y hora", "Reloj que se actualiza cada segundo."),
        ("Tarjetas de resumen", "Cifras principales del negocio (solo en el Panel principal)."),
        ("Actividad reciente", "Últimos eventos ocurridos en la sesión."),
        ("Accesos rápidos", "Botones para ir directamente a las tareas más frecuentes."),
        ("Barra de estado", "Informa el resultado de la última acción, con su hora. Su color indica si fue "
                            "un éxito (verde), una advertencia (naranja) o un error (rojo)."),
    ]))
    X(S("3.2 El menú lateral"))
    X(tabla(["Opción", "Para qué sirve"], [
        ("Panel principal", "Resumen general y accesos rápidos."),
        ("Clientes", "Registrar, buscar y actualizar clientes."),
        ("Servicios", "Registrar salas, equipos y asesorías; consultar disponibilidad y tarifas."),
        ("Reservas", "Crear, confirmar, procesar y cancelar reservas."),
        ("Eventos y logs", "Ver el registro de actividad y errores."),
        ("Demostración", "Ejecutar 15 operaciones de prueba automáticas."),
        ("Acerca de", "Información del programa."),
        ("Salir", "Cerrar el programa (pide confirmación)."),
    ], [0.27, 0.73], negrita_col0=True))
    A(P("Para cambiar de pantalla, haga un solo clic sobre la opción. Al pasar el puntero por encima, la "
        "opción se ilumina. Cada vez que entra a una pantalla, la información se actualiza "
        "automáticamente."))
    X(S("3.3 Elementos comunes de las pantallas"))
    X(H3("Formularios"))
    A(P("Son los recuadros blancos con campos para escribir. Cada campo tiene encima su nombre en negrita. "
        "Algunos campos son listas desplegables: haga clic en la flecha de la derecha y elija una opción. "
        "Si un dato está mal escrito, el programa lo indica con un mensaje y <b>marca el campo con fondo "
        "rojo</b>; al empezar a corregirlo, el color rojo desaparece."))
    X(H3("Botones y sus colores"))
    X(tabla(["Color", "Significado", "Ejemplos"], [
        ("Azul", "Acción principal de la pantalla", "Guardar, Crear reserva, Ver archivo software_fj.log"),
        ("Verde", "Aprobar o calcular", "Confirmar, Calcular tarifa"),
        ("Turquesa", "Consultar o avanzar", "Buscar, Consultar disponibilidad, Procesar"),
        ("Naranja", "Acción que conviene revisar", "Deshabilitar / Habilitar, Ejecutar simulación"),
        ("Rojo", "Acción que no se puede deshacer", "Cancelar (una reserva)"),
        ("Gris claro", "Acción secundaria", "Limpiar, Ver todos, Actualizar"),
        ("Gris apagado", "Botón no disponible en ese momento", "Procesar, cuando la reserva aún no está "
                                                               "confirmada"),
    ], [0.17, 0.4, 0.43], negrita_col0=True,
        estilos_extra=[("TEXTCOLOR", (0, 1), (0, 1), C["azul"]), ("TEXTCOLOR", (0, 2), (0, 2), C["verde"])]))
    X(H3("Tablas"))
    X(vinetas([
        "Haga <b>clic sobre una fila</b> para seleccionarla; se resalta en azul claro.",
        "Haga <b>clic sobre el título de una columna</b> para ordenar la tabla por esa columna. Un segundo "
        "clic invierte el orden.",
        "Si la información no cabe, use las <b>barras de desplazamiento</b> de la derecha y de abajo, o "
        "agrande la ventana con el botón de maximizar.",
        "En algunas tablas las filas se colorean según el estado (por ejemplo, amarillo para reservas "
        "pendientes y rojo para canceladas).",
    ]))
    X(H3("Ventanas de mensaje"))
    A(P("Después de cada acción, el programa muestra una pequeña ventana con el resultado. Léala y pulse "
        f"{B('Aceptar')} para continuar:"))
    X(tabla(["Título de la ventana", "Cuándo aparece"], [
        ("Operación exitosa", "La acción se realizó correctamente (ícono azul «i»)."),
        ("Datos no válidos", "Algún dato está vacío o mal escrito. El campo con el problema queda marcado "
                             "en rojo (ícono amarillo «!»)."),
        ("Operación no realizada", "La acción no se permite, por ejemplo, porque el cliente ya existe o "
                                   "el servicio no tiene cupo (ícono amarillo «!»)."),
        ("Error inesperado", "Ocurrió un problema imprevisto. El programa lo anota en el log y "
                             "<b>sigue funcionando</b> (ícono rojo «x»)."),
        ("Preguntas (Sí / No)", "Antes de confirmar, procesar, cancelar, deshabilitar o salir, el programa "
                                "pide su autorización."),
    ], [0.3, 0.7], negrita_col0=True))
    X(H3("Atajos de teclado"))
    X(tabla(["Tecla", "Dónde", "Efecto"], [
        ("Enter", "Campo Teléfono (Clientes)", "Guarda o actualiza el cliente."),
        ("Enter", "Casilla de búsqueda (Clientes)", "Ejecuta la búsqueda."),
        ("Doble clic", "Tablas de Reservas, Eventos y Demostración", "Abre el detalle de la fila."),
        ("Clic en un título de columna", "Cualquier tabla", "Ordena la tabla (un segundo clic invierte el "
                                                            "orden)."),
    ], [0.22, 0.38, 0.4], negrita_col0=True))
    A(aviso("nota", "Ningún error cierra el programa. Si algo sale mal, verá el mensaje correspondiente, la "
                    "situación quedará anotada en el registro de eventos y podrá seguir trabajando."))
    A(PageBreak())

    # =============== 4. Panel principal
    A(Capitulo(4, "Panel principal",
               "El tablero de control que resume en tiempo real la operación de la empresa."))
    A(Spacer(1, 10))
    A(P("Es la primera pantalla que aparece al abrir el programa. Para volver a ella en cualquier momento, "
        f"haga clic en {B('Panel principal')} en el menú lateral."))
    A(fig("46_panel_con_datos", "Panel principal con información: 5 clientes, 6 reservas y $ 248.115 en "
                                "ingresos."))
    X(S("4.1 Tarjetas de resumen"))
    X(tabla(["Tarjeta", "Qué cuenta"], [
        ("Clientes registrados", "Número total de clientes en el sistema."),
        ("Servicios disponibles", "Servicios habilitados que todavía tienen cupo, y debajo el total de "
                                  "servicios registrados (por ejemplo, «3 de 6»)."),
        ("Total de reservas", "Todas las reservas creadas, en cualquier estado."),
        ("Reservas pendientes", "Reservas creadas que esperan confirmación."),
        ("Reservas confirmadas", "Reservas aceptadas, listas para procesar (facturar)."),
        ("Reservas canceladas", "Reservas anuladas; no generan cobro."),
        ("Reservas procesadas", "Reservas facturadas."),
        ("Ingresos (conf. + proc.)", "Suma del valor total, con impuestos, de las reservas confirmadas "
                                     "y procesadas."),
    ], [0.3, 0.7], negrita_col0=True))
    A(aviso("nota", "Las tarjetas se reorganizan solas según el tamaño de la ventana: en 4, 2 o 1 columna."))
    X(S("4.2 Actividad reciente"))
    A(P("Muestra los últimos 30 eventos de la sesión, del más reciente al más antiguo, con su fecha y hora, "
        "su tipo (INFO, WARNING, ERROR o CRITICAL) y una descripción. Las filas de error aparecen con fondo "
        "rojizo. Para ver el registro completo, use la pantalla Eventos y logs (capítulo 9)."))
    X(S("4.3 Accesos rápidos"))
    X(tabla(["Botón", "Lo lleva a"], [
        ("Registrar cliente", "Pantalla Clientes"),
        ("Registrar servicio", "Pantalla Servicios"),
        ("Nueva reserva", "Pantalla Reservas"),
        ("Ver eventos y logs", "Pantalla Eventos y logs"),
        ("Ejecutar simulación de 15 operaciones", "Inicia la demostración automática (capítulo 10)"),
    ], [0.45, 0.55], negrita_col0=True))
    A(PageBreak())

    # =============== 5. Clientes
    A(Capitulo(5, "Gestión de clientes",
               "Cómo registrar, buscar y actualizar la información de los clientes."))
    A(Spacer(1, 10))
    A(P(f"Haga clic en {B('Clientes')} en el menú lateral. La pantalla tiene dos partes: el formulario a la "
        "izquierda y la lista de clientes a la derecha."))
    anotar("08_clientes_tabla", "02_clientes_vacio",
           ["formulario", "modo", "guardar", "limpiar", "busqueda", "tabla"], "a_clientes")
    A(fig("a_clientes", "Pantalla de gestión de clientes.", carpeta=ANOT))
    X(leyenda([
        ("Datos del cliente", "Formulario con los cuatro datos del cliente. Todos son obligatorios."),
        ("Modo", "Indica si está creando un cliente nuevo («nuevo registro») o modificando uno existente "
                 "(«edición»)."),
        ("Guardar / Actualizar", "Guarda la información. En modo edición, el botón se llama Actualizar."),
        ("Limpiar", "Borra el formulario y vuelve al modo de nuevo registro."),
        ("Búsqueda", "Casilla para buscar y botones Buscar y Ver todos."),
        ("Clientes registrados", "Tabla con identificación, nombre, correo, teléfono y número de reservas "
                                 "de cada cliente. Debajo se indica cuántos clientes se muestran."),
    ]))
    X(S("5.1 Registrar un cliente nuevo"))
    X(pasos([
        f"Verifique que debajo del formulario diga {K('Modo: nuevo registro')}. Si no es así, pulse "
        f"{B('Limpiar')}.",
        f"En {B('Identificación')} escriba el número de documento, solo dígitos (entre 5 y 12).",
        f"En {B('Nombre completo')} escriba nombres y apellidos.",
        f"En {B('Correo electrónico')} escriba el correo del cliente.",
        f"En {B('Teléfono')} escriba un número de 7 a 10 dígitos.",
        f"Pulse {B('Guardar')} (o la tecla <b>Enter</b> estando en el campo Teléfono).",
        f"Aparecerá el mensaje <i>«Cliente ... registrado correctamente»</i>. Pulse {B('Aceptar')}. El "
        "cliente aparecerá en la tabla y el formulario quedará limpio para el siguiente.",
    ]))
    A(fig("03_cliente_formulario", "Formulario completo con los datos de la clienta Laura Gómez, antes de "
                                   "pulsar Guardar."))
    A(fig("04_cliente_registrado", "Mensaje de confirmación después de guardar."))
    X(S("5.2 Reglas que deben cumplir los datos"))
    X(tabla(["Campo", "Regla", "Ejemplo válido", "Ejemplo no válido"], [
        ("Identificación", "Solo números, de 5 a 12 dígitos. No se puede repetir.", "1032456789",
         "10-32A (letras) · 1234 (corto)"),
        ("Nombre completo", "Solo letras, espacios y apóstrofo; mínimo 3 caracteres. Se permiten tildes "
                            "y ñ.", "Laura Gómez", "Ana3 · Lu"),
        ("Correo electrónico", "Formato usuario@dominio.ext", "laura.gomez@mail.com", "maria.ruiz@"),
        ("Teléfono", "De 7 a 10 dígitos. Los espacios y guiones se eliminan solos.", "310 456 7890",
         "31045 (corto)"),
    ], [0.18, 0.4, 0.2, 0.22], negrita_col0=True))
    A(aviso("nota", "El programa ordena automáticamente los datos: pone en mayúscula la primera letra de "
                    "cada nombre («laura gómez» se guarda como «Laura Gómez»), escribe el correo en "
                    "minúsculas y quita espacios y guiones del teléfono."))
    X(S("5.3 Si un dato está mal"))
    A(P("Si algún dato no cumple las reglas, el cliente <b>no</b> se guarda. El programa muestra la "
        f"ventana {B('Datos no válidos')} explicando el problema y marca en rojo el campo que debe "
        "corregir:"))
    A(fig("06_campo_invalido", "El correo «maria.ruiz@» está incompleto: el campo queda marcado en rojo y "
                               "la barra de estado describe el problema."))
    A(fig_doble("05_error_correo_dlg", "07_error_duplicado_dlg",
                "Izquierda: correo con formato no válido. Derecha: intento de registrar una identificación "
                "que ya existe."))
    X(pasos([
        f"Pulse {B('Aceptar')} en el mensaje.",
        "Corrija el campo marcado en rojo (el color desaparece en cuanto empieza a escribir).",
        f"Pulse {B('Guardar')} nuevamente.",
    ]))
    X(S("5.4 Buscar un cliente"))
    X(pasos([
        "En la casilla de búsqueda (encima de la tabla) escriba una parte de la identificación, del "
        "nombre o del correo. No importa si usa mayúsculas o minúsculas.",
        f"Pulse {B('Buscar')} o la tecla <b>Enter</b>.",
        "La tabla mostrará solo los clientes que coinciden. Debajo verá, por ejemplo, «1 de 5 cliente(s)».",
        f"Para volver a ver la lista completa, pulse {B('Ver todos')}.",
    ]))
    A(fig("11_busqueda", "Resultado de buscar «laura»: se muestra 1 de los 5 clientes."))
    A(aviso("nota", "Si ningún cliente coincide, aparece el aviso «Sin resultados». Si pulsa Buscar con la "
                    "casilla vacía, el programa le pedirá que escriba qué desea buscar. Tenga en cuenta "
                    "que la búsqueda por nombre distingue las tildes: «gomez» no encuentra «Gómez»."))
    X(S("5.5 Actualizar los datos de un cliente"))
    X(pasos([
        "En la tabla, haga clic sobre el cliente que desea modificar.",
        f"Sus datos se cargan en el formulario, el modo cambia a {K('Modo: edición de ...')} y el botón "
        f"pasa a llamarse {B('Actualizar')}.",
        "Corrija el nombre, el correo o el teléfono.",
        f"Pulse {B('Actualizar')}. Verá el mensaje «Cliente ... actualizado correctamente».",
    ]))
    A(fig("09_cliente_edicion", "Edición del cliente Andrés Pérez: la identificación aparece bloqueada y "
                                "se cambió el teléfono."))
    A(aviso("importante", [
        "La <b>identificación no se puede modificar</b>: en modo edición su campo aparece bloqueado. Si se "
        "registró mal, registre el cliente de nuevo con la identificación correcta.",
        f"Para salir del modo edición sin guardar cambios, pulse {B('Limpiar')}. Si un dato nuevo es "
        "inválido, el programa no guarda ningún cambio y conserva los datos anteriores."]))
    A(aviso("nota", "La versión actual del programa no incluye una opción para eliminar clientes."))
    A(PageBreak())

    # =============== 6. Servicios
    A(Capitulo(6, "Gestión de servicios",
               "Registro de salas, equipos y asesorías; disponibilidad, tarifas y habilitación."))
    A(Spacer(1, 10))
    X(S("6.1 Los tres tipos de servicio"))
    A(P("Software FJ maneja tres clases de servicio. Cada una tiene su propia unidad de tiempo, sus límites "
        "de duración y su forma de calcular el precio:"))
    X(tabla(["", "Sala", "Equipo", "Asesoría"], [
        ("Se cobra por", "Hora", "Día", "Hora"),
        ("Duración permitida", "De 1 a 12 horas", "De 1 a 30 días, solo días completos",
         "De 0,5 a 8 horas"),
        ("Datos propios", "Capacidad (personas, máx. 500) y reservas simultáneas (predeterminado: 2)",
         "Tipo de equipo y unidades disponibles (predeterminado: 1)",
         "Especialidad, nivel y reservas simultáneas (predeterminado: 1)"),
        ("Regla especial de precio", "Recargo del 10 % si la capacidad es mayor de 20 personas",
         "Seguro obligatorio del 5 % sobre el valor", "Nivel Básico × 1,0 · Intermedio × 1,3 · "
                                                      "Experto × 1,6"),
    ], [0.2, 0.27, 0.27, 0.26], negrita_col0=True))
    X(S("6.2 La pantalla de servicios"))
    A(P(f"Haga clic en {B('Servicios')} en el menú lateral. La pantalla tiene tres zonas:"))
    anotar("23_calcular_tarifa", "13_servicios_vacio",
           ["tipos", "registro", "consulta", "botones_consulta", "resultado", "filtro", "catalogo"],
           "a_servicios")
    A(fig("a_servicios", "Pantalla de gestión de servicios.", carpeta=ANOT))
    X(leyenda([
        ("Tipo de servicio", "Botones de opción Sala, Equipo y Asesoría. Al cambiar de tipo, cambian los "
                             "campos del formulario."),
        ("Registrar servicio", "Formulario con código, nombre, tarifa y los datos propios del tipo."),
        ("Disponibilidad y tarifas", "Zona de consulta para el servicio seleccionado en el catálogo."),
        ("Botones de consulta", "Consultar disponibilidad, Calcular tarifa y Deshabilitar/Habilitar."),
        ("Resultado", "Recuadro donde aparece la respuesta de cada consulta."),
        ("Mostrar", "Filtro del catálogo: Todos, Sala, Equipo o Asesoría."),
        ("Catálogo de servicios", "Tabla con todos los servicios registrados, su tarifa, su ocupación y su "
                                  "estado."),
    ]))
    X(S("6.3 Registrar una sala"))
    X(pasos([
        f"Seleccione la opción {B('Sala')}.",
        f"Escriba un {B('Código')} único (por ejemplo, {K('SAL-01')}). Las letras se convierten "
        "automáticamente a mayúsculas.",
        f"Escriba el {B('Nombre')} (mínimo 3 caracteres) y la {B('Tarifa por hora')} en pesos, solo "
        f"números, sin puntos ni signo $ (por ejemplo, {K('50000')}).",
        f"Escriba la {B('Capacidad (personas)')} y, si lo desea, cambie las {B('Reservas simultáneas')} "
        "(cuántas reservas activas puede tener la sala al mismo tiempo).",
        f"Pulse {B('Guardar')}. Aparecerá el mensaje «Servicio ... registrado con código ...».",
    ]))
    A(fig("14_form_sala", "Registro de la «Sala Ejecutiva» con tarifa de $ 50.000 por hora y capacidad para "
                          "12 personas."))
    A(fig("15_servicio_registrado_dlg", "Confirmación del registro del servicio.", ancho=95 * mm))
    X(S("6.4 Registrar un equipo"))
    X(pasos([
        f"Seleccione la opción {B('Equipo')}. La etiqueta de la tarifa cambia a {B('Tarifa por día')}.",
        "Complete código, nombre y tarifa diaria.",
        f"En {B('Tipo de equipo')} escriba la clase de equipo (por ejemplo, «Proyector»).",
        f"En {B('Unidades disponibles')} indique cuántos equipos iguales hay; ese número es el cupo de "
        "reservas simultáneas.",
        f"Pulse {B('Guardar')}.",
    ]))
    A(fig("16_form_equipo", "Registro del equipo «Videobeam Epson» con 1 unidad disponible."))
    X(S("6.5 Registrar una asesoría"))
    X(pasos([
        f"Seleccione la opción {B('Asesoría')}.",
        "Complete código, nombre y tarifa por hora.",
        f"Escriba la {B('Especialidad')} (por ejemplo, «Seguridad informática»).",
        f"Elija el {B('Nivel')} en la lista: Básico, Intermedio o Experto. El nivel aumenta el precio "
        "(ver tabla 6.1).",
        f"Indique las {B('Reservas simultáneas')} y pulse {B('Guardar')}.",
    ]))
    A(fig("17_form_asesoria", "Registro de una asesoría de nivel Experto."))
    X(S("6.6 Reglas al registrar servicios"))
    X(tabla(["Campo", "Regla"], [
        ("Código", "Obligatorio y único. No pueden existir dos servicios con el mismo código."),
        ("Nombre", "Obligatorio, mínimo 3 caracteres."),
        ("Tarifa", "Número mayor que cero, sin puntos de miles ni signo $."),
        ("Capacidad", "Número mayor que cero y hasta 500 personas (solo salas)."),
        ("Reservas simultáneas / Unidades", "Número mayor que cero."),
        ("Tipo de equipo / Especialidad", "Obligatorios para equipos y asesorías, respectivamente."),
    ], [0.32, 0.68], negrita_col0=True))
    A(fig("19_campo_tarifa_invalido", "Intento de registrar una sala con tarifa negativa: el servicio no "
                                      "se guarda y el campo Tarifa queda en rojo."))
    X(S("6.7 El catálogo de servicios"))
    A(P("La tabla inferior lista los servicios registrados. Use el filtro "
        f"{B('Mostrar')} para ver solo un tipo. Las columnas significan:"))
    X(tabla(["Columna", "Significado"], [
        ("Código, Tipo, Nombre", "Identificación del servicio."),
        ("Detalle", "Datos propios: capacidad, tipo de equipo y unidades, o especialidad y nivel."),
        ("Tarifa", "Precio por hora o por día."),
        ("Ocupación", "Reservas activas sobre el cupo total. Por ejemplo, «1/2» significa que hay una "
                      "reserva activa y cabe una más."),
        ("Estado", "<b>Disponible</b> (fondo blanco): se puede reservar. <b>Sin cupo</b> (fondo "
                   "amarillo): todas sus plazas están ocupadas. <b>Deshabilitado</b> (fondo gris): fue "
                   "desactivado manualmente."),
    ], [0.25, 0.75], negrita_col0=True))
    A(fig("45_servicios_ocupacion", "El catálogo muestra la ocupación de cada servicio. Con la pantalla de "
                                    "1366 × 768 se ve una fila a la vez; use la barra de desplazamiento "
                                    "o maximice la ventana para ver más."))
    X(S("6.8 Consultar la disponibilidad de un servicio"))
    X(pasos([
        "Haga clic sobre el servicio en el catálogo. Su código y nombre aparecen en la zona "
        f"{B('Disponibilidad y tarifas')}.",
        f"Pulse {B('Consultar disponibilidad')}.",
        "En el recuadro de resultado verá si está DISPONIBLE (en verde) o NO DISPONIBLE (en rojo), las "
        "reservas activas y los cupos libres. Si está deshabilitado, también se indica el motivo.",
    ]))
    A(fig("22_disponibilidad", "La Sala Ejecutiva está disponible: 0 reservas activas de 2 posibles."))
    X(S("6.9 Calcular la tarifa sin crear una reserva"))
    A(P("Esta opción sirve para dar un precio a un cliente que pregunta, sin registrar nada:"))
    X(pasos([
        "Seleccione el servicio en el catálogo.",
        f"Escriba la {B('Duración')} (la etiqueta indica si son horas o días), el {B('Impuesto (%)')} "
        f"(19 de forma predeterminada) y el {B('Descuento (%)')}.",
        f"Pulse {B('Calcular tarifa')}. El resultado muestra subtotal, descuento, impuesto y TOTAL.",
    ]))
    A(fig("23_calcular_tarifa", "Tarifa para 3 horas de la Sala Ejecutiva con IVA del 19 % y 10 % de "
                                "descuento: total $ 160.650."))
    X(S("6.10 Deshabilitar o habilitar un servicio"))
    A(P("Deshabilitar un servicio impide que se le hagan nuevas reservas (por ejemplo, porque un equipo "
        "está en mantenimiento), sin borrarlo del catálogo."))
    X(pasos([
        "Seleccione el servicio en el catálogo.",
        f"Pulse el botón naranja {B('Deshabilitar')}. Si el servicio ya está deshabilitado, el botón dice "
        f"{B('Habilitar')}.",
        f"Responda {B('Sí')} a la pregunta de confirmación.",
        "El estado del servicio cambia en el catálogo.",
    ]))
    A(fig_doble("24_confirmar_deshabilitar_dlg", "25_servicio_deshabilitado_dlg",
                "Confirmación y resultado al deshabilitar la «Asesoría Contable»."))
    A(fig("26_catalogo_deshabilitado", "El servicio ASE-02 aparece ahora como «Deshabilitado»."))
    A(aviso("importante", "Un servicio deshabilitado no aparece en la lista de servicios al crear reservas. "
                          "Además, si tenía reservas pendientes, estas no podrán confirmarse hasta que se "
                          "vuelva a habilitar."))
    A(aviso("nota", "La versión actual no permite modificar ni eliminar servicios ya registrados. Si un "
                    "dato quedó mal, deshabilite el servicio y registre uno nuevo con otro código."))
    A(PageBreak())

    # =============== 7. Costos
    A(Capitulo(7, "Costos, impuestos y descuentos",
               "Cómo calcula Software FJ el valor de cada servicio y de cada reserva."))
    A(Spacer(1, 10))
    X(S("7.1 El cálculo en cinco pasos"))
    A(P("Siempre que el programa muestra un precio, sigue el mismo orden. El descuento se aplica "
        "<b>antes</b> del impuesto, de modo que el impuesto se cobra sobre el valor ya descontado:"))
    A(diagrama_costo())
    A(Spacer(1, 8))
    X(tabla(["Paso", "Cómo se obtiene"], [
        ("1. Subtotal", "Tarifa × duración, más la regla especial del tipo de servicio (recargo de sala "
                        "grande, seguro del equipo o multiplicador del nivel de asesoría)."),
        ("2. Descuento", "Subtotal × porcentaje de descuento."),
        ("3. Neto", "Subtotal − descuento. (El programa lo usa internamente; no se muestra.)"),
        ("4. Impuesto", "Neto × porcentaje de impuesto."),
        ("5. Total", "Neto + impuesto. Es el valor que se cobra al cliente."),
    ], [0.2, 0.8], negrita_col0=True))
    X(S("7.2 Impuesto"))
    X(vinetas([
        "El valor predeterminado es <b>19 %</b> (IVA en Colombia). Puede cambiarlo en cada cálculo.",
        "Acepta valores entre 0 y 100. Puede escribirlo como " + K("19") + ", " + K("19%") + " o con "
        "decimales usando coma o punto (" + K("19,5") + ").",
        "Si deja el campo vacío o escribe 0, no se cobra impuesto.",
    ]))
    X(S("7.3 Descuento"))
    X(vinetas([
        "Se escribe como porcentaje, igual que el impuesto. Vacío o 0 significa sin descuento.",
        "<b>Al crear una reserva, el descuento máximo es del 50 %.</b> Si escribe más, el programa no deja "
        "crear la reserva y muestra «El descuento máximo permitido es 50%».",
        "En la herramienta «Calcular tarifa» de la pantalla Servicios el límite de 50 % no se aplica (solo "
        "el rango de 0 a 100 %), porque es una simple consulta de precio.",
    ]))
    X(S("7.4 Ejemplos resueltos"))
    A(P("Los siguientes valores fueron calculados con el mismo motor de cálculo del programa y coinciden con "
        "lo que muestra la pantalla:"))
    filas = []
    for nombre, formula, r, imp, desc in ejemplos_costos():
        filas.append((f"<b>{nombre}</b><br/><font size=7.8 color='#64748b'>{formula}</font>",
                      m(r["subtotal"]), f"{desc} % → − {m(r['descuento'])}",
                      f"{imp} % → + {m(r['impuesto'])}", f"<b>{m(r['total'])}</b>"))
    X(tabla(["Servicio y cálculo del subtotal", "Subtotal", "Descuento", "Impuesto", "TOTAL"], filas,
            [0.36, 0.14, 0.18, 0.18, 0.14]))
    A(aviso("ejemplo", [
        "<b>Auditorio Principal, 4 horas, 15 % de descuento, IVA 19 %</b>",
        "1. Subtotal: $ 80.000 × 4 horas = $ 320.000; como la capacidad (60) supera 20 personas, se suma el "
        "10 % de recargo → <b>$ 352.000</b>.",
        "2. Descuento: 15 % de $ 352.000 = <b>$ 52.800</b>.",
        "3. Neto: $ 352.000 − $ 52.800 = <b>$ 299.200</b>.",
        "4. Impuesto: 19 % de $ 299.200 = <b>$ 56.848</b>.",
        "5. Total: $ 299.200 + $ 56.848 = <b>$ 356.048</b>."]))
    X(S("7.5 Presentación de los valores"))
    A(P("En pantalla, los valores se muestran en pesos, sin decimales y con punto como separador de miles "
        "(por ejemplo, $ 160.650). Internamente el programa trabaja con dos decimales, por lo que en el "
        "historial de una reserva o en el log pueden aparecer valores como $160,650.00."))
    A(PageBreak())

    # =============== 8. Reservas
    A(Capitulo(8, "Gestión de reservas",
               "Crear reservas, seguir su ciclo de vida y consultar su historial."))
    A(Spacer(1, 10))
    X(S("8.1 El ciclo de vida de una reserva"))
    A(P("Toda reserva nace en estado <b>Pendiente</b> y avanza según las acciones que usted realice:"))
    A(diagrama_estados())
    A(Spacer(1, 8))
    X(tabla(["Estado", "Significado", "Acciones posibles", "¿Ocupa cupo?", "¿Suma ingresos?"], [
        ("Pendiente", "Recién creada; espera aprobación.", "Confirmar, Cancelar", "Sí", "No"),
        ("Confirmada", "Aceptada por la empresa.", "Procesar, Cancelar", "Sí", "Sí"),
        ("Procesada", "Facturada. Es un estado final.", "Ninguna", "No", "Sí"),
        ("Cancelada", "Anulada. Es un estado final.", "Ninguna", "No", "No"),
    ], [0.15, 0.31, 0.22, 0.15, 0.17], negrita_col0=True,
        estilos_extra=[("TEXTCOLOR", (0, 1), (0, 1), C["naranja"]), ("TEXTCOLOR", (0, 2), (0, 2), C["azul"]),
                       ("TEXTCOLOR", (0, 3), (0, 3), C["verde"]), ("TEXTCOLOR", (0, 4), (0, 4), C["rojo"])]))
    A(CondPageBreak(125 * mm))
    X(S("8.2 La pantalla de reservas"))
    anotar("42_reservas_tabla", "27_reservas_vacio",
           ["formulario", "resumen", "crear", "acciones", "filtro", "tabla", "leyenda"], "a_reservas")
    A(fig("a_reservas", "Pantalla de gestión de reservas.", carpeta=ANOT))
    X(leyenda([
        ("Nueva reserva", "Formulario: cliente, servicio, duración, impuesto y descuento."),
        ("Resumen del costo", "Subtotal, descuento, impuesto y TOTAL, calculados automáticamente mientras "
                              "escribe."),
        ("Crear reserva / Limpiar", "Registran la reserva o restablecen el formulario."),
        ("Botones de acción", "Confirmar, Procesar y Cancelar. Solo se activan los que corresponden al "
                              "estado de la reserva seleccionada."),
        ("Filtro de estado", "Muestra todas las reservas o solo las de un estado."),
        ("Reservas registradas", "Tabla de reservas, de la más reciente a la más antigua, coloreada según "
                                 "el estado. Doble clic para ver el historial."),
        ("Leyenda de colores", "Naranja: Pendiente · Azul: Confirmada · Verde: Procesada · Rojo: "
                               "Cancelada."),
    ]))
    X(S("8.3 Crear una reserva"))
    A(aviso("nota", "Antes de crear una reserva deben existir el cliente (capítulo 5) y el servicio "
                    "(capítulo 6)."))
    X(pasos([
        f"Haga clic en {B('Reservas')} en el menú lateral.",
        f"En {B('Cliente')}, despliegue la lista y elija el cliente (aparece como «identificación - "
        "nombre»).",
        f"En {B('Servicio (solo con cupo)')}, elija el servicio. La lista solo muestra servicios "
        "habilitados que tienen cupo libre.",
        f"Escriba la {B('Duración')}. Al elegir el servicio, la etiqueta indica la unidad: "
        f"{B('Duración (horas)')} o {B('Duración (días)')}.",
        f"Revise el {B('Impuesto %')} (19 por defecto) y escriba el {B('Desc. % (≤50)')} si aplica.",
        "Observe el resumen: el subtotal, el descuento, el impuesto y el TOTAL se actualizan solos "
        "mientras escribe.",
        f"Pulse {B('Crear reserva')}. Aparecerá un mensaje con el código asignado, el total y el estado "
        "Pendiente.",
    ]))
    A(fig("28_reserva_cotizacion", "Reserva de 3 horas de la Sala Ejecutiva para Laura Gómez, con IVA del "
                                   "19 % y 10 % de descuento: el total se calcula antes de crearla."))
    A(fig("29_reserva_creada_dlg", "La reserva R-0001 fue creada en estado Pendiente.", ancho=80 * mm))
    A(aviso("consejo", "Después de crear una reserva, el formulario se limpia pero <b>conserva el cliente "
                       "seleccionado</b>, para que pueda registrarle otra reserva rápidamente."))
    X(S("8.4 Avisos del resumen de costo"))
    A(P("Si la duración, el impuesto o el descuento no son válidos, el resumen muestra guiones (—) y debajo "
        "aparece un aviso en rojo que explica el problema, antes incluso de pulsar Crear reserva:"))
    A(fig("30_aviso_duracion", "40 días de alquiler superan el máximo de 30 días para equipos: el resumen "
                               "no muestra valores y explica el motivo."))
    A(fig("32_aviso_descuento", "Un descuento del 60 % supera el máximo permitido del 50 %."))
    A(P(f"Si de todas formas pulsa {B('Crear reserva')}, la reserva no se crea, aparece el mensaje de "
        "error y el campo con el problema se marca en rojo."))
    X(S("8.5 Confirmar una reserva"))
    X(pasos([
        "En la tabla, haga clic sobre una reserva en estado <b>Pendiente</b>. Se activan los botones "
        f"{B('Confirmar')} y {B('Cancelar')}.",
        f"Pulse {B('Confirmar')}.",
        f"Responda {B('Sí')} a la pregunta «¿Confirmar la reserva R-...?».",
        "Verá el mensaje «La reserva ... fue confirmada» y la fila cambia a color azul.",
    ]))
    A(fig("33_reserva_seleccionada", "Reserva pendiente seleccionada: Confirmar y Cancelar están activos; "
                                     "Procesar está apagado."))
    A(fig_doble("34_confirmar_pregunta_dlg", "35_confirmada_dlg",
                "Pregunta de confirmación y mensaje de resultado."))
    X(S("8.6 Procesar (facturar) una reserva"))
    A(P("Procesar significa facturar la reserva. Solo se pueden procesar reservas <b>Confirmadas</b>. Antes "
        "de facturar, el programa vuelve a calcular el total para verificar que no haya diferencias."))
    X(pasos([
        "Seleccione una reserva en estado <b>Confirmada</b>.",
        f"Pulse {B('Procesar')} y responda {B('Sí')} a la pregunta «¿Procesar (facturar) la reserva ...?».",
        "Verá el mensaje «Reserva ... procesada. Facturado: $ ...». La fila cambia a color verde.",
    ]))
    A(fig("36_confirmada_botones", "Reserva confirmada seleccionada: ahora está activo Procesar y "
                                   "Confirmar está apagado."))
    A(fig_doble("37_procesar_pregunta_dlg", "38_procesada_dlg", "Procesamiento de la reserva R-0002."))
    X(S("8.7 Cancelar una reserva"))
    A(aviso("atencion", "La cancelación <b>no se puede deshacer</b>. Solo se pueden cancelar reservas "
                        "Pendientes o Confirmadas. Una reserva cancelada libera el cupo del servicio y no "
                        "suma a los ingresos."))
    X(pasos([
        "Seleccione una reserva Pendiente o Confirmada.",
        f"Pulse el botón rojo {B('Cancelar')}.",
        f"Responda {B('Sí')} a la pregunta «¿Seguro que desea cancelar la reserva ...?».",
        "Escriba el motivo de la cancelación (opcional) y pulse " + B("OK") + ". Si no escribe nada, se "
        "anotará «Cancelada por el usuario».",
        "Verá el mensaje «La reserva ... fue cancelada». La fila cambia a color rojo.",
    ]))
    A(fig("40_motivo", "Ventana para escribir el motivo de la cancelación."))
    A(fig_doble("39_cancelar_pregunta_dlg", "41_cancelada_dlg", "Advertencia previa y mensaje final de la "
                                                                 "cancelación."))
    A(aviso("nota", f"Si pulsa {B('Cancel')} en la ventana del motivo, la reserva igualmente se cancela "
                    "con el motivo «Cancelada por el usuario». Para no cancelar, responda <b>No</b> en la "
                    "pregunta anterior."))
    X(S("8.8 Filtrar reservas por estado"))
    A(P(f"Use la lista {B('Estado')}, arriba a la derecha de la tabla, para ver solo las reservas Pendientes, "
        "Confirmadas, Procesadas o Canceladas. Elija «Todas» para volver a verlas todas."))
    A(fig("43_filtro_pendiente", "Filtro «Pendiente»: solo se muestran las reservas que esperan "
                                 "confirmación."))
    X(S("8.9 Ver el detalle e historial de una reserva"))
    A(P("Haga <b>doble clic</b> sobre una reserva de la tabla. Se abre una ventana con su descripción, el "
        "desglose del costo y el historial de cambios de estado con fecha, hora y nota:"))
    A(fig("44_historial_dlg", "Historial de la reserva R-0004: creada y luego cancelada con el motivo "
                              "indicado.", ancho=105 * mm))
    X(S("8.10 Cupos: cuándo un servicio deja de aparecer"))
    X(vinetas([
        "Cada reserva <b>Pendiente</b> o <b>Confirmada</b> ocupa un cupo del servicio.",
        "Cuando todas las plazas están ocupadas, el servicio pasa a «Sin cupo» y deja de aparecer en la "
        "lista de servicios de Nueva reserva.",
        "Al <b>procesar</b> o <b>cancelar</b> una reserva, su cupo se libera y el servicio vuelve a estar "
        "disponible.",
    ]))
    A(PageBreak())

    # =============== 9. Eventos
    A(Capitulo(9, "Registro de actividad",
               "Consulta de eventos, advertencias y errores, y del archivo software_fj.log."))
    A(Spacer(1, 10))
    A(P("Software FJ anota automáticamente todo lo que sucede: cada cliente, servicio o reserva registrada, "
        "cada cambio de estado y cada error. Esta información se puede consultar en la pantalla "
        f"{B('Eventos y logs')}."))
    anotar("47_eventos", "47_eventos", ["filtro", "resumen", "actualizar", "ver_archivo", "tabla"],
           "a_eventos")
    A(fig("a_eventos", "Pantalla de registro de eventos y errores.", carpeta=ANOT))
    X(leyenda([
        ("Filtrar", "Muestra Todos los eventos, Solo eventos (INFO), Advertencias o Errores."),
        ("Resumen", "Cantidad de eventos y de errores de la sesión."),
        ("Actualizar", "Vuelve a cargar la tabla."),
        ("Ver archivo software_fj.log", "Abre el archivo completo de registro."),
        ("Tabla de eventos", "Fecha y hora, nivel y mensaje de cada evento, del más reciente al más "
                             "antiguo. Doble clic para leer el mensaje completo."),
    ]))
    X(S("9.1 Niveles de los eventos"))
    X(tabla(["Nivel", "Significado", "Ejemplo"], [
        ("INFO", "Operación normal realizada con éxito.", "Cliente registrado: Cliente Laura Gómez"),
        ("WARNING", "Advertencia: situación que conviene revisar.", "—"),
        ("ERROR", "Operación rechazada por un dato inválido o una regla del negocio. Fondo rojizo.",
         "Registro de cliente rechazado -> DatoInvalidoError: [FJ-101] ..."),
        ("CRITICAL", "Error inesperado del programa. El programa sigue funcionando.",
         "Error inesperado en la interfaz"),
    ], [0.15, 0.45, 0.4], negrita_col0=True))
    X(S("9.2 Consultar solo los errores"))
    X(pasos([
        f"En la lista {B('Filtrar')} elija {B('Errores')}.",
        "La tabla muestra solo los eventos ERROR y CRITICAL.",
        "Haga doble clic sobre un evento para leer el mensaje completo en una ventana aparte.",
    ]))
    A(fig("48_eventos_errores", "Filtro «Errores»: se muestran los intentos rechazados de la sesión."))
    A(fig("49_detalle_evento_dlg", "Detalle de un evento de error (doble clic sobre la fila).",
          ancho=110 * mm))
    X(S("9.3 Ver el archivo software_fj.log"))
    X(pasos([
        f"Pulse el botón azul {B('Ver archivo software_fj.log')}.",
        "Se abre una ventana con el contenido completo del archivo. Las líneas de error aparecen en rojo, "
        "las advertencias en amarillo y los errores críticos resaltados en rojo intenso.",
        f"Pulse {B('Recargar')} para ver los eventos más recientes, o {B('Abrir carpeta')} (solo en "
        "Windows) para abrir la carpeta donde está guardado el archivo.",
    ]))
    A(fig("50_archivo_log", "Ventana del archivo software_fj.log."))
    A(aviso("importante", [
        "La tabla de la pantalla muestra solo los eventos de la <b>sesión actual</b> (hasta los últimos "
        "500). El archivo <b>software_fj.log</b>, en cambio, conserva la historia de <b>todas las "
        "sesiones</b>, porque cada vez se agregan líneas al final.",
        "El archivo se encuentra en la misma carpeta del programa; la ruta exacta aparece debajo del título "
        "de la pantalla."]))
    A(P("Cada línea del archivo tiene tres partes separadas por barras verticales: fecha y hora, nivel y "
        "mensaje. Por ejemplo:"))
    with open(os.path.join(CAPT, "log_ejemplo.txt"), encoding="utf-8") as f:
        lineas = f.read().splitlines()
    ejemplo = [lineas[1]] + [l for l in lineas if "| ERROR" in l][:1] + [l for l in lineas if "Confirmada" in l][:1]
    X(bloque_codigo("\n".join(l[:118] + ("…" if len(l) > 118 else "") for l in ejemplo), 7.3))
    A(PageBreak())

    # =============== 10. Herramientas
    A(Capitulo(10, "Herramientas adicionales",
               "Demostración automática, modo consola, información del programa y salida segura."))
    A(Spacer(1, 10))
    X(S("10.1 Demostración de 15 operaciones"))
    A(P("La demostración ejecuta automáticamente 15 operaciones de prueba (8 válidas y 7 inválidas a "
        "propósito) para comprobar que el programa registra lo correcto y rechaza lo incorrecto sin "
        "cerrarse. Es útil para conocer el programa o para presentarlo."))
    X(pasos([
        f"Pulse {B('Demostración')} en el menú lateral, o {B('Ejecutar simulación de 15 operaciones')} en "
        "el Panel principal.",
        f"Lea el aviso y responda {B('Sí')} para continuar.",
        "Se abre la ventana «Simulación de operaciones», que se llena fila por fila con el resultado de cada "
        "operación.",
        f"Al terminar, revise el resumen superior y pulse {B('Cerrar')}.",
    ]))
    A(fig("53_demo_pregunta_dlg", "Aviso previo a la demostración.", ancho=110 * mm))
    A(fig("54_demo_resultados", "Resultado de la demostración: 8 operaciones exitosas, 7 errores "
                                "controlados y 15 de 15 con el resultado esperado."))
    X(tabla(["Columna", "Significado"], [
        ("#", "Número de la operación (1 a 15)."),
        ("Operación", "Qué se intentó hacer."),
        ("Resultado", "«Exitosa» (fondo verde) o «Error controlado» (fondo rojo)."),
        ("¿Esperado?", "«Sí» si el resultado era el que debía ocurrir."),
        ("Detalle / mensaje de error", "Descripción del resultado o el mensaje del error. Doble clic para "
                                       "verlo completo."),
    ], [0.3, 0.7], negrita_col0=True))
    A(aviso("importante", "Los datos válidos de la demostración (2 clientes, 3 servicios y 2 reservas) "
                          "<b>se agregan a los datos que ya tenga</b>. Si usted ya registró clientes o "
                          "servicios con las mismas identificaciones o códigos (por ejemplo, 1032456789 o "
                          "SAL-01), algunas operaciones darán un resultado distinto y en «¿Esperado?» "
                          "aparecerá «No». Para una demostración limpia, ejecútela con el programa recién "
                          "abierto."))
    A(fig("55_panel_tras_demo", "Panel principal después de la demostración: los datos válidos quedaron "
                                "registrados."))
    X(S("10.2 Demostración en modo consola"))
    A(P(f"Si inicia el programa con {K('python main.py --consola')}, no se abre ninguna ventana: las 15 "
        "operaciones se ejecutan y sus resultados se muestran como texto. Este es un extracto real de la "
        "salida:"))
    with open(os.path.join(CAPT, "consola.txt"), encoding="utf-8") as f:
        consola = f.read().splitlines()
    X(bloque_codigo("\n".join(l[:120] for l in consola[:20]) + "\n ...", 7.2))
    X(S("10.3 Acerca de"))
    A(P(f"Pulse {B('Acerca de')} en el menú lateral para ver el nombre del programa, el curso y las "
        "tecnologías con las que fue construido."))
    A(fig("51_acerca_de_dlg", "Ventana «Acerca de Software FJ».", ancho=100 * mm))
    X(S("10.4 Salir del programa"))
    X(pasos([
        f"Pulse {B('Salir')} en la parte inferior del menú lateral (o la X de la esquina superior derecha "
        "de la ventana).",
        "El programa le recuerda que los datos están en memoria y se perderán.",
        f"Pulse {B('Sí')} para cerrar o {B('No')} para seguir trabajando.",
    ]))
    A(fig("52_salir_dlg", "Confirmación de salida.", ancho=100 * mm))
    A(PageBreak())

    # =============== 11. Caso práctico
    A(Capitulo(11, "Caso práctico completo",
               "Un recorrido de principio a fin con todas las funciones del programa."))
    A(Spacer(1, 10))
    A(aviso("ejemplo", "La empresa recibe a Laura Gómez, que necesita una sala para una reunión de 3 horas "
                       "con su equipo de 10 personas. Como es clienta frecuente, se le concede un 10 % de "
                       "descuento. Se usarán los mismos datos que aparecen en las imágenes de este "
                       "manual.", "SITUACIÓN"))
    X(pasos([
        f"<b>Abrir el programa.</b> En la carpeta de Software FJ, escriba {K('python main.py')} en el "
        "Símbolo del sistema (capítulo 2).",
        f"<b>Registrar a la clienta.</b> Vaya a {B('Clientes')} y registre: identificación "
        f"{K('1032456789')}, nombre {K('Laura Gómez')}, correo {K('laura.gomez@mail.com')}, teléfono "
        f"{K('3104567890')}. Pulse {B('Guardar')} (sección 5.1).",
        f"<b>Registrar la sala.</b> Vaya a {B('Servicios')}, elija {B('Sala')} y registre: código "
        f"{K('SAL-01')}, nombre {K('Sala Ejecutiva')}, tarifa {K('50000')}, capacidad {K('12')}, "
        f"reservas simultáneas {K('2')} (sección 6.3).",
        f"<b>Dar un precio a la clienta.</b> Seleccione SAL-01 en el catálogo, escriba duración {K('3')}, "
        f"impuesto {K('19')}, descuento {K('10')} y pulse {B('Calcular tarifa')}. El total es "
        "<b>$ 160.650</b> (sección 6.9).",
        f"<b>Crear la reserva.</b> Vaya a {B('Reservas')}, elija a Laura Gómez y la Sala Ejecutiva, "
        f"escriba los mismos valores y pulse {B('Crear reserva')}. Se crea la reserva <b>R-0001</b> en "
        "estado Pendiente (sección 8.3).",
        f"<b>Confirmarla.</b> Seleccione R-0001, pulse {B('Confirmar')} y responda Sí (sección 8.5).",
        f"<b>Facturarla.</b> Una vez prestado el servicio, seleccione R-0001, pulse {B('Procesar')} y "
        "responda Sí. La reserva queda Procesada y la sala libera su cupo (sección 8.6).",
        f"<b>Revisar el resultado.</b> En el {B('Panel principal')} verá 1 reserva procesada e ingresos por "
        f"$ 160.650. En {B('Eventos y logs')} quedará la traza de cada paso (capítulos 4 y 9).",
    ]))
    X(tabla(["Concepto", "Valor"], [
        ("Subtotal (3 h × $ 50.000)", "$ 150.000"),
        ("Descuento (10 %)", "− $ 15.000"),
        ("Impuesto (19 % sobre $ 135.000)", "+ $ 25.650"),
        ("<b>Total facturado</b>", "<b>$ 160.650</b>"),
    ], [0.6, 0.4]))
    X(H3("Para practicar más, puede usar estos datos de ejemplo:"))
    X(tabla(["Clientes", "Servicios"], [
        ("80123456 · Andrés Pérez · aperez@empresa.co · 6017654321",
         "EQU-01 · Videobeam Epson · Equipo · $ 35.000/día · Proyector · 1 unidad"),
        ("1019876543 · Camila Rodríguez · camila.rodriguez@correo.com · 3125558899",
         "ASE-01 · Asesoría en Ciberseguridad · $ 120.000/hora · Experto"),
        ("79456123 · Juan Martínez · jmartinez@outlook.com · 3157771234",
         "SAL-02 · Auditorio Principal · $ 80.000/hora · 60 personas · cupo 1"),
        ("1144223344 · Sofía Herrera · sofia.herrera@gmail.com · 3009876543",
         "EQU-02 · Portátil Lenovo · $ 45.000/día · 3 unidades"),
    ], [0.5, 0.5]))
    A(PageBreak())

    # =============== 12. Solución de problemas
    A(Capitulo(12, "Solución de problemas",
               "Qué significan los mensajes del programa y cómo resolver las situaciones más comunes."))
    A(Spacer(1, 10))
    X(S("12.1 Problemas al abrir el programa"))
    X(tabla(["Síntoma", "Causa probable", "Solución"], [
        ("«python» no se reconoce como un comando interno o externo",
         "Python no está instalado o no se marcó «Add python.exe to PATH».",
         "Reinstale Python marcando esa casilla (sección 2.2). También puede probar con " + K("py main.py")
         + "."),
        ("can't open file ... main.py: No such file or directory",
         "El Símbolo del sistema no está en la carpeta del programa.",
         "Abra el Símbolo del sistema desde la carpeta que contiene main.py (sección 2.4)."),
        ("ModuleNotFoundError: No module named 'tkinter'",
         "La instalación de Python no incluye Tkinter (frecuente en Linux).",
         "Instale Python desde python.org o, en Linux, el paquete python3-tk."),
        ("«Error al iniciar Software FJ: ... Revise software_fj.log»",
         "Un problema impidió crear la ventana.",
         "Abra software_fj.log con el Bloc de notas y lea la última línea CRITICAL; verifique que la "
         "carpeta del programa esté completa."),
        ("La ventana se ve cortada o las tablas muestran pocas filas",
         "Pantalla pequeña.", "Maximice la ventana y use las barras de desplazamiento de las tablas."),
    ], [0.3, 0.3, 0.4]))
    X(S("12.2 Mensajes del programa y cómo resolverlos"))
    X(tabla(["Mensaje que aparece", "Qué significa", "Qué hacer"], [
        ("El campo 'X' es obligatorio.", "Dejó vacío un campo requerido.", "Escriba el dato en el campo "
                                                                           "marcado en rojo."),
        ("Valor inválido para 'identificación' ...: debe tener entre 5 y 12 dígitos",
         "La identificación tiene letras, signos o una longitud incorrecta.", "Escriba solo números, de 5 a "
                                                                              "12 dígitos."),
        ("... 'nombre' ...: solo letras y mínimo 3 caracteres", "El nombre tiene números o símbolos, o es "
                                                                "muy corto.", "Escriba nombres y apellidos "
                                                                              "solo con letras."),
        ("... 'correo' ...: formato de correo no válido", "Falta la @, el dominio o la extensión.",
         "Verifique que tenga la forma usuario@dominio.com."),
        ("... 'teléfono' ...: debe tener entre 7 y 10 dígitos", "El teléfono es muy corto, muy largo o "
                                                                "tiene letras.", "Escriba de 7 a 10 "
                                                                                 "números."),
        ("Ya existe un cliente con identificador '...'", "Ese cliente ya fue registrado.",
         "Búsquelo en la tabla; si necesita cambiar sus datos, use Actualizar."),
        ("Ya existe un servicio con identificador '...'", "El código de servicio ya está en uso.",
         "Use otro código (por ejemplo, SAL-03)."),
        ("... 'tarifa' ...: debe ser numérico / debe ser mayor que cero",
         "La tarifa tiene puntos, signo $, letras o es 0 o negativa.", "Escriba solo números, por ejemplo "
                                                                       "50000."),
        ("... 'capacidad' ...: no puede superar 500", "Capacidad de sala mayor de 500 personas.",
         "Escriba un valor entre 1 y 500."),
        ("... 'duración' ...: para Sala debe estar entre 1 y 12 horas (o Equipo 1–30 días, Asesoría 0.5–8 "
         "horas)", "La duración está fuera de los límites del tipo de servicio.", "Ajuste la duración "
                                                                                  "(tabla 6.1)."),
        ("... los equipos se alquilan por días completos", "Escribió días con decimales para un equipo.",
         "Escriba un número entero de días."),
        ("El impuesto 'X' no es un número / debe estar entre 0 y 100 %", "Porcentaje mal escrito o fuera "
                                                                         "de rango.",
         "Escriba un número entre 0 y 100."),
        ("El descuento máximo permitido es 50%.", "Descuento mayor del 50 % al crear una reserva.",
         "Escriba un descuento de 0 a 50."),
        ("No existe un cliente con identificador ''", "Pulsó Crear reserva sin elegir el cliente.",
         "Elija un cliente en la lista Cliente."),
        ("No existe un servicio con identificador ''", "No eligió el servicio.",
         "Elija un servicio en la lista Servicio."),
        ("Servicio '...': no tiene cupos libres.", "Todas las plazas del servicio están ocupadas.",
         "Procese o cancele otra reserva del servicio, o elija otro servicio."),
        ("Servicio '...': está deshabilitado / se deshabilitó antes de confirmar",
         "El servicio fue deshabilitado.", "Habilítelo en la pantalla Servicios (sección 6.10)."),
        ("No se puede 'X' una reserva en estado 'Y'.", "La acción no corresponde al estado de la reserva.",
         "Revise el ciclo de vida (sección 8.1)."),
        ("Seleccione un servicio / Seleccione una reserva", "Pulsó un botón sin elegir antes una fila.",
         "Haga clic sobre una fila de la tabla y repita la acción."),
        ("Escriba una identificación, nombre o correo para buscar.", "La casilla de búsqueda está vacía.",
         "Escriba el texto que desea buscar."),
        ("Error inesperado", "Ocurrió un problema imprevisto.", "Pulse Aceptar y siga trabajando. Si se "
                                                                "repite, revise los eventos CRITICAL "
                                                                "(capítulo 9) e informe al equipo de "
                                                                "soporte."),
    ], [0.38, 0.32, 0.30]))
    X(S("12.3 Códigos de error del registro"))
    A(P("En el archivo software_fj.log, los errores incluyen un código entre corchetes que ayuda a "
        "identificar el tipo de problema:"))
    X(tabla(["Código", "Tipo de error"], [
        ("FJ-101", "Dato con formato o valor no permitido."),
        ("FJ-102", "Falta un dato obligatorio."),
        ("FJ-200", "No se encontró el cliente, servicio o reserva solicitado."),
        ("FJ-201", "Registro duplicado (identificación o código ya existente)."),
        ("FJ-300", "Servicio no disponible (deshabilitado o sin cupo)."),
        ("FJ-400", "Error general de reserva."),
        ("FJ-401", "Operación no permitida para el estado actual de la reserva."),
        ("FJ-500", "Cálculo inconsistente (impuesto o descuento inválido, o totales que no coinciden)."),
    ], [0.18, 0.82], negrita_col0=True))
    X(S("12.4 Otras situaciones"))
    X(tabla(["Situación", "Explicación y solución"], [
        ("Un servicio no aparece en la lista al crear la reserva", "Está deshabilitado o sin cupo. "
                                                                   "Revise su estado en el catálogo."),
        ("Un botón aparece gris y no responde", "La acción no aplica en ese momento (por ejemplo, Procesar "
                                                "una reserva pendiente) o no hay ninguna fila "
                                                "seleccionada."),
        ("El resumen de costo muestra «—»", "Falta elegir el servicio o un dato es inválido; lea el aviso "
                                            "en rojo debajo del resumen."),
        ("Cerré el programa y desaparecieron mis datos", "Es el funcionamiento normal: los datos solo "
                                                         "existen mientras el programa está abierto "
                                                         "(sección 1.3). El historial queda en "
                                                         "software_fj.log."),
        ("La búsqueda no encuentra un nombre con tilde", "Escriba la tilde tal como está registrada o "
                                                         "busque por la identificación."),
    ], [0.38, 0.62], negrita_col0=True))
    A(PageBreak())

    # =============== 13. FAQ
    A(Capitulo(13, "Preguntas frecuentes", "Respuestas rápidas a las dudas más comunes."))
    A(Spacer(1, 10))
    faq = [
        ("¿Necesito Internet para usar Software FJ?", "No. El programa funciona completamente en su "
                                                       "computador."),
        ("¿Dónde se guardan los datos?", "En la memoria del computador mientras el programa está abierto. Al "
                                          "cerrarlo se borran. Solo el registro de actividad se guarda en "
                                          "el archivo software_fj.log."),
        ("¿Puedo eliminar un cliente o un servicio?", "No. La versión actual no tiene esa opción. Los "
                                                       "servicios pueden deshabilitarse para que no se "
                                                       "reserven."),
        ("¿Puedo cambiar la identificación de un cliente?", "No. Solo se pueden actualizar nombre, correo y "
                                                             "teléfono."),
        ("¿Puedo modificar una reserva ya creada?", "No. Si los datos no son correctos, cancele la reserva "
                                                     "y cree una nueva."),
        ("¿Por qué el total de un equipo es mayor que tarifa × días?", "Porque todo alquiler de equipo "
                                                                        "incluye un seguro obligatorio del "
                                                                        "5 %."),
        ("¿Por qué una sala cuesta 10 % más de lo esperado?", "Las salas con capacidad mayor de 20 personas "
                                                               "tienen un recargo del 10 %."),
        ("¿El descuento se aplica antes o después del impuesto?", "Antes. El impuesto se calcula sobre el "
                                                                   "valor ya descontado."),
        ("¿Qué reservas se suman a los ingresos?", "Las Confirmadas y las Procesadas, con impuestos "
                                                    "incluidos."),
        ("¿Una reserva cancelada se puede reactivar?", "No. La cancelación es definitiva; cree una nueva "
                                                        "reserva."),
        ("¿Qué pasa si ocurre un error?", "El programa muestra un mensaje, anota el error en el registro y "
                                          "sigue funcionando. Ningún error cierra la aplicación."),
    ]
    for p_, r_ in faq:
        A(KeepTogether([P(p_, "h3"), P(r_)]))
    A(PageBreak())

    # =============== 14. Glosario
    A(Capitulo(14, "Glosario", "Términos usados en el programa y en este manual."))
    A(Spacer(1, 10))
    X(tabla(["Término", "Definición"], [
        ("Asesoría", "Servicio profesional cobrado por horas, con nivel Básico, Intermedio o Experto."),
        ("Barra de estado", "Franja inferior de la ventana que informa el resultado de la última acción."),
        ("Cancelar (reserva)", "Anular una reserva pendiente o confirmada. Es definitivo."),
        ("Catálogo", "Lista de todos los servicios registrados."),
        ("Código de reserva", "Identificador automático con el formato R-0001."),
        ("Confirmar", "Aprobar una reserva pendiente."),
        ("Cupo", "Número de reservas activas que admite un servicio al mismo tiempo."),
        ("Deshabilitar", "Bloquear un servicio para que no reciba nuevas reservas."),
        ("Equipo", "Servicio de alquiler de equipos, cobrado por días e incluye un seguro del 5 %."),
        ("Evento", "Anotación automática de algo que ocurrió en el programa."),
        ("IVA", "Impuesto al valor agregado. El programa propone 19 % por defecto."),
        ("Log", "Registro de eventos. En Software FJ es el archivo software_fj.log."),
        ("Neto", "Subtotal menos el descuento; base sobre la que se calcula el impuesto."),
        ("Procesar", "Facturar una reserva confirmada."),
        ("Reserva activa", "Reserva en estado Pendiente o Confirmada; ocupa cupo."),
        ("Sala", "Espacio físico que se reserva por horas."),
        ("Subtotal", "Valor del servicio antes de descuentos e impuestos."),
        ("Tarifa", "Precio por hora o por día de un servicio."),
        ("Tkinter", "Herramienta incluida en Python con la que se construyó la ventana del programa."),
    ], [0.25, 0.75], negrita_col0=True))
    A(PageBreak())

    # =============== Anexo
    A(Capitulo("A", "Referencia rápida", "Las tareas más comunes en una sola página."))
    A(Spacer(1, 10))
    X(tabla(["Quiero...", "Vaya a", "Haga esto"], [
        ("Abrir el programa", "Carpeta del programa", "Escriba " + K("python main.py") + " en el Símbolo del "
                                                                                     "sistema."),
        ("Registrar un cliente", "Clientes", "Llene los 4 campos → Guardar."),
        ("Buscar un cliente", "Clientes", "Escriba en la casilla de búsqueda → Buscar."),
        ("Cambiar el teléfono de un cliente", "Clientes", "Clic en el cliente → corrija → Actualizar."),
        ("Registrar una sala, equipo o asesoría", "Servicios", "Elija el tipo → llene los campos → Guardar."),
        ("Saber si un servicio tiene cupo", "Servicios", "Clic en el servicio → Consultar disponibilidad."),
        ("Dar un precio sin reservar", "Servicios", "Clic en el servicio → duración, impuesto, descuento → "
                                                    "Calcular tarifa."),
        ("Bloquear un servicio", "Servicios", "Clic en el servicio → Deshabilitar → Sí."),
        ("Crear una reserva", "Reservas", "Elija cliente y servicio → duración → Crear reserva."),
        ("Confirmar una reserva", "Reservas", "Clic en la reserva Pendiente → Confirmar → Sí."),
        ("Facturar una reserva", "Reservas", "Clic en la reserva Confirmada → Procesar → Sí."),
        ("Cancelar una reserva", "Reservas", "Clic en la reserva → Cancelar → Sí → motivo → OK."),
        ("Ver el historial de una reserva", "Reservas", "Doble clic sobre la reserva."),
        ("Ver solo los errores", "Eventos y logs", "Filtrar → Errores."),
        ("Ver el archivo de registro", "Eventos y logs", "Ver archivo software_fj.log."),
        ("Probar el programa automáticamente", "Menú lateral", "Demostración → Sí."),
        ("Cerrar el programa", "Menú lateral", "Salir → Sí."),
    ], [0.32, 0.2, 0.48], negrita_col0=True))
    return h


def construir():
    doc = Manual(SALIDA)
    doc.multiBuild(contenido())
    print("PDF generado:", SALIDA, "| figuras:", CONTADOR["fig"])


if __name__ == "__main__":
    construir()
