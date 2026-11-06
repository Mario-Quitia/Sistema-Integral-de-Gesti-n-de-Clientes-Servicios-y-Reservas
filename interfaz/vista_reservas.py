"""Vista de gestión de reservas (Integrante 3)."""
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from excepciones import SoftwareFJError
from interfaz.componentes import (FUENTE, FUENTES, PALETA, Formulario, Panel, Tabla, VistaBase,
                                  fila_botones, formato_moneda)
from modelos.reserva import EstadoReserva
from modelos.servicios import IMPUESTO_POR_DEFECTO


class VistaReservas(VistaBase):
    titulo = "Gestión de reservas"
    subtitulo = "Cree, confirme, procese o cancele reservas; el costo se calcula automáticamente"

    MAPA_CAMPOS = {"duración": "duracion", "impuesto": "impuesto", "descuento": "descuento"}

    def __init__(self, padre, app):
        super().__init__(padre, app)
        self._clientes_idx = {}
        self._servicios_idx = {}
        self._id_cotizacion = None
        self.columnconfigure(0, weight=0, minsize=360)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self._construir_formulario()
        self._construir_tabla()

    # ---------- construcción ----------
    def _construir_formulario(self):
        panel = Panel(self, "Nueva reserva")
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 16))

        self.form = Formulario(panel.cuerpo, [
            ("cliente", "Cliente", "combo", {"span": 3}),
            ("servicio", "Servicio (solo con cupo)", "combo", {"span": 3}),
            ("duracion", "Duración", "entrada", {"valor": "1"}),
            ("impuesto", "Impuesto %", "entrada", {"valor": str(IMPUESTO_POR_DEFECTO)}),
            ("descuento", "Desc. % (≤50)", "entrada", {"valor": "0"}),
        ], columnas=3)
        self.form.pack(fill="x")
        self._lbl_duracion = self.form.controles["duracion"].master.winfo_children()[0]
        for clave in ("servicio", "duracion", "impuesto", "descuento"):
            self.form.variables[clave].trace_add("write", lambda *_: self._programar_cotizacion())

        # Resumen del costo (se actualiza automáticamente)
        resumen = tk.Frame(panel.cuerpo, bg="#f8fafc", highlightthickness=1,
                           highlightbackground=PALETA["borde"])
        resumen.pack(fill="x", pady=(10, 4))
        self._valores_costo = {}
        for i, (clave, texto) in enumerate((("subtotal", "Subtotal"), ("descuento", "Descuento"),
                                            ("impuesto", "Impuesto"), ("total", "TOTAL"))):
            negrita = clave == "total"
            tk.Label(resumen, text=texto, bg="#f8fafc", fg=PALETA["texto"] if negrita else PALETA["texto_suave"],
                     font=(FUENTE, 12 if negrita else 10, "bold" if negrita else "normal")
                     ).grid(row=i, column=0, sticky="w", padx=12, pady=(6 if i == 0 else 1, 6 if negrita else 1))
            etiqueta = tk.Label(resumen, text="—", bg="#f8fafc",
                                fg=PALETA["primario"] if negrita else PALETA["texto"],
                                font=(FUENTE, 12 if negrita else 10, "bold"))
            etiqueta.grid(row=i, column=1, sticky="e", padx=12)
            self._valores_costo[clave] = etiqueta
        resumen.columnconfigure(1, weight=1)
        self.lbl_aviso = ttk.Label(panel.cuerpo, text="", style="Error.TLabel", wraplength=320)
        self.lbl_aviso.pack(anchor="w")

        botones, _ = fila_botones(panel.cuerpo, [
            ("Crear reserva", "Primario", self.crear),
            ("Limpiar", None, self.limpiar),
        ])
        botones.pack(fill="x", pady=(8, 0))

    def _construir_tabla(self):
        panel = Panel(self, "Reservas registradas", "Doble clic en una reserva para ver su historial")
        panel.grid(row=0, column=1, sticky="nsew")

        barra = ttk.Frame(panel.cuerpo, style="Superficie.TFrame")
        barra.pack(fill="x", pady=(0, 10))
        acciones, self.botones = fila_botones(barra, [
            ("Confirmar", "Exito", self.confirmar),
            ("Procesar", "Info", self.procesar),
            ("Cancelar", "Peligro", self.cancelar),
        ])
        acciones.pack(side="left")
        self.filtro = ttk.Combobox(barra, state="readonly", width=12,
                                   values=["Todas", EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA,
                                           EstadoReserva.PROCESADA, EstadoReserva.CANCELADA])
        self.filtro.set("Todas")
        self.filtro.pack(side="right")
        self.filtro.bind("<<ComboboxSelected>>", lambda _e: self.refrescar())
        ttk.Label(barra, text="Estado:", style="Superficie.TLabel").pack(side="right", padx=6)

        self.tabla = Tabla(panel.cuerpo, [
            ("codigo", "Código", 60, "center"),
            ("cliente", "Cliente", 120, "w"),
            ("servicio", "Servicio", 130, "w"),
            ("duracion", "Duración", 75, "center"),
            ("total_txt", "Total", 90, "e"),
            ("estado", "Estado", 85, "center"),
            ("subtotal_txt", "Subtotal", 90, "e"),
            ("fecha", "Fecha", 115, "center"),
        ], al_seleccionar=self._actualizar_botones, al_doble_clic=self._ver_historial)
        self.tabla.pack(fill="both", expand=True)

        leyenda = ttk.Frame(panel.cuerpo, style="Superficie.TFrame")
        leyenda.pack(fill="x", pady=(8, 0))
        for estado, color in ((EstadoReserva.PENDIENTE, PALETA["advertencia"]),
                              (EstadoReserva.CONFIRMADA, PALETA["primario"]),
                              (EstadoReserva.PROCESADA, PALETA["exito"]),
                              (EstadoReserva.CANCELADA, PALETA["peligro"])):
            tk.Label(leyenda, text="■", fg=color, bg=PALETA["superficie"]).pack(side="left")
            tk.Label(leyenda, text=estado, bg=PALETA["superficie"], fg=PALETA["texto_suave"],
                     font=FUENTES["pequena"]).pack(side="left", padx=(2, 12))
        self._actualizar_botones(None)

    # ---------- cálculo automático del costo ----------
    def _programar_cotizacion(self):
        """Espera 250 ms tras la última tecla para no recalcular en cada pulsación."""
        if self._id_cotizacion:
            self.after_cancel(self._id_cotizacion)
        self._id_cotizacion = self.after(250, self._cotizar)

    def _cotizar(self):
        self._id_cotizacion = None
        v = self.form.valores()
        servicio = self._servicios_idx.get(v["servicio"])
        if servicio:
            self._lbl_duracion.config(text=f"Duración ({servicio.unidad})")
        if not servicio or not v["duracion"]:
            self._mostrar_costos(None)
            return
        try:
            # La lógica del cálculo vive en el gestor; aquí solo se muestra
            detalle = self.sistema.reservas.cotizar(servicio.codigo, v["duracion"],
                                                    v["impuesto"], v["descuento"])
        except SoftwareFJError as error:
            self._mostrar_costos(None, error.mensaje)
        except Exception as error:   # pylint: disable=broad-except
            self._mostrar_costos(None, f"No se pudo calcular: {error}")
        else:
            self._mostrar_costos(detalle)

    def _mostrar_costos(self, detalle, aviso=""):
        for clave, etiqueta in self._valores_costo.items():
            if detalle is None:
                etiqueta.config(text="—")
            else:
                signo = "- " if clave == "descuento" else "+ " if clave == "impuesto" else ""
                etiqueta.config(text=signo + formato_moneda(detalle[clave]))
        self.lbl_aviso.config(text=aviso)

    # ---------- acciones (delegan en el gestor de reservas) ----------
    def crear(self):
        v = self.form.valores()
        cliente = self._clientes_idx.get(v["cliente"])
        servicio = self._servicios_idx.get(v["servicio"])
        reserva = self.ejecutar(
            self.sistema.reservas.crear,
            cliente.identificacion if cliente else v["cliente"],
            servicio.codigo if servicio else v["servicio"],
            v["duracion"], v["impuesto"], v["descuento"],
            formulario=self.form,
            exito=lambda r: f"Reserva {r.codigo} creada.\nTotal: {formato_moneda(r.total)}\n"
                            f"Estado: {r.estado}")
        if reserva:
            self.limpiar(conservar_cliente=True)

    def limpiar(self, conservar_cliente=False):
        cliente = self.form.variables["cliente"].get()
        self.form.limpiar({"duracion": "1", "impuesto": str(IMPUESTO_POR_DEFECTO), "descuento": "0",
                           "cliente": cliente if conservar_cliente else ""})
        self._lbl_duracion.config(text="Duración")
        self._mostrar_costos(None)
        for clave in ("duracion", "impuesto", "descuento"):
            self.form.controles[clave].configure(style="TEntry")

    def _codigo_seleccionado(self):
        fila = self.tabla.seleccion()
        if not fila:
            messagebox.showwarning("Seleccione una reserva", "Primero seleccione una reserva en la tabla.",
                                   parent=self)
            return None
        return fila["codigo"]

    def confirmar(self):
        codigo = self._codigo_seleccionado()
        if codigo and messagebox.askyesno("Confirmar reserva", f"¿Confirmar la reserva {codigo}?",
                                          parent=self):
            self.ejecutar(self.sistema.reservas.confirmar, codigo,
                          exito=f"La reserva {codigo} fue confirmada.")

    def procesar(self):
        codigo = self._codigo_seleccionado()
        if codigo and messagebox.askyesno("Procesar reserva",
                                          f"¿Procesar (facturar) la reserva {codigo}?", parent=self):
            self.ejecutar(self.sistema.reservas.procesar, codigo,
                          exito=lambda r: f"Reserva {r.codigo} procesada. Facturado: {formato_moneda(r.total)}")

    def cancelar(self):
        codigo = self._codigo_seleccionado()
        if not codigo:
            return
        if not messagebox.askyesno("Cancelar reserva",
                                   f"¿Seguro que desea cancelar la reserva {codigo}?\n"
                                   "Esta acción no se puede deshacer.", icon="warning", parent=self):
            return
        motivo = simpledialog.askstring("Motivo", "Motivo de la cancelación (opcional):", parent=self)
        self.ejecutar(self.sistema.reservas.cancelar, codigo, motivo or "Cancelada por el usuario",
                      exito=f"La reserva {codigo} fue cancelada.")

    def _actualizar_botones(self, fila):
        """Habilita solo las acciones válidas para el estado de la reserva seleccionada."""
        estado = fila["estado"] if fila else None
        permitidos = {
            "Confirmar": estado == EstadoReserva.PENDIENTE,
            "Procesar": estado == EstadoReserva.CONFIRMADA,
            "Cancelar": estado in EstadoReserva.ACTIVOS,
        }
        for texto, boton in self.botones.items():
            boton.state(["!disabled"] if permitidos.get(texto) else ["disabled"])

    def _ver_historial(self, fila):
        reserva = self.ejecutar(self.sistema.reservas.obtener, fila["codigo"], notificar=False)
        if not reserva:
            return
        c = reserva.costos
        lineas = [reserva.describir(), "",
                  f"Subtotal: {formato_moneda(c['subtotal'])}   Descuento: {formato_moneda(c['descuento'])}"
                  f"   Impuesto: {formato_moneda(c['impuesto'])}", "", "Historial:"]
        lineas += [f"  {fecha:%Y-%m-%d %H:%M:%S}  {estado:<11} {nota}"
                   for fecha, estado, nota in reserva.historial]
        messagebox.showinfo(f"Reserva {reserva.codigo}", "\n".join(lineas), parent=self)

    # ---------- refresco ----------
    def refrescar(self):
        clientes = self.sistema.clientes.listar()
        self._clientes_idx = {f"{c.identificacion} - {c.nombre}": c for c in clientes}
        self.form.controles["cliente"]["values"] = list(self._clientes_idx)

        servicios = self.sistema.servicios.listar()
        self._servicios_idx = {f"{s.codigo} - {s.nombre} ({s.tipo})": s for s in servicios}
        disponibles = [k for k, s in self._servicios_idx.items()
                       if self.sistema.servicios.consultar_disponibilidad(s.codigo)["disponible"]]
        self.form.controles["servicio"]["values"] = disponibles

        filtro = self.filtro.get()
        filas = []
        for r in self.sistema.reservas.listar(None if filtro == "Todas" else filtro):
            fila = r.a_diccionario()
            fila["subtotal_txt"] = formato_moneda(fila["subtotal"])
            fila["total_txt"] = formato_moneda(fila["total"])
            filas.append(fila)
        filas.reverse()   # las más recientes arriba
        self.tabla.cargar(filas, etiqueta=lambda f: f["estado"])
        self._actualizar_botones(None)
