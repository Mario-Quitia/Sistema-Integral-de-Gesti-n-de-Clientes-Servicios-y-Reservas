"""
Genera los diagramas del libro (PNG) en docs/libro/img.
Los datos de los diagramas UML, de imports y de Git corresponden al código y
al repositorio reales de Software FJ.
Uso: python docs/libro/herramientas/diagramas.py
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

SALIDA = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "img"))
os.makedirs(SALIDA, exist_ok=True)
FD = "C:/Windows/Fonts/"


def fuente(tam, tipo="r"):
    archivo = {"r": "segoeui.ttf", "b": "segoeuib.ttf", "sb": "seguisb.ttf", "i": "segoeuii.ttf",
               "m": "consola.ttf", "mb": "consolab.ttf"}[tipo]
    return ImageFont.truetype(FD + archivo, tam)


NAVY, AZUL, AZUL_CL, CELESTE = "#0f172a", "#2563eb", "#dbeafe", "#eff6ff"
GRIS, GRIS_CL, BORDE, TEXTO = "#64748b", "#f1f5f9", "#cbd5e1", "#1e293b"
VERDE, NARANJA, ROJO, MORADO, TURQ = "#16a34a", "#d97706", "#dc2626", "#7c3aed", "#0891b2"
BLANCO = "#ffffff"


class Lienzo:
    def __init__(self, ancho, alto, fondo=BLANCO):
        self.img = Image.new("RGB", (ancho, alto), fondo)
        self.d = ImageDraw.Draw(self.img)

    def caja(self, x, y, w, h, fondo=CELESTE, borde=AZUL, texto=None, color=TEXTO, tam=26, tipo="sb",
             radio=16, grosor=3, alinear="centro"):
        self.d.rounded_rectangle([x, y, x + w, y + h], radius=radio, fill=fondo, outline=borde, width=grosor)
        if texto:
            self.texto_centrado(x, y, w, h, texto, color, tam, tipo, alinear)
        return (x, y, w, h)

    def texto_centrado(self, x, y, w, h, texto, color=TEXTO, tam=26, tipo="sb", alinear="centro"):
        lineas = texto.split("\n")
        f = fuente(tam, tipo)
        alto_l = tam * 1.3
        y0 = y + h / 2 - alto_l * len(lineas) / 2
        for i, l in enumerate(lineas):
            fl = f
            if l.startswith("**"):
                l, fl = l[2:], fuente(tam, "b")
            if l.startswith("``"):
                l, fl = l[2:], fuente(int(tam * 0.92), "m")
            tw = self.d.textlength(l, font=fl)
            tx = x + (w - tw) / 2 if alinear == "centro" else x + 18
            self.d.text((tx, y0 + i * alto_l), l, font=fl, fill=color)

    def t(self, x, y, texto, tam=24, tipo="r", color=TEXTO, ancla="la"):
        self.d.text((x, y), texto, font=fuente(tam, tipo), fill=color, anchor=ancla)

    def flecha(self, p1, p2, color=GRIS, grosor=4, punta=16, texto=None, tam=21, dx=0, dy=-16,
               discontinua=False, hueca=False):
        x1, y1 = p1
        x2, y2 = p2
        if discontinua:
            largo = math.dist(p1, p2)
            n = int(largo // 18)
            for i in range(0, n, 2):
                a = (x1 + (x2 - x1) * i / n, y1 + (y2 - y1) * i / n)
                b = (x1 + (x2 - x1) * (i + 1) / n, y1 + (y2 - y1) * (i + 1) / n)
                self.d.line([a, b], fill=color, width=grosor)
        else:
            self.d.line([p1, p2], fill=color, width=grosor)
        ang = math.atan2(y2 - y1, x2 - x1)
        pts = [(x2, y2), (x2 - punta * math.cos(ang - 0.45), y2 - punta * math.sin(ang - 0.45)),
               (x2 - punta * math.cos(ang + 0.45), y2 - punta * math.sin(ang + 0.45))]
        if hueca:
            self.d.polygon(pts, fill=BLANCO, outline=color, width=grosor)
        else:
            self.d.polygon(pts, fill=color)
        if texto:
            f = fuente(tam, "sb")
            mx, my = (x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy
            tw = self.d.textlength(texto, font=f)
            self.d.rectangle([mx - tw / 2 - 4, my - tam * 0.7, mx + tw / 2 + 4, my + tam * 0.7], fill=BLANCO)
            self.d.text((mx, my), texto, font=f, fill=color, anchor="mm")

    def titulo(self, texto, sub=None):
        self.t(40, 28, texto, 34, "b", NAVY)
        if sub:
            self.t(40, 76, sub, 22, "r", GRIS)

    def uml(self, x, y, w, nombre, atributos, metodos, estereotipo=None, color=AZUL, tam=19):
        """Clase UML: devuelve (x, y, w, h)."""
        fl = tam * 1.38
        h_nom = 58 if estereotipo else 44
        h = h_nom + len(atributos) * fl + len(metodos) * fl + 30
        self.d.rectangle([x, y, x + w, y + h], fill=BLANCO, outline=color, width=3)
        self.d.rectangle([x, y, x + w, y + h_nom], fill=color)
        if estereotipo:
            self.d.text((x + w / 2, y + 16), f"«{estereotipo}»", font=fuente(16, "i"), fill="#e0e7ff",
                        anchor="mm")
            self.d.text((x + w / 2, y + 40), nombre, font=fuente(23, "b"), fill=BLANCO, anchor="mm")
        else:
            self.d.text((x + w / 2, y + h_nom / 2), nombre, font=fuente(23, "b"), fill=BLANCO, anchor="mm")
        yy = y + h_nom + 6
        for a in atributos:
            self.d.text((x + 10, yy), a, font=fuente(tam, "m"), fill=TEXTO)
            yy += fl
        yy += 6
        self.d.line([x, yy, x + w, yy], fill=color, width=2)
        yy += 6
        for m in metodos:
            self.d.text((x + 10, yy), m, font=fuente(tam, "m"), fill=TEXTO)
            yy += fl
        return (x, y, w, h)

    def guardar(self, nombre):
        self.img.save(os.path.join(SALIDA, nombre + ".png"))
        print("diagrama", nombre, self.img.size)


def arriba(c):
    return (c[0] + c[2] / 2, c[1])


def abajo(c):
    return (c[0] + c[2] / 2, c[1] + c[3])


def izq(c):
    return (c[0], c[1] + c[3] / 2)


def der(c):
    return (c[0] + c[2], c[1] + c[3] / 2)


# --------------------------------------------------------------------------- básicos
def d_programa():
    L = Lienzo(1800, 560)
    L.titulo("Todo programa: entrada → proceso → salida", "Así funciona también Software FJ")
    datos = [("ENTRADA", "Lo que el usuario entrega", "**Identificación, nombre,\ncorreo y teléfono\nescritos en el formulario", VERDE, "#f0fdf4"),
             ("PROCESO", "Lo que hace el programa", "**Validar los datos,\ncrear el objeto Cliente\ny guardarlo en la lista", AZUL, CELESTE),
             ("SALIDA", "Lo que el usuario recibe", "**Mensaje «Cliente registrado»,\nfila nueva en la tabla\ny línea en software_fj.log", MORADO, "#f5f3ff")]
    x = 60
    cajas = []
    for tit, sub, cuerpo, col, fondo in datos:
        L.caja(x, 130, 500, 70, col, col, tit, BLANCO, 30, "b", 14)
        L.t(x + 250, 222, sub, 21, "i", GRIS, "mm")
        cajas.append(L.caja(x, 250, 500, 250, fondo, col, cuerpo, TEXTO, 25, "r"))
        x += 600
    L.flecha(der(cajas[0]), izq(cajas[1]), GRIS, 6, 26)
    L.flecha(der(cajas[1]), izq(cajas[2]), GRIS, 6, 26)
    L.guardar("d_programa")


def d_interprete():
    L = Lienzo(1800, 620)
    L.titulo("Del archivo .py al programa funcionando", "El intérprete de Python lee tu código y le da órdenes al computador")
    a = L.caja(60, 140, 470, 400, "#1e1e1e", "#1e1e1e", radio=12)
    L.t(80, 158, "main.py", 22, "sb", "#cccccc")
    codigo = ["import sys", "", "def main():", "    app = VentanaPrincipal()", "    app.mainloop()", "",
              "if __name__ == \"__main__\":", "    sys.exit(main())"]
    for i, l in enumerate(codigo):
        L.t(80, 205 + i * 38, l, 22, "m", "#9cdcfe" if "def" in l or "import" in l else "#d4d4d4")
    L.t(295, 570, "1. Tú escribes instrucciones (texto)", 22, "sb", NAVY, "mm")
    b = L.caja(665, 220, 470, 240, NAVY, NAVY, "**Intérprete de Python\n\nlee una línea, la entiende\ny la ejecuta, una tras otra", BLANCO, 25)
    L.t(900, 570, "2. Python traduce y ejecuta", 22, "sb", NAVY, "mm")
    c = L.caja(1270, 140, 470, 400, CELESTE, AZUL)
    L.caja(1300, 175, 410, 260, BLANCO, BORDE, radio=8)
    L.caja(1300, 175, 110, 260, NAVY, NAVY, radio=8)
    L.caja(1318, 195, 40, 30, AZUL, AZUL, "FJ", BLANCO, 16, "b", 4)
    for i in range(4):
        L.caja(1430 + (i % 2) * 135, 200 + (i // 2) * 95, 120, 75, GRIS_CL, BORDE, radio=6)
    L.texto_centrado(1270, 450, 470, 80, "**El computador muestra\nla ventana de Software FJ", TEXTO, 23)
    L.t(1505, 570, "3. Ves el resultado", 22, "sb", NAVY, "mm")
    L.flecha(der(a), izq(b), AZUL, 6, 26, "python main.py", 22, dy=-24)
    L.flecha(der(b), izq(c), AZUL, 6, 26)
    L.guardar("d_interprete")


def d_variable():
    L = Lienzo(1800, 600)
    L.titulo("Una variable es una caja con etiqueta", "El nombre es la etiqueta; dentro se guarda un valor de cierto tipo")
    datos = [("nombre", "\"Laura Gómez\"", "str  (texto)", AZUL), ("duracion", "3", "int  (entero)", VERDE),
             ("tarifa", "50000.0", "float  (decimal)", NARANJA), ("disponible", "True", "bool  (verdadero/falso)", MORADO)]
    x = 50
    for nom, val, tipo, col in datos:
        L.d.polygon([(x + 30, 220), (x + 380, 220), (x + 410, 190), (x + 60, 190)], fill="#e2e8f0", outline=col)
        L.caja(x + 30, 220, 350, 220, BLANCO, col, None, radio=6, grosor=4)
        L.texto_centrado(x + 30, 260, 350, 140, "``" + val, TEXTO, 32, "m")
        L.caja(x + 85, 160, 240, 52, col, col, nom, BLANCO, 26, "mb", 10)
        L.t(x + 205, 470, tipo, 23, "sb", col, "mm")
        x += 430
    L.t(900, 540, "En Python:   nombre = \"Laura Gómez\"    →  el signo = guarda el valor en la caja", 25, "m",
        NAVY, "mm")
    L.guardar("d_variable")


def d_lista_dic():
    L = Lienzo(1800, 700)
    L.titulo("Lista frente a diccionario", "La lista se consulta por posición; el diccionario, por nombre (clave)")
    L.t(60, 130, "Lista  →  nombres = [\"Laura\", \"Andrés\", \"Camila\"]", 25, "mb", AZUL)
    for i, v in enumerate(["\"Laura\"", "\"Andrés\"", "\"Camila\""]):
        L.caja(60 + i * 270, 190, 250, 110, CELESTE, AZUL, "``" + v, TEXTO, 28)
        L.caja(140 + i * 270, 315, 90, 46, AZUL, AZUL, str(i), BLANCO, 24, "b", 23)
    L.t(60, 380, "nombres[0]  →  \"Laura\"     (las posiciones empiezan en 0)", 23, "m", GRIS)
    L.t(920, 130, "Diccionario  →  cliente = {...}", 25, "mb", MORADO)
    pares = [("\"identificacion\"", "\"1032456789\""), ("\"nombre\"", "\"Laura Gómez\""),
             ("\"correo\"", "\"laura.gomez@mail.com\""), ("\"telefono\"", "\"3104567890\"")]
    for i, (k, v) in enumerate(pares):
        y = 190 + i * 95
        L.caja(920, y, 330, 75, MORADO, MORADO, "``" + k, BLANCO, 23)
        L.flecha((1255, y + 37), (1320, y + 37), MORADO, 4, 14)
        L.caja(1325, y, 430, 75, "#f5f3ff", MORADO, "``" + v, TEXTO, 23)
    L.t(920, 590, "cliente[\"nombre\"]  →  \"Laura Gómez\"", 23, "m", GRIS)
    L.t(60, 470, "En Software FJ:", 24, "b", NAVY)
    L.t(60, 510, "• GestorClientes guarda los clientes en una lista: self._clientes = []", 22, "r", TEXTO)
    L.t(60, 548, "• Cliente.a_diccionario() devuelve un diccionario", 22, "r", TEXTO)
    L.t(60, 586, "  que la tabla de la pantalla usa para llenar sus columnas", 22, "r", TEXTO)
    L.guardar("d_lista_dic")


def d_molde():
    L = Lienzo(1800, 760)
    L.titulo("La clase es el molde; los objetos son lo que se fabrica con él")
    clase = L.uml(650, 120, 500, "Cliente", ["identificacion", "nombre", "correo", "telefono"],
                  ["describir()", "a_diccionario()"], "clase = molde", NAVY, 22)
    objetos = [("laura", "1032456789", "Laura Gómez", "laura.gomez@mail.com"),
               ("andres", "80123456", "Andrés Pérez", "aperez@empresa.co"),
               ("camila", "1019876543", "Camila Rodríguez", "camila.rodriguez@correo.com")]
    for i, (var, ide, nom, cor) in enumerate(objetos):
        x = 60 + i * 580
        c = L.caja(x, 470, 520, 230, CELESTE, AZUL, None, radio=14)
        L.caja(x, 470, 520, 54, AZUL, AZUL, f"{var} : Cliente", BLANCO, 23, "mb", 14)
        for j, l in enumerate([f"identificacion = \"{ide}\"", f"nombre = \"{nom}\"", f"correo = \"{cor}\""]):
            L.t(x + 18, 545 + j * 44, l, 19, "m", TEXTO)
        L.flecha(abajo(clase), arriba(c), GRIS, 3, 16, "Cliente(...)" if i == 1 else None, 20, dy=-30,
                 discontinua=True)
    L.t(900, 735, "Un mismo molde, muchos objetos distintos: cada uno con sus propios datos", 22, "i", GRIS, "mm")
    L.guardar("d_molde")


# --------------------------------------------------------------------------- arquitectura
def d_capas():
    L = Lienzo(1800, 1000)
    L.titulo("Arquitectura de Software FJ por capas", "Cada capa solo conversa con la de abajo; la interfaz nunca calcula ni valida")
    L.caja(560, 115, 680, 80, NAVY, NAVY, "main.py  ·  punto de entrada", BLANCO, 26, "b")
    capas = [("CAPA DE PRESENTACIÓN  ·  interfaz/", "ventana_principal.py · dashboard.py · vista_clientes.py\nvista_servicios.py · vista_reservas.py · componentes.py", AZUL, CELESTE,
              "Muestra ventanas, formularios y tablas; captura lo que escribe el usuario"),
             ("CAPA DE GESTIÓN  ·  gestores/", "SistemaFJ · GestorClientes · GestorServicios · GestorReservas", TURQ, "#ecfeff",
              "Organiza las listas de objetos y coordina las operaciones"),
             ("CAPA DE DOMINIO (MODELOS)  ·  modelos/", "Entidad · Cliente · Servicio · ReservaSala · AlquilerEquipo\nAsesoria · Reserva · EstadoReserva", VERDE, "#f0fdf4",
              "Reglas del negocio: validaciones, cálculos de costo y estados")]
    cajas = []
    y = 240
    for tit, cuerpo, col, fondo, desc in capas:
        L.caja(60, y, 1280, 190, fondo, col, None, radio=18, grosor=4)
        L.caja(60, y, 1280, 56, col, col, tit, BLANCO, 25, "b", 18)
        L.texto_centrado(60, y + 56, 1280, 90, cuerpo, TEXTO, 23, "m")
        L.t(700, y + 165, desc, 21, "i", GRIS, "mm")
        cajas.append((60, y, 1280, 190))
        y += 235
    L.flecha((700, 195), (700, 240), NAVY, 5, 18)
    L.flecha(abajo(cajas[0]), arriba(cajas[1]), GRIS, 5, 18, "llama a", 20, dx=60, dy=0)
    L.flecha(abajo(cajas[1]), arriba(cajas[2]), GRIS, 5, 18, "crea y usa", 20, dx=70, dy=0)
    L.caja(1400, 240, 340, 330, "#fef2f2", ROJO, "**excepciones.py\n\nSoftwareFJError y\nsus subclases\n\n(errores con nombre)", TEXTO, 23)
    L.caja(1400, 610, 340, 330, "#fffbeb", NARANJA, "**registro.py\n\nescribe cada evento en\nsoftware_fj.log y\nen memoria para la\npantalla de eventos", TEXTO, 23)
    L.t(1570, 960, "Transversales: los usan todas las capas", 20, "i", GRIS, "mm")
    L.caja(60, 945 - 10, 560, 50, GRIS_CL, BORDE, "simulacion.py · 15 operaciones de prueba", TEXTO, 20)
    L.guardar("d_capas")


def d_uml_modelos():
    L = Lienzo(2000, 1500)
    L.titulo("Diagrama UML de clases · paquete modelos/", "Flecha con punta hueca = herencia («es un»). Flecha simple = asociación («tiene un»)")
    ent = L.uml(760, 120, 480, "Entidad", ["# _identificador", "# _fecha_creacion"],
                ["+ identificador", "+ fecha_creacion", "+ describir()  {abstracto}", "+ a_diccionario()  {abstracto}",
                 "+ __eq__(), __hash__(), __repr__()"], "abstracta · ABC", NAVY)
    cli = L.uml(60, 560, 520, "Cliente", ["- __nombre", "- __correo", "- __telefono"],
                ["+ identificacion", "+ nombre / correo / telefono", "  (propiedades con validación)", "+ correo_oculto",
                 "+ describir()", "+ a_diccionario()"], None, AZUL)
    ser = L.uml(720, 560, 560, "Servicio", ["# _nombre, _tarifa, _cupo", "# _disponible"],
                ["+ tipo, unidad  {abstractos}", "+ validar_parametros(d)  {abs.}", "+ calcular_costo_base(d)  {abs.}",
                 "+ detalle()  {abstracto}", "+ calcular_costo(d, imp=None, desc=None)", "+ calcular_costo_detallado(...)",
                 "+ habilitar() / deshabilitar()"], "abstracta", TURQ)
    res = L.uml(1420, 560, 520, "Reserva", ["# _cliente : Cliente", "# _servicio : Servicio", "# _duracion, _costos",
                                             "# _estado, _historial"],
                ["+ codigo, total, activa", "+ confirmar()", "+ cancelar(motivo)", "+ procesar()", "+ describir()",
                 "+ a_diccionario()"], None, VERDE)
    sub = [("ReservaSala", ["# _capacidad"], ["tipo = \"Sala\"", "unidad = \"horas\"", "recargo 10% si > 20 pers."]),
           ("AlquilerEquipo", ["# _tipo_equipo"], ["tipo = \"Equipo\"", "unidad = \"días\"", "seguro 5%"]),
           ("Asesoria", ["# _especialidad", "# _nivel"], ["tipo = \"Asesoría\"", "unidad = \"horas\"", "x1.0 / x1.3 / x1.6"])]
    subs = []
    for i, (n, a, m) in enumerate(sub):
        subs.append(L.uml(240 + i * 410, 1110, 380, n, a, m, None, TURQ, 18))
    est = L.uml(1560, 1110, 400, "EstadoReserva", ["PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA"], ["ACTIVOS"],
                "constantes", GRIS, 18)
    for c in (cli, ser, res):
        L.flecha(arriba(c), (c[0] + c[2] / 2 if c is ser else (ent[0] + 60 if c is cli else ent[0] + ent[2] - 60),
                             ent[1] + ent[3]), NAVY, 3, 26, hueca=True)
    for c in subs:
        L.flecha(arriba(c), (ser[0] + ser[2] / 2, ser[1] + ser[3]), TURQ, 3, 26, hueca=True)
    L.flecha((res[0], res[1] + 120), (ser[0] + ser[2], ser[1] + 120), VERDE, 3, 18, "1   servicio", 19)
    L.d.line([(res[0] + 100, res[1] + res[3]), (res[0] + 100, res[1] + res[3] + 40), (cli[0] + cli[2] / 2, res[1] + res[3] + 40)],
             fill=VERDE, width=3)
    L.flecha((cli[0] + cli[2] / 2, res[1] + res[3] + 40), abajo(cli), VERDE, 3, 18)
    L.t(cli[0] + cli[2] / 2 + 12, res[1] + res[3] + 4, "1   cliente", 19, "sb", VERDE)
    L.flecha((est[0] + 100, est[1]), (res[0] + 300, res[1] + res[3]), GRIS, 3, 16, "usa", 18, discontinua=True)
    L.t(60, 1460, "Símbolos: + público   # protegido (un guion bajo)   - privado (dos guiones bajos, «name mangling»)",
        21, "r", GRIS)
    L.guardar("d_uml_modelos")


def d_uml_gestores():
    L = Lienzo(2000, 1000)
    L.titulo("Diagrama UML · paquete gestores/", "SistemaFJ agrupa a los tres gestores (patrón fachada)")
    sis = L.uml(720, 120, 560, "SistemaFJ", ["+ clientes : GestorClientes", "+ servicios : GestorServicios",
                                             "+ reservas : GestorReservas"], ["+ estadisticas() : dict"], "fachada", NAVY)
    gc = L.uml(40, 470, 560, "GestorClientes", ["- _clientes : list"],
               ["+ registrar(id, nombre, correo, tel)", "+ actualizar(id, nombre, correo, tel)", "+ obtener(id)",
                "+ buscar(texto)", "+ listar()", "+ total()"], None, AZUL)
    gs = L.uml(720, 470, 560, "GestorServicios", ["- _servicios : list", "+ contador_ocupacion : función"],
               ["+ registrar_sala(...)", "+ registrar_equipo(...)", "+ registrar_asesoria(...)", "+ obtener(codigo)",
                "+ listar(tipo=None), total()", "+ consultar_disponibilidad(codigo)", "+ cambiar_habilitacion(codigo, h)",
                "+ calcular_tarifa(codigo, d, imp, desc)"], None, TURQ)
    gr = L.uml(1400, 470, 560, "GestorReservas", ["- _clientes : GestorClientes", "- _servicios : GestorServicios",
                                                  "- _reservas : list"],
               ["+ contar_activas(servicio)", "+ cotizar(...)", "+ crear(id, codigo, d, imp, desc)",
                "+ confirmar(codigo)", "+ cancelar(codigo, motivo)", "+ procesar(codigo)", "+ obtener / listar / total",
                "+ ingresos()"], None, VERDE)
    for c in (gc, gs, gr):
        x = c[0] + c[2] / 2
        L.d.line([(x, sis[1] + sis[3] + 40), (x, c[1])], fill=NAVY, width=3)
        L.d.polygon([(x, c[1]), (x - 10, c[1] - 14), (x, c[1] - 28), (x + 10, c[1] - 14)], fill=NAVY)
    L.d.line([(gc[0] + gc[2] / 2, sis[1] + sis[3] + 40), (gr[0] + gr[2] / 2, sis[1] + sis[3] + 40)], fill=NAVY, width=3)
    L.d.line([abajo(sis), (sis[0] + sis[2] / 2, sis[1] + sis[3] + 40)], fill=NAVY, width=3)
    L.flecha((gr[0], gr[1] + 330), (gs[0] + gs[2], gr[1] + 330), VERDE, 3, 16, "usa", 19)
    L.d.line([(gr[0] + 60, gr[1] + gr[3]), (gr[0] + 60, 960), (gc[0] + gc[2] / 2, 960)], fill=VERDE, width=3)
    L.flecha((gc[0] + gc[2] / 2, 960), abajo(gc), VERDE, 3, 16)
    L.t(gc[0] + gc[2] / 2 + 14, 930, "usa", 19, "sb", VERDE)
    L.t(1000, 990, "Rombo relleno = composición: SistemaFJ crea y contiene a los tres gestores", 20, "i", GRIS, "mm")
    L.guardar("d_uml_gestores")


def d_uml_interfaz():
    L = Lienzo(2000, 1180)
    L.titulo("Diagrama UML · paquete interfaz/", "Clases de Tkinter (gris) y clases propias de Software FJ (azul)")
    tk_ = [("tk.Tk", 120), ("ttk.Frame", 760), ("tk.Toplevel", 1400)]
    tkc = {}
    for n, x in tk_:
        tkc[n] = L.caja(x, 130, 380, 70, GRIS_CL, GRIS, n, TEXTO, 25, "mb", 8)
    vp = L.uml(40, 300, 540, "VentanaPrincipal", ["+ sistema : SistemaFJ", "+ vistas : dict", "+ botones_menu : dict"],
               ["+ mostrar(clave)", "+ notificar_cambio()", "+ estado(texto, tipo)", "- _error_global(...)",
                "+ ejecutar_demostracion()", "+ acerca_de(), salir()"], None, NAVY)
    vb = L.uml(720, 300, 460, "VistaBase", ["+ app, sistema", "+ titulo, subtitulo", "+ MAPA_CAMPOS"],
               ["+ refrescar()", "+ ejecutar(accion, ...)"], None, AZUL)
    vd = L.uml(1360, 300, 420, "VentanaDemostracion", ["+ tabla : Tabla"], ["- _ejecutar()", "- _agregar(fila)"], None, NAVY)
    vistas = ["VistaDashboard", "VistaEventos", "VistaClientes", "VistaServicios", "VistaReservas"]
    vs = []
    for i, n in enumerate(vistas):
        vs.append(L.uml(40 + i * 390, 720, 360, n, [], ["+ refrescar()"], None, AZUL, 18))
    comps = ["Panel(tk.Frame)", "Tarjeta(tk.Frame)", "Tabla(ttk.Frame)", "Formulario(ttk.Frame)", "BotonMenu(tk.Label)"]
    for i, n in enumerate(comps):
        L.caja(40 + i * 390, 1000, 360, 70, "#f5f3ff", MORADO, n, TEXTO, 21, "mb", 8)
    L.t(40, 965, "Componentes reutilizables (componentes.py y ventana_principal.py)", 22, "b", MORADO)
    L.flecha(arriba(vp), abajo(tkc["tk.Tk"]), GRIS, 3, 24, hueca=True)
    L.flecha(arriba(vb), abajo(tkc["ttk.Frame"]), GRIS, 3, 24, hueca=True)
    L.flecha(arriba(vd), (tkc["tk.Toplevel"][0] + 190, 200), GRIS, 3, 24, hueca=True)
    for c in vs:
        L.flecha(arriba(c), (vb[0] + vb[2] / 2, vb[1] + vb[3]), AZUL, 3, 24, hueca=True)
    L.flecha((vp[0] + vp[2], vp[1] + 100), (vb[0], vb[1] + 100), NAVY, 3, 16, "contiene 5", 19)
    L.t(1000, 1130, "Cada vista hereda de VistaBase el método ejecutar(), que llama a los gestores y muestra los errores", 21, "i", GRIS, "mm")
    L.guardar("d_uml_interfaz")


def d_herencia():
    L = Lienzo(1800, 760)
    L.titulo("Herencia: tres servicios, una misma base", "Lo común está en Servicio; cada hija cambia solo lo que la hace distinta")
    padre = L.caja(560, 120, 680, 190, NAVY, NAVY, "**Servicio  (clase abstracta)\ncódigo · nombre · tarifa · cupo · disponible\ncalcular_costo(...) · habilitar() · deshabilitar()", BLANCO, 24)
    hijas = [("ReservaSala", "se cobra por horas (1 a 12)\ncapacidad de personas\n+10 % si capacidad > 20", AZUL, CELESTE),
             ("AlquilerEquipo", "se cobra por días (1 a 30)\ntipo de equipo y unidades\n+5 % de seguro", VERDE, "#f0fdf4"),
             ("Asesoria", "se cobra por horas (0,5 a 8)\nespecialidad y nivel\nBásico ×1 · Interm. ×1,3 · Experto ×1,6", MORADO, "#f5f3ff")]
    for i, (n, t, col, fondo) in enumerate(hijas):
        c = L.caja(60 + i * 580, 450, 520, 250, fondo, col, None, radio=16, grosor=4)
        L.caja(60 + i * 580, 450, 520, 60, col, col, n, BLANCO, 27, "b", 16)
        L.texto_centrado(60 + i * 580, 510, 520, 190, t, TEXTO, 23, "r")
        L.flecha(arriba(c), (padre[0] + 140 + i * 200, padre[1] + padre[3]), GRIS, 4, 30, "hereda de" if i == 1 else None, 20, dy=-10, hueca=True)
    L.guardar("d_herencia")


def d_excepciones():
    L = Lienzo(1800, 900)
    L.titulo("Jerarquía de excepciones personalizadas (excepciones.py)", "Entre paréntesis, el código que aparece en el log")
    raiz = L.caja(650, 120, 500, 80, NAVY, NAVY, "Exception  (de Python)", BLANCO, 25, "mb")
    base = L.caja(650, 260, 500, 80, ROJO, ROJO, "SoftwareFJError  (FJ-000)", BLANCO, 25, "mb")
    L.flecha(arriba(base), abajo(raiz), GRIS, 3, 24, hueca=True)
    hijos = [("ValidacionError\n(FJ-100)", 30), ("EntidadNoEncontrada\nError (FJ-200)", 320), ("EntidadDuplicada\nError (FJ-201)", 610),
             ("ServicioNoDisponible\nError (FJ-300)", 900), ("ReservaError\n(FJ-400)", 1190), ("CalculoInconsistente\nError (FJ-500)", 1480)]
    cajas = {}
    for n, x in hijos:
        cajas[n] = L.caja(x, 450, 280, 100, "#fef2f2", ROJO, n, TEXTO, 21, "m")
        L.flecha(arriba(cajas[n]), (base[0] + base[2] / 2, base[1] + base[3]), GRIS, 2, 20, hueca=True)
    nietos = [("DatoInvalidoError\n(FJ-101)", 30, hijos[0][0]), ("ParametroFaltante\nError (FJ-102)", 330, hijos[0][0]),
              ("OperacionNoPermitida\nError (FJ-401)", 1190, hijos[4][0])]
    for n, x, padre in nietos:
        c = L.caja(x, 680, 280, 100, BLANCO, ROJO, n, TEXTO, 21, "m")
        L.flecha(arriba(c), abajo(cajas[padre]), GRIS, 2, 20, hueca=True)
    L.t(900, 850, "Atrapar SoftwareFJError atrapa también a todas sus hijas: así la interfaz maneja cualquier error del negocio", 21, "i", GRIS, "mm")
    L.guardar("d_excepciones")


def d_try():
    L = Lienzo(1800, 1060)
    L.titulo("Flujo de try / except / else / finally", "Ejemplo real: Reserva.procesar() en modelos/reserva.py")
    t = L.caja(600, 120, 600, 120, AZUL, AZUL, "**try:\nintenta procesar la reserva", BLANCO, 25)
    L.caja(760, 290, 280, 110, BLANCO, NAVY, "¿Ocurrió\nun error?", TEXTO, 25, "b", 55)
    L.flecha(abajo(t), (900, 290), GRIS, 4, 20)
    e = L.caja(120, 470, 600, 170, "#fef2f2", ROJO, "**except:\nregistra el error en el log y\nlanza ReservaError «from» el original", TEXTO, 23)
    el = L.caja(1080, 470, 600, 170, "#f0fdf4", VERDE, "**else:\nsolo si todo salió bien:\nla reserva pasa a «Procesada»", TEXTO, 23)
    L.flecha((760, 345), (420, 470), ROJO, 4, 20, "SÍ", 24, dy=-10)
    L.flecha((1040, 345), (1380, 470), VERDE, 4, 20, "NO", 24, dy=-10)
    f = L.caja(600, 740, 600, 150, "#fffbeb", NARANJA, "**finally:\nSIEMPRE se ejecuta: anota en el log\n«Intento de procesamiento de R-...»", TEXTO, 23)
    L.flecha(abajo(e), (760, 740), GRIS, 4, 20)
    L.flecha(abajo(el), (1040, 740), GRIS, 4, 20)
    L.t(900, 960, "Haya error o no, el bloque finally deja constancia. El programa nunca se cierra por el error.", 22, "i", GRIS, "mm")
    L.guardar("d_try")


def d_estados():
    L = Lienzo(1800, 640)
    L.titulo("Ciclo de vida de una reserva (EstadoReserva)")
    p = L.caja(60, 150, 400, 130, NARANJA, NARANJA, "**Pendiente\nrecién creada", BLANCO, 27)
    c = L.caja(700, 150, 400, 130, AZUL, AZUL, "**Confirmada\naceptada", BLANCO, 27)
    pr = L.caja(1340, 150, 400, 130, VERDE, VERDE, "**Procesada\nfacturada (final)", BLANCO, 27)
    ca = L.caja(700, 440, 400, 130, ROJO, ROJO, "**Cancelada\nsin cobro (final)", BLANCO, 27)
    L.flecha(der(p), izq(c), GRIS, 5, 22, "confirmar()", 23)
    L.flecha(der(c), izq(pr), GRIS, 5, 22, "procesar()", 23)
    L.flecha(abajo(p), (760, 440), ROJO, 5, 22, "cancelar()", 23, dx=-60, dy=10)
    L.flecha(abajo(c), arriba(ca), ROJO, 5, 22, "cancelar()", 23, dx=80, dy=0)
    L.t(60, 120, "Reserva(...) →", 22, "sb", GRIS)
    L.t(1340, 330, "Pendiente y Confirmada = «activas»:", 21, "sb", GRIS)
    L.t(1340, 362, "ocupan cupo del servicio.", 21, "r", GRIS)
    L.t(1340, 400, "Otra acción no permitida lanza", 21, "r", GRIS)
    L.t(1340, 432, "OperacionNoPermitidaError (FJ-401).", 21, "m", ROJO)
    L.guardar("d_estados")


def d_costo():
    L = Lienzo(1800, 560)
    L.titulo("Cálculo del costo en cinco pasos", "Servicio.calcular_costo_detallado() · ejemplo: Sala Ejecutiva, 3 h, desc. 10 %, IVA 19 %")
    pasos = [("1. Subtotal", "tarifa × duración\n× regla del tipo", "$ 150.000", NAVY),
             ("2. Descuento", "subtotal × %desc", "− $ 15.000", NARANJA),
             ("3. Neto", "subtotal − descuento", "$ 135.000", TURQ),
             ("4. Impuesto", "neto × %impuesto", "+ $ 25.650", MORADO),
             ("5. Total", "neto + impuesto", "$ 160.650", AZUL)]
    for i, (t, f, v, col) in enumerate(pasos):
        x = 50 + i * 350
        L.caja(x, 150, 300, 330, col, col, None, radio=18)
        L.texto_centrado(x, 165, 300, 60, "**" + t, BLANCO, 30)
        L.texto_centrado(x, 235, 300, 90, f, "#e2e8f0", 22, "r")
        L.caja(x + 20, 360, 260, 90, BLANCO, BLANCO, v, col, 30, "b", 12)
        if i < 4:
            L.flecha((x + 304, 315), (x + 346, 315), GRIS, 5, 16)
    L.guardar("d_costo")


def d_recorrido():
    pasos = [("Se ejecuta main.py", "main.py"), ("Se abre la ventana principal", "interfaz/ventana_principal.py"),
             ("El usuario elige «Clientes» en el menú", "ventana_principal.py · mostrar()"),
             ("Escribe los datos y pulsa Guardar", "interfaz/vista_clientes.py · guardar()"),
             ("Se validan los datos", "modelos/cliente.py (propiedades)"),
             ("Se crea el objeto Cliente y se guarda", "gestores/gestor_clientes.py · registrar()"),
             ("Se registra un servicio", "vista_servicios.py → gestor_servicios.py → servicios.py"),
             ("Se genera una reserva", "vista_reservas.py → gestor_reservas.py · crear()"),
             ("Se calcula el precio", "modelos/servicios.py · calcular_costo_detallado()"),
             ("Se confirma la reserva", "gestor_reservas.py → modelos/reserva.py · confirmar()"),
             ("Se registra el evento", "registro.py → software_fj.log"),
             ("Se presenta el resultado", "componentes.py · ejecutar() → messagebox + refrescar")]
    L = Lienzo(1800, 160 + len(pasos) * 100)
    L.titulo("Recorrido completo: qué archivo trabaja en cada paso")
    for i, (txt, arch) in enumerate(pasos):
        y = 120 + i * 100
        col = [NAVY, AZUL, AZUL, AZUL, VERDE, TURQ, TURQ, TURQ, VERDE, VERDE, NARANJA, AZUL][i]
        L.caja(60, y, 76, 76, col, col, str(i + 1), BLANCO, 30, "b", 38)
        L.caja(170, y, 700, 76, CELESTE, AZUL, txt, TEXTO, 24, "sb", 12, 2, "izq")
        L.caja(910, y, 830, 76, GRIS_CL, BORDE, arch, TEXTO, 21, "m", 12, 2, "izq")
        if i < len(pasos) - 1:
            L.flecha((98, y + 78), (98, y + 100), GRIS, 3, 10)
    L.guardar("d_recorrido")


def d_evento():
    L = Lienzo(1800, 520)
    L.titulo("Cómo un clic se convierte en una acción", "Ejemplo real: botón «Guardar» de la pantalla Clientes")
    pasos = [("Clic en\n«Guardar»", "el usuario", NARANJA), ("ttk.Button\ncommand=self.guardar", "vista_clientes.py", AZUL),
             ("guardar()\nlee el formulario", "vista_clientes.py", AZUL), ("self.ejecutar(...)\ncaptura errores", "componentes.py", MORADO),
             ("clientes.registrar(...)\ncrea el Cliente", "gestor_clientes.py", TURQ), ("messagebox +\nrefrescar tablas", "resultado", VERDE)]
    for i, (t, a, col) in enumerate(pasos):
        x = 30 + i * 295
        L.caja(x, 160, 265, 190, col, col, "**" + t.split("\n")[0] + "\n" + t.split("\n")[1], BLANCO, 21)
        L.t(x + 132, 380, a, 19, "m", GRIS, "mm")
        if i < 5:
            L.flecha((x + 267, 255), (x + 293, 255), GRIS, 4, 12)
    L.t(900, 460, "command= conecta el botón con el método; bind() conecta teclas y clics (Enter, doble clic)", 22, "i", GRIS, "mm")
    L.guardar("d_evento")


def d_tk_arbol():
    L = Lienzo(1900, 1000)
    L.titulo("Árbol de widgets de la ventana principal", "Cada control vive dentro de otro: el de arriba es su «padre»")
    raiz = L.caja(700, 110, 500, 80, NAVY, NAVY, "VentanaPrincipal (tk.Tk)", BLANCO, 24, "mb")
    lat = L.caja(120, 270, 520, 80, AZUL, AZUL, "lateral (tk.Frame)", BLANCO, 23, "mb")
    der_ = L.caja(1180, 270, 600, 80, AZUL, AZUL, "derecha (ttk.Frame)", BLANCO, 23, "mb")
    for c in (lat, der_):
        L.flecha(abajo(raiz), arriba(c), GRIS, 3, 14)
    hijos_l = ["marca: «FJ» + SOFTWARE FJ (tk.Label)", "MENÚ: 5 × BotonMenu", "HERRAMIENTAS: Demostración,\nAcerca de (BotonMenu)",
               "pie: Salir + «UNAD · Programación»"]
    for i, h in enumerate(hijos_l):
        c = L.caja(60, 420 + i * 125, 640, 100, CELESTE, AZUL, h, TEXTO, 21, "r")
        L.d.line([(90, 350), (90, 470 + i * 125)], fill=GRIS, width=3)
    hijos_d = [("encabezado (tk.Frame): título, subtítulo, reloj", 420), ("barra_estado (tk.Label)", 545),
               ("contenedor (ttk.Frame)", 670)]
    for h, y in hijos_d:
        L.caja(1100, y, 760, 100, CELESTE, AZUL, h, TEXTO, 21, "r")
        L.d.line([(1130, 350), (1130, y + 50)], fill=GRIS, width=3)
    for i, v in enumerate(["Dashboard", "Clientes", "Servicios", "Reservas", "Eventos"]):
        L.caja(1100 + i * 154, 820, 146, 90, "#f5f3ff", MORADO, "Vista\n" + v, TEXTO, 18, "sb", 8)
    L.flecha((1480, 770), (1480, 820), GRIS, 3, 12)
    L.t(1480, 945, "Las 5 vistas se apilan en la misma celda; tkraise() muestra la elegida", 20, "i", GRIS, "mm")
    L.guardar("d_tk_arbol")


def d_imports():
    L = Lienzo(2000, 1200)
    L.titulo("¿Quién importa a quién?", "Una flecha A → B significa: el archivo A usa algo definido en B")
    pos = {"main.py": (820, 120), "simulacion.py": (1450, 120),
           "interfaz/ventana_principal.py": (720, 290), "interfaz/dashboard.py": (60, 470),
           "interfaz/vista_clientes.py": (480, 470), "interfaz/vista_servicios.py": (900, 470),
           "interfaz/vista_reservas.py": (1320, 470), "interfaz/componentes.py": (480, 640),
           "gestores/__init__.py": (1400, 290), "gestores/gestor_*.py": (1400, 640),
           "modelos/reserva.py": (1100, 820), "modelos/cliente.py": (600, 820), "modelos/servicios.py": (1560, 820),
           "modelos/entidad.py": (1100, 1000), "excepciones.py": (200, 1000), "registro.py": (200, 820)}
    W, H = 400, 70
    cajas = {}
    for n, (x, y) in pos.items():
        col = AZUL if n.startswith("interfaz") else TURQ if n.startswith("gestores") else VERDE if n.startswith("modelos") else NAVY
        cajas[n] = L.caja(x, y, W, H, BLANCO, col, n, TEXTO, 19, "mb", 10)
    rel = [("main.py", "interfaz/ventana_principal.py"), ("interfaz/ventana_principal.py", "simulacion.py"),
           ("interfaz/ventana_principal.py", "gestores/__init__.py"), ("interfaz/ventana_principal.py", "interfaz/dashboard.py"),
           ("interfaz/ventana_principal.py", "interfaz/vista_clientes.py"), ("interfaz/ventana_principal.py", "interfaz/vista_servicios.py"),
           ("interfaz/ventana_principal.py", "interfaz/vista_reservas.py"), ("interfaz/vista_clientes.py", "interfaz/componentes.py"),
           ("interfaz/dashboard.py", "interfaz/componentes.py"), ("interfaz/vista_servicios.py", "interfaz/componentes.py"),
           ("interfaz/vista_reservas.py", "interfaz/componentes.py"), ("gestores/__init__.py", "gestores/gestor_*.py"),
           ("gestores/gestor_*.py", "modelos/reserva.py"), ("gestores/gestor_*.py", "modelos/servicios.py"),
           ("gestores/gestor_*.py", "modelos/cliente.py"), ("modelos/reserva.py", "modelos/entidad.py"),
           ("modelos/cliente.py", "modelos/entidad.py"), ("modelos/servicios.py", "modelos/entidad.py"),
           ("modelos/cliente.py", "excepciones.py"), ("interfaz/componentes.py", "registro.py"),
           ("interfaz/componentes.py", "excepciones.py"), ("interfaz/vista_reservas.py", "modelos/servicios.py")]
    for a, b in rel:
        ca, cb = cajas[a], cajas[b]
        p1 = abajo(ca) if cb[1] > ca[1] + 10 else (der(ca) if cb[0] > ca[0] else izq(ca))
        p2 = arriba(cb) if cb[1] > ca[1] + 10 else (izq(cb) if cb[0] > ca[0] else der(cb))
        L.flecha(p1, p2, "#94a3b8", 2, 14)
    L.t(60, 1110, "También importan registro.py: main, gestores, modelos/reserva, dashboard, ventana_principal y simulacion.", 20, "i", GRIS)
    L.t(60, 1145, "También importan excepciones.py: gestores, modelos/servicios, modelos/reserva, vista_reservas y simulacion.", 20, "i", GRIS)
    L.guardar("d_imports")


def d_git_flujo():
    L = Lienzo(1800, 620)
    L.titulo("El viaje de un cambio con Git y GitHub", "Concepto general (cómo se trabaja normalmente en equipo)")
    pasos = [("Tu carpeta", "editas archivos", GRIS), ("git add", "eliges qué guardar", AZUL), ("git commit", "foto con mensaje\n(en tu PC)", AZUL),
             ("git push", "subes la rama\na GitHub", TURQ), ("Pull Request", "pides revisión\npara unir", MORADO), ("merge", "se une a main", VERDE)]
    for i, (t, s, col) in enumerate(pasos):
        x = 30 + i * 295
        L.caja(x, 170, 265, 110, col, col, t, BLANCO, 27, "b")
        L.texto_centrado(x, 290, 265, 90, s, TEXTO, 21, "r")
        if i < 5:
            L.flecha((x + 267, 225), (x + 293, 225), GRIS, 4, 12)
    L.caja(30, 440, 830, 120, GRIS_CL, BORDE, "**En tu computador (repositorio local)\ncarpeta + historial de commits (.git)", TEXTO, 22)
    L.caja(920, 440, 850, 120, CELESTE, AZUL, "**En GitHub (repositorio remoto)\ncopia compartida con todo el equipo", TEXTO, 22)
    L.flecha((860, 500), (920, 500), AZUL, 4, 14)
    L.t(890, 590, "git pull trae a tu PC los cambios que otros subieron", 21, "i", GRIS, "mm")
    L.guardar("d_git_flujo")


def d_git_ramas():
    L = Lienzo(1800, 700)
    L.titulo("Ramas reales del repositorio de Software FJ", "Fuente: git ls-remote / git log --graph --all (5 de noviembre de 2026)")
    y_main = 200
    L.d.line([(120, y_main), (1500, y_main)], fill=NAVY, width=8)
    L.t(60, y_main - 16, "main", 26, "mb", NAVY)
    c1, c2 = (420, y_main), (1100, y_main)
    for (x, y), h, msg in ((c1, "1199503", "first commit"), (c2, "64663c0", "cambios actualizados")):
        L.d.ellipse([x - 26, y - 26, x + 26, y + 26], fill=BLANCO, outline=NAVY, width=7)
        L.t(x, y - 64, h, 22, "mb", NAVY, "mm")
        L.t(x, y - 40, f"«{msg}»", 20, "i", GRIS, "mm")
    L.t(1100, y_main + 50, "HEAD → main · origin/main", 20, "m", AZUL, "mm")
    ramas = [("Jully", AZUL), ("Kathe", MORADO), ("Sebastian", TURQ), ("Vanesa", VERDE)]
    for i, (n, col) in enumerate(ramas):
        y = 330 + i * 80
        L.d.line([(420, y_main + 26), (420, y), (700, y)], fill=col, width=5)
        L.caja(710, y - 28, 240, 56, col, col, f"origin/{n}", BLANCO, 21, "mb", 10)
        L.t(980, y, "apunta a 1199503 (sin commits propios aún)", 20, "r", GRIS, "lm")
    L.t(60, 660, "Las cuatro ramas personales nacen del primer commit; los dos commits existentes los hizo Mario-Quitia en main.", 21, "i", GRIS)
    L.guardar("d_git_ramas")


if __name__ == "__main__":
    for nombre, funcion in list(globals().items()):
        if nombre.startswith("d_") and callable(funcion):
            funcion()
