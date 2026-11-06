# Explicación del código real
> Abrimos uno por uno los veinte archivos de Software FJ y los leemos juntos, línea por línea.

@objetivos
- Reconocer cada archivo del proyecto, su ubicación y su propósito.
- Leer el código original de Software FJ y entender qué hace cada línea.
- Traducir las palabras técnicas del código a lenguaje cotidiano.
- Explicar cómo se relacionan los archivos entre sí (quién usa a quién).
- Identificar con honestidad las partes del proyecto que están incompletas o que se comportan de forma curiosa.
@fin

## 7.0 Cómo leer este capítulo

Este es el capítulo más largo del libro, y es normal. Aquí no hay código inventado: cada bloque gris con números de línea fue copiado automáticamente del archivo real del proyecto en el momento de construir el libro. Si algún día el código cambia y se vuelve a generar el libro, estos bloques cambiarán con él.

Cada archivo se presenta siempre con la misma estructura, para que sepas dónde buscar:

1. **Ficha**: una tabla con el nombre, la ubicación (la carpeta donde vive), el propósito, lo que contiene y con qué otros archivos se relaciona.
2. **Código original por partes**: el archivo completo, dividido en segmentos. Ninguna línea queda por fuera.
3. **Explicación línea por línea**: debajo de cada segmento, una tabla que dice qué hace cada línea (o cada grupo pequeño de líneas, cuando son muy parecidas, como varias líneas en blanco seguidas).
4. **Palabras difíciles**: un pequeño diccionario con las palabras nuevas del archivo.
5. **Ejemplo de funcionamiento**: una prueba real. Todos los ejemplos de este capítulo se ejecutaron con Python desde la carpeta del proyecto y la salida que ves es la que apareció en pantalla.
6. **Relación con otros archivos**: un párrafo que conecta el archivo con el resto del sistema.

En los archivos más importantes (cliente.py, servicios.py, reserva.py y gestor_reservas.py) encontrarás además un **código comentado**: un fragmento clave del archivo con comentarios en español añadidos por el libro. Esos comentarios se marcan con `# ◀` para que no los confundas con los comentarios originales del equipo. El código en sí no se modifica.

@consejo: Un método para no perderte
No intentes leer este capítulo de un tirón. Lee primero el mapa de archivos, luego elige un archivo, mira su ficha y lee su código con la tabla al lado. Cuando termines un archivo, intenta explicárselo en voz alta a alguien (o a ti mismo) sin mirar el libro. Si puedes hacerlo, ya lo entendiste.
@fin

### El mapa del proyecto

Software FJ tiene veinte archivos de código Python (archivos que terminan en `.py`). Están organizados en una carpeta raíz y tres carpetas llamadas *paquetes*. Un **paquete** es simplemente una carpeta de Python que contiene un archivo especial llamado `__init__.py`; ese archivo le dice a Python «esta carpeta es un grupo de módulos que se pueden importar». Un **módulo** es cualquier archivo `.py`.

| Carpeta | Archivos | Para qué sirve la carpeta |
|---|---|---|
| raíz del proyecto | main.py, excepciones.py, registro.py, simulacion.py | Arranque del programa, errores propios, bitácora y demostración. |
| modelos/ | __init__.py, entidad.py, cliente.py, servicios.py, reserva.py | Las «cosas» del negocio: clientes, servicios y reservas, con sus reglas. |
| gestores/ | __init__.py, gestor_clientes.py, gestor_servicios.py, gestor_reservas.py | Los «administradores» que guardan las listas y coordinan las operaciones. |
| interfaz/ | __init__.py, componentes.py, dashboard.py, ventana_principal.py, vista_clientes.py, vista_servicios.py, vista_reservas.py | Todo lo que se ve en pantalla (Tkinter). |

El siguiente diagrama muestra qué archivo **importa** a cuál. Importar significa «traer herramientas de otro archivo para usarlas aquí», como cuando pides prestada una herramienta al vecino.

::img d_imports | Qué archivo importa a cuál dentro de Software FJ.

Y este otro muestra la idea general de la arquitectura en capas: la interfaz solo habla con los gestores, los gestores hablan con los modelos, y las excepciones y el registro atraviesan todas las capas.

::img d_capas | Arquitectura en capas de Software FJ.

@recuerda
La regla de oro del proyecto es: **la interfaz no toma decisiones de negocio**. La ventana solo recoge lo que el usuario escribe y muestra resultados. Quien decide si un correo es válido o cuánto cuesta una reserva son los modelos y los gestores. Esta separación aparece una y otra vez en este capítulo.
@fin

\salto

## 7.1 main.py — la puerta de entrada

| Dato | Descripción |
|---|---|
| Nombre | main.py |
| Ubicación | Raíz del proyecto (la carpeta principal) |
| Propósito | Es el archivo que se ejecuta para abrir el programa. Decide en qué modo arrancar (ventana normal, ventana con demostración o solo consola). |
| Contiene | Una función: `main()` |
| Usa a | registro.py, interfaz (VentanaPrincipal), simulacion.py (en modo consola) |
| Lo usan | Nadie: es el punto de partida. Lo ejecuta la persona con `python main.py`. |

Piensa en main.py como el portero de un edificio: no hace el trabajo de las oficinas, pero es quien abre la puerta, enciende las luces y te dice a qué piso subir.

::img vscode_main | El archivo main.py abierto en Visual Studio Code.

::codigo main.py 1-13 | main.py: documentación inicial e importaciones
::lineas
1-8 | Un texto entre tres comillas dobles al inicio de un archivo se llama **docstring** (cadena de documentación). Python no lo ejecuta como instrucción: sirve para que las personas sepan qué hace el archivo. Aquí explica las tres formas de usar el programa.
9 | `import sys` trae el módulo `sys` (sistema), que viene con Python. Lo necesitamos para leer lo que el usuario escribió después de `python main.py` y para terminar el programa con un código de salida.
10 | Línea en blanco: solo separa visualmente.
11 | Trae dos funciones del archivo registro.py: `registrar_critico` (anota errores graves) y `registrar_evento` (anota sucesos normales). Así main.py puede escribir en la bitácora `software_fj.log`.
12-13 | Dos líneas en blanco. Por convención, en Python se dejan dos líneas vacías antes de definir una función o clase de nivel superior.
::fin

::codigo main.py 14-20 | main.py: lectura de argumentos y modo consola
::lineas
14 | `def main():` define (crea) una función llamada `main`. Una **función** es un bloque de instrucciones con nombre que se puede ejecutar cuando se necesite. Todo lo que está más a la derecha (con sangría) pertenece a ella.
15 | `sys.argv` es la lista de palabras escritas en la terminal. Si escribes `python main.py --demo`, `sys.argv` vale `["main.py", "--demo"]`. Con `[1:]` se toma desde la segunda palabra en adelante (se descarta el nombre del archivo), y `set(...)` lo convierte en un **conjunto**, una colección sin repetidos donde es muy rápido preguntar «¿está esta palabra?».
16 | `if "--consola" in argumentos:` pregunta si el usuario pidió el modo consola.
17 | `import runpy` trae un módulo de Python que sirve para ejecutar otro módulo como si fuera un programa. Se importa aquí adentro (y no arriba) porque solo se necesita en este caso.
18 | Ejecuta el archivo simulacion.py como programa principal (`run_name="__main__"`), lo que activa su bloque final que imprime las 15 operaciones en la consola.
19 | `return 0` termina la función y devuelve 0. En los sistemas operativos, 0 significa «terminó bien».
20 | Línea en blanco.
::fin

::codigo main.py 21-37 | main.py: arranque de la ventana con manejo de errores
::lineas
21 | `try:` abre un bloque «intenta hacer esto». Si algo falla dentro, Python salta al `except` en lugar de cerrar el programa con un mensaje feo.
22 | Importa la clase `VentanaPrincipal` desde el paquete `interfaz`. Se importa dentro del `try` a propósito: si Tkinter no estuviera instalado, el error se atraparía aquí.
23 | Crea el **objeto** ventana: `VentanaPrincipal()` construye la ventana con su menú y sus cinco pantallas, y la guarda en la variable `app` (abreviatura de *application*, aplicación).
24-25 | Si el usuario escribió `--demo`, se programa la demostración: `app.after(600, ...)` significa «dentro de 600 milisegundos (0,6 segundos) ejecuta `ejecutar_demostracion`». Se espera un poco para que la ventana alcance a dibujarse primero.
26 | `app.mainloop()` arranca el **ciclo principal** de Tkinter: un bucle que se queda esperando clics y teclas hasta que se cierre la ventana. Mientras la ventana está abierta, el programa «vive» en esta línea.
27 | `except Exception as error:` atrapa cualquier error que haya ocurrido en el `try` y lo guarda en la variable `error`. El comentario explica que es un error fatal al iniciar.
28 | Anota el error en la bitácora como CRITICAL, con todos sus detalles.
29 | Imprime un mensaje para la persona. `file=sys.stderr` lo envía al canal de errores de la terminal. La `f` antes de las comillas crea una **f-string**: un texto donde lo que va entre llaves `{error}` se reemplaza por su valor.
30 | Devuelve 1, que significa «terminó con error».
31-32 | `finally:` se ejecuta **siempre**, haya error o no. Aquí deja constancia en el log de que el programa terminó.
33 | Si todo salió bien, devuelve 0.
34-35 | Líneas en blanco.
36 | `if __name__ == "__main__":` es una frase típica de Python. Cada archivo tiene una variable oculta `__name__`; vale `"__main__"` solo cuando ese archivo es el que se ejecutó directamente. Si otro archivo importara main.py, esta condición sería falsa y el programa no arrancaría solo.
37 | Ejecuta `main()` y entrega su resultado (0 o 1) al sistema operativo mediante `sys.exit`.
::fin

### Palabras difíciles de main.py

| Palabra | En lenguaje cotidiano |
|---|---|
| docstring | Nota explicativa al inicio de un archivo, clase o función. |
| argumento de línea de comandos | Palabra extra que escribes después del nombre del programa, como `--demo`. |
| conjunto (set) | Bolsa de elementos sin repetir. |
| mainloop | El «modo espera» de la ventana: escucha clics hasta que la cierres. |
| código de salida | Número que el programa le entrega al sistema al terminar (0 = bien). |
| `__name__ == "__main__"` | «¿Me ejecutaron a mí directamente?» |

@ejemplo: Ejecutar el modo consola
Desde la carpeta del proyecto se ejecutó `python main.py --consola`. Estas son las dos últimas operaciones que aparecieron en pantalla:
```salida
14. [ERROR] Cancelar la reserva ya procesada (operación no permitida)
      -> [FJ-401] No se puede 'cancelar' una reserva en estado 'Procesada'.
15. [ERROR] Reserva para cliente inexistente
      -> [FJ-200] No existe un cliente con identificador '99999999'.
```
No se abrió ninguna ventana: main.py vio la palabra `--consola` (línea 16) y ejecutó simulacion.py (línea 18).
@fin

**Relación con otros archivos.** main.py es el único archivo que no importa nadie. Depende de registro.py para anotar el inicio y el fin, de interfaz/ventana_principal.py (a través de interfaz/__init__.py) para mostrar la ventana, y de simulacion.py para el modo consola. Es corto a propósito: su trabajo es solo «encender» el resto.

\salto

## 7.2 excepciones.py — los errores con nombre propio

| Dato | Descripción |
|---|---|
| Nombre | excepciones.py |
| Ubicación | Raíz del proyecto |
| Propósito | Define los tipos de error propios de Software FJ, organizados en familias, cada uno con un mensaje claro y un código (FJ-101, FJ-200...). |
| Contiene | 10 clases: SoftwareFJError, ValidacionError, DatoInvalidoError, ParametroFaltanteError, EntidadNoEncontradaError, EntidadDuplicadaError, ServicioNoDisponibleError, ReservaError, OperacionNoPermitidaError, CalculoInconsistenteError |
| Usa a | Nadie (solo la clase `Exception` que trae Python) |
| Lo usan | Casi todos: modelos, gestores, interfaz/componentes.py, interfaz/vista_reservas.py y simulacion.py |

En la vida real no es lo mismo decir «algo salió mal» que decir «el correo no tiene @». Este archivo crea **nombres precisos para cada tipo de problema**. Una **excepción** es la forma en que Python avisa que algo no salió como se esperaba; si nadie la «atrapa», el programa se detiene. Aquí se crean excepciones propias, a la medida del negocio.

::img d_excepciones | Árbol familiar de las excepciones de Software FJ.

::codigo excepciones.py 1-17 | excepciones.py: documentación con el árbol de excepciones
::lineas
1-15 | Docstring del archivo. Dibuja con caracteres el árbol de herencia: todas las excepciones descienden de `SoftwareFJError`. Las ramas `├──` y `└──` son solo dibujo, no código.
16-17 | Líneas en blanco antes de la primera clase.
::fin

::codigo excepciones.py 18-29 | La excepción madre: SoftwareFJError
::lineas
18 | `class SoftwareFJError(Exception):` crea una **clase** (un molde) llamada SoftwareFJError. Lo que va entre paréntesis es su clase madre: hereda todo lo que sabe hacer una excepción normal de Python (`Exception`).
19 | Docstring de la clase: «Excepción base de todo el sistema».
20 | Línea en blanco.
21 | `def __init__(self, mensaje, codigo="FJ-000"):` es el **constructor**: el método que se ejecuta al crear un error de este tipo. Recibe el mensaje y un código; si no se da un código, usa `"FJ-000"` (eso es un **valor por defecto**). `self` es «este error en particular».
22 | `super().__init__(mensaje)` llama al constructor de la clase madre (`Exception`) para que Python también conozca el mensaje. `super()` significa «mi clase madre».
23 | Guarda el mensaje dentro del objeto, en el **atributo** `mensaje`. Así la interfaz puede mostrar solo el texto, sin el código.
24 | Guarda el código en el atributo `codigo`.
25 | Línea en blanco.
26 | `def __str__(self):` define cómo se ve el error cuando se convierte en texto (por ejemplo, al imprimirlo o escribirlo en el log). Los métodos con doble guion bajo a cada lado se llaman **métodos especiales** o *dunder*: Python los llama automáticamente en ciertas situaciones.
27 | Devuelve el texto con el formato `[FJ-101] mensaje`.
28-29 | Líneas en blanco.
::fin

::codigo excepciones.py 30-53 | La familia de errores de validación
::lineas
30 | `ValidacionError` hereda de `SoftwareFJError`: es un SoftwareFJError más específico, para datos mal escritos.
31 | Docstring.
33 | Su constructor recibe además `campo`: el nombre del dato que falló (por ejemplo, `"correo"`). Por defecto el código es FJ-100.
34 | Le pasa mensaje y código a la clase madre, que los guarda.
35 | Guarda el campo. La interfaz usa este dato para pintar de rojo justamente esa casilla del formulario.
38 | `DatoInvalidoError` hereda de `ValidacionError`: el dato existe pero tiene un valor no permitido.
41 | Recibe tres cosas: el campo, el valor que llegó y el motivo del rechazo.
42-43 | Arma el mensaje automáticamente: «Valor inválido para 'correo' ('maria.ruiz@'): formato de correo no válido». El `!r` dentro de las llaves muestra el valor «tal cual» (con comillas si es texto), para que se note si había espacios o letras. Fija el código FJ-101.
44 | Guarda el valor rechazado por si alguien lo necesita.
47-51 | `ParametroFaltanteError`: el dato obligatorio está vacío. Solo necesita el nombre del campo y arma el mensaje «El campo 'X' es obligatorio.» con código FJ-102.
32, 36-37, 39-40, 45-46, 48-49, 52-53 | Docstrings y líneas en blanco.
::fin

::codigo excepciones.py 54-81 | Errores de búsqueda, duplicados, disponibilidad, reservas y cálculos
::lineas
54-56 | `EntidadNoEncontradaError`: se busca algo que no existe. Recibe el tipo («un cliente») y el identificador buscado. Código FJ-200.
59-61 | `EntidadDuplicadaError`: se intenta registrar algo que ya existe. Código FJ-201.
64-66 | `ServicioNoDisponibleError`: el servicio está deshabilitado o sin cupo. El motivo tiene un texto por defecto. Código FJ-300.
69-71 | `ReservaError`: problema general con una reserva. Código FJ-400, pero permite cambiarlo.
74-76 | `OperacionNoPermitidaError` hereda de `ReservaError`: la acción no corresponde al estado de la reserva (por ejemplo, cancelar una reserva ya facturada). Código FJ-401.
79-81 | `CalculoInconsistenteError`: un porcentaje inválido o un total que no cuadra. Código FJ-500.
57-58, 62-63, 67-68, 72-73, 77-78 | Líneas en blanco entre clases.
::fin

### Palabras difíciles de excepciones.py

| Palabra | En lenguaje cotidiano |
|---|---|
| excepción | Alarma que suena cuando algo sale mal. |
| herencia | Una clase hija recibe todo lo de su madre y puede añadir cosas. |
| constructor (`__init__`) | Las instrucciones de «armado» de un objeto nuevo. |
| `super()` | «Pídeselo a mi clase madre». |
| atributo | Dato que se guarda dentro de un objeto. |
| `__str__` | Cómo se presenta el objeto cuando se convierte en texto. |
| valor por defecto | El valor que se usa si no te dan otro. |

@ejemplo: Crear y leer un error propio
Se ejecutó este fragmento en Python desde la carpeta del proyecto:
```python
from excepciones import *
e = DatoInvalidoError("correo", "maria.ruiz@", "formato de correo no válido")
print(e)
print(e.mensaje)
print(e.codigo, e.campo)
print(isinstance(e, ValidacionError), isinstance(e, SoftwareFJError))
```
```salida
[FJ-101] Valor inválido para 'correo' ('maria.ruiz@'): formato de correo no válido
Valor inválido para 'correo' ('maria.ruiz@'): formato de correo no válido
FJ-101 correo
True True
```
La última línea demuestra la herencia: un `DatoInvalidoError` *también es* un `ValidacionError` y *también es* un `SoftwareFJError`. Por eso, quien atrape `SoftwareFJError` atrapa toda la familia.
@fin

**Relación con otros archivos.** Este archivo no importa nada del proyecto, por eso cualquier otro puede usarlo sin crear enredos. Los modelos *lanzan* (con `raise`) estas excepciones cuando una regla no se cumple; los gestores las registran en el log y las vuelven a lanzar; la interfaz (componentes.py, en el método `ejecutar`) las atrapa y las muestra en una ventana de mensaje. El capítulo 9 profundiza en este viaje del error.

\salto
