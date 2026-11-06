"""Vista de gestión de clientes (Integrante 1)."""
from tkinter import messagebox, ttk

from interfaz.componentes import Formulario, Panel, Tabla, VistaBase, fila_botones


class VistaClientes(VistaBase):
    titulo = "Gestión de clientes"
    subtitulo = "Registre, consulte y actualice los clientes de Software FJ"

    MAPA_CAMPOS = {"identificación": "identificacion", "nombre": "nombre",
                   "correo": "correo", "teléfono": "telefono"}

    def __init__(self, padre, app):
        super().__init__(padre, app)
        self._modo_edicion = False
        self.columnconfigure(0, weight=0, minsize=330)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self._construir_formulario()
        self._construir_tabla()

    # ---------- construcción ----------
    def _construir_formulario(self):
        panel = Panel(self, "Datos del cliente", "Todos los campos son obligatorios")
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        self.form = Formulario(panel.cuerpo, [
            ("identificacion", "Identificación (5-12 dígitos)", "entrada", {}),
            ("nombre", "Nombre completo", "entrada", {}),
            ("correo", "Correo electrónico", "entrada", {}),
            ("telefono", "Teléfono (7-10 dígitos)", "entrada", {}),
        ])
        self.form.pack(fill="x")

        self.lbl_modo = ttk.Label(panel.cuerpo, text="Modo: nuevo registro", style="Suave.TLabel")
        self.lbl_modo.pack(anchor="w", pady=(10, 6))

        botones, self.botones = fila_botones(panel.cuerpo, [
            ("Guardar", "Primario", self.guardar),
            ("Limpiar", None, self.limpiar),
        ])
        botones.pack(fill="x", pady=(4, 0))
        self.form.controles["telefono"].bind("<Return>", lambda _e: self.guardar())

    def _construir_tabla(self):
        panel = Panel(self, "Clientes registrados")
        panel.grid(row=0, column=1, sticky="nsew")

        barra = ttk.Frame(panel.cuerpo, style="Superficie.TFrame")
        barra.pack(fill="x", pady=(0, 10))
        self.busqueda = ttk.Entry(barra)
        self.busqueda.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.busqueda.bind("<Return>", lambda _e: self.buscar())
        ttk.Button(barra, text="Buscar", style="Info.TButton", command=self.buscar,
                   cursor="hand2").pack(side="left", padx=(0, 8))
        ttk.Button(barra, text="Ver todos", command=self.ver_todos, cursor="hand2").pack(side="left")

        self.tabla = Tabla(panel.cuerpo, [
            ("identificacion", "Identificación", 120, "w"),
            ("nombre", "Nombre", 200, "w"),
            ("correo", "Correo", 220, "w"),
            ("telefono", "Teléfono", 110, "center"),
            ("reservas", "Reservas", 80, "center"),
        ], al_seleccionar=self._al_seleccionar)
        self.tabla.pack(fill="both", expand=True)
        self.lbl_total = ttk.Label(panel.cuerpo, style="Suave.TLabel")
        self.lbl_total.pack(anchor="w", pady=(8, 0))

    # ---------- acciones (solo delegan en el gestor) ----------
    def guardar(self):
        datos = self.form.valores()
        if self._modo_edicion:
            cliente = self.ejecutar(self.sistema.clientes.actualizar, **datos, formulario=self.form,
                                    exito=lambda c: f"Cliente {c.nombre} actualizado correctamente.")
        else:
            cliente = self.ejecutar(self.sistema.clientes.registrar, **datos, formulario=self.form,
                                    exito=lambda c: f"Cliente {c.nombre} registrado correctamente.")
        if cliente:
            self.limpiar()

    def limpiar(self):
        self.form.limpiar()
        self._modo_edicion = False
        self.form.controles["identificacion"].configure(state="normal")
        self.lbl_modo.config(text="Modo: nuevo registro")
        self.botones["Guardar"].config(text="Guardar")
        self.tabla.arbol.selection_remove(self.tabla.arbol.selection())
        self.form.controles["identificacion"].focus_set()

    def buscar(self):
        texto = self.busqueda.get().strip()
        if not texto:
            messagebox.showinfo("Buscar", "Escriba una identificación, nombre o correo para buscar.",
                                parent=self)
            return
        resultados = self.ejecutar(self.sistema.clientes.buscar, texto, notificar=False)
        if resultados is not None:
            self._cargar(resultados)
            if not resultados:
                messagebox.showwarning("Sin resultados", f"No se encontraron clientes con '{texto}'.",
                                       parent=self)
            self.app.estado(f"Búsqueda '{texto}': {len(resultados)} resultado(s)")

    def ver_todos(self):
        self.busqueda.delete(0, "end")
        self.refrescar()

    def _al_seleccionar(self, fila):
        if not fila:
            return
        self.form.limpiar()
        self.form.asignar(fila)
        self._modo_edicion = True
        self.form.controles["identificacion"].configure(state="disabled")
        self.lbl_modo.config(text=f"Modo: edición de {fila['identificacion']}")
        self.botones["Guardar"].config(text="Actualizar")

    # ---------- refresco ----------
    def _cargar(self, clientes):
        reservas = self.sistema.reservas.listar()
        filas = []
        for c in clientes:
            fila = c.a_diccionario()
            fila["reservas"] = sum(1 for r in reservas if r.cliente is c)
            filas.append(fila)
        self.tabla.cargar(filas)
        self.lbl_total.config(text=f"{len(filas)} de {self.sistema.clientes.total()} cliente(s)")

    def refrescar(self):
        texto = self.busqueda.get().strip()
        self._cargar(self.sistema.clientes.buscar(texto))
