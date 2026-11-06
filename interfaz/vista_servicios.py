"""Vista de gestión de servicios: salas, equipos y asesorías (Integrante 2)."""
import tkinter as tk
from tkinter import messagebox, ttk

from interfaz.componentes import (FUENTES, PALETA, Formulario, Panel, Tabla, VistaBase,
                                  fila_botones, formato_moneda)
from modelos.servicios import IMPUESTO_POR_DEFECTO, Asesoria

# Campos específicos de cada tipo de servicio
CAMPOS_TIPO = {
    "Sala": [
        ("capacidad", "Capacidad (personas)", "entrada", {}),
        ("cupo", "Reservas simultáneas", "entrada", {"valor": "2"}),
    ],
    "Equipo": [
        ("tipo_equipo", "Tipo de equipo", "entrada", {}),
        ("unidades", "Unidades disponibles", "entrada", {"valor": "1"}),
    ],
    "Asesoría": [
        ("especialidad", "Especialidad", "entrada", {}),
        ("nivel", "Nivel", "combo", {"valores": list(Asesoria.NIVELES), "valor": "Básico"}),
        ("cupo", "Reservas simultáneas", "entrada", {"valor": "1"}),
    ],
}
ETIQUETA_TARIFA = {"Sala": "Tarifa por hora", "Equipo": "Tarifa por día", "Asesoría": "Tarifa por hora"}


class VistaServicios(VistaBase):
    titulo = "Gestión de servicios"
    subtitulo = "Registre salas, equipos y asesorías; consulte disponibilidad y tarifas"

    MAPA_CAMPOS = {"código": "codigo", "nombre": "nombre", "tarifa": "tarifa",
                   "capacidad": "capacidad", "cupo": "cupo", "tipo de equipo": "tipo_equipo",
                   "especialidad": "especialidad", "duración": "duracion"}

    def __init__(self, padre, app):
        super().__init__(padre, app)
        self.tipo = tk.StringVar(value="Sala")
        self.columnconfigure(0, weight=1, uniform="col")
        self.columnconfigure(1, weight=1, uniform="col")
        self.rowconfigure(1, weight=1)
        self._construir_registro()
        self._construir_consulta()
        self._construir_tabla()

    # ---------- construcción ----------
    def _construir_registro(self):
        panel = Panel(self, "Registrar servicio", "Seleccione el tipo y complete los datos")
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 16))

        tipos = ttk.Frame(panel.cuerpo, style="Superficie.TFrame")
        tipos.pack(fill="x", pady=(0, 6))
        for texto in CAMPOS_TIPO:
            ttk.Radiobutton(tipos, text=texto, value=texto, variable=self.tipo,
                            command=self._cambiar_tipo).pack(side="left", padx=(0, 16))

        self.form_comun = Formulario(panel.cuerpo, [
            ("codigo", "Código", "entrada", {}),
            ("nombre", "Nombre", "entrada", {}),
            ("tarifa", "Tarifa por hora", "entrada", {}),
        ], columnas=3)
        self.form_comun.pack(fill="x")
        self._lbl_tarifa = self.form_comun.controles["tarifa"].master.winfo_children()[0]

        self.contenedor_tipo = ttk.Frame(panel.cuerpo, style="Superficie.TFrame")
        self.contenedor_tipo.pack(fill="x")
        self.form_tipo = None
        self._cambiar_tipo()

        botones, _ = fila_botones(panel.cuerpo, [
            ("Guardar", "Primario", self.guardar),
            ("Limpiar", None, self.limpiar),
        ])
        botones.pack(fill="x", pady=(12, 0))

    def _construir_consulta(self):
        panel = Panel(self, "Disponibilidad y tarifas", "Seleccione un servicio en la tabla")
        panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=(0, 16))

        self.lbl_servicio = ttk.Label(panel.cuerpo, text="Ningún servicio seleccionado",
                                      style="Superficie.TLabel", font=FUENTES["negrita"])
        self.lbl_servicio.pack(anchor="w", pady=(0, 6))

        self.form_calculo = Formulario(panel.cuerpo, [
            ("duracion", "Duración", "entrada", {"valor": "1"}),
            ("impuesto", "Impuesto (%)", "entrada", {"valor": str(IMPUESTO_POR_DEFECTO)}),
            ("descuento", "Descuento (%)", "entrada", {"valor": "0"}),
        ], columnas=3)
        self.form_calculo.pack(fill="x")

        botones, self.botones_consulta = fila_botones(panel.cuerpo, [
            ("Consultar disponibilidad", "Info", self.consultar_disponibilidad),
            ("Calcular tarifa", "Exito", self.calcular_tarifa),
            ("Deshabilitar", "Advertencia", self.alternar_habilitacion),
        ])
        botones.pack(fill="x", pady=(12, 8))

        self.resultado = tk.Label(panel.cuerpo, text="", justify="left", anchor="nw",
                                  bg="#f8fafc", fg=PALETA["texto"], font=FUENTES["normal"],
                                  padx=12, pady=10, highlightthickness=1,
                                  highlightbackground=PALETA["borde"])
        self.resultado.pack(fill="both", expand=True)
        self.resultado.bind("<Configure>", lambda e: self.resultado.config(wraplength=max(e.width - 24, 100)))

    def _construir_tabla(self):
        panel = Panel(self, "Catálogo de servicios")
        panel.grid(row=1, column=0, columnspan=2, sticky="nsew")
        filtro = ttk.Frame(panel.cuerpo, style="Superficie.TFrame")
        filtro.pack(fill="x", pady=(0, 8))
        ttk.Label(filtro, text="Mostrar:", style="Superficie.TLabel").pack(side="left", padx=(0, 6))
        self.filtro = ttk.Combobox(filtro, values=["Todos", *CAMPOS_TIPO], state="readonly", width=14)
        self.filtro.set("Todos")
        self.filtro.pack(side="left")
        self.filtro.bind("<<ComboboxSelected>>", lambda _e: self.refrescar())

        self.tabla = Tabla(panel.cuerpo, [
            ("codigo", "Código", 80, "center"),
            ("tipo", "Tipo", 80, "center"),
            ("nombre", "Nombre", 180, "w"),
            ("detalle", "Detalle", 260, "w"),
            ("tarifa_txt", "Tarifa", 110, "e"),
            ("cupos", "Ocupación", 90, "center"),
            ("estado", "Estado", 110, "center"),
        ], alto=7, al_seleccionar=self._al_seleccionar)
        self.tabla.pack(fill="both", expand=True)

    # ---------- comportamiento del formulario ----------
    def _cambiar_tipo(self):
        if self.form_tipo is not None:
            self.form_tipo.destroy()
        tipo = self.tipo.get()
        self.form_tipo = Formulario(self.contenedor_tipo, CAMPOS_TIPO[tipo], columnas=3)
        self.form_tipo.pack(fill="x")
        self._lbl_tarifa.config(text=ETIQUETA_TARIFA[tipo])

    def guardar(self):
        c = self.form_comun.valores()
        t = self.form_tipo.valores()
        gestor = self.sistema.servicios
        tipo = self.tipo.get()
        if tipo == "Sala":
            accion = lambda: gestor.registrar_sala(c["codigo"], c["nombre"], c["tarifa"],
                                                   t["capacidad"], t["cupo"])
        elif tipo == "Equipo":
            accion = lambda: gestor.registrar_equipo(c["codigo"], c["nombre"], c["tarifa"],
                                                     t["tipo_equipo"], t["unidades"])
        else:
            accion = lambda: gestor.registrar_asesoria(c["codigo"], c["nombre"], c["tarifa"],
                                                       t["especialidad"], t["nivel"], t["cupo"])
        servicio = self.ejecutar(accion, formulario=[self.form_comun, self.form_tipo],
                                 exito=lambda s: f"Servicio '{s.nombre}' ({s.tipo}) registrado "
                                                 f"con código {s.codigo}.")
        if servicio:
            self.limpiar()

    def limpiar(self):
        self.form_comun.limpiar()
        self._cambiar_tipo()
        self.form_comun.controles["codigo"].focus_set()

    # ---------- consulta ----------
    def _codigo_seleccionado(self):
        fila = self.tabla.seleccion()
        if not fila:
            messagebox.showwarning("Seleccione un servicio",
                                   "Primero seleccione un servicio en la tabla.", parent=self)
            return None
        return fila["codigo"]

    def _al_seleccionar(self, fila):
        if not fila:
            return
        servicio = self.ejecutar(self.sistema.servicios.obtener, fila["codigo"], notificar=False)
        if servicio:
            self.lbl_servicio.config(text=f"{servicio.codigo} · {servicio.nombre}")
            self.form_calculo.controles["duracion"].master.winfo_children()[0].config(
                text=f"Duración ({servicio.unidad})")
            self.botones_consulta["Deshabilitar"].config(
                text="Deshabilitar" if servicio.disponible else "Habilitar")
            self.resultado.config(text=servicio.describir())

    def consultar_disponibilidad(self):
        codigo = self._codigo_seleccionado()
        if not codigo:
            return
        info = self.ejecutar(self.sistema.servicios.consultar_disponibilidad, codigo, notificar=False)
        if info:
            s = info["servicio"]
            estado = "DISPONIBLE ✔" if info["disponible"] else "NO DISPONIBLE ✖"
            motivo = "" if info["habilitado"] else "\nMotivo: el servicio está deshabilitado."
            self.resultado.config(
                text=f"{s.nombre}: {estado}\nReservas activas: {info['ocupados']} de {s.cupo}"
                     f"\nCupos libres: {info['libres']}{motivo}",
                fg=PALETA["exito"] if info["disponible"] else PALETA["peligro"])

    def calcular_tarifa(self):
        codigo = self._codigo_seleccionado()
        if not codigo:
            return
        v = self.form_calculo.valores()
        detalle = self.ejecutar(self.sistema.servicios.calcular_tarifa, codigo,
                                v["duracion"], v["impuesto"], v["descuento"],
                                formulario=self.form_calculo, notificar=False)
        if detalle:
            servicio = self.sistema.servicios.obtener(codigo)
            self.resultado.config(
                fg=PALETA["texto"],
                text=(f"Tarifa para {detalle['duracion']:g} {servicio.unidad} de {servicio.nombre}\n"
                      f"Subtotal:   {formato_moneda(detalle['subtotal'])}\n"
                      f"Descuento: -{formato_moneda(detalle['descuento'])}\n"
                      f"Impuesto:  +{formato_moneda(detalle['impuesto'])}\n"
                      f"TOTAL:      {formato_moneda(detalle['total'])}"))

    def alternar_habilitacion(self):
        codigo = self._codigo_seleccionado()
        if not codigo:
            return
        servicio = self.sistema.servicios.obtener(codigo)
        accion = "deshabilitar" if servicio.disponible else "habilitar"
        if messagebox.askyesno("Confirmar", f"¿Desea {accion} el servicio '{servicio.nombre}'?",
                               parent=self):
            self.ejecutar(self.sistema.servicios.cambiar_habilitacion, codigo, not servicio.disponible,
                          exito=f"Servicio {codigo} {'deshabilitado' if servicio.disponible else 'habilitado'}.")

    # ---------- refresco ----------
    def refrescar(self):
        seleccion = self.tabla.seleccion()
        filtro = self.filtro.get()
        gestor = self.sistema.servicios
        filas = []
        for s in gestor.listar(None if filtro == "Todos" else filtro):
            info = gestor.consultar_disponibilidad(s.codigo)
            fila = s.a_diccionario()
            fila["tarifa_txt"] = f"{formato_moneda(s.tarifa)}/{s.unidad[:-1] if s.unidad.endswith('s') else s.unidad}"
            fila["cupos"] = f"{info['ocupados']}/{s.cupo}"
            fila["estado"] = ("Disponible" if info["disponible"]
                              else "Sin cupo" if s.disponible else "Deshabilitado")
            filas.append(fila)
        self.tabla.cargar(filas, etiqueta=lambda f: None if f["estado"] == "Disponible"
                          else "inactivo" if f["estado"] == "Deshabilitado" else "WARNING")
        if seleccion:
            for iid in self.tabla.arbol.get_children():
                if self.tabla.arbol.set(iid, "codigo") == seleccion["codigo"]:
                    self.tabla.arbol.selection_set(iid)
                    break
