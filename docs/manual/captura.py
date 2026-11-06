"""
Toma capturas de pantalla REALES de Software FJ para el manual de usuario.

Abre la aplicación, la maneja automáticamente (llena formularios, pulsa
botones, abre diálogos) y guarda las imágenes en docs/manual/capturas.
Los cuadros de diálogo nativos se fotografían y se cierran desde un hilo
auxiliar. El archivo software_fj.log se respalda y se restaura al final.

Uso (solo Windows):  python docs/manual/captura.py
"""
import ctypes
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from ctypes import wintypes

ctypes.windll.shcore.SetProcessDpiAwareness(2)

AQUI = os.path.dirname(os.path.abspath(__file__))
PROYECTO = os.path.abspath(os.path.join(AQUI, "..", ".."))
SALIDA = os.path.join(AQUI, "capturas")
os.makedirs(SALIDA, exist_ok=True)
sys.path.insert(0, PROYECTO)
os.chdir(PROYECTO)

LOG = os.path.join(PROYECTO, "software_fj.log")
RESPALDO = LOG + ".respaldo_manual"
if os.path.exists(LOG):
    shutil.copy2(LOG, RESPALDO)
open(LOG, "w", encoding="utf-8").close()     # log limpio para las capturas

from PIL import ImageGrab                       # noqa: E402
from tkinter import simpledialog                # noqa: E402

from interfaz import VentanaPrincipal           # noqa: E402

user32 = ctypes.windll.user32
dwmapi = ctypes.windll.dwmapi
WM_COMMAND = 0x0111
IDOK, IDYES, IDNO = 1, 6, 7
WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
COORDS = {}


# --------------------------------------------------------------------------- utilidades Win32
def rect(hwnd):
    r = wintypes.RECT()
    if dwmapi.DwmGetWindowAttribute(wintypes.HWND(hwnd), 9, ctypes.byref(r), ctypes.sizeof(r)) != 0:
        user32.GetWindowRect(wintypes.HWND(hwnd), ctypes.byref(r))
    return r.left, r.top, r.right, r.bottom


def clase(hwnd):
    buf = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(wintypes.HWND(hwnd), buf, 256)
    return buf.value


def ventanas_propias():
    res, pid = [], os.getpid()

    def cb(h, _l):
        p = wintypes.DWORD()
        user32.GetWindowThreadProcessId(h, ctypes.byref(p))
        if p.value == pid and user32.IsWindowVisible(h):
            res.append(h)
        return True
    user32.EnumWindows(WNDENUMPROC(cb), 0)
    return res


def grabar(bbox, nombre):
    ImageGrab.grab(bbox=bbox, all_screens=True).save(os.path.join(SALIDA, nombre + ".png"))
    print("captura", nombre)


# --------------------------------------------------------------------------- capturas
app = None


def hwnd_de(ventana):
    return int(ventana.wm_frame(), 16)


def esperar(segundos=0.35):
    fin = time.time() + segundos
    while time.time() < fin:
        app.update()
        time.sleep(0.03)


def cap(nombre, ventana=None, zonas=None):
    """Captura la ventana completa y guarda, opcionalmente, rectángulos de widgets."""
    ventana = ventana or app
    esperar()
    r = rect(hwnd_de(ventana))
    grabar(r, nombre)
    if zonas:
        COORDS[nombre] = {"tam": [r[2] - r[0], r[3] - r[1]],
                          "zonas": {k: zona(w, r) for k, w in zonas.items()}}


def zona(widget, r):
    widget.update_idletasks()
    x, y = widget.winfo_rootx() - r[0], widget.winfo_rooty() - r[1]
    return [x, y, x + widget.winfo_width(), y + widget.winfo_height()]


def dialogos(secuencia):
    """
    Lanza un hilo que espera cada diálogo nativo (MessageBox) de la secuencia,
    lo fotografía (con y sin la ventana principal) y pulsa el botón indicado.
    secuencia: lista de (nombre_captura | None, id_boton)
    """
    antes = set(ventanas_propias())
    principal = rect(hwnd_de(app))

    def trabajo():
        for nombre, boton in secuencia:
            h, limite = None, time.time() + 15
            while time.time() < limite and h is None:
                nuevos = [w for w in ventanas_propias() if w not in antes and clase(w) == "#32770"]
                h = nuevos[0] if nuevos else None
                time.sleep(0.1)
            if h is None:
                print("!! no apareció el diálogo", nombre)
                return
            time.sleep(0.7)
            if nombre:
                d = rect(h)
                grabar(principal, nombre)
                grabar(d, nombre + "_dlg")
            user32.PostMessageW(wintypes.HWND(h), WM_COMMAND, boton, 0)
            while user32.IsWindow(wintypes.HWND(h)):
                time.sleep(0.05)
    hilo = threading.Thread(target=trabajo, daemon=True)
    hilo.start()
    return hilo


def dialogo_tk(nombre, texto):
    """Fotografía el simpledialog (Tk) que se abrirá, escribe `texto` y pulsa OK."""
    def sondear():
        for w in _todos(app):
            if isinstance(w, simpledialog.Dialog) and w.winfo_ismapped():
                w.entry.insert(0, texto)
                w.after(700, lambda d=w: (grabar(rect(hwnd_de(app)), nombre),
                                          grabar(rect(hwnd_de(d)), nombre + "_dlg"), d.ok()))
                return
        app.after(100, sondear)
    app.after(100, sondear)


def _todos(w):
    for hijo in w.winfo_children():
        yield hijo
        yield from _todos(hijo)


def seleccionar(tabla, columna, valor):
    for iid in tabla.arbol.get_children():
        if tabla.arbol.set(iid, columna) == valor:
            tabla.arbol.selection_set(iid)
            tabla.arbol.see(iid)
            esperar(0.2)
            return
    raise RuntimeError(f"No se encontró {valor} en la tabla")


def nueva_app():
    global app
    app = VentanaPrincipal()
    app.geometry("1340x686+6+0")
    app.attributes("-topmost", True)
    app.lift()
    app.focus_force()
    esperar(1.0)
    return app


# --------------------------------------------------------------------------- guion principal
def guion():
    s = app.sistema
    v = app.vistas

    # 1. Panel principal vacío
    app.mostrar("dashboard")
    d = v["dashboard"]
    cap("01_panel_vacio", zonas={
        "lateral": app.botones_menu["dashboard"].master, "encabezado": app.lbl_titulo.master.master,
        "reloj": app.lbl_reloj, "tarjetas": d.zona_tarjetas, "actividad": d.tabla_actividad.master.master,
        "accesos": d.tabla_actividad.master.master.master.grid_slaves(row=0, column=1)[0],
        "estado": app.barra_estado, "menu": app.botones_menu["dashboard"]})

    # 2. Clientes
    app.mostrar("clientes")
    c = v["clientes"]
    cap("02_clientes_vacio", zonas={"formulario": c.form.master.master, "tabla": c.tabla.master.master,
                                    "busqueda": c.busqueda.master, "guardar": c.botones["Guardar"],
                                    "limpiar": c.botones["Limpiar"], "modo": c.lbl_modo})
    c.form.asignar({"identificacion": "1032456789", "nombre": "Laura Gómez",
                    "correo": "laura.gomez@mail.com", "telefono": "3104567890"})
    cap("03_cliente_formulario")
    h = dialogos([("04_cliente_registrado", IDOK)])
    c.guardar()
    h.join()
    s.clientes.registrar("80123456", "Andrés Pérez", "aperez@empresa.co", "6017654321")
    s.clientes.registrar("1019876543", "Camila Rodríguez", "camila.rodriguez@correo.com", "3125558899")
    s.clientes.registrar("79456123", "Juan Martínez", "jmartinez@outlook.com", "3157771234")
    s.clientes.registrar("1144223344", "Sofía Herrera", "sofia.herrera@gmail.com", "3009876543")
    app.notificar_cambio()

    c.form.asignar({"identificacion": "52987654", "nombre": "María Ruiz",
                    "correo": "maria.ruiz@", "telefono": "3001112233"})
    h = dialogos([("05_error_correo", IDOK)])
    c.guardar()
    h.join()
    cap("06_campo_invalido")
    c.form.asignar({"identificacion": "1032456789", "nombre": "Laura Duplicada",
                    "correo": "otra@mail.com", "telefono": "3100000000"})
    h = dialogos([("07_error_duplicado", IDOK)])
    c.guardar()
    h.join()
    c.limpiar()
    cap("08_clientes_tabla")

    seleccionar(c.tabla, "identificacion", "80123456")
    c.form.asignar({"telefono": "3201234567"})
    cap("09_cliente_edicion")
    h = dialogos([("10_cliente_actualizado", IDOK)])
    c.guardar()
    h.join()

    c.busqueda.insert(0, "laura")
    c.buscar()
    cap("11_busqueda")
    c.busqueda.delete(0, "end")
    c.busqueda.insert(0, "pedro")
    h = dialogos([("12_sin_resultados", IDOK)])
    c.buscar()
    h.join()
    c.ver_todos()

    # 3. Servicios
    app.mostrar("servicios")
    sv = v["servicios"]
    cap("13_servicios_vacio", zonas={
        "tipos": sv.contenedor_tipo.master.winfo_children()[0], "registro": sv.form_comun.master.master,
        "consulta": sv.form_calculo.master.master, "catalogo": sv.tabla.master.master,
        "resultado": sv.resultado, "botones_consulta": sv.botones_consulta["Consultar disponibilidad"].master,
        "filtro": sv.filtro})
    sv.form_comun.asignar({"codigo": "SAL-01", "nombre": "Sala Ejecutiva", "tarifa": "50000"})
    sv.form_tipo.asignar({"capacidad": "12", "cupo": "2"})
    cap("14_form_sala")
    h = dialogos([("15_servicio_registrado", IDOK)])
    sv.guardar()
    h.join()

    sv.tipo.set("Equipo")
    sv._cambiar_tipo()
    sv.form_comun.asignar({"codigo": "EQU-01", "nombre": "Videobeam Epson", "tarifa": "35000"})
    sv.form_tipo.asignar({"tipo_equipo": "Proyector", "unidades": "1"})
    cap("16_form_equipo")
    h = dialogos([(None, IDOK)])
    sv.guardar()
    h.join()

    sv.tipo.set("Asesoría")
    sv._cambiar_tipo()
    sv.form_comun.asignar({"codigo": "ASE-01", "nombre": "Asesoría en Ciberseguridad", "tarifa": "120000"})
    sv.form_tipo.asignar({"especialidad": "Seguridad informática", "nivel": "Experto", "cupo": "1"})
    cap("17_form_asesoria")
    h = dialogos([(None, IDOK)])
    sv.guardar()
    h.join()

    s.servicios.registrar_sala("SAL-02", "Auditorio Principal", 80000, 60, 1)
    s.servicios.registrar_equipo("EQU-02", "Portátil Lenovo", 45000, "Computador portátil", 3)
    s.servicios.registrar_asesoria("ASE-02", "Asesoría Contable", 90000, "Contabilidad", "Intermedio", 2)
    app.notificar_cambio()

    sv.tipo.set("Sala")
    sv._cambiar_tipo()
    sv.form_comun.asignar({"codigo": "SAL-03", "nombre": "Sala Mini", "tarifa": "-20000"})
    sv.form_tipo.asignar({"capacidad": "4", "cupo": "1"})
    h = dialogos([("18_error_tarifa", IDOK)])
    sv.guardar()
    h.join()
    cap("19_campo_tarifa_invalido")
    sv.limpiar()
    cap("20_catalogo")

    seleccionar(sv.tabla, "codigo", "SAL-01")
    cap("21_servicio_seleccionado")
    sv.consultar_disponibilidad()
    cap("22_disponibilidad")
    sv.form_calculo.asignar({"duracion": "3", "impuesto": "19", "descuento": "10"})
    sv.calcular_tarifa()
    cap("23_calcular_tarifa")

    seleccionar(sv.tabla, "codigo", "ASE-02")
    h = dialogos([("24_confirmar_deshabilitar", IDYES), ("25_servicio_deshabilitado", IDOK)])
    sv.alternar_habilitacion()
    h.join()
    cap("26_catalogo_deshabilitado")

    # 4. Reservas
    app.mostrar("reservas")
    r = v["reservas"]
    cap("27_reservas_vacio", zonas={
        "formulario": r.form.master.master, "resumen": r._valores_costo["total"].master,
        "crear": r.form.master.winfo_children()[-1], "acciones": r.botones["Confirmar"].master,
        "filtro": r.filtro, "tabla": r.tabla, "leyenda": r.tabla.master.winfo_children()[-1]})
    r.form.asignar({"cliente": "1032456789 - Laura Gómez", "servicio": "SAL-01 - Sala Ejecutiva (Sala)",
                    "duracion": "3", "impuesto": "19", "descuento": "10"})
    esperar(0.8)
    cap("28_reserva_cotizacion")
    h = dialogos([("29_reserva_creada", IDOK)])
    r.crear()
    h.join()

    r.form.asignar({"cliente": "80123456 - Andrés Pérez", "servicio": "EQU-01 - Videobeam Epson (Equipo)",
                    "duracion": "40", "impuesto": "19", "descuento": "0"})
    esperar(0.8)
    cap("30_aviso_duracion")
    h = dialogos([("31_error_duracion", IDOK)])
    r.crear()
    h.join()
    r.form.asignar({"duracion": "2", "descuento": "60"})
    esperar(0.8)
    cap("32_aviso_descuento")
    r.limpiar()

    s.reservas.crear("80123456", "EQU-01", 2, 19)                 # R-0002
    s.reservas.crear("1019876543", "ASE-01", 2, 19, 5)            # R-0003
    s.reservas.crear("79456123", "EQU-02", 3, 19)                 # R-0004
    s.reservas.crear("1144223344", "SAL-02", 4, 19, 15)           # R-0005
    s.reservas.crear("1032456789", "EQU-02", 1, 19)               # R-0006
    s.reservas.confirmar("R-0001")
    app.notificar_cambio()

    seleccionar(r.tabla, "codigo", "R-0002")
    cap("33_reserva_seleccionada")
    h = dialogos([("34_confirmar_pregunta", IDYES), ("35_confirmada", IDOK)])
    r.confirmar()
    h.join()
    seleccionar(r.tabla, "codigo", "R-0002")
    cap("36_confirmada_botones")
    h = dialogos([("37_procesar_pregunta", IDYES), ("38_procesada", IDOK)])
    r.procesar()
    h.join()
    seleccionar(r.tabla, "codigo", "R-0004")
    h = dialogos([("39_cancelar_pregunta", IDYES), ("41_cancelada", IDOK)])
    dialogo_tk("40_motivo", "El cliente reprogramó su evento")
    r.cancelar()
    h.join()
    cap("42_reservas_tabla")
    r.filtro.set("Pendiente")
    r.refrescar()
    cap("43_filtro_pendiente")
    r.filtro.set("Todas")
    r.refrescar()
    h = dialogos([("44_historial", IDOK)])
    r._ver_historial({"codigo": "R-0004"})
    h.join()

    app.mostrar("servicios")
    cap("45_servicios_ocupacion")

    # 5. Panel con datos
    app.mostrar("dashboard")
    cap("46_panel_con_datos")

    # 6. Eventos y logs
    app.mostrar("eventos")
    e = v["eventos"]
    cap("47_eventos", zonas={"filtro": e.filtro, "resumen": e.lbl_resumen, "tabla": e.tabla,
                             "ver_archivo": e.filtro.master.winfo_children()[2],
                             "actualizar": e.filtro.master.winfo_children()[3]})
    e.filtro.set("Errores")
    e.refrescar()
    cap("48_eventos_errores")
    primero = e.tabla.arbol.get_children()[0]
    e.tabla.arbol.selection_set(primero)
    esperar(0.2)
    h = dialogos([("49_detalle_evento", IDOK)])
    # Mismo diálogo que abre el doble clic sobre la fila (ver VistaEventos)
    f = e.tabla.seleccion()
    from tkinter import messagebox
    messagebox.showinfo(f"{f['nivel']} - {f['fecha']}", f["mensaje"], parent=e)
    h.join()
    e.filtro.set("Todos")
    e.refrescar()
    antes = set(app.winfo_children())
    e.ver_archivo()
    ventana_log = [w for w in app.winfo_children() if w not in antes][0] if False else \
        [w for w in _todos(app) if w.winfo_class() == "Toplevel"][-1]
    ventana_log.attributes("-topmost", True)
    esperar(0.8)
    cap("50_archivo_log", ventana=ventana_log)
    ventana_log.destroy()

    # 7. Acerca de y salir
    h = dialogos([("51_acerca_de", IDOK)])
    app.acerca_de()
    h.join()
    h = dialogos([("52_salir", IDNO)])
    app.salir()
    h.join()


def guion_demo():
    """Demostración sobre un sistema vacío (como al abrir el programa)."""
    h = dialogos([("53_demo_pregunta", IDYES)])
    app.ejecutar_demostracion()
    h.join()
    esperar(2.5)
    demo = [w for w in _todos(app) if w.winfo_class() == "Toplevel"][-1]
    demo.attributes("-topmost", True)
    cap("54_demo_resultados", ventana=demo)
    demo.destroy()
    app.mostrar("dashboard")
    cap("55_panel_tras_demo")


def ejecutar(funcion):
    nueva_app()
    try:
        funcion()
    except Exception:
        import traceback
        traceback.print_exc()
    finally:
        app.destroy()


if __name__ == "__main__":
    try:
        ejecutar(guion)
        ejecutar(guion_demo)
        with open(os.path.join(SALIDA, "coords.json"), "w", encoding="utf-8") as f:
            json.dump(COORDS, f, indent=1)
        with open(LOG, encoding="utf-8") as f:
            log_sesion = f.read()
        consola = subprocess.run([sys.executable, "main.py", "--consola"], capture_output=True,
                                 text=True, encoding="utf-8", cwd=PROYECTO)
        with open(os.path.join(SALIDA, "consola.txt"), "w", encoding="utf-8") as f:
            f.write(consola.stdout)
        with open(os.path.join(SALIDA, "log_ejemplo.txt"), "w", encoding="utf-8") as f:
            f.write(log_sesion)
    finally:
        if os.path.exists(RESPALDO):
            shutil.move(RESPALDO, LOG)
