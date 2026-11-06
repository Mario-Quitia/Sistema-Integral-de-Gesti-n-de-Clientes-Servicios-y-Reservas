"""
Componentes gráficos reutilizables y puente seguro con los gestores.

- PALETA / FUENTES / configurar_estilos: apariencia común (ttk).
- Tarjeta: tarjeta informativa con una estadística.
- Tabla: ttk.Treeview con barras de desplazamiento.
- Formulario: etiquetas + campos con valores y limpieza centralizados.
- VistaBase: clase base de todas las vistas; su método `ejecutar` llama al
  gestor, captura cualquier excepción y la muestra con messagebox, de modo que
  ningún error cierre la aplicación.
"""
import tkinter as tk
from tkinter import messagebox, ttk

from excepciones import SoftwareFJError, ValidacionError
from registro import registrar_critico

PALETA = {
    "fondo": "#f1f5f9",
    "superficie": "#ffffff",
    "borde": "#e2e8f0",
    "texto": "#0f172a",
    "texto_suave": "#64748b",
    "lateral": "#0f172a",
    "lateral_hover": "#1e293b",
    "lateral_activo": "#2563eb",
    "lateral_texto": "#cbd5e1",
    "primario": "#2563eb",
    "primario_hover": "#1d4ed8",
    "exito": "#16a34a",
    "advertencia": "#d97706",
    "peligro": "#dc2626",
    "info": "#0891b2",
    "morado": "#7c3aed",
}

FUENTE = "Segoe UI"
FUENTES = {
    "titulo": (FUENTE, 20, "bold"),
    "subtitulo": (FUENTE, 11),
    "seccion": (FUENTE, 13, "bold"),
    "normal": (FUENTE, 10),
    "negrita": (FUENTE, 10, "bold"),
    "pequena": (FUENTE, 9),
    "dato": (FUENTE, 24, "bold"),
    "marca": (FUENTE, 17, "bold"),
}


def configurar_estilos(raiz):
    """Configura el tema ttk de toda la aplicación."""
    estilo = ttk.Style(raiz)
    try:
        estilo.theme_use("clam")
    except tk.TclError:
        pass
    p = PALETA
    raiz.option_add("*TCombobox*Listbox.font", FUENTES["normal"])
    estilo.configure(".", font=FUENTES["normal"], background=p["fondo"], foreground=p["texto"])
    estilo.configure("TFrame", background=p["fondo"])
    estilo.configure("Superficie.TFrame", background=p["superficie"])
    estilo.configure("TLabel", background=p["fondo"], foreground=p["texto"])
    estilo.configure("Superficie.TLabel", background=p["superficie"])
    estilo.configure("Suave.TLabel", background=p["superficie"], foreground=p["texto_suave"],
                     font=FUENTES["pequena"])
    estilo.configure("Seccion.TLabel", background=p["superficie"], font=FUENTES["seccion"])
    estilo.configure("Titulo.TLabel", font=FUENTES["titulo"])
    estilo.configure("Subtitulo.TLabel", foreground=p["texto_suave"], font=FUENTES["subtitulo"])
    estilo.configure("Error.TLabel", background=p["superficie"], foreground=p["peligro"],
                     font=FUENTES["pequena"])
    estilo.configure("TRadiobutton", background=p["superficie"])
    estilo.configure("TCheckbutton", background=p["superficie"])

    estilo.configure("TEntry", padding=6, fieldbackground="#ffffff", bordercolor=p["borde"],
                     lightcolor=p["borde"], darkcolor=p["borde"])
    estilo.map("TEntry", bordercolor=[("focus", p["primario"])], lightcolor=[("focus", p["primario"])])
    estilo.configure("Invalido.TEntry", fieldbackground="#fef2f2", bordercolor=p["peligro"])
    estilo.configure("TCombobox", padding=5, arrowsize=14)

    # Botones
    estilo.configure("TButton", padding=(14, 8), font=FUENTES["negrita"], borderwidth=0,
                     background="#e2e8f0", foreground=p["texto"])
    estilo.map("TButton", background=[("active", "#cbd5e1"), ("disabled", "#f1f5f9")],
               foreground=[("disabled", "#94a3b8")])
    for nombre, color, hover in (("Primario", p["primario"], p["primario_hover"]),
                                 ("Exito", p["exito"], "#15803d"),
                                 ("Peligro", p["peligro"], "#b91c1c"),
                                 ("Advertencia", p["advertencia"], "#b45309"),
                                 ("Info", p["info"], "#0e7490")):
        estilo.configure(f"{nombre}.TButton", background=color, foreground="#ffffff")
        estilo.map(f"{nombre}.TButton",
                   background=[("disabled", "#cbd5e1"), ("active", hover)],
                   foreground=[("disabled", "#f8fafc")])

    # Tablas
    estilo.configure("Treeview", rowheight=30, background=p["superficie"], fieldbackground=p["superficie"],
                     bordercolor=p["borde"], borderwidth=0, font=FUENTES["normal"])
    estilo.configure("Treeview.Heading", font=FUENTES["negrita"], background="#e2e8f0",
                     foreground=p["texto"], relief="flat", padding=6)
    estilo.map("Treeview", background=[("selected", "#dbeafe")], foreground=[("selected", p["texto"])])
    estilo.map("Treeview.Heading", background=[("active", "#cbd5e1")])

    estilo.configure("TNotebook", background=p["superficie"], borderwidth=0)
    estilo.configure("TNotebook.Tab", padding=(14, 6), font=FUENTES["negrita"])
    estilo.configure("TLabelframe", background=p["superficie"], bordercolor=p["borde"])
    estilo.configure("TLabelframe.Label", background=p["superficie"], font=FUENTES["negrita"])
    return estilo


def formato_moneda(valor):
    try:
        return f"$ {float(valor):,.0f}".replace(",", ".")
    except (TypeError, ValueError):
        return str(valor)


# ---------------------------------------------------------------------------
# Contenedores
# ---------------------------------------------------------------------------
class Panel(tk.Frame):
    """Contenedor blanco con borde suave, título opcional y área `cuerpo`."""

    def __init__(self, padre, titulo=None, subtitulo=None, **kwargs):
        super().__init__(padre, bg=PALETA["superficie"], highlightthickness=1,
                         highlightbackground=PALETA["borde"], **kwargs)
        if titulo:
            cabecera = ttk.Frame(self, style="Superficie.TFrame")
            cabecera.pack(fill="x", padx=16, pady=(14, 4))
            ttk.Label(cabecera, text=titulo, style="Seccion.TLabel").pack(anchor="w")
            if subtitulo:
                ttk.Label(cabecera, text=subtitulo, style="Suave.TLabel").pack(anchor="w")
        self.cuerpo = ttk.Frame(self, style="Superficie.TFrame")
        self.cuerpo.pack(fill="both", expand=True, padx=16, pady=(4, 14))


class Tarjeta(tk.Frame):
    """Tarjeta informativa con una franja de color, un título y un valor."""

    def __init__(self, padre, titulo, color, icono="●", valor="0", detalle=""):
        super().__init__(padre, bg=PALETA["superficie"], highlightthickness=1,
                         highlightbackground=PALETA["borde"])
        tk.Frame(self, bg=color, width=5).pack(side="left", fill="y")
        cuerpo = tk.Frame(self, bg=PALETA["superficie"])
        cuerpo.pack(side="left", fill="both", expand=True, padx=14, pady=12)
        fila = tk.Frame(cuerpo, bg=PALETA["superficie"])
        fila.pack(fill="x")
        tk.Label(fila, text=titulo.upper(), bg=PALETA["superficie"], fg=PALETA["texto_suave"],
                 font=(FUENTE, 9, "bold")).pack(side="left")
        tk.Label(fila, text=icono, bg=PALETA["superficie"], fg=color,
                 font=(FUENTE, 14)).pack(side="right")
        self._valor = tk.Label(cuerpo, text=valor, bg=PALETA["superficie"], fg=PALETA["texto"],
                               font=FUENTES["dato"], anchor="w")
        self._valor.pack(fill="x")
        self._detalle = tk.Label(cuerpo, text=detalle, bg=PALETA["superficie"],
                                 fg=PALETA["texto_suave"], font=FUENTES["pequena"], anchor="w")
        self._detalle.pack(fill="x")

    def actualizar(self, valor, detalle=None):
        self._valor.config(text=str(valor))
        if detalle is not None:
            self._detalle.config(text=detalle)


class Tabla(ttk.Frame):
    """
    Treeview con scroll. `columnas` es una lista de tuplas
    (clave, encabezado, ancho, alineación).
    """

    def __init__(self, padre, columnas, alto=10, al_seleccionar=None, al_doble_clic=None):
        super().__init__(padre, style="Superficie.TFrame")
        self._claves = [c[0] for c in columnas]
        self.arbol = ttk.Treeview(self, columns=self._claves, show="headings", height=alto,
                                  selectmode="browse")
        for clave, encabezado, ancho, alineacion in columnas:
            self.arbol.heading(clave, text=encabezado, anchor=alineacion,
                               command=lambda c=clave: self._ordenar(c, False))
            self.arbol.column(clave, width=ancho, minwidth=50, anchor=alineacion, stretch=True)
        barra_v = ttk.Scrollbar(self, orient="vertical", command=self.arbol.yview)
        barra_h = ttk.Scrollbar(self, orient="horizontal", command=self.arbol.xview)
        self.arbol.configure(yscrollcommand=barra_v.set, xscrollcommand=barra_h.set)
        self.arbol.grid(row=0, column=0, sticky="nsew")
        barra_v.grid(row=0, column=1, sticky="ns")
        barra_h.grid(row=1, column=0, sticky="ew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.arbol.tag_configure("par", background="#f8fafc")
        for etiqueta, color in (("Pendiente", "#fffbeb"), ("Confirmada", "#eff6ff"),
                                ("Procesada", "#f0fdf4"), ("Cancelada", "#fef2f2"),
                                ("ERROR", "#fef2f2"), ("CRITICAL", "#fee2e2"),
                                ("WARNING", "#fffbeb"), ("ok", "#f0fdf4"), ("fallo", "#fef2f2"),
                                ("inactivo", "#f1f5f9")):
            self.arbol.tag_configure(etiqueta, background=color)

        if al_seleccionar:
            self.arbol.bind("<<TreeviewSelect>>", lambda _e: al_seleccionar(self.seleccion()))
        if al_doble_clic:
            self.arbol.bind("<Double-1>", lambda _e: self.seleccion() and al_doble_clic(self.seleccion()))

    def cargar(self, filas, etiqueta=None):
        """
        filas: lista de diccionarios con las claves de las columnas.
        etiqueta: función opcional fila -> nombre de tag para colorear.
        """
        self.arbol.delete(*self.arbol.get_children())
        for i, fila in enumerate(filas):
            valores = [fila.get(c, "") for c in self._claves]
            tags = [etiqueta(fila)] if etiqueta else ["par"] if i % 2 else []
            self.arbol.insert("", "end", iid=str(i), values=valores, tags=[t for t in tags if t])

    def seleccion(self):
        """Devuelve un diccionario con la fila seleccionada (o None)."""
        elegido = self.arbol.selection()
        if not elegido:
            return None
        return dict(zip(self._claves, self.arbol.item(elegido[0], "values")))

    def _ordenar(self, columna, descendente):
        datos = [(self.arbol.set(i, columna), i) for i in self.arbol.get_children("")]

        def clave(par):
            texto = str(par[0]).replace("$", "").replace(".", "").replace(" ", "")
            try:
                return (0, float(texto))
            except ValueError:
                return (1, str(par[0]).lower())

        datos.sort(key=clave, reverse=descendente)
        for posicion, (_v, iid) in enumerate(datos):
            self.arbol.move(iid, "", posicion)
        self.arbol.heading(columna, command=lambda: self._ordenar(columna, not descendente))


class Formulario(ttk.Frame):
    """
    Formulario sencillo en una rejilla de dos columnas (etiqueta / control).
    Los campos se describen con tuplas (clave, etiqueta, tipo, opciones),
    donde tipo es "entrada" o "combo".
    """

    def __init__(self, padre, campos, columnas=1):
        super().__init__(padre, style="Superficie.TFrame")
        self.variables = {}
        self.controles = {}
        for i, (clave, etiqueta, tipo, opciones) in enumerate(campos):
            fila, col = divmod(i, columnas)
            caja = ttk.Frame(self, style="Superficie.TFrame")
            caja.grid(row=fila, column=col, sticky="ew", padx=(0 if col == 0 else 12, 0), pady=4)
            ttk.Label(caja, text=etiqueta, style="Superficie.TLabel",
                      font=FUENTES["negrita"]).pack(anchor="w")
            variable = tk.StringVar(value=opciones.get("valor", ""))
            if tipo == "combo":
                control = ttk.Combobox(caja, textvariable=variable, values=opciones.get("valores", []),
                                       state=opciones.get("estado", "readonly"))
            else:
                control = ttk.Entry(caja, textvariable=variable)
            control.pack(fill="x", pady=(2, 0))
            control.bind("<Key>", lambda _e, c=control: self._limpiar_marca(c), add="+")
            self.variables[clave] = variable
            self.controles[clave] = control
        for col in range(columnas):
            self.columnconfigure(col, weight=1)

    def valores(self):
        return {clave: var.get().strip() for clave, var in self.variables.items()}

    def asignar(self, datos):
        for clave, valor in datos.items():
            if clave in self.variables:
                self.variables[clave].set(valor)

    def limpiar(self, valores_por_defecto=None):
        for clave, variable in self.variables.items():
            variable.set((valores_por_defecto or {}).get(clave, ""))
            self._limpiar_marca(self.controles[clave])

    def marcar_invalido(self, clave):
        control = self.controles.get(clave)
        if isinstance(control, ttk.Entry) and not isinstance(control, ttk.Combobox):
            control.configure(style="Invalido.TEntry")
        if control:
            control.focus_set()

    @staticmethod
    def _limpiar_marca(control):
        if isinstance(control, ttk.Entry) and not isinstance(control, ttk.Combobox):
            control.configure(style="TEntry")


def fila_botones(padre, botones):
    """Crea una fila de botones: lista de (texto, estilo, comando). Devuelve dict texto->botón."""
    marco = ttk.Frame(padre, style="Superficie.TFrame")
    creados = {}
    for texto, estilo, comando in botones:
        boton = ttk.Button(marco, text=texto, style=f"{estilo}.TButton" if estilo else "TButton",
                           command=comando, cursor="hand2")
        boton.pack(side="left", padx=(0, 8))
        creados[texto] = boton
    return marco, creados


# ---------------------------------------------------------------------------
# Vista base con manejo de errores centralizado
# ---------------------------------------------------------------------------
class VistaBase(ttk.Frame):
    """
    Clase base de las vistas. Mantiene referencias al sistema (gestores) y a la
    ventana principal, y ofrece `ejecutar` para invocar a los gestores de forma
    segura. Las subclases implementan `refrescar`.
    """

    titulo = ""
    subtitulo = ""

    # Relaciona el nombre de campo de las excepciones con la clave del formulario
    MAPA_CAMPOS = {}

    def __init__(self, padre, app):
        super().__init__(padre)
        self.app = app
        self.sistema = app.sistema

    def refrescar(self):
        """Recarga tablas y listas desde los gestores."""

    def ejecutar(self, accion, *args, exito=None, formulario=None, notificar=True, **kwargs):
        """
        Llama a un método de un gestor. Devuelve su resultado o None si falló.
        - Errores de negocio (SoftwareFJError): advertencia con el mensaje.
        - Errores de validación: además se resalta el campo en `formulario`
          (un Formulario o una lista de ellos).
        - Errores inesperados: ventana de error; la aplicación sigue abierta.
        Si `notificar` es True, tras el éxito se refrescan todas las vistas
        (usar False en consultas que no modifican datos).
        """
        try:
            resultado = accion(*args, **kwargs)
        except ValidacionError as error:
            clave = self.MAPA_CAMPOS.get(error.campo)
            formularios = formulario if isinstance(formulario, (list, tuple)) else [formulario]
            for form in formularios:
                if form is not None and clave in form.controles:
                    form.marcar_invalido(clave)
                    break
            messagebox.showwarning("Datos no válidos", error.mensaje, parent=self)
            self.app.estado(f"Validación: {error.mensaje}", "advertencia")
        except SoftwareFJError as error:
            messagebox.showwarning("Operación no realizada", error.mensaje, parent=self)
            self.app.estado(error.mensaje, "advertencia")
        except Exception as error:   # pylint: disable=broad-except
            registrar_critico("Error inesperado en la interfaz", error)
            messagebox.showerror("Error inesperado",
                                 f"Ocurrió un error inesperado y quedó registrado en el log.\n\n"
                                 f"{type(error).__name__}: {error}", parent=self)
            self.app.estado("Error inesperado (ver registro de eventos)", "peligro")
        else:
            if exito:
                texto = exito(resultado) if callable(exito) else exito
                messagebox.showinfo("Operación exitosa", texto, parent=self)
                self.app.estado(texto, "exito")
            if notificar:
                self.app.notificar_cambio()
            return resultado
        return None
