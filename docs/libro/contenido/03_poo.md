# Entendiendo la programación orientada a objetos
> Aprenderás a pensar el software como un conjunto de «cosas» que tienen datos y saben hacer acciones, igual que el mundo real.

@objetivos
- Explicar con tus propias palabras qué es la programación orientada a objetos (POO) y por qué existe.
- Reconocer los problemas que la POO ayuda a resolver en un programa como Software FJ.
- Distinguir entre clase y objeto, y entre atributo y método.
- Comprender qué es un constructor, qué significa `__init__` y para qué sirve `self`.
- Leer la clase `Cliente` del proyecto e identificar cada una de sus partes.
@fin

En los capítulos anteriores aprendiste a leer instrucciones sueltas de Python: variables, listas, condicionales y funciones. Con eso ya se pueden hacer programas pequeños. Pero cuando un programa crece y empieza a manejar clientes, servicios, reservas, pantallas y errores, escribir todo como una lista larga de instrucciones se vuelve un desorden. Este capítulo te presenta una forma diferente de organizar el código, que es justamente la que usa Software FJ: la **programación orientada a objetos**.

No te preocupes si el nombre suena complicado. Lo vamos a construir paso a paso, primero con ejemplos de la vida diaria, luego con la explicación informática y, al final, señalando el código real del proyecto.

## 3.1 ¿Qué es la programación orientada a objetos?

@nivel1
Piensa en una empresa real que alquila salas de reuniones. En ella hay **cosas** concretas: clientes, salas, equipos, empleados y reservas. Cada cosa tiene **información propia** (un cliente tiene nombre, correo y teléfono; una sala tiene capacidad y precio por hora) y además puede **hacer o sufrir acciones** (una reserva se confirma o se cancela; un cliente actualiza su teléfono).

Cuando la recepcionista trabaja, no piensa en «instrucciones sueltas»: piensa en «el cliente Laura», «la Sala Ejecutiva», «la reserva número 1». Organiza su trabajo alrededor de esas cosas.
@fin

@nivel2
La **programación orientada a objetos** (en adelante **POO**) es una manera de escribir programas en la que el código se organiza alrededor de **objetos**. Un objeto es un paquete que reúne dos cosas:

- **Datos**: la información que describe al objeto (por ejemplo, el nombre de un cliente).
- **Comportamiento**: las acciones que el objeto sabe realizar (por ejemplo, describirse a sí mismo o validar su correo).

Para fabricar objetos se usan **clases**, que son como planos o moldes. En lugar de tener los datos en un lugar y las funciones que los usan en otro lugar muy distinto, la POO los mantiene juntos, dentro del mismo objeto.
@fin

@nivel3
Software FJ está construido casi por completo con clases. En la carpeta `modelos/` están las clases que representan las «cosas» del negocio: `Cliente`, `Servicio`, `ReservaSala`, `AlquilerEquipo`, `Asesoria` y `Reserva`. En la carpeta `gestores/` están las clases que administran listas de esas cosas, y en `interfaz/` las clases que dibujan las pantallas. Esta es la primera línea de la clase que representa a un cliente:

::codigo modelos/cliente.py 11-12 | Inicio de la clase Cliente
::lineas
11 | La palabra `class` anuncia que comienza una clase llamada `Cliente`. Lo que está entre paréntesis, `Entidad`, indica que se apoya en otra clase más general (lo verás en el capítulo 4, en la sección de herencia).
12 | Es un texto de documentación (llamado *docstring*) que explica para qué sirve la clase. No se ejecuta como instrucción; sirve para las personas que leen el código.
::fin
@fin

::img d_uml_modelos | Las principales clases del proyecto Software FJ y cómo se relacionan. En este capítulo aprenderás a leer cada caja.

## 3.2 ¿Por qué existe la POO?

@nivel1
Imagina que llevas el control de una tienda en un cuaderno. Al principio anotas todo en una sola hoja: ventas, clientes, inventario y pagos mezclados. Funciona durante una semana. Pero a los tres meses, encontrar el teléfono de un cliente o saber cuánto se vendió de un producto se vuelve una pesadilla. La solución natural es **separar**: una carpeta para clientes, otra para productos, otra para ventas, cada una con su propio formato.
@fin

@nivel2
Con los programas pasa exactamente lo mismo. En los años sesenta y setenta los programas eran cada vez más grandes y los programadores notaron que, si los datos estaban regados por todo el código, cualquier cambio pequeño rompía algo en otro lugar. La POO apareció para **ordenar** los programas grandes: cada clase se encarga de una sola responsabilidad y guarda sus propios datos. Lenguajes como Simula, Smalltalk, C++, Java y, más tarde, Python adoptaron esta idea.
@fin

@nivel3
En Software FJ, cada responsabilidad tiene su propia clase. Por ejemplo, todo lo que tiene que ver con validar un cliente vive en `modelos/cliente.py`; todo lo que tiene que ver con calcular el precio de un servicio vive en `modelos/servicios.py`; y todo lo que tiene que ver con mostrar los clientes en pantalla vive en `interfaz/vista_clientes.py`. Si mañana la regla del teléfono cambia de «7 a 10 dígitos» a «10 dígitos exactos», solo hay que tocar un lugar: el método `telefono` de la clase `Cliente`.
@fin

## 3.3 ¿Qué problemas resuelve la POO?

La POO no es magia, pero resuelve problemas muy concretos. La siguiente tabla los resume con ejemplos del proyecto.

| Problema sin POO | Cómo lo resuelve la POO | Ejemplo en Software FJ |
|---|---|---|
| Los datos de un cliente quedan sueltos en muchas variables (`nombre1`, `correo1`, `nombre2`...). | Se agrupan en un solo objeto. | Cada cliente es un objeto `Cliente` con su nombre, correo y teléfono. |
| Cualquier parte del programa puede cambiar un dato y dejarlo mal escrito. | Se protegen los datos y se validan al cambiarlos (encapsulación). | No se puede guardar un correo sin @: la clase `Cliente` lo rechaza. |
| Hay que copiar y pegar el mismo código para cosas parecidas. | Se reutiliza código mediante herencia. | `ReservaSala`, `AlquilerEquipo` y `Asesoria` heredan lo común de `Servicio`. |
| Para cada tipo de cosa hay que escribir un `if` diferente. | Cada objeto sabe responder a su manera (polimorfismo). | Cada servicio calcula su costo con su propia regla, pero todos se llaman igual. |
| Es difícil repartir el trabajo entre varias personas. | Cada clase es una pieza independiente. | El proyecto se repartió por archivos: vistas, gestores y modelos. |

@recuerda
La POO es una **forma de organizar** el código. No hace que el programa sea más rápido; hace que sea más fácil de entender, de cambiar y de repartir entre un equipo.
@fin

## 3.4 ¿Qué es una clase?

@nivel1
Imagina un **molde para fabricar sillas**. El molde no es una silla: no te puedes sentar en él. Pero define cómo serán todas las sillas que se fabriquen con él: cuántas patas tendrán, de qué tamaño será el asiento y qué forma tendrá el espaldar. Con un solo molde puedes fabricar cien sillas iguales en forma, aunque cada una se pinte de un color distinto.

Otro ejemplo: el **formulario de inscripción** de una universidad. El formulario en blanco dice qué datos se piden (nombre, documento, programa). Cada formulario lleno por un estudiante es un caso concreto.
@fin

@nivel2
Una **clase** es una plantilla que define dos cosas:

- Qué **datos** tendrán los objetos creados a partir de ella (se llaman **atributos**).
- Qué **acciones** podrán realizar esos objetos (se llaman **métodos**).

En Python, una clase se escribe con la palabra `class`, seguida del nombre y de dos puntos. Todo lo que pertenece a la clase va **sangrado** (corrido hacia la derecha) debajo de esa línea. Por costumbre, los nombres de las clases empiezan con mayúscula: `Cliente`, `Sala`, `Reserva`.

```python
class Empleado:
    """Plantilla para representar a un empleado de la empresa."""

    def __init__(self, nombre, cargo):
        self.nombre = nombre
        self.cargo = cargo

    def presentarse(self):
        return f"Hola, soy {self.nombre} y trabajo como {self.cargo}."
```

Este ejemplo didáctico (no es parte del proyecto) define la clase `Empleado`. Todavía no existe ningún empleado: solo existe el molde.
@fin

@nivel3
La clase `Cliente` de Software FJ es el molde de todos los clientes. Define que cada cliente tendrá identificación, nombre, correo y teléfono, y que sabrá describirse y convertirse en un diccionario para mostrarse en tablas.

::codigo modelos/cliente.py 11-19 | La clase Cliente y su constructor
::lineas
11 | Comienza la clase `Cliente`. Se apoya en la clase `Entidad`.
12 | Documentación de la clase: «todos sus datos se validan al asignarse».
14 | Se define el constructor `__init__` (lo verás en la sección 3.8): es lo que se ejecuta cuando se crea un cliente nuevo. Recibe cuatro datos.
15 | Se valida la identificación y se le entrega a la clase `Entidad` para que la guarde.
16-18 | Se guardan el nombre, el correo y el teléfono. Aunque parece una simple asignación, cada una pasa por una validación (lo explica el capítulo 4).
::fin
@fin

::img d_molde | La clase es el molde; los objetos son las piezas fabricadas con él. Cada cliente tiene sus propios datos.

## 3.5 ¿Qué es un objeto?

@nivel1
Volviendo al molde de sillas: cada silla fabricada es un **objeto**. Todas tienen la misma forma, pero cada una existe por separado: puedes pintar una de rojo sin que las demás cambien. Lo mismo pasa con los formularios llenos de una universidad: todos tienen los mismos campos, pero cada uno tiene los datos de un estudiante distinto.
@fin

@nivel2
Un **objeto** (también llamado **instancia**) es un ejemplar concreto creado a partir de una clase. Para crear un objeto en Python se escribe el nombre de la clase seguido de paréntesis, como si se llamara a una función, y se le pasan los datos que pide el constructor:

```python
ana = Empleado("Ana Torres", "Recepcionista")
luis = Empleado("Luis Mora", "Contador")

print(ana.presentarse())
print(luis.presentarse())
```

```salida
Hola, soy Ana Torres y trabajo como Recepcionista.
Hola, soy Luis Mora y trabajo como Contador.
```

`ana` y `luis` son dos objetos distintos de la misma clase. Cada uno guarda su propio nombre y su propio cargo. A la acción de crear un objeto se le llama **instanciar** la clase.
@fin

@nivel3
En Software FJ, los objetos `Cliente` se crean dentro del gestor de clientes, en el momento en que el usuario pulsa **Guardar** en la pantalla de clientes:

::codigo gestores/gestor_clientes.py 11-23 | Aquí nace cada objeto Cliente
::lineas
11 | Método `registrar` del gestor: recibe los cuatro datos escritos en el formulario.
13 | Limpia la identificación: la convierte en texto y le quita espacios al inicio y al final.
14-15 | Revisa si ya existe un cliente con esa identificación. Si existe, detiene el registro con un error.
16 | **Esta es la línea donde se crea el objeto.** `Cliente(...)` usa el molde para fabricar un cliente nuevo con los datos recibidos, y lo guarda en la variable `cliente`.
21 | El objeto nuevo se agrega a la lista interna `self._clientes`, que es donde el gestor recuerda a todos los clientes.
22 | Se anota en el registro de eventos que el cliente fue creado.
23 | Se devuelve el objeto a quien pidió el registro (la pantalla), para que pueda mostrar el mensaje de éxito.
::fin

Cada vez que registras un cliente en la aplicación, se ejecuta la línea 16 y aparece un objeto nuevo en la memoria del computador.
@fin

::img 08_clientes_tabla | Cada fila de esta tabla real corresponde a un objeto Cliente distinto guardado en memoria.

### Clase y objeto: comparación directa

| | Clase | Objeto |
|---|---|---|
| ¿Qué es? | Un molde o plantilla. | Una pieza concreta fabricada con el molde. |
| ¿Cuántos hay? | Una sola definición (`class Cliente`). | Tantos como se creen (uno por cada cliente registrado). |
| ¿Tiene datos concretos? | No: solo dice qué datos habrá. | Sí: «Laura Gómez», «1032456789»... |
| ¿Cómo se escribe? | `class Cliente(Entidad):` | `Cliente("1032456789", "Laura Gómez", ...)` |
| Ejemplo cotidiano | El plano de una casa. | Cada casa construida con ese plano. |

@ejercicio: Identifica clases y objetos
Clasifica cada palabra como **clase** u **objeto**: «Sala», «Sala Ejecutiva SAL-01», «Reserva», «Reserva R-0001», «Cliente», «Andrés Pérez».

*Pista:* las clases son ideas generales; los objetos son casos concretos con nombre o código propio.
@fin

## 3.6 ¿Qué es un atributo?

@nivel1
Un atributo es una **característica** de algo. Tu documento de identidad, tu nombre y tu fecha de nacimiento son atributos tuyos. Una sala tiene como atributos su capacidad, su precio por hora y si está disponible o no.
@fin

@nivel2
Un **atributo** es una variable que pertenece a un objeto. Guarda un dato que describe a ese objeto en particular. Se lee y se escribe con un punto: `objeto.atributo`. Por ejemplo, `ana.nombre` es el atributo `nombre` del objeto `ana`.

Hay dos clases de atributos:

- **Atributos de instancia**: cada objeto tiene su propio valor. Se crean normalmente dentro del constructor con `self.nombre = ...`. El nombre de Ana y el de Luis son diferentes.
- **Atributos de clase**: se escriben directamente dentro de la clase (no dentro de un método) y son **compartidos** por todos los objetos de esa clase.

```python
class Sala:
    tipo = "Sala"                       # atributo de clase: igual para todas

    def __init__(self, nombre, capacidad):
        self.nombre = nombre            # atributo de instancia
        self.capacidad = capacidad      # atributo de instancia
```
@fin

@nivel3
En Software FJ encontramos los dos tipos. La clase `ReservaSala` tiene atributos de clase (iguales para todas las salas) y atributos de instancia (propios de cada sala):

::codigo modelos/servicios.py 184-196 | Atributos de la clase ReservaSala
::lineas
184 | Comienza la clase `ReservaSala`, que representa una sala que se reserva por horas.
187 | Constructor: recibe el código, el nombre, la tarifa por hora, la capacidad y el cupo (si no se indica cupo, vale 2).
188 | Pide a la clase general `Servicio` que guarde los datos comunes (código, nombre, tarifa y cupo).
189 | Crea el atributo de instancia `_capacidad`, después de comprobar que sea un número positivo y no mayor de 500.
191-192 | **Atributos de clase**: todas las salas son de tipo «Sala» y se miden en «horas». No dependen de una sala en particular.
194-196 | Una *propiedad* llamada `capacidad` permite leer el atributo `_capacidad` desde fuera (lo verás en el capítulo 4).
::fin

Fíjate en que muchos atributos empiezan con guion bajo (`_capacidad`, `_nombre`, `_tarifa`). Es una convención de Python que significa «este dato es interno; no lo cambies directamente desde fuera de la clase». En el capítulo 4 verás también atributos que empiezan con **dos** guiones bajos, como `__nombre` en la clase `Cliente`.
@fin

| Atributo | Clase | Tipo de atributo | Qué guarda |
|---|---|---|---|
| `_identificador` | `Entidad` | De instancia | El código único: identificación del cliente, código del servicio o código de la reserva. |
| `_fecha_creacion` | `Entidad` | De instancia | Fecha y hora en que se creó el objeto. |
| `__nombre`, `__correo`, `__telefono` | `Cliente` | De instancia (privados) | Datos personales ya validados. |
| `_tarifa`, `_cupo`, `_disponible` | `Servicio` | De instancia | Precio, plazas simultáneas y si está habilitado. |
| `tipo`, `unidad` | `ReservaSala`, `AlquilerEquipo`, `Asesoria` | De clase | «Sala»/«horas», «Equipo»/«días», «Asesoría»/«horas». |
| `TASA_SEGURO` | `AlquilerEquipo` | De clase | El 5 % de seguro de los equipos. |
| `NIVELES` | `Asesoria` | De clase | Diccionario con los multiplicadores 1,0 / 1,3 / 1,6. |
| `_estado`, `_historial` | `Reserva` | De instancia | Estado actual y lista de cambios de la reserva. |

## 3.7 ¿Qué es un método?

@nivel1
Si los atributos son lo que una cosa **tiene**, los métodos son lo que una cosa **sabe hacer**. Un empleado sabe presentarse, registrar su entrada y solicitar vacaciones. Una reserva sabe confirmarse y cancelarse.
@fin

@nivel2
Un **método** es una función que pertenece a una clase. Se define con `def` dentro de la clase y se usa con un punto: `objeto.metodo()`. La diferencia con una función normal es que el método trabaja **sobre los datos de su propio objeto**. Por eso su primer parámetro es siempre `self` (lo explicamos en la sección 3.9).

```python
class Reserva:
    def __init__(self, codigo):
        self.codigo = codigo
        self.estado = "Pendiente"

    def confirmar(self):
        self.estado = "Confirmada"

r = Reserva("R-0001")
r.confirmar()
print(r.estado)     # Confirmada
```

Cuando se escribe `r.confirmar()`, Python busca el método `confirmar` en la clase `Reserva` y lo ejecuta usando los datos del objeto `r`.
@fin

@nivel3
La clase `Reserva` real del proyecto tiene métodos para cambiar de estado. Mira cómo confirmar y cancelar trabajan sobre los atributos de la propia reserva:

::codigo modelos/reserva.py 86-100 | Métodos de la clase Reserva
::lineas
86-88 | Método interno `_cambiar_estado`: cambia el atributo `_estado` y agrega una línea al historial con la fecha y hora actual, el estado nuevo y una nota.
90 | Método `confirmar`. Solo necesita `self`, porque toda la información está en la propia reserva.
91-92 | Si la reserva no está «Pendiente», no se puede confirmar: se lanza un error (verás `raise` en el capítulo 9).
93-94 | Si el servicio fue deshabilitado mientras tanto, tampoco se puede confirmar.
95 | Si todo está bien, se cambia el estado a «Confirmada» usando el método interno.
97 | Método `cancelar`. Recibe un motivo; si no se le da ninguno, usa «Cancelada por el usuario».
98-99 | Solo se pueden cancelar reservas activas (Pendientes o Confirmadas).
100 | Cambia el estado a «Cancelada» y guarda el motivo en el historial.
::fin
@fin

### Tipos de métodos que verás en el proyecto

| Tipo | Cómo se reconoce | Primer parámetro | Ejemplo real |
|---|---|---|---|
| Método de instancia (el normal) | `def nombre(self, ...)` | `self` (el objeto) | `Reserva.confirmar(self)` |
| Método estático | Lleva encima `@staticmethod` | Ninguno especial | `Cliente._obligatorio(campo, valor)` |
| Método de clase | Lleva encima `@classmethod` | `cls` (la clase) | `Cliente._validar_identificacion(cls, valor)` |
| Propiedad | Lleva encima `@property` | `self` | `Cliente.nombre`, `Servicio.tarifa` |

Las palabras que empiezan con `@` y se escriben justo encima de un método se llaman **decoradores**. Un decorador es una etiqueta que le cambia o le agrega algo al método. Por ahora basta con saber reconocerlos; en el capítulo 4 verás con calma `@property` y `@abstractmethod`.

::codigo modelos/cliente.py 21-32 | Un método estático y un método de clase
::lineas
21 | `@staticmethod` indica que el método siguiente no necesita ni el objeto ni la clase: es una herramienta auxiliar que vive dentro de la clase por orden.
22-25 | `_obligatorio` revisa que un dato no esté vacío. Si está vacío lanza `ParametroFaltanteError`; si no, devuelve el dato sin espacios sobrantes.
27 | `@classmethod` indica que el método recibe la **clase** (`cls`) en lugar de un objeto.
28-32 | `_validar_identificacion` usa `cls._obligatorio` para revisar que no esté vacía y luego comprueba que tenga solo dígitos y entre 5 y 12 caracteres. Se usa como clase porque se necesita **antes** de que el objeto exista del todo (en la línea 15 del constructor).
::fin

@ejercicio: Atributo o método
En la frase «La reserva R-0002 tiene un total de $ 87.465 y se puede confirmar», ¿qué palabras corresponden a atributos y cuáles a métodos? Busca en el archivo `modelos/reserva.py` los nombres reales que usa el proyecto para cada uno.
@fin

## 3.8 ¿Qué es un constructor? ¿Qué significa `__init__`?

@nivel1
Cuando abres una cuenta en un banco, el asesor no te entrega una cuenta vacía y sin dueño: en el mismo momento de crearla te pide tu documento, tu nombre y tu dirección, y los verifica. Ese «trámite de apertura» que se hace una sola vez, al nacer la cuenta, es lo que en programación se llama **constructor**.
@fin

@nivel2
El **constructor** es un método especial que se ejecuta **automáticamente** cada vez que se crea un objeto. Su trabajo es dejar el objeto listo para usarse: recibir los datos iniciales, validarlos y guardarlos en atributos.

En Python, el constructor siempre se llama `__init__` (se lee «init», abreviatura de *initialize*, inicializar en inglés). Los **dos guiones bajos** a cada lado indican que es un método especial que Python conoce y llama por su cuenta; a estos métodos se les dice informalmente *dunder methods* («double underscore»). Tú nunca escribes `objeto.__init__(...)`: basta con escribir `Clase(...)`.

```python
class Sala:
    def __init__(self, nombre, capacidad):
        print("Creando la sala...")
        self.nombre = nombre
        self.capacidad = capacidad

auditorio = Sala("Auditorio", 60)   # aquí Python llama a __init__ solo
```

```salida
Creando la sala...
```

Lo que ocurre paso a paso cuando escribes `Sala("Auditorio", 60)`:

1. Python crea un objeto vacío de la clase `Sala`.
2. Llama a `__init__` pasándole ese objeto vacío como `self`, y los datos `"Auditorio"` y `60`.
3. El constructor guarda los datos en `self.nombre` y `self.capacidad`.
4. Python entrega el objeto ya lleno y lo guarda en la variable `auditorio`.
@fin

@nivel3
El constructor de `Reserva` es uno de los más completos del proyecto. Antes de que una reserva exista, comprueba que todo esté en orden:

::codigo modelos/reserva.py 24-46 | Constructor de la clase Reserva
::lineas
24 | El constructor recibe el cliente, el servicio, la duración y, opcionalmente, el impuesto y el descuento (si no se dan, valen `None`, que en Python significa «nada»).
25-26 | Comprueba que el cliente sea realmente un objeto de la clase `Cliente`. `isinstance` responde «sí» o «no» a la pregunta «¿este objeto fue fabricado con este molde?».
27-28 | Lo mismo con el servicio.
29-30 | Si el servicio está deshabilitado, no se puede reservar.
31-36 | Calcula el costo usando el método del servicio. Si algo inesperado falla, lo convierte en un error del sistema (capítulo 9).
38 | Llama al constructor de la clase general `Entidad` con un código consecutivo: `R-0001`, `R-0002`... El código solo se asigna cuando la reserva ya es válida.
39-44 | Guarda en atributos el cliente, el servicio, el impuesto, el descuento, los costos y la duración.
45 | Toda reserva nace en estado «Pendiente».
46 | Se inicia el historial con una primera anotación: «Reserva creada».
::fin
@fin

@importante
Si el constructor encuentra un problema y lanza un error, **el objeto no llega a existir**. Por eso en Software FJ es imposible tener un cliente con un correo mal escrito o una reserva con una duración fuera de rango: el constructor los rechaza antes de que nazcan.
@fin

### El constructor que llama a otro constructor: `super().__init__`

Muchas clases del proyecto empiezan su constructor con `super().__init__(...)`. La palabra `super()` significa «la clase de la que heredo» (la clase «madre»). Así, el constructor de `Cliente` primero le pide a `Entidad` que haga su parte (guardar el identificador y la fecha de creación) y luego hace la suya (guardar nombre, correo y teléfono). Lo estudiarás con detalle en el capítulo 4, en la sección de herencia.

::codigo modelos/entidad.py 6-11 | El constructor de la clase Entidad
::lineas
6 | Clase `Entidad`, la «madre» de clientes, servicios y reservas.
9 | Su constructor recibe el identificador.
10 | Lo guarda en el atributo `_identificador`.
11 | Guarda la fecha y hora exactas de creación usando `datetime.now()` («ahora»).
::fin

## 3.9 ¿Qué significa `self`?

@nivel1
Imagina un formulario que dice: «Escriba **su** nombre». La palabra «su» cambia de significado según quién llene el formulario: si lo llena Laura, «su nombre» es «Laura»; si lo llena Andrés, es «Andrés». El formulario es uno solo, pero «su» siempre se refiere a la persona que lo está usando en ese momento.
@fin

@nivel2
`self` es exactamente eso: una palabra que, dentro de una clase, significa «**este objeto**», el objeto con el que se está trabajando en ese momento. Como la clase se escribe una sola vez pero puede haber miles de objetos, los métodos necesitan saber **de cuál objeto** deben leer o cambiar los datos.

Cuando escribes `laura.describir()`, Python lo traduce internamente a `Cliente.describir(laura)`. Es decir, el objeto que está antes del punto se entrega como primer argumento, y dentro del método recibe el nombre `self`.

```python
class Cliente:
    def __init__(self, nombre):
        self.nombre = nombre          # «el nombre DE ESTE cliente»

    def saludar(self):
        return f"Hola, {self.nombre}"

laura = Cliente("Laura")
andres = Cliente("Andrés")
print(laura.saludar())    # aquí self es laura
print(andres.saludar())   # aquí self es andres
```

```salida
Hola, Laura
Hola, Andrés
```

Tres detalles importantes:

- `self` debe ser el **primer parámetro** de todo método de instancia.
- Al llamar el método **no** se escribe `self`: Python lo pone solo.
- `self` no es una palabra reservada; es una convención que todos los programadores de Python respetan. Podría llamarse de otra forma, pero nunca lo hagas.
@fin

@nivel3
En el proyecto, `self` aparece en casi todas las líneas de las clases. Mira el método `describir` de la clase `Cliente`:

::codigo modelos/cliente.py 79-88 | self en acción: describir y a_diccionario
::lineas
79 | El método recibe `self`, que será el cliente concreto que se quiere describir.
80 | Usa `self.nombre` y `self.identificacion`, es decir, el nombre y la identificación **de ese cliente**. Si el objeto es Laura, devuelve «Cliente Laura Gómez (ID 1032456789)».
82-88 | `a_diccionario` empaca los datos del cliente en un diccionario (una estructura de clave y valor que viste en el capítulo 2). La pantalla usa ese diccionario para llenar una fila de la tabla.
::fin

En el registro de eventos que viste en las capturas aparece exactamente el texto que produce este método: «Cliente registrado: Cliente Laura Gómez (ID 1032456789)».
@fin

::img 50_archivo_log | El texto «Cliente Laura Gómez (ID 1032456789)» del archivo de registro lo produjo el método describir de ese objeto.

@recuerda
- `self.algo = valor` **crea o cambia** un atributo del objeto actual.
- `self.algo` **lee** un atributo del objeto actual.
- `self.metodo()` **llama** a otro método del mismo objeto.
@fin

## 3.10 Todo junto: anatomía de una clase real

Ya conoces todas las piezas. Ahora vamos a mirar la clase `Cliente` completa como si la estuviéramos desarmando sobre una mesa. Lee primero el código y después la tabla.

::codigo modelos/cliente.py 1-48 | La clase Cliente (primera parte)

| Líneas | Pieza | Qué es |
|---|---|---|
| 1 | Docstring del archivo | Explica de qué trata el archivo. |
| 2 | `import re` | Trae la herramienta de Python para revisar patrones de texto (expresiones regulares). |
| 4-5 | Otros `import` | Traen las excepciones del proyecto y la clase `Entidad`. |
| 7-8 | Constantes del módulo | Patrones que dicen cómo debe verse un correo y un nombre válidos. |
| 11 | `class Cliente(Entidad):` | Declaración de la clase. |
| 14-18 | `__init__` | Constructor. |
| 21-25 | `@staticmethod` | Método auxiliar para datos obligatorios. |
| 27-32 | `@classmethod` | Validación de la identificación. |
| 35-48 | `@property` y `.setter` | Lectura y escritura controlada de identificación y nombre (capítulo 4). |

::codigo modelos/cliente.py 50-88 | La clase Cliente (segunda parte)

| Líneas | Pieza | Qué es |
|---|---|---|
| 50-59 | Propiedad `correo` | Lee y valida el correo; lo guarda en minúsculas. |
| 61-70 | Propiedad `telefono` | Lee y valida el teléfono; quita espacios y guiones. |
| 72-76 | Propiedad `correo_oculto` | Devuelve el correo parcialmente oculto, por ejemplo `la***@mail.com`. |
| 79-80 | `describir` | Método obligatorio que exige la clase `Entidad`. |
| 82-88 | `a_diccionario` | Segundo método obligatorio exigido por `Entidad`. |

@nota
La propiedad `correo_oculto` existe en el código, pero ninguna pantalla de la versión actual la utiliza. Es un buen ejemplo de una capacidad preparada para un uso futuro (por ejemplo, mostrar correos en un informe sin revelarlos completos).
@fin

### Ejemplo de funcionamiento

Si tuvieras que probar la clase `Cliente` desde la consola de Python, ubicado en la carpeta del proyecto, podrías escribir lo siguiente. El resultado corresponde exactamente a lo que hace el código mostrado:

```python
from modelos.cliente import Cliente

laura = Cliente("1032456789", "laura gómez", "LAURA.GOMEZ@MAIL.COM", "310 456 7890")
print(laura.nombre)
print(laura.correo)
print(laura.telefono)
print(laura.describir())
```

```salida
Laura Gómez
laura.gomez@mail.com
3104567890
Cliente Laura Gómez (ID 1032456789)
```

Observa cómo el objeto «se arregla» solo: el nombre quedó con mayúsculas iniciales, el correo en minúsculas y el teléfono sin espacios. Eso lo hacen los métodos de la clase, no la pantalla.

## 3.11 Más ejemplos con clientes, empleados, salas y reservas

Para fijar las ideas, aquí tienes un pequeño programa didáctico que **no** forma parte de Software FJ pero imita su organización. Léelo con calma e identifica clases, objetos, atributos, métodos, constructor y `self`.

```python
class Sala:
    def __init__(self, nombre, tarifa_hora, capacidad):
        self.nombre = nombre
        self.tarifa_hora = tarifa_hora
        self.capacidad = capacidad

    def costo(self, horas):
        return self.tarifa_hora * horas


class Reserva:
    def __init__(self, cliente, sala, horas):
        self.cliente = cliente
        self.sala = sala
        self.horas = horas
        self.estado = "Pendiente"

    def total(self):
        return self.sala.costo(self.horas)

    def confirmar(self):
        self.estado = "Confirmada"


ejecutiva = Sala("Sala Ejecutiva", 50000, 12)
r1 = Reserva("Laura Gómez", ejecutiva, 3)
r1.confirmar()
print(r1.estado, r1.total())
```

```salida
Confirmada 150000
```

| Elemento | Dónde aparece |
|---|---|
| Clases | `Sala`, `Reserva` |
| Objetos | `ejecutiva`, `r1` |
| Atributos | `nombre`, `tarifa_hora`, `capacidad`, `cliente`, `sala`, `horas`, `estado` |
| Métodos | `costo`, `total`, `confirmar` |
| Constructores | Los dos `__init__` |
| Un objeto dentro de otro | El atributo `sala` de la reserva guarda el objeto `ejecutiva` |

El último renglón es muy importante: **un objeto puede guardar a otro objeto como atributo**. En Software FJ ocurre igual: cada `Reserva` guarda dentro de sí al objeto `Cliente` y al objeto `Servicio` (líneas 39 y 40 de `modelos/reserva.py`). A esta relación se le llama **composición** o **asociación**: la reserva «tiene un» cliente y «tiene un» servicio.

@consejo
Una buena forma de descubrir las clases de un problema es subrayar los **sustantivos** del enunciado (cliente, sala, reserva, empleado) y los **verbos** (registrar, confirmar, cancelar). Los sustantivos suelen convertirse en clases y atributos; los verbos, en métodos.
@fin

@ejercicio: Diseña tu propia clase
Escribe en papel una clase `Empleado` para Software FJ que tenga como atributos `documento`, `nombre` y `cargo`, y un método `describir` que devuelva un texto como «Empleado Ana Torres (Recepcionista)». Compárala con la clase `Cliente` real: ¿qué se parece y qué cambia?

*Nota:* Software FJ no tiene una clase `Empleado`; este ejercicio es solo para practicar.
@fin

@ejercicio: Lectura de código
Abre `modelos/servicios.py` y responde: ¿cuál es el constructor de la clase `AlquilerEquipo`? ¿Qué atributos de instancia crea? ¿Qué atributos de clase tiene? (Ayuda: busca las líneas 209 a 222.)
@fin

@resumen
- La **programación orientada a objetos** organiza el código alrededor de objetos que reúnen datos y acciones.
- Existe para ordenar programas grandes: separa responsabilidades, protege los datos y permite reutilizar código.
- Una **clase** es un molde (`class Cliente`); un **objeto** es un ejemplar concreto (`Cliente("1032456789", ...)`).
- Un **atributo** es un dato del objeto; puede ser de instancia (propio) o de clase (compartido).
- Un **método** es una acción del objeto; se define con `def` dentro de la clase.
- El **constructor** `__init__` se ejecuta solo al crear el objeto y lo deja listo y validado.
- `self` significa «este objeto» y es el primer parámetro de los métodos de instancia.
- En Software FJ, los objetos `Cliente` nacen en `GestorClientes.registrar` (línea 16) y las reservas validan todo en su constructor antes de existir.
@fin
