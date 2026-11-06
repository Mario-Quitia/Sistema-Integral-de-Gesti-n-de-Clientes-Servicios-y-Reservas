"""
Ventana principal de Software FJ (Integrante 5).

Contiene el encabezado, el menú lateral de navegación, el panel de contenido,
la barra de estado, el manejo global de errores y la ventana de demostración.
"""
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from gestores import SistemaFJ
from interfaz.componentes import FUENTE, FUENTES, PALETA, Tabla, configurar_estilos
from interfaz.dashboard import VistaDashboard, VistaEventos
from interfaz.vista_clientes import VistaClientes
from interfaz.vista_reservas import VistaReservas
from interfaz.vista_servicios import VistaServicios
from registro import registrar_critico, registrar_evento
from simulacion import ejecutar_simulacion


class BotonMenu(tk.Label):
    """Botón plano del menú lateral con efecto hover y estado activo."""

    def __init__(self, padre, texto, icono, comando):
        super().__init__(padre, text=f"  {icono}   {texto}", anchor="w", cursor="hand2",
                         bg=PALETA["lateral"], fg=PALETA["lateral_texto"], font=(FUENTE, 11),
                         padx=18, pady=11)
        self._activo = False
        self.bind("<Button-1>", lambda _e: comando())
        self.bind("<Enter>", lambda _e: self._pintar(hover=True))
        self.bind("<Leave>", lambda _e: self._pintar())

    def activar(self, activo):
        self._activo = activo
        self._pintar()

    def _pintar(self, hover=False):
        if self._activo:
            self.config(bg=PALETA["lateral_activo"], fg="#ffffff", font=(FUENTE, 11, "bold"))
        else:
            self.config(bg=PALETA["lateral_hover"] if hover else PALETA["lateral"],
                        fg="#ffffff" if hover else PALETA["lateral_texto"], font=(FUENTE, 11))


class VentanaPrincipal(tk.Tk):
    SECCIONES = [
        ("dashboard", "Panel principal", "🏠", VistaDashboard),
        ("clientes", "Clientes", "👥", VistaClientes),
        ("servicios", "Servicios", "🛠", VistaServicios),
        ("reservas", "Reservas", "📅", VistaReservas),
        ("eventos", "Eventos y logs", "📄", VistaEventos),
    ]

    def __init__(self, sistema=None):
        super().__init__()
        self.sistema = sistema or SistemaFJ()
        self.title("SOFTWARE FJ - Gestión de Clientes, Servicios y Reservas")
        self.geometry(self._geometria_inicial())
        self.minsize(1000, 640)
        self.configure(bg=PALETA["fondo"])
        configurar_estilos(self)
        # Manejo global: cualquier excepción no capturada en un evento de Tk
        # se registra y se muestra, pero la aplicación sigue abierta.
        self.report_callback_exception = self._error_global
        self.protocol("WM_DELETE_WINDOW", self.salir)

        self.vistas = {}
        self.botones_menu = {}
        self.seccion_actual = None
        self._construir_lateral()
        self._construir_contenido()
        self.mostrar("dashboard")
        self._reloj()
        registrar_evento("Interfaz gráfica iniciada")

    def _geometria_inicial(self):
        ancho = min(1366, int(self.winfo_screenwidth() * 0.9))
        alto = min(820, int(self.winfo_screenheight() * 0.85))
        x = (self.winfo_screenwidth() - ancho) // 2
        y = max((self.winfo_screenheight() - alto) // 2 - 20, 0)
        return f"{ancho}x{alto}+{x}+{y}"

    # ---------- estructura ----------
    def _construir_lateral(self):
        lateral = tk.Frame(self, bg=PALETA["lateral"], width=240)
        lateral.pack(side="left", fill="y")
        lateral.pack_propagate(False)

        marca = tk.Frame(lateral, bg=PALETA["lateral"])
        marca.pack(fill="x", padx=18, pady=(22, 24))
        tk.Label(marca, text="FJ", bg=PALETA["primario"], fg="#ffffff", font=(FUENTE, 14, "bold"),
                 width=3, pady=4).pack(side="left")
        textos = tk.Frame(marca, bg=PALETA["lateral"])
        textos.pack(side="left", padx=10)
        tk.Label(textos, text="SOFTWARE FJ", bg=PALETA["lateral"], fg="#ffffff",
                 font=FUENTES["marca"]).pack(anchor="w")
        tk.Label(textos, text="Sistema integral", bg=PALETA["lateral"], fg="#94a3b8",
                 font=FUENTES["pequena"]).pack(anchor="w")

        tk.Label(lateral, text="MENÚ", bg=PALETA["lateral"], fg="#64748b",
                 font=(FUENTE, 8, "bold"), anchor="w", padx=22).pack(fill="x", pady=(0, 6))
        for clave, texto, icono, _ in self.SECCIONES:
            boton = BotonMenu(lateral, texto, icono, lambda c=clave: self.mostrar(c))
            boton.pack(fill="x", padx=10, pady=1)
            self.botones_menu[clave] = boton

        tk.Label(lateral, text="HERRAMIENTAS", bg=PALETA["lateral"], fg="#64748b",
                 font=(FUENTE, 8, "bold"), anchor="w", padx=22).pack(fill="x", pady=(22, 6))
        BotonMenu(lateral, "Demostración", "▶", self.ejecutar_demostracion).pack(fill="x", padx=10)
        BotonMenu(lateral, "Acerca de", "ℹ", self.acerca_de).pack(fill="x", padx=10, pady=1)

        pie = tk.Frame(lateral, bg=PALETA["lateral"])
        pie.pack(side="bottom", fill="x", pady=16)
        BotonMenu(pie, "Salir", "⏻", self.salir).pack(fill="x", padx=10)
        tk.Label(pie, text="UNAD · Programación 213023", bg=PALETA["lateral"], fg="#475569",
                 font=(FUENTE, 8)).pack(pady=(10, 0))

    def _construir_contenido(self):
        derecha = ttk.Frame(self)
        derecha.pack(side="left", fill="both", expand=True)

        encabezado = tk.Frame(derecha, bg=PALETA["superficie"], highlightthickness=1,
                              highlightbackground=PALETA["borde"])
        encabezado.pack(fill="x")
        textos = tk.Frame(encabezado, bg=PALETA["superficie"])
        textos.pack(side="left", padx=28, pady=14)
        self.lbl_titulo = tk.Label(textos, bg=PALETA["superficie"], fg=PALETA["texto"],
                                   font=FUENTES["titulo"])
        self.lbl_titulo.pack(anchor="w")
        self.lbl_subtitulo = tk.Label(textos, bg=PALETA["superficie"], fg=PALETA["texto_suave"],
                                      font=FUENTES["subtitulo"])
        self.lbl_subtitulo.pack(anchor="w")
        self.lbl_reloj = tk.Label(encabezado, bg=PALETA["superficie"], fg=PALETA["texto_suave"],
                                  font=FUENTES["normal"], justify="right")
        self.lbl_reloj.pack(side="right", padx=28)

        self.barra_estado = tk.Label(derecha, anchor="w", padx=16, pady=5, font=FUENTES["pequena"],
                                     bg="#e2e8f0", fg=PALETA["texto_suave"], text="Listo")
        self.barra_estado.pack(side="bottom", fill="x")

        contenedor = ttk.Frame(derecha)
        contenedor.pack(fill="both", expand=True, padx=28, pady=20)
        contenedor.rowconfigure(0, weight=1)
        contenedor.columnconfigure(0, weight=1)
        for clave, _texto, _icono, clase in self.SECCIONES:
            vista = clase(contenedor, self)
            vista.grid(row=0, column=0, sticky="nsew")
            self.vistas[clave] = vista

    # ---------- navegación y comunicación entre vistas ----------
    def mostrar(self, clave):
        vista = self.vistas[clave]
        for c, boton in self.botones_menu.items():
            boton.activar(c == clave)
        self.lbl_titulo.config(text=vista.titulo)
        self.lbl_subtitulo.config(text=vista.subtitulo)
        vista.refrescar()
        vista.tkraise()
        self.seccion_actual = clave

    def notificar_cambio(self):
        """Mantiene todas las tablas actualizadas después de cada operación."""
        for vista in self.vistas.values():
            try:
                vista.refrescar()
            except Exception as error:   # pylint: disable=broad-except
                registrar_critico(f"Error al refrescar {type(vista).__name__}", error)

    def estado(self, texto, tipo="info"):
        colores = {"info": PALETA["texto_suave"], "exito": PALETA["exito"],
                   "advertencia": PALETA["advertencia"], "peligro": PALETA["peligro"]}
        primera_linea = str(texto).splitlines()[0] if texto else ""
        self.barra_estado.config(text=f"{datetime.now():%H:%M:%S}  ·  {primera_linea}",
                                 fg=colores.get(tipo, PALETA["texto_suave"]))

    def _reloj(self):
        self.lbl_reloj.config(text=datetime.now().strftime("%A %d/%m/%Y\n%H:%M:%S"))
        self.after(1000, self._reloj)

    # ---------- manejo global de errores ----------
    def _error_global(self, tipo, valor, traza):
        registrar_critico("Excepción no controlada en la interfaz", valor)
        messagebox.showerror("Error inesperado",
                             "Se produjo un error inesperado. Quedó registrado en software_fj.log "
                             f"y la aplicación seguirá funcionando.\n\n{tipo.__name__}: {valor}",
                             parent=self)
        self.estado("Error inesperado registrado en el log", "peligro")

    # ---------- herramientas ----------
    def ejecutar_demostracion(self):
        if not messagebox.askyesno(
                "Demostración",
                "Se ejecutarán 15 operaciones de prueba (registros válidos e inválidos de "
                "clientes, servicios y reservas).\n\nLos datos válidos se agregarán al sistema "
                "actual. ¿Desea continuar?", parent=self):
            return
        VentanaDemostracion(self)

    def acerca_de(self):
        messagebox.showinfo(
            "Acerca de Software FJ",
            "SOFTWARE FJ\nSistema Integral de Gestión de Clientes, Servicios y Reservas\n\n"
            "UNAD · Curso Programación (213023) · Fase 4\n\n"
            "Programación orientada a objetos, manejo avanzado de excepciones,\n"
            "registro de eventos en software_fj.log e interfaz gráfica Tkinter.", parent=self)

    def salir(self):
        if messagebox.askyesno("Salir", "¿Desea cerrar Software FJ?\n"
                               "Los datos están en memoria y se perderán al salir.", parent=self):
            registrar_evento("Aplicación cerrada por el usuario")
            self.destroy()


class VentanaDemostracion(tk.Toplevel):
    """Ventana emergente que ejecuta y muestra las 15 operaciones de la simulación."""

    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.title("Demostración - 15 operaciones")
        self.geometry("1000x560")
        self.configure(bg=PALETA["fondo"])
        self.transient(app)

        ttk.Label(self, text="Simulación de operaciones", style="Titulo.TLabel").pack(
            anchor="w", padx=20, pady=(16, 0))
        self.lbl_resumen = ttk.Label(self, text="Ejecutando...", style="Subtitulo.TLabel")
        self.lbl_resumen.pack(anchor="w", padx=20, pady=(0, 10))

        marco = ttk.Frame(self, style="Superficie.TFrame")
        marco.pack(fill="both", expand=True, padx=20)
        self.tabla = Tabla(marco, [
            ("numero", "#", 40, "center"),
            ("descripcion", "Operación", 330, "w"),
            ("resultado", "Resultado", 110, "center"),
            ("esperado_txt", "¿Esperado?", 90, "center"),
            ("detalle", "Detalle / mensaje de error", 480, "w"),
        ], al_doble_clic=lambda f: messagebox.showinfo(f"Operación {f['numero']}", f["detalle"],
                                                     parent=self))
        self.tabla.pack(fill="both", expand=True)
        ttk.Button(self, text="Cerrar", command=self.destroy).pack(anchor="e", padx=20, pady=12)

        self._filas = []
        self.after(100, self._ejecutar)

    def _agregar(self, fila):
        fila["resultado"] = "✔ Exitosa" if fila["ok"] else "✖ Error controlado"
        fila["esperado_txt"] = "Sí" if fila["ok"] == fila["esperado"] else "No"
        self._filas.append(fila)
        self.tabla.cargar(self._filas, etiqueta=lambda f: "ok" if f["ok"] else "fallo")
        self.update_idletasks()

    def _ejecutar(self):
        try:
            resultados = ejecutar_simulacion(self.app.sistema, self._agregar)
        except Exception as error:   # pylint: disable=broad-except
            registrar_critico("Fallo general en la demostración", error)
            messagebox.showerror("Demostración", f"La demostración se interrumpió: {error}", parent=self)
            return
        finally:
            self.app.notificar_cambio()
        exitos = sum(r["ok"] for r in resultados)
        esperados = sum(r["ok"] == r["esperado"] for r in resultados)
        self.lbl_resumen.config(
            text=f"{len(resultados)} operaciones · {exitos} exitosas · "
                 f"{len(resultados) - exitos} errores controlados · "
                 f"{esperados}/{len(resultados)} con el resultado esperado. La aplicación sigue activa.")
        self.app.estado("Demostración finalizada", "exito")
