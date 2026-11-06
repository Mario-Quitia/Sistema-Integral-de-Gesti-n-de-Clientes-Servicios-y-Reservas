# Aprendiendo a leer Python
> Diecisiete piezas básicas del lenguaje, explicadas una por una, para que puedas reconocerlas en el código real de Software FJ.

@objetivos
- Reconocer y explicar las instrucciones fundamentales de Python: `print`, `input`, variables, tipos de datos, listas, diccionarios, operadores, condicionales, ciclos, funciones e `import`.
- Leer un fragmento corto de código y decir qué hace, línea por línea.
- Encontrar cada una de esas piezas dentro de los archivos reales de Software FJ.
- Practicar con ejercicios sencillos de lectura e interpretación de código.
@fin

En el capítulo anterior aprendiste que programar es escribir instrucciones en un idioma especial. Ahora vamos a aprender el «vocabulario» básico de ese idioma. No necesitas memorizarlo todo: el objetivo es que, cuando veas una línea de Python, puedas decir «ah, esto guarda un dato» o «esto repite algo varias veces».

Cada pieza se presenta siempre con el mismo orden: **qué significa**, **para qué sirve**, **cómo se usa**, un **ejemplo sencillo** y un **ejemplo aplicado a Software FJ** tomado del código real del proyecto.

@consejo: Cómo leer los ejemplos
Los recuadros oscuros con código de colores son código Python. Cuando debajo aparece un recuadro de **salida**, es lo que mostraría la pantalla al ejecutarlo. Los fragmentos con números de línea y el nombre de un archivo son **copias exactas** del código de Software FJ: los números te permiten encontrar esas mismas líneas en Visual Studio Code.
@fin

## 2.1 print(): mostrar información

@nivel1
Cuando un mesero termina de tomar tu pedido, lo repite en voz alta para que lo escuches: «Entonces son dos jugos y una arepa». Está **mostrando** información.
@fin

@nivel2
**Qué significa.** `print` significa «imprimir» en inglés. Es una **función** (una instrucción con nombre que realiza una tarea; la verás con detalle en la sección 2.13) que muestra en la pantalla lo que pongas dentro de sus paréntesis.

**Para qué sirve.** Para mostrar mensajes, resultados de cálculos o información que ayude a revisar si el programa funciona bien.

**Cómo se usa.** Se escribe `print(` seguido de lo que quieres mostrar y se cierra con `)`. Si es un texto, va entre comillas. Puedes poner varias cosas separadas por comas y Python las muestra separadas por un espacio.
@fin

```python
print("Bienvenido a Software FJ")
print("Clientes registrados:", 5)
print(2 + 3)
```

```salida
Bienvenido a Software FJ
Clientes registrados: 5
5
```

@nivel3
Software FJ casi no usa `print`, porque se comunica contigo mediante ventanas y mensajes gráficos. Sin embargo, aparece en dos lugares importantes. El primero es en `main.py`: si la ventana no puede abrirse, el programa escribe un aviso en la terminal.
@fin

::codigo main.py 29 | main.py usa print para avisar de un error grave al iniciar.

::lineas
29 | Muestra el mensaje «Error al iniciar Software FJ: ...» seguido de la descripción del error. La parte `file=sys.stderr` indica que el texto se envíe al canal de errores de la terminal en lugar del canal normal.
::fin

El segundo lugar es `simulacion.py`, que muestra en la terminal el resultado de las 15 operaciones de prueba cuando se ejecuta `python main.py --consola`:

::codigo simulacion.py 102-104 | print en el modo consola de la demostración.

::lineas
102 | Recorre (repite para) cada resultado de la simulación. Verás este tipo de instrucción en la sección 2.12.
103 | Decide si la marca será «OK» o «ERROR» según el resultado.
104 | Muestra en pantalla el número, la marca, la descripción y el detalle de cada operación.
::fin

```salida
 1. [OK   ] Registrar cliente válido: Laura Gómez
      -> Cliente Laura Gómez (ID 1032456789)
 3. [ERROR] Registrar cliente con correo inválido
      -> [FJ-101] Valor inválido para 'correo' ('maria.ruiz@'): formato de correo no válido
```

## 2.2 input(): pedir información al usuario

@nivel1
En un formulario de papel hay espacios en blanco para que la persona escriba su nombre. El formulario «pregunta» y espera tu respuesta.
@fin

@nivel2
**Qué significa.** `input` significa «entrada». Es una función que muestra una pregunta en la terminal y **espera** a que la persona escriba algo y presione Enter.

**Para qué sirve.** Para que el programa reciba datos de quien lo usa mientras está funcionando.

**Cómo se usa.** Se guarda lo que la persona escribe en una variable (sección 2.3). Importante: lo que devuelve `input` siempre es **texto**, aunque la persona escriba números.
@fin

```python
nombre = input("¿Cuál es tu nombre? ")
print("Hola,", nombre)
```

```salida
¿Cuál es tu nombre? Laura
Hola, Laura
```

@nivel3
Aquí hay que ser honestos: **Software FJ no usa `input()` en ninguna parte**. La razón es que `input` solo sirve para programas de terminal (texto en una ventana negra), y Software FJ es una aplicación gráfica. En su lugar, los datos entran por **campos de texto** de Tkinter, la herramienta de ventanas que estudiarás en el capítulo 5. Cada campo está conectado a una variable especial llamada `StringVar`, que guarda lo que la persona escribe.
@fin

::codigo interfaz/componentes.py 257-262 | El equivalente de input() en la interfaz gráfica: un campo de texto (Entry) conectado a una StringVar.

::lineas
257 | Crea una `StringVar`, una «caja de texto invisible» que recordará lo que se escriba en el campo.
258-260 | Si el campo es una lista desplegable («combo»), crea un `Combobox` conectado a esa variable.
261-262 | En los demás casos crea un `Entry`, es decir, una casilla para escribir, conectada a la variable.
::fin

Más tarde, cuando pulsas **Guardar**, el programa «lee» todos esos campos de una vez. Es lo que haría `input`, pero con varios datos y sin terminal:

::codigo interfaz/componentes.py 270-271 | Lectura de todos los campos del formulario.

::lineas
270 | Define la acción `valores`, que entrega lo escrito en el formulario.
271 | Para cada campo, toma su texto con `.get()`, le quita los espacios sobrantes con `.strip()` y lo guarda con su nombre.
::fin

::img 03_cliente_formulario | Los cuatro campos del formulario de clientes cumplen la función que en un programa de terminal cumpliría input().

## 2.3 Variables: cajas con nombre

@nivel1
En una mudanza, guardas cosas en cajas y les pegas una etiqueta: «Libros», «Ropa de invierno». Después, cuando necesitas algo, buscas la caja por su etiqueta, sin abrirlas todas.
@fin

::img d_variable | Una variable es como una caja con etiqueta que guarda un valor.

@nivel2
**Qué significa.** Una **variable** es un nombre que guarda un dato en la memoria del computador.

**Para qué sirve.** Para recordar información y usarla después: un nombre, un precio, un resultado.

**Cómo se usa.** Se escribe el nombre, el signo `=` y el valor. Ojo: en Python el signo `=` **no** significa «es igual»; significa «guarda esto en esta caja» (se llama **asignación**). Si vuelves a asignar, el valor anterior se reemplaza.

Reglas para los nombres: pueden tener letras, números y guion bajo (`_`), no pueden empezar con número ni tener espacios, y Python distingue mayúsculas de minúsculas (`total` y `Total` son variables distintas).
@fin

```python
cliente = "Laura Gómez"
horas = 3
tarifa = 50000
subtotal = horas * tarifa
print(cliente, "debe", subtotal)
horas = 4                 # la caja «horas» ahora guarda 4
print(horas)
```

```salida
Laura Gómez debe 150000
4
```

@nivel3
Software FJ usa variables en todas partes. Dos ejemplos muy claros son los valores fijos de impuesto y de descuento máximo. Cuando el nombre de una variable está escrito todo en MAYÚSCULAS, es una convención (un acuerdo entre programadores) para indicar que ese valor **no debería cambiar**: se le llama **constante**.
@fin

::codigo modelos/servicios.py 20 | El impuesto por defecto, guardado en una variable constante.

::codigo gestores/gestor_reservas.py 8 | El descuento máximo permitido en una reserva.

::lineas
20 | `IMPUESTO_POR_DEFECTO` guarda el número 19. Todo el programa usa este nombre en lugar de escribir 19 en muchos lugares; si el IVA cambiara, bastaría con modificar esta línea. Lo que va después de `#` es un comentario: «IVA Colombia, en porcentaje».
8 | `DESCUENTO_MAXIMO` guarda 0.50, es decir, el 50 % expresado como fracción.
::fin

@ejercicio: ¿Qué guarda cada caja?
Después de ejecutar estas líneas, ¿qué valor tiene `total`?

```python
precio = 35000
dias = 2
total = precio * dias
dias = 5
```

Respuesta: `total` vale 70000. Cambiar `dias` después no modifica `total`, porque el cálculo ya se hizo y su resultado quedó guardado.
@fin

## 2.4 Tipos de datos

@nivel1
En una cocina no se guarda igual la leche, los huevos y el arroz: cada cosa necesita un recipiente distinto y se usa de manera distinta. No tiene sentido «pelar» la leche ni «servir» un huevo en un vaso.
@fin

@nivel2
**Qué significa.** El **tipo de dato** indica qué clase de valor guarda una variable y, por tanto, qué se puede hacer con él.

**Para qué sirve.** Para que Python sepa cómo tratar cada valor: con números puede sumar; con textos puede pasar a mayúsculas; con listas puede agregar elementos.

**Cómo se usa.** No hace falta declarar el tipo: Python lo deduce del valor. Puedes preguntarlo con la función `type()`.

| Tipo | Nombre en Python | Ejemplo | Uso típico |
|---|---|---|---|
| Texto (cadena) | `str` | `"Sala Ejecutiva"` | Nombres, correos, códigos |
| Número entero | `int` | `12` | Cantidades, capacidad, días |
| Número decimal | `float` | `0.19` | Tarifas, porcentajes, totales |
| Lógico (booleano) | `bool` | `True` o `False` | Sí/no: ¿está disponible? |
| Nada | `None` | `None` | «Todavía no hay valor» |
| Lista | `list` | `[1, 2, 3]` | Varios elementos en orden |
| Diccionario | `dict` | `{"total": 160650}` | Datos con nombre |
@fin

```python
print(type("Laura"))
print(type(12))
print(type(0.19))
print(type(True))
```

```salida
<class 'str'>
<class 'int'>
<class 'float'>
<class 'bool'>
```

@nivel3
En el constructor de la clase `Servicio` (el código que «fabrica» un servicio nuevo) aparecen varios tipos de datos juntos:
@fin

::codigo modelos/servicios.py 44-50 | Distintos tipos de datos al crear un servicio.

::lineas
44 | Convierte el nombre en texto (`str`) y le quita espacios sobrantes.
45-46 | Si el texto tiene menos de 3 letras, se produce un error (esto lo verás en el capítulo 9).
47 | Guarda el nombre, que es un `str`.
48 | Guarda la tarifa como número decimal (`float`), revisando que sea positiva.
49 | Guarda el cupo como número entero (`int`). La función `int()` convierte un valor en entero.
50 | Guarda `True`, un valor lógico (`bool`): todo servicio nuevo empieza disponible.
::fin

@nota
`None` se usa mucho en Software FJ para decir «no se indicó». Por ejemplo, si al calcular un precio no se escribe descuento, el valor que llega es `None` y el programa lo trata como cero.
@fin

## 2.5 Cadenas de texto (str)

@nivel1
Un collar de cuentas es una fila de piezas pequeñas unidas en orden. Una palabra también es una fila de letras unidas.
@fin

@nivel2
**Qué significa.** Una **cadena** (en inglés *string*, abreviado `str`) es una secuencia de caracteres: letras, números, espacios o símbolos. Se escribe entre comillas dobles `"..."` o simples `'...'`.

**Para qué sirve.** Para manejar cualquier dato escrito: nombres, correos, mensajes.

**Cómo se usa.** Las cadenas tienen **métodos**, es decir, acciones propias que se escriben con un punto después de la cadena:

| Método | Qué hace | Ejemplo | Resultado |
|---|---|---|---|
| `.upper()` | Pasa a mayúsculas | `"sal-01".upper()` | `"SAL-01"` |
| `.lower()` | Pasa a minúsculas | `"Laura@MAIL.com".lower()` | `"laura@mail.com"` |
| `.strip()` | Quita espacios al inicio y al final | `"  Ana  ".strip()` | `"Ana"` |
| `.capitalize()` | Primera letra mayúscula | `"gómez".capitalize()` | `"Gómez"` |
| `.replace(a, b)` | Reemplaza un texto por otro | `"19%".replace("%", "")` | `"19"` |
| `.isdigit()` | ¿Son solo dígitos? | `"1032".isdigit()` | `True` |

También existen las **cadenas f** (con una `f` antes de las comillas). Dentro de ellas, lo que va entre llaves `{}` se reemplaza por el valor de una variable. Son la forma más cómoda de armar mensajes.
@fin

```python
nombre = "  laura gómez  "
limpio = nombre.strip()
print(limpio.upper())
total = 160650
print(f"El total de {limpio} es {total}")
```

```salida
LAURA GÓMEZ
El total de laura gómez es 160650
```

@nivel3
La clase `Cliente` usa métodos de cadenas para dejar los datos ordenados. Al guardar el correo, lo pasa a minúsculas; al guardar el nombre, pone en mayúscula la primera letra de cada palabra.
@fin

::codigo modelos/cliente.py 54-59 | Tratamiento del correo electrónico.

::lineas
55 | Empieza la acción que se ejecuta cuando se asigna un correo al cliente.
56 | Revisa que el correo no esté vacío y lo convierte a minúsculas con `.lower()`.
57-58 | Si el texto no tiene forma de correo, se produce un error con el mensaje «formato de correo no válido».
59 | Guarda el correo ya limpio.
::fin

::codigo modelos/cliente.py 48 | Nombre con mayúscula inicial en cada palabra.

::lineas
48 | `valor.split()` parte el nombre en palabras; `p.capitalize()` pone mayúscula inicial a cada una; `" ".join(...)` las vuelve a unir con espacios. Así «laura gómez» se guarda como «Laura Gómez».
::fin

Y en `servicios.py` hay una cadena f que arma la descripción de una sala:

::codigo modelos/servicios.py 205-206 | Una cadena f que inserta la capacidad dentro del texto.

## 2.6 Números enteros (int)

@nivel1
Las personas, los días o las sillas se cuentan con números completos: no existe «media persona» en una reunión.
@fin

@nivel2
**Qué significa.** Un **entero** (`int`, del inglés *integer*) es un número sin parte decimal: `0`, `7`, `-3`, `500`.

**Para qué sirve.** Para contar cosas: cantidades, posiciones, capacidades, días.

**Cómo se usa.** Se escribe el número sin comillas. Con la función `int()` puedes convertir un texto o un decimal en entero (si es decimal, se descarta la parte después del punto). La función `len()` devuelve un entero: cuántos elementos o caracteres tiene algo.
@fin

```python
capacidad = 12
mas_personas = capacidad + 3
print(mas_personas)
print(int("25") + 5)
print(len("1032456789"))
```

```salida
15
30
10
```

@nivel3
Los equipos se alquilan por **días completos**. Por eso `AlquilerEquipo` revisa que la duración sea un número entero y, si alguien escribe 2.5 días, muestra un error.
@fin

::codigo modelos/servicios.py 228-232 | Validación de días completos en el alquiler de equipos.

::lineas
228 | Define la acción que revisa la duración de un alquiler.
229 | Comprueba que la duración esté entre 1 y 30 días.
230 | Compara el valor con su versión entera: si 2.5 es distinto de 2, no son días completos.
231 | En ese caso produce el error «los equipos se alquilan por días completos».
232 | Si todo está bien, devuelve la duración convertida en entero.
::fin

Otro ejemplo es la regla de la identificación del cliente, que usa `len()`:

::codigo modelos/cliente.py 30 | len() cuenta los dígitos de la identificación.

## 2.7 Números decimales (float)

@nivel1
El dinero, el peso o la estatura no siempre son números redondos: 1,75 metros o 2,5 kilos.
@fin

@nivel2
**Qué significa.** Un **número decimal** (en Python, `float`, de *floating point* o «coma flotante») es un número con parte fraccionaria. En Python el separador decimal es el **punto**, no la coma: se escribe `0.19`, no `0,19`.

**Para qué sirve.** Para precios, porcentajes, promedios y cualquier medida que no sea entera.

**Cómo se usa.** Se escribe con punto. `float()` convierte un texto en decimal. `round(numero, 2)` redondea a dos decimales, algo muy útil con dinero.
@fin

```python
iva = 0.19
neto = 135000
impuesto = neto * iva
print(impuesto)
print(round(10 / 3, 2))
print(float("19.5"))
```

```salida
25650.0
3.33
19.5
```

@nivel3
El cálculo de precios de Software FJ trabaja con decimales y redondea cada valor a dos cifras. Este es el corazón del cálculo:
@fin

::codigo modelos/servicios.py 128-136 | Cálculo del costo con números decimales.

::lineas
128 | Empieza la acción que calcula el costo detallado. Recibe duración, impuesto y descuento.
129 | Revisa que la duración sea válida para ese tipo de servicio.
130 | Calcula el valor base (tarifa por duración, con las reglas de cada tipo).
131 | Si no hay impuesto, usa 0.0; si lo hay, lo revisa y lo usa.
132 | Lo mismo con el descuento.
133 | Calcula el valor del descuento y lo redondea a 2 decimales.
134 | Resta el descuento a la base: el resultado se llama «neto».
135 | Calcula el impuesto sobre el neto, redondeado.
136 | Suma neto e impuesto: ese es el total.
::fin

Por ejemplo, para 3 horas de la Sala Ejecutiva ($ 50.000 la hora) con 10 % de descuento e IVA del 19 %: base 150000.0, descuento 15000.0, neto 135000.0, impuesto 25650.0 y total **160650.0**.

Para mostrar ese número bonito en pantalla ($ 160.650), la interfaz usa la función `formato_moneda`:

::codigo interfaz/componentes.py 110-114 | Conversión de un decimal en texto con formato de pesos.

::lineas
112 | `float(valor)` asegura que sea decimal; `:,.0f` lo muestra sin decimales y con comas de miles; `.replace(",", ".")` cambia las comas por puntos, como se escribe en Colombia.
113-114 | Si el valor no se puede convertir, lo devuelve tal cual, sin romper el programa.
::fin

## 2.8 Listas

@nivel1
Una lista de mercado tiene elementos en un orden: primero leche, luego pan, luego huevos. Puedes agregar cosas al final, tachar elementos o contar cuántos hay.
@fin

::img d_lista_dic | Una lista guarda elementos por posición; un diccionario los guarda por nombre (clave).

@nivel2
**Qué significa.** Una **lista** (`list`) es una colección ordenada de valores, escrita entre corchetes `[ ]` y separada por comas.

**Para qué sirve.** Para guardar muchos datos del mismo tipo juntos: todos los clientes, todas las reservas.

**Cómo se usa.**

- Crear: `numeros = [10, 20, 30]` o una lista vacía `[]`.
- Leer por posición: `numeros[0]` es 10. **Las posiciones empiezan en 0**, no en 1.
- Agregar al final: `numeros.append(40)`.
- Contar elementos: `len(numeros)`.
- Preguntar si algo está: `20 in numeros` devuelve `True`.
@fin

```python
clientes = ["Laura", "Andrés"]
clientes.append("Camila")
print(clientes)
print(clientes[0])
print(len(clientes))
print("Andrés" in clientes)
```

```salida
['Laura', 'Andrés', 'Camila']
Laura
3
True
```

@nivel3
Software FJ no usa base de datos: guarda todo en listas dentro de la memoria. El gestor de clientes empieza con una lista vacía y le agrega cada cliente nuevo.
@fin

::codigo gestores/gestor_clientes.py 8-9 | La lista donde viven todos los clientes.

::codigo gestores/gestor_clientes.py 20-23 | Agregar un cliente a la lista con append.

::lineas
9 | `self._clientes = []` crea una lista vacía. Allí se guardarán los clientes mientras el programa esté abierto.
21 | `append` agrega el cliente recién creado al final de la lista.
22 | Anota en el registro que se registró un cliente.
23 | Devuelve el cliente para que la pantalla pueda mostrar un mensaje.
::fin

::codigo gestores/gestor_clientes.py 54-58 | Copiar la lista y contar sus elementos.

::lineas
55 | `list(self._clientes)` entrega una **copia** de la lista, para que nadie desde afuera modifique la original por accidente.
58 | `len(...)` dice cuántos clientes hay. Es el número que ves en la tarjeta «Clientes registrados» del panel principal.
::fin

## 2.9 Diccionarios

@nivel1
En un diccionario de español buscas una palabra y encuentras su significado. No buscas «la palabra número 5.320»; buscas por la palabra misma. Una agenda de contactos funciona igual: buscas «Mamá» y obtienes su teléfono.
@fin

@nivel2
**Qué significa.** Un **diccionario** (`dict`) guarda parejas **clave: valor** entre llaves `{ }`. La clave es la «palabra» y el valor es su «significado».

**Para qué sirve.** Para guardar datos con nombre, en lugar de por posición. Es ideal para fichas: el nombre, el correo y el teléfono de una persona.

**Cómo se usa.**

- Crear: `persona = {"nombre": "Laura", "edad": 30}`.
- Leer: `persona["nombre"]` devuelve `"Laura"`.
- Agregar o cambiar: `persona["ciudad"] = "Bogotá"`.
- Preguntar si existe una clave: `"edad" in persona`.
@fin

```python
costo = {"subtotal": 150000, "descuento": 15000}
costo["impuesto"] = 25650
print(costo["subtotal"])
print(costo)
```

```salida
150000
{'subtotal': 150000, 'descuento': 15000, 'impuesto': 25650}
```

@nivel3
En la asesoría, cada nivel tiene un multiplicador de precio. En lugar de muchas preguntas, el programa usa un diccionario: busca el nivel y obtiene su multiplicador.
@fin

::codigo modelos/servicios.py 244 | Diccionario de niveles de asesoría.

::codigo modelos/servicios.py 270-271 | Uso del diccionario para calcular el costo base.

::lineas
244 | Tres parejas: «Básico» vale 1.0, «Intermedio» 1.3 y «Experto» 1.6.
271 | `self.NIVELES[self._nivel]` busca el multiplicador del nivel de esa asesoría. Si es «Experto», el costo es tarifa × duración × 1.6.
::fin

El resultado del cálculo de costos también se entrega como diccionario, para que cada valor tenga nombre:

::codigo modelos/servicios.py 140-146 | El desglose del costo, devuelto como diccionario.

## 2.10 Operadores

@nivel1
En una calculadora tienes teclas para sumar y restar. En la vida diaria también comparamos («¿cuesta más de 100 mil?») y combinamos condiciones («si llueve **y** hace frío, llevo chaqueta»).
@fin

@nivel2
**Qué significa.** Un **operador** es un símbolo que realiza una operación entre valores.

**Para qué sirve.** Para calcular, comparar y combinar condiciones.

**Cómo se usa.**

| Familia | Operadores | Ejemplo | Resultado |
|---|---|---|---|
| Aritméticos | `+  -  *  /  //  %  **` | `7 / 2`, `7 // 2`, `7 % 2` | `3.5`, `3`, `1` |
| Asignación | `=  +=  -=` | `x += 1` | suma 1 a `x` |
| Comparación | `==  !=  <  >  <=  >=` | `5 >= 3` | `True` |
| Lógicos | `and  or  not` | `True and False` | `False` |
| Pertenencia | `in`, `not in` | `"a" in "casa"` | `True` |
| Identidad | `is`, `is not` | `valor is None` | `True` si no hay valor |

No confundas `=` (guardar) con `==` (preguntar si son iguales). Python permite encadenar comparaciones como en matemáticas: `5 <= x <= 12`.
@fin

```python
horas = 3
print(horas * 50000)
print(horas > 12)
print(1 <= horas <= 12)
print(horas > 0 and horas < 8)
print(not horas == 3)
```

```salida
150000
False
True
True
False
```

@nivel3
La regla del recargo de las salas grandes combina un operador de comparación (`>`) y operadores aritméticos (`*`):
@fin

::codigo modelos/servicios.py 201-203 | Operadores en el cálculo del costo de una sala.

::lineas
202 | Si la capacidad es mayor que 20, el recargo es 1.10 (10 % más); si no, es 1.0. Es una condición escrita en una sola línea.
203 | Multiplica tarifa × duración × recargo.
::fin

La validación de la identificación combina operadores lógicos y una comparación encadenada:

::codigo modelos/cliente.py 30 | not, or y comparación encadenada.

::lineas
30 | Se lee: «si **no** son solo dígitos, **o** **no** se cumple que 5 ≤ longitud ≤ 12...». Basta con que una de las dos partes sea verdadera para que haya error.
::fin

Y la búsqueda de clientes usa el operador `in` para preguntar si un texto está **contenido** en otro:

::codigo gestores/gestor_clientes.py 51-52 | El operador in en la búsqueda de clientes.

## 2.11 Condicionales: if, elif y else

@nivel1
Todos los días tomas decisiones: «**si** llueve, llevo paraguas; **si no**, pero hace sol, llevo gorra; **en cualquier otro caso**, no llevo nada».
@fin

@nivel2
**Qué significa.** `if` significa «si», `elif` es una abreviación de *else if* («si no, si...») y `else` significa «si no».

**Para qué sirve.** Para que el programa tome decisiones y ejecute instrucciones distintas según una condición.

**Cómo se usa.** Se escribe la condición seguida de dos puntos `:`. Las instrucciones que dependen de esa condición se escriben **más adentro** (con sangría de 4 espacios). Python revisa las condiciones en orden y ejecuta solo el primer bloque cuya condición sea verdadera. `elif` y `else` son opcionales.
@fin

```python
dias = 40
if dias < 1:
    print("Debe alquilar al menos un día")
elif dias > 30:
    print("Máximo 30 días")
else:
    print("Duración correcta")
```

```salida
Máximo 30 días
```

@importante
La sangría (los espacios al comienzo de la línea) **no es decorativa** en Python: es la forma de indicar qué instrucciones están dentro del `if`. Si la sangría está mal, Python muestra un error de sintaxis.
@fin

@nivel3
Cuando registras un servicio, la pantalla de servicios decide qué método llamar según el tipo que elegiste en los botones de opción (Sala, Equipo o Asesoría). Es un `if / elif / else` perfecto:
@fin

::codigo interfaz/vista_servicios.py 140-149 | Decisión según el tipo de servicio.

::lineas
140 | Lee qué tipo eligió la persona.
141-143 | Si es «Sala», prepara el registro de una sala (con capacidad y cupo).
144-146 | Si no, pero es «Equipo», prepara el registro de un equipo (con tipo de equipo y unidades).
147-149 | En cualquier otro caso (solo queda «Asesoría»), prepara el registro de una asesoría.
::fin

::img 14_form_sala | El tipo elegido (Sala) determina qué rama del if se ejecuta.

Otro `if` importante está en `main.py`, que decide si abrir la ventana o trabajar solo en la terminal:

::codigo main.py 15-19 | main.py decide el modo de ejecución.

@ejercicio: ¿Qué se imprime?
```python
capacidad = 60
if capacidad > 20:
    print("Sala grande: recargo del 10 %")
else:
    print("Sin recargo")
```
Respuesta: «Sala grande: recargo del 10 %», porque 60 es mayor que 20. Es la misma regla de la línea 202 de `modelos/servicios.py`.
@fin

## 2.12 Ciclos: for y while

@nivel1
Una profesora llama a lista: «Ana, presente. Bruno, presente. Carla, presente...». Repite la misma acción para cada estudiante hasta terminar la lista. Otra situación: revuelves una sopa **mientras** no hierva.
@fin

@nivel2
**Qué significa.** Un **ciclo** (o bucle) repite instrucciones. `for` significa «para» y `while` significa «mientras».

**Para qué sirve.** Para no escribir mil veces lo mismo: procesar todos los clientes, revisar todas las reservas.

**Cómo se usa.**

- `for elemento in coleccion:` repite el bloque **una vez por cada elemento** de una lista, cadena, diccionario, etc.
- `while condicion:` repite el bloque **mientras** la condición sea verdadera. Hay que asegurarse de que en algún momento sea falsa, o el ciclo no terminaría nunca (un **ciclo infinito**).
- `range(n)` genera los números 0, 1, ..., n−1, útil para repetir un número fijo de veces.
- `break` sale del ciclo antes de tiempo; dentro de una función, `return` también lo detiene.
@fin

```python
clientes = ["Laura", "Andrés", "Camila"]
for nombre in clientes:
    print("Bienvenido,", nombre)

intentos = 0
while intentos < 3:
    print("Intento", intentos + 1)
    intentos += 1
```

```salida
Bienvenido, Laura
Bienvenido, Andrés
Bienvenido, Camila
Intento 1
Intento 2
Intento 3
```

@nivel3
Para encontrar un cliente por su identificación, el gestor recorre la lista con un `for` y, en cuanto lo encuentra, lo devuelve:
@fin

::codigo gestores/gestor_clientes.py 37-44 | Búsqueda de un cliente con un ciclo for.

::lineas
38 | Limpia la identificación recibida.
39 | Para cada cliente de la lista...
40 | ...pregunta si su identificación coincide con la buscada.
41 | Si coincide, lo devuelve; `return` termina la búsqueda inmediatamente.
42-44 | Si el ciclo terminó sin encontrarlo, crea un error «No existe un cliente...», lo anota en el registro y lo lanza.
::fin

La simulación usa un `for` para ejecutar las 15 operaciones, una tras otra:

::codigo simulacion.py 70 | El ciclo de la demostración de 15 operaciones.

@nota: ¿Y el ciclo while?
En el código de Software FJ **no hay ningún `while`**: todas las repeticiones recorren colecciones conocidas (listas de clientes, servicios, reservas u operaciones), y para eso `for` es la herramienta natural. Es bueno que lo sepas por si el docente te pregunta: `while` se usa cuando no se sabe de antemano cuántas veces repetir.
@fin

@nota: Ciclos «comprimidos»
En el código verás formas cortas de ciclo dentro de corchetes, llamadas **comprensiones de lista**, por ejemplo en `gestores/gestor_reservas.py`, línea 90: `[r for r in self._reservas if r.estado == estado]`. Se lee: «una lista con cada reserva `r` de la lista de reservas, solo si su estado es el pedido». Es un `for` más un `if` en una línea.
@fin

## 2.13 Funciones

@nivel1
Una licuadora es una máquina con un propósito: le das frutas y leche, presionas el botón y te devuelve un jugo. No necesitas saber cómo está hecho el motor; solo cómo usarla. Y puedes usarla todas las veces que quieras.
@fin

@nivel2
**Qué significa.** Una **función** es un bloque de código con nombre que realiza una tarea concreta. Se **define** una vez y se **llama** (se usa) todas las veces que se necesite.

**Para qué sirve.** Para no repetir código, para dividir un problema grande en partes pequeñas y para darle un nombre claro a cada tarea.

**Cómo se usa.** Se define con la palabra `def`, el nombre, paréntesis y dos puntos. El cuerpo va con sangría. Para usarla, se escribe su nombre seguido de paréntesis. Python ya trae muchas funciones listas (`print`, `len`, `round`...); a las que tú escribes se les llama funciones propias.

Cuando una función pertenece a una clase (lo verás en el capítulo 3), se le llama **método**.
@fin

```python
def saludar():
    print("Bienvenido a Software FJ")

saludar()
saludar()
```

```salida
Bienvenido a Software FJ
Bienvenido a Software FJ
```

@nivel3
En `modelos/servicios.py` hay una función muy útil que convierte un porcentaje escrito por la persona («19», «19%», «19,5») en una fracción que el programa pueda usar (0.19):
@fin

::codigo modelos/servicios.py 23-33 | Una función real: porcentaje_a_fraccion.

::lineas
23 | `def` define la función `porcentaje_a_fraccion`, que recibe dos datos: `campo` (qué se está convirtiendo) y `valor`.
24 | Texto entre triples comillas: es la **documentación** de la función (se llama *docstring*). Explica qué hace.
25-26 | Si el valor está vacío, devuelve `None` («no se indicó»).
27-28 | Intenta quitar el símbolo %, cambiar la coma por punto y convertirlo en decimal.
29-30 | Si no se puede convertir (por ejemplo, «abc»), produce un error explicativo.
31-32 | Si el número no está entre 0 y 100, también produce un error.
33 | Devuelve el porcentaje dividido entre 100: 19 se convierte en 0.19.
::fin

Esta función se usa en varios lugares, por ejemplo en el gestor de reservas (líneas 25 y 26 de `gestores/gestor_reservas.py`). Gracias a ella, la regla está escrita **una sola vez**.

## 2.14 Parámetros

@nivel1
En una cafetería, el pedido «un café» no es suficiente: te preguntan el tamaño y si lo quieres con leche. Esas preguntas son los espacios que la cafetería necesita llenar para preparar tu bebida. Algunas tienen una respuesta por defecto: si no dices nada, te sirven el tamaño mediano.
@fin

@nivel2
**Qué significa.** Los **parámetros** son los nombres que se escriben entre los paréntesis cuando se **define** una función. Son como casillas vacías que la función espera recibir.

**Para qué sirve.** Para que una misma función trabaje con datos distintos cada vez.

**Cómo se usa.** Se separan con comas. Un parámetro puede tener un **valor por defecto** con `=`: si quien llama no lo envía, se usa ese valor.
@fin

```python
def calcular_total(precio, cantidad, descuento=0):
    return precio * cantidad - descuento

print(calcular_total(50000, 3))
print(calcular_total(50000, 3, 15000))
```

```salida
150000
135000
```

@nivel3
El método que calcula el costo de un servicio tiene un parámetro obligatorio (`duracion`) y dos opcionales (`impuesto` y `descuento`), que por defecto valen `None`:
@fin

::codigo modelos/servicios.py 119-126 | Parámetros obligatorios y opcionales.

::lineas
119 | `self` es un parámetro especial que verás en el capítulo 3 (representa al propio servicio). `duracion` es obligatorio; `impuesto=None` y `descuento=None` son opcionales.
120-125 | La documentación explica las tres formas de llamarlo: solo con la duración, con duración e impuesto, o con los tres.
126 | Llama al cálculo detallado y se queda solo con el valor de la clave «total».
::fin

La clase `Asesoria` también define parámetros con valores por defecto: si no se dice el nivel, será «Básico», y si no se dice el cupo, será 1.

::codigo modelos/servicios.py 246 | Parámetros con valores por defecto en Asesoria.

## 2.15 Argumentos

@nivel1
Siguiendo con la cafetería: los parámetros eran las preguntas del formulario («tamaño», «leche»). Los **argumentos** son tus respuestas concretas: «grande», «sí».
@fin

@nivel2
**Qué significa.** Un **argumento** es el valor real que se entrega a una función cuando se **llama**.

**Para qué sirve.** Para llenar los parámetros con datos concretos.

**Cómo se usa.** Hay dos formas:

- **Por posición**: los valores se asignan en el mismo orden de los parámetros. `calcular_total(50000, 3)`.
- **Por nombre** (argumentos con palabra clave): se indica el nombre del parámetro. `calcular_total(cantidad=3, precio=50000)`. Así el orden no importa y el código se lee mejor.

Una forma especial es `**diccionario`: «desempaca» un diccionario y entrega cada pareja clave–valor como argumento por nombre.
@fin

| Concepto | Dónde aparece | Ejemplo |
|---|---|---|
| Parámetro | En la **definición** (`def`) | `def registrar(self, identificacion, nombre, correo, telefono)` |
| Argumento | En la **llamada** | `registrar("1032456789", "Laura Gómez", ...)` |

```python
def ficha(nombre, telefono):
    print(nombre, "-", telefono)

ficha("Laura", "3104567890")                  # por posición
ficha(telefono="3001112233", nombre="María")  # por nombre
datos = {"nombre": "Andrés", "telefono": "6017654321"}
ficha(**datos)                                # desempacando un diccionario
```

```salida
Laura - 3104567890
María - 3001112233
Andrés - 6017654321
```

@nivel3
La simulación llama al método `registrar` del gestor de clientes con cuatro argumentos por posición:
@fin

::codigo simulacion.py 28-29 | Argumentos por posición: identificación, nombre, correo y teléfono.

La pantalla de clientes usa la forma con `**`: lee el formulario como diccionario y lo entrega «desempacado», más dos argumentos por nombre (`formulario` y `exito`):

::codigo interfaz/vista_clientes.py 70-77 | Argumentos por nombre y desempaque de un diccionario.

::lineas
71 | `datos` es un diccionario con las claves `identificacion`, `nombre`, `correo` y `telefono`.
76-77 | `**datos` entrega cada dato a su parámetro con el mismo nombre. `formulario=self.form` y `exito=...` son argumentos por nombre para el método `ejecutar` de la pantalla.
::fin

## 2.16 return: devolver un resultado

@nivel1
Le pides a un amigo que vaya a la tienda. Él va, compra y **te entrega** el cambio y el recibo. Lo que te entrega es el resultado del encargo.
@fin

@nivel2
**Qué significa.** `return` significa «devolver». Termina la función y entrega un valor a quien la llamó.

**Para qué sirve.** Para que el resultado de una función pueda guardarse en una variable o usarse en otro cálculo.

**Cómo se usa.** `return valor`. En cuanto Python ejecuta un `return`, sale de la función: lo que esté escrito después no se ejecuta. Si una función no tiene `return`, devuelve `None`. Se pueden devolver varios valores separados por comas.

No confundas `print` con `return`: `print` **muestra** algo en pantalla para una persona; `return` **entrega** un valor al resto del programa.
@fin

```python
def subtotal(tarifa, horas):
    return tarifa * horas

valor = subtotal(50000, 3)
print(valor + 10000)
```

```salida
160000
```

@nivel3
El método `_preparar` del gestor de reservas devuelve **tres valores a la vez**: el servicio, el impuesto y el descuento ya convertidos.
@fin

::codigo gestores/gestor_reservas.py 22-30 | Una función que devuelve tres valores.

::lineas
24 | Busca el servicio por su código.
25-26 | Convierte impuesto y descuento de porcentaje a fracción, con la función de la sección 2.13.
27-29 | Si el descuento supera el máximo (50 %), produce un error.
30 | Devuelve los tres valores juntos.
::fin

Y quien lo llama los recibe en tres variables, en el mismo orden:

::codigo gestores/gestor_reservas.py 35-36 | Recibir los tres valores devueltos.

## 2.17 import: usar código de otros archivos

@nivel1
No necesitas fabricar tu propio taladro para colgar un cuadro: lo pides prestado de la caja de herramientas. Y si en tu casa cada cosa tiene su cajón, sabes exactamente dónde buscar.
@fin

@nivel2
**Qué significa.** `import` significa «importar»: traer a tu archivo código que está escrito en otro archivo (módulo) o en la biblioteca de Python.

**Para qué sirve.** Para reutilizar herramientas ya hechas y para dividir un programa grande en varios archivos ordenados.

**Cómo se usa.**

- `import modulo` trae el módulo completo; se usa como `modulo.algo`.
- `from modulo import nombre` trae solo una pieza; se usa directamente como `nombre`.
- `from paquete.modulo import nombre` trae una pieza de un módulo que está dentro de una carpeta (paquete).
@fin

```python
import math
from datetime import date

print(math.sqrt(16))
print(date(2026, 11, 5))
```

```salida
4.0
2026-11-05
```

@nivel3
Las primeras líneas de casi todos los archivos de Software FJ son `import`. En `modelos/cliente.py` se ven los tres tipos de importación:
@fin

::codigo modelos/cliente.py 2-5 | Importaciones al inicio de cliente.py.

::lineas
2 | Importa el módulo `re` (expresiones regulares) de la biblioteca de Python, que sirve para revisar patrones de texto como la forma de un correo.
4 | Del archivo propio `excepciones.py` trae dos tipos de error: `DatoInvalidoError` y `ParametroFaltanteError`.
5 | Del paquete `modelos`, archivo `entidad.py`, trae la clase `Entidad`, de la que hereda `Cliente` (capítulo 3).
::fin

En `main.py` hay algo interesante: algunas importaciones se hacen **dentro** de la función, justo cuando se necesitan.

::codigo main.py 9-11 | Importaciones al inicio de main.py.

::codigo main.py 21-23 | Importación dentro de un bloque: la interfaz solo se carga si se va a usar.

::lineas
9 | Importa `sys`, que permite leer lo que se escribió al ejecutar el programa (por ejemplo `--demo`).
11 | Trae dos funciones del archivo propio `registro.py`.
22 | Trae la clase `VentanaPrincipal` del paquete `interfaz` solo en este punto. Si se usa el modo `--consola`, la ventana nunca se importa.
23 | Crea la ventana principal.
::fin

::img d_imports | Mapa de qué archivo de Software FJ importa a cuál.

@recuerda
Las importaciones son las «conexiones» entre los archivos del proyecto. Si alguna vez quieres saber de dónde viene una palabra en un archivo, mira las primeras líneas: casi siempre encontrarás un `import` que lo explica.
@fin

## 2.18 Practica lo aprendido

@ejercicio: Lee y explica
Explica con tus palabras qué hace este código y qué muestra:

```python
reservas = [160650, 87465, 356048]
total = 0
for valor in reservas:
    if valor > 100000:
        total += valor
print(total)
```

Respuesta: suma solo los valores mayores que 100 000. Muestra `516698` (160650 + 356048).
@fin

@ejercicio: Encuentra las piezas
Abre `gestores/gestor_reservas.py` y localiza: (a) una variable constante, (b) una lista vacía, (c) un `if`, (d) un `return`, (e) un `import`. Anota el número de línea de cada una.

Una posible respuesta: (a) línea 8; (b) línea 15; (c) línea 27; (d) línea 30; (e) línea 4.
@fin

@ejercicio: Parámetro o argumento
En la llamada `s.reservas.crear("80123456", "EQU-01", 2, 19)` de `simulacion.py`, ¿los valores entre paréntesis son parámetros o argumentos? ¿Qué parámetro de `crear` recibe el número 2? (Mira la línea 38 de `gestores/gestor_reservas.py`.)

Respuesta: son argumentos. El 2 llega al parámetro `duracion` (2 días de alquiler del videobeam).
@fin

@ejercicio: Diccionario de niveles
Si una asesoría de nivel «Intermedio» cuesta $ 90.000 la hora y se contratan 2 horas, ¿cuál es el costo base según la línea 271 de `modelos/servicios.py`?

Respuesta: 90000 × 2 × 1.3 = 234000.
@fin

@resumen
- `print()` muestra información; `input()` la pide en la terminal. Software FJ no usa `input()`: recibe los datos mediante campos de Tkinter conectados a `StringVar`.
- Una **variable** es una caja con nombre; `=` significa «guardar». Los nombres en MAYÚSCULAS indican constantes, como `IMPUESTO_POR_DEFECTO`.
- Los **tipos de datos** básicos son `str` (texto), `int` (entero), `float` (decimal), `bool` (verdadero/falso) y `None` (sin valor).
- Las **listas** guardan elementos en orden (posición desde 0); los **diccionarios** guardan parejas clave–valor. Software FJ guarda clientes, servicios y reservas en listas.
- Los **operadores** calculan, comparan y combinan condiciones; `=` guarda y `==` compara.
- `if / elif / else` toman decisiones; la **sangría** indica qué está dentro de cada bloque.
- `for` repite por cada elemento; `while` repite mientras una condición se cumpla. Software FJ solo usa `for`.
- Una **función** (`def`) agrupa una tarea con nombre; sus **parámetros** son las casillas de la definición y los **argumentos**, los valores de la llamada; `return` entrega el resultado.
- `import` conecta los archivos del proyecto y trae herramientas de la biblioteca de Python.
@fin
