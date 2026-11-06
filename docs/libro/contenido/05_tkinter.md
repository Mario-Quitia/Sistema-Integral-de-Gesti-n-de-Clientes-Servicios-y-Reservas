# Conociendo Tkinter
> Aprenderás cómo se construyen las ventanas, botones, formularios y tablas de Software FJ, y cómo un clic se convierte en una acción del programa.

@objetivos
- Explicar qué es una interfaz gráfica y qué es Tkinter.
- Reconocer en la ventana real de Software FJ los principales elementos gráficos: ventana, marcos, etiquetas, campos de texto, listas desplegables, botones, tablas y ventanas emergentes.
- Entender cómo se acomodan los elementos en la pantalla con `pack` y `grid`.
- Comprender qué es un evento y cómo se conecta un botón con una función (`command`, `bind`, `after`, `trace_add`).
- Seguir en el código real el camino de un clic en el botón **Guardar**.
@fin

En los capítulos anteriores trabajaste con programas que muestran texto en una consola. Software FJ, en cambio, tiene ventanas, colores, botones y tablas. Todo eso se construye con **Tkinter**. En este capítulo vas a aprender a reconocer cada pieza de la interfaz y a encontrarla en el código.

::img a_ventana | La ventana principal real de Software FJ. Al final del capítulo podrás decir qué código dibuja cada zona numerada.

## 5.1 ¿Qué es una interfaz gráfica?

@nivel1
Cuando usas un cajero automático no escribes órdenes en un idioma especial: tocas botones en una pantalla que dicen «Retirar», «Consultar saldo» o «Cancelar». Esa pantalla es la **interfaz**: el lugar donde la persona y la máquina se comunican. La palabra «interfaz» significa justamente «la cara que está entre dos cosas».
@fin

@nivel2
Una **interfaz gráfica de usuario** (en inglés *Graphical User Interface*, abreviada **GUI**) es la parte visual de un programa: ventanas, botones, cuadros de texto, menús e imágenes que el usuario maneja con el ratón y el teclado. Lo contrario es una **interfaz de consola** (o de línea de comandos), donde todo se hace escribiendo texto.

| Interfaz de consola | Interfaz gráfica |
|---|---|
| Se escriben órdenes y se leen respuestas en texto. | Se hace clic en botones y se llenan formularios. |
| Ejemplo: `python main.py --consola`. | Ejemplo: `python main.py`. |
| Más sencilla de programar. | Más fácil de usar para cualquier persona. |
@fin

@nivel3
Software FJ tiene las dos. Si lo inicias con `python main.py --consola` muestra resultados como texto; si lo inicias con `python main.py` abre la ventana gráfica. El archivo `main.py` decide cuál usar:

::codigo main.py 14-26 | main.py decide si abrir la interfaz gráfica o la consola
::lineas
15 | Lee las opciones escritas después de `python main.py`.
16-19 | Si se escribió `--consola`, ejecuta la simulación como texto y termina.
22 | Si no, importa la clase `VentanaPrincipal` del paquete `interfaz`.
23 | Crea el objeto ventana: en este momento se construye toda la interfaz gráfica.
24-25 | Si se escribió `--demo`, programa la demostración para que empiece 600 milisegundos después.
26 | `mainloop()` pone la ventana «a escuchar» al usuario. Lo explicamos en la sección 5.11.
::fin
@fin

## 5.2 ¿Qué es Tkinter?

@nivel1
Para construir una casa no fabricas tú mismo los ladrillos, las puertas y las ventanas: los compras ya hechos en una ferretería y los acomodas. Tkinter es como esa ferretería: trae piezas listas (botones, cuadros de texto, tablas) para que tú solo las acomodes y les digas qué hacer.
@fin

@nivel2
**Tkinter** es la biblioteca (un conjunto de código ya escrito y listo para usar) que viene incluida con Python para crear interfaces gráficas. Su nombre viene de *Tk interface*: es la conexión de Python con **Tk**, una herramienta gráfica muy antigua y estable. No hay que instalar nada adicional en Windows ni en macOS.

A cada pieza gráfica se le llama **widget** (de *window gadget*, «aparato de ventana»). Tkinter tiene dos familias de widgets:

| Familia | Cómo se importa | Características |
|---|---|---|
| `tk` (clásicos) | `import tkinter as tk` | Widgets básicos; su apariencia se configura uno por uno (colores, fuentes). |
| `ttk` (temáticos) | `from tkinter import ttk` | Widgets más modernos que comparten un **tema** de estilos; incluye `Treeview` (tablas) y `Combobox` (listas desplegables). |

El programa más pequeño posible con Tkinter es este:

```python
import tkinter as tk

ventana = tk.Tk()                 # 1. crear la ventana
ventana.title("Mi primera app")   # 2. ponerle título
ventana.mainloop()                # 3. mostrarla y esperar al usuario
```
@fin

@nivel3
Software FJ usa las dos familias. Por ejemplo, la ventana de clientes importa `messagebox` y `ttk`:

::codigo interfaz/vista_clientes.py 1-4 | Importaciones de Tkinter en la vista de clientes
::lineas
2 | De Tkinter trae `messagebox` (ventanas de mensaje) y `ttk` (widgets temáticos).
4 | De su propio proyecto trae piezas ya armadas: `Formulario`, `Panel`, `Tabla`, `VistaBase` y `fila_botones`.
::fin

Una decisión importante del proyecto es que **la interfaz no contiene reglas del negocio**: no valida correos ni calcula precios. Solo muestra datos y llama a los gestores. Esa separación la explica el primer comentario del paquete:

::codigo interfaz/__init__.py 1-9 | La interfaz solo presenta datos y captura entradas
@fin

::img d_capas | La interfaz está en la capa superior: habla con los gestores, y los gestores con los modelos.

## 5.3 ¿Qué es una ventana?

@nivel1
Una ventana es como un **tablero de corcho** enmarcado: un espacio rectangular donde vas pegando avisos, fotos y notas. Puedes moverlo, agrandarlo o cerrarlo, y todo lo que pegaste viaja con él.
@fin

@nivel2
En Tkinter, la ventana principal se crea con la clase `tk.Tk`. Solo debe haber **una** ventana principal por programa; las ventanas adicionales se crean con `tk.Toplevel` (sección 5.10). A la ventana se le pueden dar un título (`title`), un tamaño y posición (`geometry`, con el formato `"ancho x alto + x + y"`), un tamaño mínimo (`minsize`) y un color de fondo (`configure(bg=...)`).

Dentro de la ventana se colocan **contenedores** llamados `Frame` (marco): rectángulos invisibles o con color que sirven para agrupar otros widgets, como las cajas de una estantería. Un `Frame` puede contener otros `Frame`, y así se arma un **árbol**: la ventana contiene marcos, los marcos contienen etiquetas y botones.
@fin

@nivel3
`VentanaPrincipal` **hereda** de `tk.Tk` (herencia, capítulo 4): es una ventana de Tkinter con capacidades extra.

::codigo interfaz/ventana_principal.py 45-74 | La clase VentanaPrincipal
::lineas
45 | `class VentanaPrincipal(tk.Tk)`: la ventana principal **es una** ventana de Tkinter.
46-52 | Lista de las cinco secciones del menú: clave interna, texto, ícono y la clase de la vista que se muestra.
55 | `super().__init__()` crea la ventana real de Tkinter.
56 | Crea (o recibe) el sistema con los tres gestores.
57 | Título que aparece en la barra superior de la ventana.
58-59 | Tamaño inicial calculado según la pantalla y tamaño mínimo de 1000 × 640 píxeles.
60-61 | Color de fondo y estilos visuales de toda la aplicación.
64 | Si un error escapa en cualquier clic, lo atiende el método `_error_global` en lugar de cerrar el programa.
65 | Si el usuario pulsa la X de la ventana, se ejecuta `salir`, que pide confirmación.
70-71 | Construye el menú lateral y la zona de contenido.
72 | Muestra el panel principal.
73 | Pone a andar el reloj.
::fin
@fin

::img d_tk_arbol | Árbol de widgets de la ventana principal: la ventana contiene el menú lateral y la zona derecha; cada una contiene a su vez otros widgets.

## 5.4 Cómo se acomodan los widgets: `pack` y `grid`

Crear un widget no basta para verlo: hay que decirle a Tkinter **dónde** ponerlo. Para eso existen los **administradores de geometría**. Software FJ usa dos.

@nivel1
Imagina dos formas de organizar una nevera. En la primera, metes las cosas **apiladas** una detrás de otra: «esto arriba, esto debajo, esto a la izquierda». En la segunda, la nevera tiene una **cuadrícula** de compartimentos numerados: «fila 1, columna 2».
@fin

@nivel2
- `pack()` apila los widgets uno tras otro, arriba, abajo, a la izquierda o a la derecha (`side="left"`). Con `fill="x"` el widget se estira a lo ancho y con `expand=True` aprovecha el espacio sobrante.
- `grid()` ubica los widgets en una cuadrícula de filas y columnas (`row=0, column=1`). Con `sticky="nsew"` el widget se pega a los cuatro bordes de su celda (*north, south, east, west*). Con `columnconfigure(..., weight=1)` una columna crece cuando la ventana se agranda.

Regla importante: dentro de un mismo contenedor no se deben mezclar `pack` y `grid`.
@fin

@nivel3
La vista de clientes usa `grid` para dividir la pantalla en dos columnas: formulario a la izquierda y tabla a la derecha.

::codigo interfaz/vista_clientes.py 14-26 | Dos columnas con grid
::lineas
17 | La columna 0 (formulario) no crece, pero mide al menos 330 píxeles.
18 | La columna 1 (tabla) crece cuando se agranda la ventana.
19 | La fila 0 también crece hacia abajo.
26 | El panel del formulario se pone en la fila 0, columna 0, pegado a todos los bordes, con 16 píxeles de separación a la derecha.
::fin
@fin

## 5.5 ¿Qué es una etiqueta?

@nivel1
Una etiqueta es como el **letrero** pegado sobre un casillero que dice «Correspondencia» o «Archivo». No se puede escribir en él; solo informa.
@fin

@nivel2
Una **etiqueta** (`Label`) es un widget que muestra un texto o una imagen que el usuario no puede editar. Se usa para títulos, nombres de campos, mensajes y valores calculados. Su texto se puede cambiar desde el código con `config(text="...")`.

```python
import tkinter as tk
ventana = tk.Tk()
saludo = tk.Label(ventana, text="Bienvenido a Software FJ", font=("Segoe UI", 14))
saludo.pack(padx=20, pady=20)
ventana.mainloop()
```
@fin

@nivel3
Las etiquetas están en todas partes de Software FJ: el nombre de cada campo, los títulos de los paneles, el reloj, la barra de estado y el letrero «Modo: nuevo registro». El reloj es una etiqueta cuyo texto se cambia cada segundo:

::codigo interfaz/ventana_principal.py 176-178 | El reloj: una etiqueta que se actualiza sola
::lineas
177 | Cambia el texto de la etiqueta `lbl_reloj` por el día, la fecha y la hora actuales.
178 | Pide a Tkinter que vuelva a ejecutar este mismo método dentro de 1000 milisegundos (un segundo). Así el reloj nunca se detiene (ver `after`, sección 5.12).
::fin
@fin

@nota
El día de la semana aparece en inglés en las capturas (por ejemplo, «Thursday») porque el código usa el formato `%A` de Python, que depende del idioma configurado en el sistema.
@fin

::img t_widgets_clientes | Widgets reales de la pantalla de clientes: etiquetas (Label), campos de texto (Entry), botones (Button), tabla (Treeview) y marcos (Frame).

## 5.6 ¿Qué es un campo de texto?

@nivel1
Un campo de texto es como el **espacio en blanco** de un formulario de papel donde escribes tu nombre. Es el lugar reservado para que tú pongas información.
@fin

@nivel2
El **campo de texto** de una sola línea se llama `Entry`. El usuario escribe en él y el programa lee lo escrito con el método `get()`. Hay una forma más cómoda de manejarlo: conectarlo a una **variable de Tkinter** (`tk.StringVar`). Una `StringVar` es una caja especial que se mantiene sincronizada con el campo: si el usuario escribe, la variable cambia; si el programa cambia la variable con `set()`, el campo se actualiza en pantalla.

```python
nombre = tk.StringVar()
campo = ttk.Entry(ventana, textvariable=nombre)
campo.pack()
# más tarde...
print(nombre.get())     # lo que el usuario escribió
nombre.set("")          # borra el campo
```

Un pariente cercano es la **lista desplegable** (`ttk.Combobox`): un campo con una flecha que muestra opciones para elegir. Si se configura como `state="readonly"`, el usuario solo puede elegir, no escribir.
@fin

@nivel3
Software FJ crea sus campos dentro de la clase `Formulario` (archivo `interfaz/componentes.py`), que recibe una lista de campos y los dibuja automáticamente, cada uno con su etiqueta encima:

::codigo interfaz/componentes.py 242-268 | La clase Formulario crea etiquetas, campos y listas desplegables
::lineas
242 | El formulario recibe la lista de `campos` y en cuántas columnas acomodarlos.
244-245 | Dos diccionarios: `variables` guarda las `StringVar` y `controles` guarda los widgets, ambos por nombre de campo.
247 | Recorre cada campo: clave interna, texto de la etiqueta, tipo («entrada» o «combo») y opciones.
251-254 | Crea un marquito para el campo y lo ubica en la cuadrícula.
255-256 | Crea la **etiqueta** con el nombre del campo, en negrita.
257 | Crea la variable de Tkinter con el valor inicial (si lo hay).
258-260 | Si el tipo es «combo», crea una **lista desplegable** de solo lectura.
261-262 | Si no, crea un **campo de texto** (`Entry`).
264 | Cuando el usuario presiona una tecla en el campo, se le quita la marca roja de error.
265-266 | Guarda la variable y el control en los diccionarios.
::fin

Así, la vista de clientes describe su formulario en solo seis líneas:

::codigo interfaz/vista_clientes.py 27-33 | Los cuatro campos del formulario de clientes

Para leer todo el formulario de una vez, la clase ofrece el método `valores`:

::codigo interfaz/componentes.py 270-271 | Leer todos los campos en un diccionario
::lineas
271 | Devuelve un diccionario con cada clave y lo escrito en su campo, sin espacios sobrantes. Por ejemplo: `{"identificacion": "1032456789", "nombre": "Laura Gómez", ...}`.
::fin
@fin

::img t_widgets_reservas | En la pantalla de reservas hay listas desplegables (Combobox) para el cliente y el servicio, y campos de texto (Entry) para duración, impuesto y descuento.

## 5.7 ¿Qué es un formulario?

@nivel1
Un formulario es la **hoja completa** que llenas en una oficina: tiene un título, varios espacios para escribir, instrucciones y, al final, un botón o una casilla de «Enviar».
@fin

@nivel2
En Tkinter no existe un widget llamado «formulario». Un formulario es una **combinación** de widgets: un contenedor (`Frame`) que agrupa etiquetas, campos de texto, listas desplegables y botones, organizados con `pack` o `grid`. Programar un formulario es decidir qué campos lleva, cómo se acomodan y qué pasa al pulsar sus botones.
@fin

@nivel3
En Software FJ un formulario completo se arma con tres piezas del archivo `componentes.py`: un `Panel` (el recuadro blanco con título), un `Formulario` (los campos) y una `fila_botones` (los botones). La vista de clientes las combina así:

::codigo interfaz/vista_clientes.py 24-43 | El formulario completo de clientes
::lineas
25 | Crea un panel con el título «Datos del cliente» y el subtítulo «Todos los campos son obligatorios».
26 | Lo ubica en la columna izquierda.
27-33 | Crea los cuatro campos dentro del panel.
35-36 | Agrega la etiqueta que indica el modo: «nuevo registro» o «edición».
38-42 | Crea los botones **Guardar** y **Limpiar**, cada uno conectado a un método.
43 | Si el usuario presiona Enter en el campo Teléfono, también se guarda.
::fin
@fin

::img a_clientes | El formulario real: panel con título (1), modo (2), botón Guardar (3), botón Limpiar (4), búsqueda (5) y tabla (6).

## 5.8 ¿Qué es un botón?

@nivel1
Un botón es como el **timbre** de una casa: lo presionas y algo ocurre (suena adentro). El timbre en sí no sabe abrir la puerta; solo avisa. Quien abre es la persona que escucha el timbre.
@fin

@nivel2
Un **botón** (`Button`) es un widget que ejecuta una función cuando el usuario hace clic. La función se indica con el parámetro `command`. **Importante:** se escribe el nombre de la función **sin paréntesis**, porque no queremos ejecutarla en ese momento, sino entregársela al botón para que la ejecute cuando lo presionen.

```python
def saludar():
    print("¡Hola!")

boton = ttk.Button(ventana, text="Saludar", command=saludar)   # bien: sin ()
# command=saludar()  ← error común: ejecutaría la función de inmediato
boton.pack()
```

A una función que se entrega para que otro la llame más tarde se le llama **función de retorno** o *callback* («llámame después»).
@fin

@nivel3
Todos los botones de los formularios se crean con la función auxiliar `fila_botones`:

::codigo interfaz/componentes.py 296-305 | fila_botones: crea botones y los conecta con sus funciones
::lineas
296 | Recibe el contenedor y una lista de botones, cada uno descrito como (texto, estilo, función).
298 | Crea un marco para alinear los botones en fila.
301-302 | Crea cada botón con su texto, su estilo de color (por ejemplo «Primario» para azul) y `command=comando`: aquí se conecta el botón con su función.
303 | Lo coloca a la izquierda del anterior, con 8 píxeles de separación.
304-305 | Guarda cada botón por su texto y devuelve el marco y el diccionario de botones (sirve para cambiarles el texto o desactivarlos después).
::fin

Los botones de la pantalla de reservas se **activan y desactivan** según el estado de la reserva seleccionada:

::codigo interfaz/vista_reservas.py 210-219 | Botones que se activan solo cuando tienen sentido
::lineas
212 | Toma el estado de la fila seleccionada (o ninguno si no hay selección).
213-217 | Decide qué botones tienen sentido: Confirmar solo para pendientes, Procesar solo para confirmadas, Cancelar para ambas.
218-219 | Activa (`!disabled`) o desactiva (`disabled`) cada botón.
::fin
@fin

::img 33_reserva_seleccionada | Con una reserva pendiente seleccionada, Confirmar y Cancelar están activos y Procesar aparece apagado.

## 5.9 ¿Qué es un menú?

@nivel1
El menú de un restaurante te muestra todas las opciones disponibles para que elijas una. El menú de un programa hace lo mismo: te muestra las secciones o acciones disponibles.
@fin

@nivel2
Tkinter trae un widget llamado `tk.Menu` para crear la clásica barra de menús («Archivo, Edición, Ayuda») en la parte superior de la ventana. Pero un menú también se puede **construir a mano** con otros widgets, por ejemplo una columna de etiquetas que responden al clic. Esta segunda opción da más libertad de diseño.
@fin

@nivel3
**Software FJ no usa `tk.Menu`.** Su menú es un **menú lateral personalizado**: una columna oscura con «botones» que en realidad son etiquetas (`tk.Label`) a las que se les enseñó a responder al clic y a cambiar de color al pasar el ratón. Esa clase se llama `BotonMenu`:

::codigo interfaz/ventana_principal.py 21-42 | BotonMenu: una etiqueta que se comporta como botón
::lineas
21 | `BotonMenu` hereda de `tk.Label`: es una etiqueta.
24-27 | Su constructor crea la etiqueta con el ícono y el texto, el cursor de «mano» y los colores del menú.
29 | `bind("<Button-1>", ...)`: cuando se hace clic con el botón izquierdo del ratón, se ejecuta la función `comando`.
30 | `bind("<Enter>", ...)`: cuando el ratón **entra** sobre la etiqueta, se ilumina.
31 | `bind("<Leave>", ...)`: cuando el ratón **sale**, vuelve a su color normal.
33-35 | `activar` marca la opción como seleccionada.
37-42 | `_pintar` elige los colores: azul si está activa, gris oscuro si el ratón está encima, normal en otro caso.
::fin

Las opciones del menú se crean recorriendo la lista `SECCIONES`:

::codigo interfaz/ventana_principal.py 100-114 | Creación del menú lateral
::lineas
100-101 | Etiqueta gris con el título «MENÚ».
102-105 | Por cada sección se crea un `BotonMenu` cuyo comando es `self.mostrar(clave)`; se guarda en el diccionario `botones_menu`.
107-110 | Sección «HERRAMIENTAS» con Demostración y Acerca de.
112-114 | Al final, pegado abajo, el botón Salir.
::fin

Cuando eliges una opción, el método `mostrar` cambia de pantalla:

::codigo interfaz/ventana_principal.py 151-159 | Cambiar de pantalla
::lineas
152 | Busca la vista correspondiente a la opción elegida.
153-154 | Marca en azul la opción elegida y apaga las demás.
155-156 | Cambia el título y el subtítulo del encabezado.
157 | Pide a la vista que recargue sus datos.
158 | `tkraise()` trae esa vista al frente. Todas las vistas están en la misma celda, una encima de otra; solo se ve la que está arriba.
::fin
@fin

::img t_menu | El menú lateral real: cada opción es un BotonMenu. La opción activa se pinta de azul.

## 5.10 ¿Qué es una tabla?

@nivel1
Una tabla es como una **hoja de cálculo** o la **planilla de asistencia** de un salón: filas para cada persona y columnas para cada dato.
@fin

@nivel2
Tkinter no tiene un widget llamado «tabla», pero `ttk.Treeview` sirve para eso. Su nombre significa «vista de árbol» porque puede mostrar elementos anidados (como las carpetas de un explorador de archivos); con la opción `show="headings"` se muestra solo como tabla con encabezados. Se le agregan filas con `insert`, se borran con `delete` y se sabe qué fila eligió el usuario con `selection()`. Las tablas largas se acompañan de **barras de desplazamiento** (`Scrollbar`).

```python
tabla = ttk.Treeview(ventana, columns=("id", "nombre"), show="headings")
tabla.heading("id", text="Identificación")
tabla.heading("nombre", text="Nombre")
tabla.insert("", "end", values=("1032456789", "Laura Gómez"))
tabla.pack()
```
@fin

@nivel3
Software FJ encapsula el `Treeview` en su propia clase `Tabla`, que agrega barras de desplazamiento, colores por estado y ordenamiento al hacer clic en los encabezados:

::codigo interfaz/componentes.py 170-199 | La clase Tabla construida sobre ttk.Treeview
::lineas
170 | La tabla recibe la lista de columnas, el alto y, opcionalmente, qué hacer al seleccionar una fila y al hacer doble clic.
173-174 | Crea el `Treeview` en modo tabla, permitiendo seleccionar una sola fila a la vez.
175-178 | Configura cada encabezado; al hacer clic en él se ordena la tabla por esa columna.
179-184 | Crea las barras de desplazamiento vertical y horizontal y las conecta con la tabla.
188-194 | Define colores de fondo para cada estado (pendiente, confirmada, procesada, cancelada, error...).
196-197 | Si se indicó qué hacer al seleccionar, se conecta al evento `<<TreeviewSelect>>`.
198-199 | Si se indicó qué hacer al hacer doble clic, se conecta al evento `<Double-1>`.
::fin

La vista de clientes crea su tabla indicando las columnas y qué hacer al seleccionar una fila:

::codigo interfaz/vista_clientes.py 58-65 | La tabla de clientes
@fin

::img 42_reservas_tabla | Tabla real de reservas: cada fila se colorea según el estado de la reserva.

## 5.11 ¿Qué es una ventana emergente?

@nivel1
Una ventana emergente es como cuando alguien **interrumpe** tu trabajo con una nota: «¿Seguro que quieres botar estos papeles?». Mientras no respondas, no sigues con lo que hacías.
@fin

@nivel2
Una **ventana emergente** (o cuadro de diálogo) es una ventana pequeña que aparece encima de la principal para informar algo o pedir una respuesta. Tkinter ofrece tres herramientas:

| Herramienta | Para qué sirve | Ejemplos |
|---|---|---|
| `messagebox` | Mensajes y preguntas listas para usar. | `showinfo` (información), `showwarning` (advertencia), `showerror` (error), `askyesno` (pregunta Sí/No, devuelve `True` o `False`). |
| `simpledialog` | Pedir un dato sencillo. | `askstring` pide un texto; devuelve lo escrito o `None` si se cancela. |
| `tk.Toplevel` | Crear una ventana adicional completamente personalizada. | Ventana con su propio título, tamaño y contenido. |

Las ventanas de `messagebox` y `simpledialog` son **modales**: mientras están abiertas, el programa espera la respuesta antes de continuar con la siguiente línea de código.
@fin

@nivel3
Software FJ usa las tres. Para salir pide confirmación con `askyesno`:

::codigo interfaz/ventana_principal.py 207-211 | Pregunta Sí/No antes de cerrar
::lineas
208-209 | Muestra la pregunta. Si el usuario responde «Sí», `askyesno` devuelve `True` y se entra al bloque.
210 | Se anota en el registro que el usuario cerró la aplicación.
211 | `destroy()` cierra la ventana y termina el programa.
::fin

Para cancelar una reserva usa dos ventanas seguidas: una pregunta y luego una solicitud de texto:

::codigo interfaz/vista_reservas.py 198-208 | askyesno y simpledialog.askstring al cancelar
::lineas
199-201 | Si no hay una reserva seleccionada, no hace nada.
202-205 | Pregunta «¿Seguro que desea cancelar...?». Si responde «No», termina.
206 | `simpledialog.askstring` abre una ventanita para escribir el motivo (es opcional).
207-208 | Llama al gestor para cancelar; si el motivo quedó vacío, usa «Cancelada por el usuario».
::fin

Y para mostrar el archivo de registro crea una ventana nueva con `Toplevel`:

::codigo interfaz/dashboard.py 146-152 | Una ventana adicional con Toplevel
::lineas
148 | Crea una ventana nueva que depende de la principal.
149-150 | Le pone título y tamaño: 980 × 560 píxeles.
151 | `transient` la mantiene siempre encima de la ventana principal.
152 | Color de fondo.
::fin
@fin

::img 39_cancelar_pregunta_dlg | Ventana emergente askyesno real, con ícono de advertencia.

::img 40_motivo_dlg | Ventana emergente simpledialog.askstring real, para escribir el motivo de la cancelación.

## 5.12 ¿Qué son los eventos?

@nivel1
Piensa en un **portero** de edificio. Pasa el día esperando. Cuando suena el citófono, contesta; cuando llega un paquete, lo recibe; cuando alguien toca la puerta, la abre. No hace nada por iniciativa propia: **reacciona** a lo que pasa. Cada cosa que pasa es un **evento**, y el portero tiene una respuesta preparada para cada uno.
@fin

@nivel2
Un **evento** es cualquier cosa que ocurre en la interfaz: un clic, una tecla presionada, el ratón que entra o sale de un widget, una fila seleccionada en una tabla, el paso del tiempo. Los programas gráficos funcionan **esperando eventos y reaccionando a ellos**. A esto se le llama **programación dirigida por eventos**.

El método `mainloop()` es el «portero»: un ciclo que se repite sin parar mientras la ventana está abierta, preguntando «¿pasó algo?». Cuando ocurre un evento, ejecuta la función que tenga asignada y vuelve a esperar.

Tkinter ofrece varias formas de asignar una función a un evento:

| Mecanismo | Para qué evento | Ejemplo en Software FJ |
|---|---|---|
| `command=funcion` | Clic en un botón. | `fila_botones` (componentes.py, línea 302). |
| `widget.bind("<Evento>", funcion)` | Cualquier evento de teclado o ratón. | `<Button-1>` en `BotonMenu`, `<Return>` en el campo Teléfono, `<Double-1>` en la tabla. |
| Eventos virtuales `<<...>>` | Eventos generados por ciertos widgets. | `<<TreeviewSelect>>` (fila elegida), `<<ComboboxSelected>>` (opción elegida). |
| `widget.after(ms, funcion)` | Que pase un tiempo. | El reloj (cada 1000 ms) y la cotización automática (250 ms). |
| `variable.trace_add("write", funcion)` | Que cambie una variable de Tkinter. | Recalcular el costo cuando cambia la duración. |
| `protocol("WM_DELETE_WINDOW", funcion)` | Que el usuario cierre la ventana con la X. | `self.protocol("WM_DELETE_WINDOW", self.salir)`. |

Cuando se usa `bind`, Tkinter le entrega a la función un objeto con información del evento (por ejemplo, qué tecla se presionó). Por eso en el proyecto verás funciones escritas como `lambda _e: self.guardar()`: la `lambda` es una función pequeña sin nombre que recibe ese dato (`_e`), lo ignora (el guion bajo indica «no lo uso») y llama al método deseado.
@fin

@nivel3
El ejemplo más interesante del proyecto es el **cálculo automático del costo** en la pantalla de reservas. Cada vez que el usuario cambia el servicio, la duración, el impuesto o el descuento, el resumen se actualiza solo. Se combinan dos mecanismos: `trace_add` y `after`.

::codigo interfaz/vista_reservas.py 43-44 | trace_add: avisar cuando cambia un campo
::lineas
43 | Recorre los cuatro campos que afectan el precio.
44 | A la variable de cada campo le dice: «cada vez que te escriban (`"write"`), llama a `_programar_cotizacion`».
::fin

::codigo interfaz/vista_reservas.py 116-120 | after: esperar un momento antes de calcular
::lineas
117 | La documentación lo explica: espera 250 milisegundos después de la última tecla, para no recalcular con cada letra.
118-119 | Si ya había un cálculo programado, lo cancela (`after_cancel`).
120 | Programa un cálculo nuevo para dentro de 250 ms y guarda su identificador.
::fin

Así, si escribes «12» en la duración, no se calcula con «1» y luego con «12»: se espera a que termines y se calcula una sola vez.
@fin

::img 28_reserva_cotizacion | El resumen del costo se actualiza automáticamente gracias a trace_add y after.

::img d_evento | Camino de un evento: clic → Tkinter → método de la vista → ejecutar → gestor → resultado en pantalla.

## 5.13 Cómo se conectan los botones con las funciones: el recorrido de un clic

Ahora vamos a juntar todo lo aprendido siguiendo, paso a paso, qué pasa cuando el usuario llena el formulario de clientes y hace clic en **Guardar**.

@nivel1
Es como entregar un formulario en una ventanilla. El funcionario (la pantalla) recibe la hoja, la pasa a la oficina de revisión (el gestor), que verifica los datos con el reglamento (la clase `Cliente`). Si todo está bien, archiva el formulario y le dice al funcionario «listo»; si hay un error, devuelve la hoja con la casilla equivocada marcada en rojo.
@fin

@nivel2
En una aplicación bien organizada, el botón no hace el trabajo: solo **delega**. La pantalla recoge los datos, llama a la capa que contiene las reglas y luego muestra el resultado. Si algo falla, la pantalla captura el error y lo muestra en una ventana emergente, sin cerrarse.
@fin

@nivel3
**Paso 1. El clic llama al método `guardar`.** El botón fue creado con `command=self.guardar` (vista_clientes.py, línea 39). Cuando el usuario hace clic, `mainloop` detecta el evento y ejecuta:

::codigo interfaz/vista_clientes.py 70-79 | El método guardar de la vista de clientes
::lineas
71 | Lee todos los campos del formulario en un diccionario.
72-74 | Si se está editando un cliente existente, pide al gestor que lo **actualice**.
75-77 | Si es un cliente nuevo, pide al gestor que lo **registre**. Le entrega los datos (`**datos` reparte el diccionario como argumentos con nombre), el formulario (para marcar errores) y el mensaje de éxito.
78-79 | Si todo salió bien, limpia el formulario.
::fin

**Paso 2. `ejecutar` llama al gestor de forma segura.** El método `ejecutar` está en `VistaBase`, la clase madre de todas las vistas, para que todas manejen los errores igual:

::codigo interfaz/componentes.py 342-370 | VistaBase.ejecutar: el puente seguro entre la interfaz y los gestores
::lineas
343 | **Aquí se llama al gestor** (en este ejemplo, `GestorClientes.registrar`).
344-352 | Si el gestor rechazó un dato, se busca el campo correspondiente, se marca en rojo, se muestra la ventana «Datos no válidos» y se escribe el aviso en la barra de estado.
353-355 | Si fue otro error del negocio (por ejemplo, cliente duplicado), se muestra «Operación no realizada».
356-361 | Si fue un error inesperado, se registra en el log y se muestra «Error inesperado»; la aplicación sigue abierta.
362-366 | Si todo salió bien (`else`), se muestra la ventana «Operación exitosa» y el mensaje verde en la barra de estado.
367-368 | Se piden a todas las vistas que se refresquen (por ejemplo, para que el panel principal sume un cliente).
369 | Se devuelve el objeto creado.
::fin

**Paso 3. El gestor crea el objeto y la clase `Cliente` valida.** Lo viste en el capítulo 3: `GestorClientes.registrar` crea `Cliente(...)` y el constructor valida cada dato con sus *setters* (capítulo 4).

**Paso 4. La pantalla muestra el resultado.** Si los datos eran válidos aparece la ventana de éxito y el cliente se ve en la tabla; si no, aparece la advertencia y el campo queda en rojo.
@fin

| Paso | Qué ocurre | Archivo | Mecanismo de Tkinter |
|---|---|---|---|
| 1 | El usuario hace clic en Guardar. | `interfaz/vista_clientes.py` | `command=self.guardar` |
| 2 | La vista llama al gestor de forma segura. | `interfaz/componentes.py` | — (Python puro: `try/except`) |
| 3 | Se crea y valida el objeto `Cliente`. | `gestores/gestor_clientes.py`, `modelos/cliente.py` | — |
| 4a | Éxito: mensaje y tabla actualizada. | `interfaz/componentes.py` | `messagebox.showinfo`, `Treeview.insert` |
| 4b | Error: mensaje y campo en rojo. | `interfaz/componentes.py` | `messagebox.showwarning`, estilo `Invalido.TEntry` |

::img 04_cliente_registrado | Resultado del paso 4a: la ventana «Operación exitosa» sobre la pantalla de clientes.

::img 05_error_correo | Resultado del paso 4b: la ventana «Datos no válidos» cuando el correo está mal escrito.

@ejercicio: Sigue el rastro
Siguiendo el mismo método de esta sección, describe qué pasa cuando el usuario selecciona una reserva pendiente y pulsa **Confirmar**. Busca en `interfaz/vista_reservas.py` el método `confirmar` y responde: ¿qué ventana emergente aparece primero?, ¿qué método del gestor se llama?, ¿qué mensaje se muestra si todo sale bien?
@fin

@ejercicio: Tu primera ventana
Escribe un programa didáctico con Tkinter que tenga una etiqueta «Nombre del cliente», un campo de texto y un botón «Saludar». Al pulsar el botón, debe aparecer un `messagebox.showinfo` que diga «Hola, (nombre escrito)». Usa una `StringVar` y `command`.
@fin

@ejercicio: Eventos del teclado
En `interfaz/vista_clientes.py` hay dos líneas que usan `bind("<Return>", ...)`. Encuéntralas (líneas 43 y 53) y explica qué hace cada una en la pantalla real.
@fin

@resumen
- Una **interfaz gráfica** permite usar el programa con ventanas, botones y formularios; **Tkinter** es la biblioteca incluida en Python para construirla.
- Los elementos gráficos se llaman **widgets**: `Tk` (ventana principal), `Frame` (marco), `Label` (etiqueta), `Entry` (campo de texto), `Combobox` (lista desplegable), `Button` (botón), `Treeview` (tabla), `Toplevel` (ventana adicional).
- Se acomodan con `pack` (apilar) o `grid` (cuadrícula).
- El menú de Software FJ es un **menú lateral personalizado** hecho con la clase `BotonMenu` (etiquetas con `bind`), no con `tk.Menu`.
- Las ventanas emergentes se crean con `messagebox`, `simpledialog` y `Toplevel`.
- Un **evento** es algo que ocurre en la interfaz; `mainloop()` espera eventos y ejecuta la función asignada con `command`, `bind`, `after`, `trace_add` o `protocol`.
- En Software FJ los botones solo **delegan**: llaman a `VistaBase.ejecutar`, que llama al gestor y muestra el resultado o el error sin cerrar la aplicación.
@fin
