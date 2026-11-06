# Los cinco pilares de la POO
> Abstracción, encapsulación, herencia, polimorfismo y sobrecarga: las cinco ideas que sostienen el diseño de Software FJ.

@objetivos
- Explicar con ejemplos cotidianos los cinco pilares de la programación orientada a objetos.
- Reconocer cada pilar en el código real de Software FJ y señalar el archivo y las líneas exactas.
- Entender qué son `ABC` y `@abstractmethod`, `@property` y `.setter`, y los atributos con doble guion bajo.
- Diferenciar con claridad la **sobrescritura** de la **sobrecarga**, y saber por qué Python no tiene sobrecarga tradicional.
- Defender ante un docente cómo el proyecto aplica cada pilar.
@fin

En el capítulo 3 aprendiste las piezas básicas: clases, objetos, atributos, métodos, constructor y `self`. Con esas piezas se puede escribir código ordenado, pero la verdadera fuerza de la POO aparece cuando se combinan siguiendo ciertos principios. Los libros suelen hablar de **cuatro pilares** (abstracción, encapsulación, herencia y polimorfismo); la guía de tu curso agrega un quinto tema, la **sobrecarga de métodos**, que en Python tiene una historia particular. Los veremos uno por uno.

::img d_uml_modelos | Mapa de clases del proyecto. Lo usaremos como referencia en todo el capítulo.

## 4.1 Abstracción

@nivel1
Cuando conduces un carro usas el volante, los pedales y la palanca de cambios. No necesitas saber cómo funciona la inyección de combustible ni cómo se sincronizan las válvulas del motor. El carro te ofrece **lo esencial** para manejarlo y esconde los detalles.

Otro ejemplo: en un restaurante, el menú dice «Bandeja paisa – $ 25.000». No te explica la receta. Te da exactamente la información que necesitas para pedir.
@fin

@nivel2
La **abstracción** consiste en quedarse con las características **importantes** de algo y dejar de lado los detalles que no importan para el problema. En la POO se aplica de dos maneras:

1. **Al diseñar clases**: un cliente real tiene estatura, color de ojos y comida favorita, pero a Software FJ solo le importan su identificación, nombre, correo y teléfono. La clase `Cliente` es una abstracción de una persona.
2. **Con clases abstractas**: son clases que definen *qué* deben saber hacer sus «hijas», sin decir *cómo*. Son contratos. No se pueden usar para crear objetos directamente; solo sirven de molde para otras clases.

En Python, las clases abstractas se crean con el módulo `abc` (sigla de *Abstract Base Classes*, «clases base abstractas»):

- `ABC` es la clase de la que se hereda para volverse abstracta.
- `@abstractmethod` es un decorador (una etiqueta encima del método) que marca un método como **obligatorio**: toda clase hija tendrá que escribirlo.

```python
from abc import ABC, abstractmethod

class Figura(ABC):
    @abstractmethod
    def area(self):
        """Cada figura debe saber calcular su área."""

class Cuadrado(Figura):
    def __init__(self, lado):
        self.lado = lado

    def area(self):
        return self.lado * self.lado

Cuadrado(3).area()   # 9
Figura()             # ERROR: no se puede crear una figura «en abstracto»
```
@fin

@nivel3
Software FJ tiene **dos** clases abstractas. La primera es `Entidad`, la clase general de la que heredan clientes, servicios y reservas:

::codigo modelos/entidad.py 1-27 | La clase abstracta Entidad
::lineas
2 | Se importan `ABC` y `abstractmethod` del módulo `abc` de Python.
3 | Se importa `datetime`, para saber la fecha y hora actuales.
6 | `class Entidad(ABC)`: al heredar de `ABC`, `Entidad` se vuelve una clase abstracta.
9-11 | Constructor común: toda entidad tiene un identificador y una fecha de creación.
13-19 | Dos propiedades de solo lectura para consultar esos datos.
21-23 | `describir` es **abstracto**: toda entidad debe saber describirse, pero cada una lo hará a su manera.
25-27 | `a_diccionario` también es abstracto: toda entidad debe poder convertirse en un diccionario para las tablas.
::fin

La segunda es `Servicio`. Hereda de `Entidad` y agrega su propio contrato: todo servicio debe decir su tipo, su unidad de tiempo, cómo valida la duración, cómo calcula su costo base y cómo se describe en detalle.

::codigo modelos/servicios.py 95-116 | El contrato abstracto de Servicio
::lineas
96-99 | `tipo` es una propiedad abstracta: cada servicio debe decir si es «Sala», «Equipo» o «Asesoría».
101-104 | `unidad` es abstracta: «horas» o «días».
106-108 | `validar_parametros`: cada tipo tiene sus propios límites de duración.
110-112 | `calcular_costo_base`: cada tipo tiene su propia regla de precio.
114-116 | `detalle`: cada tipo describe sus datos propios.
::fin

Si alguien intenta crear un servicio «genérico», Python lo impide. Esta es la respuesta real que da Python al ejecutar `Servicio("X", "abc", 1, 1)` en el proyecto:

```salida
TypeError: Can't instantiate abstract class Servicio without an implementation
for abstract methods 'calcular_costo_base', 'detalle', 'tipo', 'unidad', 'validar_parametros'
```

Es decir: «no puedo crear un Servicio abstracto porque le faltan esos cinco métodos». Solo se pueden crear `ReservaSala`, `AlquilerEquipo` o `Asesoria`, que sí los escriben.
@fin

@recuerda
**Abstraer** es decidir qué es lo esencial. Una **clase abstracta** es un contrato: dice qué debe hacerse, no cómo. Sus métodos marcados con `@abstractmethod` son obligatorios para las clases hijas.
@fin

## 4.2 Encapsulación

@nivel1
Piensa en un **cajero automático**. El dinero está guardado dentro de una caja fuerte. Nadie puede meter la mano y sacar billetes: hay que usar la pantalla, poner la tarjeta y la clave, y el cajero verifica todo antes de entregar dinero. El cajero **protege** lo que guarda y solo permite usarlo a través de **operaciones controladas**.

Otro ejemplo: en un hospital, la historia clínica no se puede modificar libremente; cada cambio pasa por un médico autorizado que verifica y firma.
@fin

@nivel2
La **encapsulación** consiste en **proteger los datos de un objeto** para que no se puedan cambiar de cualquier manera desde afuera. Los datos se guardan «encerrados» dentro del objeto y solo se leen o modifican a través de métodos que verifican que el cambio sea correcto.

Python no tiene candados absolutos como otros lenguajes, pero ofrece tres herramientas:

| Herramienta | Cómo se escribe | Qué significa |
|---|---|---|
| Atributo público | `self.nombre` | Cualquiera puede leerlo y cambiarlo. |
| Atributo «protegido» (convención) | `self._nombre` | Un guion bajo: «es interno, por favor no lo toques desde fuera». Python no lo impide, es un acuerdo entre programadores. |
| Atributo «privado» (*name mangling*) | `self.__nombre` | Dos guiones bajos: Python le **cambia el nombre** internamente a `_Clase__nombre`, de modo que desde fuera no se encuentra con el nombre original. |
| Propiedad | `@property` y `@x.setter` | Permite leer y escribir como si fuera un atributo, pero en realidad se ejecuta un método que puede validar. |

**¿Qué es una propiedad?** Es un método disfrazado de atributo. Con `@property` escribes un método que se ejecuta cuando alguien **lee** el dato (`cliente.nombre`). Con `@nombre.setter` escribes el método que se ejecuta cuando alguien **asigna** el dato (`cliente.nombre = "Ana"`). Quien usa la clase no nota la diferencia, pero tú controlas cada lectura y cada cambio.

```python
class CuentaBancaria:
    def __init__(self, saldo):
        self.__saldo = saldo

    @property
    def saldo(self):              # se ejecuta al leer cuenta.saldo
        return self.__saldo

    @saldo.setter
    def saldo(self, valor):       # se ejecuta al escribir cuenta.saldo = ...
        if valor < 0:
            raise ValueError("El saldo no puede ser negativo")
        self.__saldo = valor
```
@fin

@nivel3
La clase `Cliente` es el mejor ejemplo de encapsulación del proyecto. Sus datos personales se guardan en atributos con doble guion bajo y **cada asignación pasa por una validación**:

::codigo modelos/cliente.py 39-59 | Propiedades encapsuladas de Cliente
::lineas
39-41 | `@property nombre`: cuando alguien lee `cliente.nombre`, se devuelve el atributo privado `__nombre`.
43 | `@nombre.setter`: este método se ejecuta cada vez que alguien escribe `cliente.nombre = algo`.
45 | Primero se verifica que el nombre no esté vacío.
46-47 | Si tiene menos de 3 letras o contiene números o símbolos, se rechaza con un error.
48 | Si es válido, se guarda con cada palabra iniciando en mayúscula: «laura gómez» se convierte en «Laura Gómez».
50-52 | Propiedad de lectura del correo.
54-59 | Setter del correo: lo convierte a minúsculas, comprueba el formato con un patrón y solo entonces lo guarda.
::fin

Recuerda el constructor de `Cliente` (líneas 14 a 18). Allí se escribía simplemente `self.nombre = nombre`. Ahora entiendes por qué esa línea **valida**: como `nombre` es una propiedad con *setter*, la asignación ejecuta el método de las líneas 44 a 48.

Esto es lo que ocurre si alguien intenta saltarse las reglas desde fuera (resultados reales en el proyecto):

```python
laura = Cliente("1032456789", "laura gómez", "LAURA.GOMEZ@MAIL.COM", "310 456 7890")

laura.correo = "malo"          # intenta poner un correo inválido
```

```salida
DatoInvalidoError: [FJ-101] Valor inválido para 'correo' ('malo'): formato de correo no válido
```

```python
print(laura.correo)            # el dato anterior sigue intacto
print(laura.__nombre)          # intenta leer el atributo privado directamente
```

```salida
laura.gomez@mail.com
AttributeError: 'Cliente' object has no attribute '__nombre'
```

El correo malo no se guardó y el atributo privado no se encuentra con su nombre original. (Técnicamente, Python lo guardó como `_Cliente__nombre`; por eso decimos que en Python la privacidad es un acuerdo fuerte, no un candado absoluto.)

En otras clases del proyecto la encapsulación es más sencilla: los atributos llevan un solo guion bajo y se exponen con propiedades de **solo lectura** (con `@property` pero sin *setter*). Así nadie puede cambiar la tarifa de un servicio o el estado de una reserva sin pasar por sus métodos:

::codigo modelos/servicios.py 69-93 | Propiedades de solo lectura y métodos controlados de Servicio
::lineas
69-87 | Propiedades `codigo`, `nombre`, `tarifa`, `cupo` y `disponible`: se pueden leer, pero no tienen *setter*, así que no se pueden asignar desde fuera.
89-93 | La única forma de cambiar la disponibilidad es a través de los métodos `habilitar` y `deshabilitar`.
::fin
@fin

::img 06_campo_invalido | La encapsulación en acción: la clase Cliente rechazó el correo «maria.ruiz@» y la pantalla marcó el campo en rojo.

@consejo
Para la sustentación: «Aplicamos encapsulación en la clase `Cliente` con atributos privados `__nombre`, `__correo` y `__telefono`, y propiedades con *setter* que validan cada dato antes de guardarlo. En las demás clases usamos atributos protegidos con un guion bajo y propiedades de solo lectura.»
@fin

## 4.3 Herencia

@nivel1
En una familia, los hijos heredan rasgos de sus padres: el color de ojos, el apellido. Pero cada hijo también tiene cosas propias. En el mundo laboral pasa algo parecido: todos los **empleados** de una empresa tienen documento, nombre y salario, pero un **vendedor** además tiene comisiones y un **conductor** tiene licencia de conducción. No tiene sentido volver a describir desde cero «nombre y documento» para cada cargo: todos lo heredan de la idea general de «empleado».
@fin

@nivel2
La **herencia** permite crear una clase nueva a partir de otra que ya existe. La clase nueva (llamada **hija**, **subclase** o **clase derivada**) recibe automáticamente todos los atributos y métodos de la clase original (llamada **madre**, **superclase** o **clase base**), y puede:

- **Agregar** atributos y métodos nuevos.
- **Reemplazar** (sobrescribir) métodos que hereda, para hacerlos a su manera.

En Python, la herencia se indica poniendo la clase madre entre paréntesis: `class Vendedor(Empleado):`. Para usar el constructor de la madre desde la hija se escribe `super().__init__(...)`.

```python
class Empleado:
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario

class Vendedor(Empleado):                   # Vendedor hereda de Empleado
    def __init__(self, nombre, salario, comision):
        super().__init__(nombre, salario)   # la madre guarda nombre y salario
        self.comision = comision            # la hija agrega lo suyo
```

La herencia expresa una relación de tipo **«es un»**: un vendedor **es un** empleado.
@fin

@nivel3
Software FJ tiene un árbol de herencia de tres niveles:

::img d_herencia | Árbol de herencia de Software FJ: Entidad → Cliente / Servicio / Reserva, y Servicio → ReservaSala / AlquilerEquipo / Asesoria.

| Clase hija | Hereda de | Qué recibe de la madre | Qué agrega |
|---|---|---|---|
| `Cliente` | `Entidad` | identificador, fecha de creación, comparación entre objetos | nombre, correo, teléfono y sus validaciones |
| `Servicio` | `Entidad` | lo mismo | tarifa, cupo, disponibilidad, cálculo del costo |
| `Reserva` | `Entidad` | lo mismo | cliente, servicio, costos, estado, historial |
| `ReservaSala` | `Servicio` | todo lo de `Servicio` y `Entidad` | capacidad, recargo del 10 % |
| `AlquilerEquipo` | `Servicio` | todo lo de `Servicio` y `Entidad` | tipo de equipo, seguro del 5 % |
| `Asesoria` | `Servicio` | todo lo de `Servicio` y `Entidad` | especialidad, nivel |

Mira cómo `AlquilerEquipo` usa la herencia:

::codigo modelos/servicios.py 209-238 | La clase AlquilerEquipo hereda de Servicio
::lineas
209 | `class AlquilerEquipo(Servicio)`: un alquiler de equipo **es un** servicio.
212 | Atributo de clase propio: la tasa del seguro, 5 %.
214 | Constructor de la hija. Recibe la tarifa por día, el tipo de equipo y las unidades.
215 | `super().__init__(...)` pide a `Servicio` que guarde y valide código, nombre, tarifa y cupo. Las «unidades» del equipo se usan como cupo.
216-219 | La hija valida y guarda su dato propio: el tipo de equipo.
221-222 | Responde al contrato abstracto: su tipo es «Equipo» y su unidad son «días».
228-232 | Su propia validación: de 1 a 30 días y solo días completos.
234-235 | Su propia regla de precio: tarifa × días × 1,05.
237-238 | Su propio detalle.
::fin

Gracias a la herencia, `AlquilerEquipo` **no** tiene que volver a escribir cómo se valida la tarifa, cómo se habilita o deshabilita, ni cómo se aplican el impuesto y el descuento: todo eso lo hereda de `Servicio`.
@fin

@nota
Las clases de la interfaz también usan herencia. `VistaClientes`, `VistaServicios`, `VistaReservas`, `VistaDashboard` y `VistaEventos` heredan de `VistaBase` (archivo `interfaz/componentes.py`), y `VentanaPrincipal` hereda de `tk.Tk`, la clase de Tkinter que representa una ventana. Lo verás en el capítulo 5.
@fin

## 4.4 Polimorfismo

@nivel1
La palabra **polimorfismo** viene del griego y significa «muchas formas». Imagina que en una empresa el jefe dice en voz alta: «¡Todos, calculen su pago del mes!». El empleado por horas multiplica sus horas por su tarifa; el vendedor suma su salario más las comisiones; el practicante recibe un auxilio fijo. **Una sola orden**, y cada uno la cumple **a su manera**. El jefe no necesita preguntar «¿tú qué tipo de empleado eres?» antes de dar la orden.

Otro ejemplo cotidiano: el botón de «reproducir» funciona en un video, en una canción y en un audiolibro. Es el mismo botón, pero cada cosa se reproduce como le corresponde.
@fin

@nivel2
En programación, **polimorfismo** significa que objetos de clases distintas responden al **mismo mensaje** (el mismo nombre de método) cada uno con su propio comportamiento. Quien llama al método no necesita saber de qué clase exacta es el objeto; solo confía en que sabe hacer esa acción.

El polimorfismo normalmente se logra combinando herencia con **sobrescritura de métodos**: la clase madre declara un método y cada clase hija escribe su propia versión con el mismo nombre. A esa acción de «volver a escribir en la hija un método que ya existe en la madre» se le llama **sobrescribir** (en inglés, *override*).

```python
class Empleado:
    def pago(self):
        return 0

class PorHoras(Empleado):
    def __init__(self, horas, tarifa):
        self.horas, self.tarifa = horas, tarifa
    def pago(self):                       # sobrescribe pago()
        return self.horas * self.tarifa

class Practicante(Empleado):
    def pago(self):                       # sobrescribe pago()
        return 1300000

for e in [PorHoras(10, 20000), Practicante()]:
    print(e.pago())                       # una sola orden, dos formas
```
@fin

@nivel3
El polimorfismo es el corazón del cálculo de precios de Software FJ. Las tres clases de servicio sobrescriben el método `calcular_costo_base`, cada una con su regla:

::codigo modelos/servicios.py 201-203 | ReservaSala: recargo del 10 % para salas grandes
::codigo modelos/servicios.py 234-235 | AlquilerEquipo: seguro del 5 %
::codigo modelos/servicios.py 270-271 | Asesoria: multiplicador según el nivel

Y la clase madre `Servicio` usa ese método **sin saber** de qué tipo es el servicio:

::codigo modelos/servicios.py 128-136 | Servicio.calcular_costo_detallado llama a los métodos polimórficos
::lineas
128 | Método común a todos los servicios, escrito una sola vez en la clase madre.
129 | `self.validar_parametros(duracion)`: si `self` es una sala, se ejecuta la validación de 1 a 12 horas; si es un equipo, la de 1 a 30 días enteros; si es una asesoría, la de 0,5 a 8 horas.
130 | `self.calcular_costo_base(duracion)`: igual que arriba, cada servicio aplica su propia regla.
131-136 | Lo demás (descuento, impuesto y total) es igual para todos, así que se escribe una sola vez.
::fin

Gracias al polimorfismo, el gestor de reservas puede crear una reserva de una sala, de un equipo o de una asesoría con exactamente la misma instrucción, y el precio siempre sale correcto. Si mañana se agrega un cuarto tipo de servicio (por ejemplo, «Transporte»), basta con crear la clase nueva con sus cinco métodos; **no hay que tocar** ni `calcular_costo_detallado`, ni los gestores, ni las pantallas.

Hay más polimorfismo en el proyecto:

| Método polimórfico | Clases que lo escriben a su manera | Quién lo llama sin saber la clase exacta |
|---|---|---|
| `describir()` | `Cliente`, `Servicio`, `Reserva` | Los gestores, al anotar en el registro de eventos. |
| `a_diccionario()` | `Cliente`, `Servicio`, `Reserva` | Las vistas, al llenar las tablas. |
| `detalle()` | `ReservaSala`, `AlquilerEquipo`, `Asesoria` | `Servicio.describir` y `Servicio.a_diccionario`. |
| `refrescar()` | Las cinco vistas | `VentanaPrincipal.notificar_cambio`. |
| `__eq__`, `__hash__`, `__repr__` | `Entidad` (sobrescribe los de `object`) | Python, al comparar o imprimir objetos. |

::codigo interfaz/ventana_principal.py 161-167 | Polimorfismo en la interfaz: una orden para cinco vistas distintas
::lineas
163 | Recorre todas las vistas: panel principal, clientes, servicios, reservas y eventos.
165 | A cada una le dice «refréscate». Cada vista sabe recargar sus propias tablas a su manera.
166-167 | Si alguna falla, se anota el error y se continúa con las demás.
::fin
@fin

::img 20_catalogo | Un catálogo con salas, equipos y asesorías: cada fila se dibuja con el mismo método a_diccionario, pero el detalle y la tarifa salen de la versión propia de cada clase.

## 4.5 Sobrecarga de métodos

Este es el pilar que más confusión genera, porque **Python funciona diferente a lenguajes como Java o C++**. Vamos despacio.

@nivel1
Piensa en una cafetería donde puedes pedir «un café», «un café con leche» o «un café con leche y azúcar». Es el **mismo pedido** («café») con **distintas cantidades de detalles**. La persona que atiende entiende las tres formas y prepara lo que corresponde.
@fin

@nivel2
La **sobrecarga de métodos** (en inglés, *overloading*) significa tener **varios métodos con el mismo nombre en la misma clase**, que se diferencian por la cantidad o el tipo de sus parámetros. A la combinación «nombre + lista de parámetros» se le llama **firma** del método. En Java, por ejemplo, se puede escribir:

```consola
// Ejemplo en Java (no es Python)
double calcularCosto(double duracion) { ... }
double calcularCosto(double duracion, double impuesto) { ... }
double calcularCosto(double duracion, double impuesto, double descuento) { ... }
```

y Java elige automáticamente cuál ejecutar según cuántos datos le pases.

**Python NO permite esto.** Si en una clase de Python escribes dos métodos con el mismo nombre, el segundo simplemente **reemplaza** al primero; el primero desaparece:

```python
class Prueba:
    def saludo(self):
        return "Hola"

    def saludo(self, nombre):         # reemplaza al anterior
        return f"Hola, {nombre}"

Prueba().saludo()                     # ERROR: falta el argumento «nombre»
```

Entonces, ¿cómo se consigue en Python el efecto de la sobrecarga? Con **parámetros opcionales**, también llamados **valores por defecto**. Un parámetro opcional tiene un valor que se usa cuando quien llama no lo envía:

```python
def pedir_cafe(tamano, leche=False, azucar=0):
    ...

pedir_cafe("mediano")
pedir_cafe("mediano", True)
pedir_cafe("mediano", True, 2)
```

Un solo método acepta varias formas de llamarlo. A esto se le dice **simular** la sobrecarga. Python ofrece además otras herramientas para casos más avanzados (como `*args` o `functools.singledispatch`), pero Software FJ no las usa.
@fin

@nivel3
Software FJ simula la sobrecarga en el método `calcular_costo` de la clase `Servicio`. El propio archivo lo documenta al inicio:

::codigo modelos/servicios.py 8-12 | Documentación de la «sobrecarga» en el encabezado del archivo
::codigo modelos/servicios.py 118-126 | Un solo método, tres formas de llamarlo
::lineas
118 | El comentario dice «métodos "sobrecargados"» entre comillas: los autores sabían que es una sobrecarga simulada.
119 | `impuesto=None` y `descuento=None` son parámetros opcionales. Si no se envían, valen `None` («nada»).
120-125 | La documentación explica las tres variantes de uso.
126 | Todas las variantes terminan en el mismo cálculo detallado; luego se toma solo el total.
::fin

Con una sala de $ 50.000 por hora y capacidad para 12 personas, las tres formas dan estos resultados reales (el impuesto y el descuento se expresan aquí como fracciones: 0.19 significa 19 %):

| Forma de llamarlo | Qué calcula | Resultado |
|---|---|---|
| `sala.calcular_costo(3)` | Solo el costo base (3 horas) | 150000.0 |
| `sala.calcular_costo(3, 0.19)` | Base más 19 % de impuesto | 178500.0 |
| `sala.calcular_costo(3, 0.19, 0.10)` | Base menos 10 % de descuento, más 19 % de impuesto | 160650.0 |

En las pantallas, el usuario escribe los porcentajes como «19» o «10»; antes de llamar a este método, la función `porcentaje_a_fraccion` (líneas 23 a 33 del mismo archivo) los convierte a 0.19 y 0.10.
@fin

@importante
Si un docente te pregunta «¿Dónde está la sobrecarga en su proyecto?», la respuesta honesta y correcta es: «Python no admite sobrecarga por firma como Java. La simulamos en `Servicio.calcular_costo` con parámetros opcionales (`impuesto=None`, `descuento=None`), de modo que el mismo método se puede llamar con uno, dos o tres argumentos.» Esa honestidad suma puntos: demuestra que entiendes cómo funciona el lenguaje.
@fin

### Sobrescritura frente a sobrecarga

Estas dos palabras se parecen mucho en español, pero significan cosas muy diferentes:

| | Sobrescritura (*override*) | Sobrecarga (*overload*) |
|---|---|---|
| ¿Qué es? | Una clase **hija** vuelve a escribir un método que ya tenía la **madre**, con el mismo nombre. | Varias versiones de un método con el mismo nombre en la **misma clase**, distinguidas por sus parámetros. |
| ¿Dónde ocurre? | Entre dos clases relacionadas por herencia. | Dentro de una sola clase. |
| ¿Para qué sirve? | Para el polimorfismo: cada clase hace la acción a su manera. | Para aceptar distintas combinaciones de datos. |
| ¿Python la admite? | **Sí**, de forma natural. | **No** por firma; se **simula** con parámetros opcionales. |
| Ejemplo cotidiano | Cada empleado calcula «su pago» a su manera. | Pedir «café», «café con leche» o «café con leche y azúcar». |
| Ejemplo en Software FJ | `calcular_costo_base` en `ReservaSala`, `AlquilerEquipo` y `Asesoria`. | `Servicio.calcular_costo(duracion, impuesto=None, descuento=None)`. |

@ejercicio: ¿Sobrescritura o sobrecarga?
Para cada caso, di si es sobrescritura, sobrecarga simulada o ninguna:
1. `Cliente.describir` y `Reserva.describir`.
2. `cancelar(self, motivo="Cancelada por el usuario")` en la clase `Reserva`.
3. `Entidad.__repr__`.
4. `Asesoria.__init__(..., nivel="Básico", cupo=1)`.

*Pista:* busca si el método existe también en una clase madre y si tiene parámetros con valor por defecto.
@fin

## 4.6 Sobrescritura de métodos especiales: `__eq__`, `__hash__` y `__repr__`

@nivel1
Dos billetes de $ 50.000 son físicamente diferentes, pero para pagar valen lo mismo. En cambio, dos cédulas con el mismo número representan a **la misma persona**, aunque una sea el original y la otra una fotocopia. Cada tipo de cosa tiene su propia regla para decidir si dos ejemplares «son iguales».
@fin

@nivel2
Todas las clases de Python heredan, sin que lo escribas, de una clase madre universal llamada `object`. Esa clase trae unos **métodos especiales** (los de doble guion bajo, como `__init__`) que Python llama automáticamente en ciertas situaciones:

| Método especial | Python lo llama cuando... | Comportamiento heredado de `object` |
|---|---|---|
| `__eq__(self, otro)` | se compara con `==`. | Dos objetos solo son iguales si son exactamente el mismo objeto en memoria. |
| `__hash__(self)` | el objeto se usa en un conjunto (`set`) o como clave de diccionario. | Un número basado en la posición en memoria. |
| `__repr__(self)` | se muestra el objeto en la consola o dentro de una lista. | Algo poco útil como `<Cliente object at 0x000002A1...>`. |

Si una clase escribe su propia versión de esos métodos, los está **sobrescribiendo**, igual que hacen las hijas con los métodos de su madre. Es otra forma de polimorfismo: el operador `==` funciona para números, textos y clientes, pero cada uno decide a su manera qué significa «igual».
@fin

@nivel3
La clase `Entidad` sobrescribe los tres métodos para que todas las entidades del proyecto se comporten de forma razonable:

::codigo modelos/entidad.py 29-37 | Entidad sobrescribe __eq__, __hash__ y __repr__
::lineas
29-31 | Dos entidades son iguales si son de **la misma clase** y tienen **el mismo identificador**. Dos objetos `Cliente` con la identificación 1032456789 se consideran el mismo cliente, como las dos cédulas del ejemplo.
33-34 | El «hash» se calcula a partir del nombre de la clase y del identificador, de modo que coincida con la regla de igualdad.
36-37 | La representación muestra el nombre de la clase y el identificador. Así, al imprimir una lista de clientes en la consola se ve `[Cliente('1032456789'), Cliente('80123456')]` en lugar de direcciones de memoria.
::fin

Gracias a la herencia, `Cliente`, `Servicio` (y sus tres hijas) y `Reserva` reciben este comportamiento sin escribir una sola línea adicional.
@fin

@nota
La regla `type(self) is type(otro)` de la línea 30 evita una confusión: aunque un cliente y un servicio tuvieran por casualidad el mismo identificador, nunca se considerarían iguales, porque son de clases distintas.
@fin

## 4.7 Caso práctico: ¿qué haría falta para agregar un nuevo servicio?

Una excelente manera de comprobar que entiendes los pilares es imaginar un cambio en el proyecto. Supongamos que la empresa quiere ofrecer **transporte de equipos**, cobrado por kilómetro. Este ejemplo es **didáctico**: el servicio «Transporte» **no existe** en Software FJ.

@ejemplo: Una clase hipotética Transporte
```python
class Transporte(Servicio):                 # HERENCIA: un transporte es un servicio
    """Servicio hipotético cobrado por kilómetro (no existe en el proyecto)."""

    tipo = "Transporte"                     # cumple el contrato ABSTRACTO
    unidad = "kilómetros"

    def __init__(self, codigo, nombre, tarifa_km, vehiculo, cupo=1):
        super().__init__(codigo, nombre, tarifa_km, cupo)
        self._vehiculo = vehiculo           # ENCAPSULACIÓN: atributo protegido

    def validar_parametros(self, duracion):
        return self._validar_rango(duracion, 1, 300)

    def calcular_costo_base(self, duracion):    # POLIMORFISMO: su propia regla
        return self.tarifa * duracion

    def detalle(self):
        return f"Vehículo {self._vehiculo}"
```
@fin

Analicemos qué se aprovecharía de cada pilar:

| Pilar | Cómo ayuda en este cambio |
|---|---|
| Abstracción | La clase `Servicio` dice exactamente qué cinco cosas hay que escribir. Si se olvida una, Python avisa al intentar crear el objeto. |
| Herencia | La validación del código, el nombre, la tarifa y el cupo, la habilitación y el cálculo con impuesto y descuento ya existen en `Servicio`. |
| Encapsulación | El vehículo se guarda como `_vehiculo` y nadie lo cambia desde fuera. |
| Polimorfismo | `calcular_costo_detallado`, el gestor de reservas y la tabla de reservas funcionarían sin cambios, porque solo llaman a métodos que todo servicio tiene. |
| Sobrecarga (simulada) | `calcular_costo(km)`, `calcular_costo(km, impuesto)` y `calcular_costo(km, impuesto, descuento)` funcionarían de inmediato. |

@importante
Para que el nuevo servicio apareciera en la **pantalla**, sí habría que agregar trabajo en la interfaz y en el gestor: un método `registrar_transporte` en `GestorServicios` y una opción «Transporte» con sus campos en `interfaz/vista_servicios.py`. La POO reduce el trabajo, pero no lo elimina: la regla del negocio se escribe una vez y las pantallas se adaptan para pedir los datos nuevos.
@fin

## 4.8 Los cinco pilares de un vistazo

| Pilar | Idea en una frase | Ejemplo cotidiano | Dónde está en Software FJ |
|---|---|---|---|
| Abstracción | Quedarse con lo esencial y definir contratos. | El menú de un restaurante. | `Entidad(ABC)` y `Servicio` con `@abstractmethod` (`modelos/entidad.py`, `modelos/servicios.py` líneas 95-116). |
| Encapsulación | Proteger los datos y cambiarlos solo de forma controlada. | El cajero automático. | `Cliente` con `__nombre`, `__correo`, `__telefono` y propiedades con *setter* (`modelos/cliente.py` líneas 35-70). |
| Herencia | Crear clases nuevas a partir de otras. | Un vendedor es un empleado. | `Servicio` → `ReservaSala`, `AlquilerEquipo`, `Asesoria`; todo hereda de `Entidad`. |
| Polimorfismo | Una misma orden, muchas formas de cumplirla. | «Calculen su pago». | `calcular_costo_base`, `validar_parametros`, `detalle`, `describir`, `refrescar`. |
| Sobrecarga (simulada) | Un método que acepta distintas cantidades de datos. | Café solo, con leche, con azúcar. | `Servicio.calcular_costo(duracion, impuesto=None, descuento=None)`. |

::img d_uml_modelos | Vuelve a mirar el diagrama: ahora puedes señalar en él los cinco pilares.

@ejercicio: Encuentra los pilares
Abre `modelos/reserva.py` y responde:
1. ¿De qué clase hereda `Reserva`? ¿Qué métodos abstractos tuvo que escribir?
2. ¿Qué atributos están protegidos con un guion bajo?
3. ¿El constructor `__init__` tiene parámetros opcionales? ¿Cuáles?
@fin

@ejercicio: Explica con tus palabras
Prepara una explicación de un minuto, sin leer, sobre por qué agregar un nuevo tipo de servicio a Software FJ requiere escribir una sola clase nueva. Usa las palabras «herencia», «polimorfismo» y «clase abstracta».
@fin

@resumen
- **Abstracción**: `Entidad` y `Servicio` son clases abstractas (heredan de `ABC` y usan `@abstractmethod`); definen qué deben hacer las clases hijas.
- **Encapsulación**: `Cliente` guarda sus datos en atributos privados (`__nombre`) y los valida con `@property` y `.setter`; las demás clases usan `_atributo` y propiedades de solo lectura.
- **Herencia**: las clases hijas reciben lo de la madre con `class Hija(Madre)` y llaman a su constructor con `super().__init__()`.
- **Polimorfismo**: las tres clases de servicio sobrescriben `calcular_costo_base`, y `Servicio` lo usa sin saber el tipo exacto.
- **Sobrecarga**: Python no la tiene por firma; Software FJ la simula con parámetros opcionales en `calcular_costo`.
- **Sobrescribir** es redefinir en la hija; **sobrecargar** es tener varias versiones en la misma clase. No son lo mismo.
@fin
