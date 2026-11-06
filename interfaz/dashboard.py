"""
Panel principal (dashboard) y vista de registro de eventos y errores
(Integrante 5).
"""
import os
import tkinter as tk
from tkinter import messagebox, ttk

from interfaz.componentes import FUENTES, PALETA, Panel, Tabla, Tarjeta, VistaBase, formato_moneda
from registro import RUTA_LOG, eventos_recientes, leer_archivo_log


class VistaDashboard(VistaBase):
    titulo = "Panel principal"
    subtitulo = "Resumen general de la operación de Software FJ"

    TARJETAS = [
        ("clientes", "Clientes registrados", PALETA["primario"], "👥"),
        ("servicios", "Servicios disponibles", PALETA["morado"], "🛠"),
        ("reservas", "Total de reservas", PALETA["info"], "📅"),
        ("pendientes", "Reservas pendientes", PALETA["advertencia"], "⏳"),
        ("confirmadas", "Reservas confirmadas", PALETA["exito"], "✔"),
        ("canceladas", "Reservas canceladas", PALETA["peligro"], "✖"),
        ("procesadas", "Reservas procesadas", "#0d9488", "🧾"),
        ("ingresos", "Ingresos (conf. + proc.)", "#ca8a04", "$"),
    ]

    def __init__(self, padre, app):
        super().__init__(padre, app)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.zona_tarjetas = ttk.Frame(self)
        self.zona_tarjetas.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        self.tarjetas = {clave: Tarjeta(self.zona_tarjetas, titulo, color, icono)
                         for clave, titulo, color, icono in self.TARJETAS}
        self._columnas_actuales = 0
        self.zona_tarjetas.bind("<Configure>", self._reorganizar)

        inferior = ttk.Frame(self)
        inferior.grid(row=1, column=0, sticky="nsew")
        inferior.columnconfigure(0, weight=3)
        inferior.columnconfigure(1, weight=2)
        inferior.rowconfigure(0, weight=1)

        actividad = Panel(inferior, "Actividad reciente", "Últimos eventos registrados en esta sesión")
        actividad.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.tabla_actividad = Tabla(actividad.cuerpo, [
            ("fecha", "Fecha y hora", 140, "center"),
            ("nivel", "Tipo", 80, "center"),
            ("mensaje", "Descripción", 460, "w"),
        ], alto=8)
        self.tabla_actividad.pack(fill="both", expand=True)

        accesos = Panel(inferior, "Accesos rápidos")
        accesos.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        for texto, estilo, destino in (("➕  Registrar cliente", "Primario", "clientes"),
                                       ("🛠  Registrar servicio", "Info", "servicios"),
                                       ("📅  Nueva reserva", "Exito", "reservas"),
                                       ("📄  Ver eventos y logs", None, "eventos")):
            ttk.Button(accesos.cuerpo, text=texto, cursor="hand2",
                       style=f"{estilo}.TButton" if estilo else "TButton",
                       command=lambda d=destino: self.app.mostrar(d)).pack(fill="x", pady=4)
        ttk.Separator(accesos.cuerpo).pack(fill="x", pady=10)
        ttk.Label(accesos.cuerpo, text="Demostración", style="Seccion.TLabel").pack(anchor="w")
        ttk.Label(accesos.cuerpo, style="Suave.TLabel", wraplength=280, justify="left",
                  text="Ejecuta las 15 operaciones de prueba (válidas e inválidas) sin "
                       "interrumpir el uso normal de la aplicación.").pack(anchor="w", pady=(2, 8))
        ttk.Button(accesos.cuerpo, text="▶  Ejecutar simulación de 15 operaciones", cursor="hand2",
                   style="Advertencia.TButton", command=self.app.ejecutar_demostracion).pack(fill="x")

    def _reorganizar(self, evento):
        """Diseño adaptable: 4, 2 o 1 columnas de tarjetas según el ancho disponible."""
        columnas = 4 if evento.width >= 900 else 2 if evento.width >= 480 else 1
        if columnas == self._columnas_actuales:
            return
        self._columnas_actuales = columnas
        for i in range(4):
            self.zona_tarjetas.columnconfigure(i, weight=1 if i < columnas else 0, uniform="t")
        for i, tarjeta in enumerate(self.tarjetas.values()):
            fila, col = divmod(i, columnas)
            tarjeta.grid(row=fila, column=col, sticky="nsew",
                         padx=(0 if col == 0 else 6, 0 if col == columnas - 1 else 6), pady=6)

    def refrescar(self):
        est = self.sistema.estadisticas()
        self.tarjetas["clientes"].actualizar(est["clientes"], "Clientes activos en memoria")
        self.tarjetas["servicios"].actualizar(est["servicios_disponibles"],
                                              f"de {est['servicios']} servicios registrados")
        self.tarjetas["reservas"].actualizar(est["reservas"], "Reservas creadas")
        self.tarjetas["pendientes"].actualizar(est["pendientes"], "Esperando confirmación")
        self.tarjetas["confirmadas"].actualizar(est["confirmadas"], "Listas para procesar")
        self.tarjetas["canceladas"].actualizar(est["canceladas"], "No generan cobro")
        self.tarjetas["procesadas"].actualizar(est["procesadas"], "Facturadas")
        self.tarjetas["ingresos"].actualizar(formato_moneda(est["ingresos"]), "Incluye impuestos")
        self.tabla_actividad.cargar(eventos_recientes()[:30], etiqueta=lambda f: f["nivel"])


class VistaEventos(VistaBase):
    titulo = "Registro de eventos y errores"
    subtitulo = f"Archivo de log: {RUTA_LOG}"

    FILTROS = {
        "Todos": None,
        "Solo eventos (INFO)": ("INFO",),
        "Advertencias": ("WARNING",),
        "Errores": ("ERROR", "CRITICAL"),
    }

    def __init__(self, padre, app):
        super().__init__(padre, app)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        panel = Panel(self, "Eventos de la sesión actual")
        panel.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Frame(panel.cuerpo, style="Superficie.TFrame")
        barra.pack(fill="x", pady=(0, 10))
        ttk.Label(barra, text="Filtrar:", style="Superficie.TLabel").pack(side="left", padx=(0, 6))
        self.filtro = ttk.Combobox(barra, values=list(self.FILTROS), state="readonly", width=20)
        self.filtro.set("Todos")
        self.filtro.pack(side="left")
        self.filtro.bind("<<ComboboxSelected>>", lambda _e: self.refrescar())
        ttk.Button(barra, text="Ver archivo software_fj.log", style="Primario.TButton",
                   cursor="hand2", command=self.ver_archivo).pack(side="right")
        ttk.Button(barra, text="Actualizar", cursor="hand2",
                   command=self.refrescar).pack(side="right", padx=8)
        self.lbl_resumen = ttk.Label(barra, style="Suave.TLabel")
        self.lbl_resumen.pack(side="left", padx=12)

        self.tabla = Tabla(panel.cuerpo, [
            ("fecha", "Fecha y hora", 150, "center"),
            ("nivel", "Nivel", 90, "center"),
            ("mensaje", "Mensaje", 700, "w"),
        ], al_doble_clic=lambda f: messagebox.showinfo(f"{f['nivel']} - {f['fecha']}", f["mensaje"],
                                                     parent=self))
        self.tabla.pack(fill="both", expand=True)

    def refrescar(self):
        todos = eventos_recientes()
        filas = eventos_recientes(self.FILTROS[self.filtro.get()])
        errores = sum(1 for e in todos if e["nivel"] in ("ERROR", "CRITICAL"))
        self.tabla.cargar(filas, etiqueta=lambda f: f["nivel"])
        self.lbl_resumen.config(text=f"{len(todos)} eventos · {errores} errores en esta sesión")

    def ver_archivo(self):
        """Muestra el contenido completo de software_fj.log en una ventana emergente."""
        ventana = tk.Toplevel(self)
        ventana.title("software_fj.log")
        ventana.geometry("980x560")
        ventana.transient(self.winfo_toplevel())
        ventana.configure(bg=PALETA["fondo"])

        barra = ttk.Frame(ventana)
        barra.pack(fill="x", padx=12, pady=(12, 6))
        ttk.Label(barra, text=RUTA_LOG, style="Subtitulo.TLabel").pack(side="left")
        texto = tk.Text(ventana, wrap="none", font=("Consolas", 10), bg="#0f172a", fg="#e2e8f0",
                        insertbackground="#e2e8f0", padx=10, pady=10, relief="flat")
        barra_v = ttk.Scrollbar(ventana, orient="vertical", command=texto.yview)
        texto.configure(yscrollcommand=barra_v.set)
        barra_v.pack(side="right", fill="y", pady=(0, 12), padx=(0, 12))
        texto.pack(fill="both", expand=True, padx=(12, 0), pady=(0, 12))
        texto.tag_configure("ERROR", foreground="#f87171")
        texto.tag_configure("CRITICAL", foreground="#ffffff", background="#b91c1c")
        texto.tag_configure("WARNING", foreground="#fbbf24")

        def cargar():
            texto.configure(state="normal")
            texto.delete("1.0", "end")
            for linea in leer_archivo_log().splitlines():
                nivel = next((n for n in ("CRITICAL", "ERROR", "WARNING") if f"| {n}" in linea), None)
                texto.insert("end", linea + "\n", nivel or ())
            texto.configure(state="disabled")
            texto.see("end")

        ttk.Button(barra, text="Recargar", command=cargar).pack(side="right")
        if os.name == "nt":
            ttk.Button(barra, text="Abrir carpeta", command=lambda: os.startfile(os.path.dirname(RUTA_LOG))
                       ).pack(side="right", padx=8)
        cargar()
