# Primeros pasos en la programación
> Antes de leer una sola línea de código, entendamos qué es un computador, qué es un programa y qué hace una persona cuando «programa».

@objetivos
- Explicar con tus propias palabras qué es un computador y qué es un programa.
- Entender qué significa programar y por qué se usa un lenguaje como Python.
- Reconocer un archivo `.py` y saber para qué sirve Visual Studio Code.
- Comprender qué es un intérprete y qué ocurre cuando se «ejecuta» un programa.
- Distinguir los tipos de errores más comunes y no asustarte cuando aparezcan.
@fin

Bienvenido. Si nunca has escrito una línea de código, este capítulo es para ti. No vamos a correr: cada idea se explica primero con algo de la vida diaria, luego con su significado en informática y, por último, con un ejemplo tomado de Software FJ, el proyecto que vas a aprender a leer y a defender.

@nota: Cómo está organizado cada concepto
A lo largo del libro verás tres recuadros que se repiten. El **Nivel 1** explica la idea con una situación cotidiana. El **Nivel 2** explica qué significa dentro de la informática. El **Nivel 3** te muestra dónde aparece esa idea en Software FJ. Si un nivel te resulta difícil, vuelve al anterior: siempre son la misma idea vista desde tres ángulos.
@fin

## 1.1 ¿Qué es un computador?

@nivel1
Piensa en una cocina muy ordenada. Hay una persona que cocina (hace el trabajo), una mesa donde pone los ingredientes mientras cocina, una despensa donde guarda todo lo que no está usando y una ventanilla por donde recibe los pedidos y entrega los platos. La persona no inventa recetas: sigue al pie de la letra las que le entregan.
@fin

@nivel2
Un **computador** es una máquina que recibe datos, los procesa siguiendo instrucciones y entrega resultados. Sus partes principales se parecen a la cocina:

- El **procesador** es quien «cocina»: ejecuta las instrucciones, una tras otra, a enorme velocidad.
- La **memoria RAM** es la mesa de trabajo: guarda los datos mientras se usan. Es rápida, pero se borra cuando se apaga el equipo o se cierra el programa.
- El **disco** (almacenamiento) es la despensa: guarda archivos de forma permanente.
- Los **dispositivos de entrada y salida** son la ventanilla: teclado y ratón para recibir órdenes; pantalla para mostrar resultados.
@fin

@nivel3
Software FJ vive justamente entre la mesa y la despensa. Los clientes, servicios y reservas que registras se guardan en la **memoria RAM**: por eso, cuando cierras el programa, se pierden (el propio programa te lo advierte al salir). En cambio, el registro de actividad se escribe en un archivo del **disco** llamado `software_fj.log`, que permanece aunque apagues el computador.
@fin

::img 52_salir_dlg | Al salir, Software FJ recuerda que los datos están en memoria (RAM) y se perderán.

## 1.2 ¿Qué es un programa?

@nivel1
Una receta de cocina es una lista de pasos escrita para que alguien los siga en orden: «calienta el aceite, agrega la cebolla, espera dos minutos». Si la receta está bien escrita, cualquier cocinero obtiene el mismo plato.
@fin

@nivel2
Un **programa** es un conjunto de instrucciones escritas para que un computador las siga. Casi todos los programas hacen tres cosas: reciben información (**entrada**), la transforman (**proceso**) y muestran o guardan un resultado (**salida**).
@fin

::img d_programa | Todo programa sigue el esquema entrada → proceso → salida.

@nivel3
En Software FJ, la **entrada** son los datos que escribes en el formulario (por ejemplo, la identificación y el nombre de un cliente). El **proceso** es la revisión de esos datos y el cálculo del precio de una reserva. La **salida** es lo que ves: un mensaje de «Operación exitosa», una fila nueva en la tabla o un total de $ 160.650.
@fin

::img 04_cliente_registrado | Salida de un proceso: el cliente quedó registrado y aparece el mensaje de confirmación.

## 1.3 ¿Qué es programar?

@nivel1
Imagina que tienes que explicarle a un turista, por teléfono, cómo llegar a tu casa. No puedes decir «ya sabes, por donde siempre». Tienes que ser preciso: «camina dos cuadras, gira a la derecha en la panadería, la casa azul es la tercera». Si te saltas un paso, el turista se pierde.
@fin

@nivel2
**Programar** es escribir esas instrucciones precisas para un computador. El computador es muy rápido pero no adivina nada: hace exactamente lo que dice el programa, ni más ni menos. Programar implica tres tareas: **entender el problema**, **diseñar los pasos** para resolverlo y **escribirlos en un lenguaje** que el computador pueda seguir. A ese texto escrito se le llama **código fuente** o simplemente **código**.
@fin

@nivel3
El equipo que construyó Software FJ tuvo que traducir reglas de negocio a instrucciones exactas. Por ejemplo, la regla «la identificación debe tener entre 5 y 12 dígitos» quedó escrita así en el código real:

::codigo modelos/cliente.py 30-31 | Una regla del negocio convertida en instrucción.

No te preocupes si todavía no entiendes cada palabra. Fíjate en que la regla se reconoce: «si no son solo dígitos, o la longitud no está entre 5 y 12, avisa de un error». Eso es programar: convertir una regla en pasos exactos.
@fin

## 1.4 ¿Qué es Python?

@nivel1
Las personas usamos idiomas para entendernos: español, inglés, portugués. Cada idioma tiene sus palabras y su gramática. Para hablar con un computador también hay «idiomas» especiales.
@fin

@nivel2
Un **lenguaje de programación** es un idioma con palabras y reglas muy estrictas que sirve para escribir programas. **Python** es uno de esos lenguajes. Fue creado por Guido van Rossum y publicado en 1991. Es famoso porque se lee casi como inglés sencillo, usa pocas palabras especiales y obliga a escribir el código ordenado, con sangrías (espacios al inicio de la línea) que muestran qué instrucciones van dentro de otras.
@fin

```python
# Esto es Python: una línea que empieza con # es un comentario para personas
print("Hola, Software FJ")
```

```salida
Hola, Software FJ
```

@nivel3
Todo Software FJ está escrito en Python. Su archivo de documentación indica que necesita **Python 3.8 o superior** y que no usa ninguna base de datos ni librería externa: solo herramientas que vienen incluidas con Python, como **Tkinter** (para las ventanas) y **logging** (para el registro de eventos).
@fin

## 1.5 ¿Para qué sirve Python?

Python se usa en muchísimos campos. Algunos ejemplos:

| Campo | Ejemplo de uso |
|---|---|
| Aplicaciones de escritorio | Programas con ventanas y botones, como Software FJ |
| Páginas y servicios web | Tiendas en línea, sistemas de inscripción |
| Análisis de datos | Hojas de cálculo gigantes, estadísticas, gráficos |
| Inteligencia artificial | Programas que reconocen imágenes o texto |
| Automatización | Renombrar mil archivos o enviar reportes automáticamente |
| Educación | Es uno de los lenguajes más usados para aprender a programar |

@nivel1
Python es como una navaja suiza: una sola herramienta que sirve para muchas tareas distintas.
@fin

@nivel2
Esa versatilidad se debe a que Python trae una gran **biblioteca estándar** (un conjunto de herramientas ya hechas que vienen con el lenguaje) y a que existen miles de paquetes adicionales escritos por otras personas.
@fin

@nivel3
Software FJ aprovecha la biblioteca estándar: usa `tkinter` para dibujar la ventana, `logging` para escribir el archivo de registro, `re` para revisar el formato del correo electrónico y `datetime` para anotar fechas y horas. Todo eso venía incluido con Python; no hubo que instalar nada más.
@fin

::codigo registro.py 7-10 | Herramientas de la biblioteca estándar que usa registro.py.

## 1.6 ¿Qué es un archivo .py?

@nivel1
Cuando guardas una foto, su nombre termina en `.jpg`; un documento de Word termina en `.docx`. Esa terminación, llamada **extensión**, le dice al computador qué tipo de archivo es y con qué programa abrirlo.
@fin

@nivel2
Un archivo `.py` es un archivo de texto que contiene código Python. Por dentro no tiene nada mágico: lo puedes abrir incluso con el Bloc de notas. A cada archivo `.py` también se le llama **módulo**, porque es una pieza que se puede unir con otras.
@fin

@nivel3
Software FJ está dividido en varios archivos `.py`, cada uno con una responsabilidad. La siguiente tabla muestra los principales:

| Archivo | Qué contiene |
|---|---|
| `main.py` | El punto de inicio: es el archivo que se ejecuta para abrir el programa. |
| `excepciones.py` | Los tipos de error propios del sistema. |
| `registro.py` | Lo necesario para escribir el archivo `software_fj.log`. |
| `simulacion.py` | Las 15 operaciones de demostración. |
| `modelos/cliente.py`, `modelos/servicios.py`, `modelos/reserva.py`, `modelos/entidad.py` | Las reglas del negocio: qué es un cliente, un servicio, una reserva. |
| `gestores/*.py` | Los encargados de guardar y organizar clientes, servicios y reservas. |
| `interfaz/*.py` | Las pantallas: ventana principal, clientes, servicios, reservas, eventos. |
@fin

@consejo
Una carpeta que contiene archivos `.py` y un archivo especial llamado `__init__.py` se llama **paquete**. En Software FJ, `modelos`, `gestores` e `interfaz` son paquetes: cajas que agrupan módulos relacionados.
@fin

## 1.7 ¿Qué es Visual Studio Code?

@nivel1
Para escribir una carta puedes usar una hoja en blanco, pero un buen procesador de texto te marca las faltas de ortografía, te deja buscar palabras y te muestra el documento ordenado. Para escribir código pasa lo mismo.
@fin

@nivel2
**Visual Studio Code** (también llamado **VS Code**) es un **editor de código**: un programa gratuito, creado por Microsoft, para escribir y revisar código. Colorea las palabras según su función (a eso se le llama **resaltado de sintaxis**), numera las líneas, muestra los archivos del proyecto en una columna lateral, avisa de errores mientras escribes y trae una **terminal** integrada (una ventana donde se escriben órdenes de texto) para ejecutar el programa sin salir del editor.
@fin

@nivel3
Así se ve un archivo real de Software FJ abierto en Visual Studio Code. Observa los números de línea a la izquierda y los colores: las palabras clave de Python, los textos entre comillas y los comentarios tienen colores distintos.
@fin

::img vscode_cliente | El archivo modelos/cliente.py abierto en Visual Studio Code.

@importante
VS Code no es Python. VS Code es solo el lugar donde escribes; quien entiende y ejecuta el código es Python, que debe estar instalado aparte. Puedes escribir Python con cualquier editor, incluso el Bloc de notas, aunque es mucho más incómodo.
@fin

## 1.8 ¿Qué es un intérprete?

@nivel1
Imagina una conferencia con un invitado que solo habla japonés. A su lado hay un intérprete que escucha cada frase y la traduce al español en el momento, frase por frase, para que el público entienda.
@fin

@nivel2
El computador, en el fondo, solo entiende instrucciones muy simples en un lenguaje de máquina. Python es un lenguaje pensado para personas. El **intérprete de Python** es el programa que lee tu archivo `.py` y lo va traduciendo y ejecutando instrucción por instrucción. Cuando instalas Python en tu computador, lo que instalas principalmente es ese intérprete; en Windows se llama `python.exe`.
@fin

::img d_interprete | El intérprete traduce el archivo .py a acciones que el computador puede realizar.

@nivel3
Cuando alguien escribe `python main.py`, le está pidiendo al intérprete: «lee el archivo `main.py` y haz lo que dice». El intérprete empieza por la primera línea y, al llegar al final del archivo, encuentra esta orden:

::codigo main.py 36-37 | Las últimas líneas de main.py: aquí arranca realmente el programa.

En palabras sencillas: «si este archivo es el que se está ejecutando directamente, llama a la función `main` y termina con el resultado que ella devuelva». Más adelante entenderás cada pieza.
@fin

## 1.9 ¿Qué significa ejecutar un programa?

@nivel1
Tener una receta guardada en un cuaderno no produce comida. Hay que **cocinarla**: seguir los pasos, uno por uno, hasta que el plato está listo.
@fin

@nivel2
**Ejecutar** (también se dice «correr», del inglés *run*) es poner en marcha un programa: el intérprete lee el código y realiza sus instrucciones. Mientras el programa se ejecuta, ocupa memoria y procesador; cuando termina o lo cierras, esa memoria se libera. Se puede ejecutar desde la **terminal** escribiendo una orden, o desde VS Code con un botón.
@fin

```consola
python main.py
```

@nivel3
Software FJ se puede ejecutar de tres maneras, según lo que se escriba después de `main.py`:

| Orden | Qué sucede |
|---|---|
| `python main.py` | Abre la ventana del programa. |
| `python main.py --demo` | Abre la ventana y lanza la demostración de 15 operaciones. |
| `python main.py --consola` | No abre ventana: ejecuta la demostración y muestra el resultado como texto. |

El archivo `main.py` revisa qué se escribió y decide qué hacer:

::codigo main.py 14-19 | main.py revisa las palabras escritas al ejecutarlo.

El resultado de ejecutar `python main.py` es la ventana principal:
@fin

::img 01_panel_vacio | Resultado de ejecutar python main.py: la ventana principal de Software FJ.

## 1.10 ¿Qué son los errores de programación?

@nivel1
Cuando escribes un mensaje de texto puedes equivocarte de varias formas: una palabra mal escrita («ola» en vez de «hola»), una instrucción imposible («compra leche en la tienda cerrada») o una instrucción bien escrita pero que no era la que querías («compra 100 litros» cuando querías uno). Los programas tienen los mismos tres tipos de tropiezos.
@fin

@nivel2
En programación se distinguen tres grandes familias de errores:

| Tipo | Qué es | Ejemplo |
|---|---|---|
| **Error de sintaxis** | El código está mal escrito: rompe la gramática de Python. El programa ni siquiera arranca. | Olvidar cerrar un paréntesis: `print("Hola"` |
| **Error de ejecución** | El código está bien escrito, pero algo imposible ocurre mientras corre. En Python se llama **excepción**. | Dividir entre cero, o convertir la palabra «abc» en número. |
| **Error lógico** | El programa funciona sin quejarse, pero da un resultado equivocado porque la idea estaba mal. | Sumar el impuesto antes de restar el descuento cuando la regla decía lo contrario. |
@fin

```python
precio = int("abc")
```

```salida
ValueError: invalid literal for int() with base 10: 'abc'
```

El mensaje parece intimidante, pero se lee así: «Error de valor: el texto 'abc' no es un número entero válido». Python te dice **qué tipo de error** ocurrió (`ValueError`) y **por qué**.

@nivel3
Software FJ está construido para que los errores de ejecución no cierren la aplicación. Cuando escribes un dato imposible, por ejemplo un correo sin dominio, el programa «atrapa» el error, te muestra un mensaje claro, marca el campo en rojo y deja una anotación en el registro. En el capítulo 9 verás en detalle cómo lo hace.
@fin

::img 06_campo_invalido | Un error de ejecución controlado: el correo «maria.ruiz@» no es válido y el campo queda marcado en rojo.

@recuerda
Equivocarse es parte normal de programar. Los programadores con experiencia también cometen errores a diario; la diferencia es que aprendieron a **leer los mensajes de error** en lugar de asustarse con ellos.
@fin

@ejercicio: Clasifica el error
Indica si cada situación es un error de sintaxis, de ejecución o lógico:
1. El programa no arranca porque falta una comilla al final de un texto.
2. El programa calcula el total de una reserva sumando dos veces el impuesto.
3. El usuario escribe «diez» en el campo de la tarifa y el programa intenta convertirlo en número.

Respuestas: 1. Sintaxis. 2. Lógico. 3. Ejecución (Software FJ lo controla y muestra «debe ser numérico»).
@fin

@ejercicio: Entrada, proceso y salida
Piensa en la acción «crear una reserva» en Software FJ. Escribe en una frase cuál es la entrada, cuál es el proceso y cuál es la salida. Pista: mira la captura `28_reserva_cotizacion` en el capítulo 6.
@fin

@resumen
- Un **computador** procesa datos siguiendo instrucciones; guarda lo temporal en la **memoria RAM** y lo permanente en el **disco**.
- Un **programa** es una lista de instrucciones con el esquema entrada → proceso → salida.
- **Programar** es convertir reglas e ideas en instrucciones exactas escritas en un lenguaje.
- **Python** es un lenguaje fácil de leer, con muchas herramientas incluidas; Software FJ está escrito completamente en Python.
- Un **archivo .py** contiene código Python; varios archivos agrupados forman un **paquete**.
- **Visual Studio Code** es el editor donde se escribe el código; el **intérprete** de Python es quien lo lee y lo ejecuta.
- **Ejecutar** es poner en marcha el programa, por ejemplo con `python main.py`.
- Hay errores de **sintaxis**, de **ejecución** (excepciones) y **lógicos**; Software FJ controla los de ejecución para no cerrarse.
@fin
