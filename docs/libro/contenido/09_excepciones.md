# Manejo de errores y excepciones
> Un buen programa no es el que nunca se equivoca, sino el que sabe qué hacer cuando algo sale mal.

@objetivos
- Diferenciar entre un error de programación y una excepción que ocurre mientras el programa funciona.
- Leer y escribir bloques `try`, `except`, `else` y `finally`, y saber en qué orden se ejecutan.
- Comprender para qué sirve `raise` y cómo se lanza una excepción a propósito.
- Explicar qué es una excepción personalizada y recorrer la jerarquía de excepciones de Software FJ.
- Entender qué significa encadenar excepciones con `raise ... from`.
- Saber qué es el registro de eventos (*logging*) y leer el archivo `software_fj.log`.
@fin

## 9.1 ¿Qué es un error?

Antes de hablar de código, pensemos en algo que nos pasa a todos. Vas a pagar en una tienda, entregas la tarjeta y el datáfono dice «Fondos insuficientes». El datáfono no se apagó, no explotó y la tienda no cerró. Simplemente detectó un problema, te lo informó con un mensaje claro y quedó listo para el siguiente intento. Eso, en pocas palabras, es lo que este capítulo te va a enseñar a construir.

En programación hay dos grandes familias de errores, y conviene distinguirlas desde el principio.

@nivel1
Imagina que escribes una receta de cocina. Puede fallar de dos formas. La primera: escribiste mal la receta, por ejemplo «agregue 2 tazas de harna». Quien la lea ni siquiera entiende la palabra; la receta está mal escrita. La segunda: la receta está perfecta, pero al cocinar descubres que no hay huevos en la nevera. La receta no tiene la culpa; el problema aparece *en el momento de cocinar*.
@fin

@nivel2
En programación, el primer caso se llama **error de sintaxis**: el código está mal escrito y Python ni siquiera puede empezar a ejecutarlo (por ejemplo, olvidar cerrar un paréntesis). El segundo caso se llama **error en tiempo de ejecución**: el código está bien escrito, pero mientras corre ocurre una situación que impide continuar, como dividir entre cero, convertir la palabra «hola» en número o buscar un cliente que no existe. Los errores en tiempo de ejecución son los que Python llama **excepciones**. La palabra *sintaxis* significa «las reglas de escritura de un lenguaje», igual que la ortografía y la gramática del español.
@fin

```python
# Error de sintaxis: falta cerrar el paréntesis. Python no ejecuta nada.
print("Hola"

# Error en tiempo de ejecución: el código está bien escrito,
# pero "abc" no se puede convertir en número.
numero = float("abc")
```

```salida
ValueError: could not convert string to float: 'abc'
```

@nivel3
En Software FJ los errores de sintaxis no deberían existir: si los hubiera, el programa ni abriría. Lo que sí ocurre todo el tiempo son situaciones de ejecución: alguien escribe un correo sin arroba, una tarifa negativa, 40 días de alquiler para un equipo que solo admite 30, o intenta reservar un videobeam que ya está ocupado. Todo el proyecto está pensado para que esas situaciones se conviertan en mensajes claros y nunca cierren la aplicación.
@fin

::img 05_error_correo | Un error de ejecución bien manejado: el usuario escribió «maria.ruiz@» y el programa muestra un mensaje en lugar de cerrarse.

## 9.2 ¿Qué es una excepción?

@nivel1
Piensa en un árbitro de fútbol. El partido avanza normalmente hasta que ocurre una falta. En ese instante el árbitro pita, el juego se detiene y alguien tiene que decidir qué hacer: tiro libre, tarjeta, penal. El pitazo no arregla nada por sí solo: solo *avisa* que pasó algo fuera de lo normal.
@fin

@nivel2
Una **excepción** es un aviso que Python genera cuando algo impide continuar con la instrucción actual. Técnicamente es un **objeto** (recuerda el capítulo 3: un objeto es un «paquete» de datos y acciones) que contiene información sobre lo que pasó: su tipo (por ejemplo `ValueError` o `ZeroDivisionError`) y un mensaje. Cuando una excepción aparece, Python deja de ejecutar las líneas siguientes y empieza a buscar «quién la atrapa». Si nadie la atrapa, el programa se detiene y muestra en pantalla un informe llamado **traceback** (rastro), que indica en qué línea ocurrió el problema.
@fin

```python
print("Inicio")
resultado = 10 / 0        # aquí se "pita la falta"
print("Esta línea nunca se ejecuta")
```

```salida
Inicio
Traceback (most recent call last):
  File "ejemplo.py", line 2, in <module>
    resultado = 10 / 0
ZeroDivisionError: division by zero
```

Fíjate en tres cosas: se imprimió «Inicio»; la tercera línea nunca se ejecutó; y el mensaje final dice el **tipo** de la excepción (`ZeroDivisionError`) y una **descripción** («division by zero»).

@nivel3
Software FJ no deja que el programa llegue a ese traceback. Cada vez que algo sale mal, se lanza una excepción con un nombre propio del proyecto, por ejemplo `DatoInvalidoError` o `ServicioNoDisponibleError`, y siempre hay alguien encargado de atraparla y mostrar un mensaje amable. En la pantalla verás frases como «Ya existe un cliente con identificador '1032456789'.» en lugar de un rastro técnico.
@fin

| Excepción común de Python | Cuándo aparece | Ejemplo |
|---|---|---|
| `ValueError` | Un valor tiene el tipo correcto pero un contenido imposible | `float("abc")` |
| `TypeError` | Se usa un dato del tipo equivocado | `"5" + 3` |
| `ZeroDivisionError` | Se divide entre cero | `10 / 0` |
| `KeyError` | Se pide una clave que no está en un diccionario | `{"a": 1}["b"]` |
| `IndexError` | Se pide una posición que no existe en una lista | `[1, 2][5]` |
| `FileNotFoundError` | Se intenta abrir un archivo que no existe | `open("no_existe.txt")` |
| `NameError` | Se usa una variable que no fue creada | `print(edad)` sin definir `edad` |

## 9.3 El bloque try y except: intentar y atrapar

@nivel1
Un trapecista hace su acrobacia (*intenta*) con una red debajo. Si todo sale bien, la red no se usa. Si cae, la red lo *atrapa* y el espectáculo continúa. La acrobacia es el `try`; la red es el `except`.
@fin

@nivel2
La palabra inglesa **try** significa «intentar» y **except** significa «excepto» o «salvo que». Escribimos dentro de `try` las instrucciones que podrían fallar. Debajo, en uno o varios `except`, escribimos qué hacer si aparece una excepción de cierto tipo. Si nada falla, los `except` se saltan por completo. Si algo falla, Python abandona el resto del `try` y salta al primer `except` cuyo tipo coincida con la excepción.
@fin

```python
texto = input("Escribe la tarifa: ")
try:
    tarifa = float(texto)          # puede fallar si escriben letras
    print("Tarifa registrada:", tarifa)
except ValueError:
    print("La tarifa debe ser un número.")
print("El programa sigue funcionando.")
```

```salida
Escribe la tarifa: cincuenta mil
La tarifa debe ser un número.
El programa sigue funcionando.
```

Dos detalles importantes:

- Puedes escribir `except ValueError as error:`. La palabra **as** («como») guarda la excepción en una variable llamada `error` para que puedas leer su mensaje.
- Puedes tener varios `except` uno debajo del otro. Python los revisa **en orden, de arriba hacia abajo**, y usa solo el primero que coincide. Por eso los más específicos van primero y los más generales al final.

@nivel3
El método `registrar` del gestor de clientes es un ejemplo perfecto. Intenta crear el cliente; si algo falla por una regla del negocio, deja constancia en el registro y vuelve a lanzar el problema para que la pantalla lo muestre.
@fin

::codigo gestores/gestor_clientes.py 11-23 | Método registrar de GestorClientes: try, except y else en acción
::lineas
11 | Se define el método `registrar`, que recibe los cuatro datos del cliente.
12 | Empieza la zona de «intento»: todo lo que está debajo y con sangría puede fallar.
13 | Se limpia la identificación: si llegó vacía (`None`) se usa texto vacío, y `strip()` quita espacios sobrantes.
14-15 | Si ya existe un cliente con esa identificación, se lanza a propósito una `EntidadDuplicadaError` (veremos `raise` en la sección 9.6).
16 | Se crea el objeto `Cliente`. Si el correo, el nombre o el teléfono son inválidos, el propio constructor lanza una excepción.
17 | Si apareció cualquier excepción del proyecto (todas descienden de `SoftwareFJError`), se atrapa y se guarda en la variable `error`.
18 | Se anota el rechazo en el archivo de registro (sección 9.10).
19 | `raise` solo, sin nada más, significa «vuelve a lanzar la misma excepción»: el gestor la anotó, pero deja que la pantalla decida cómo mostrarla.
20-23 | El bloque `else` se ejecuta **solo si no hubo excepción**: se guarda el cliente en la lista, se registra el evento y se devuelve el cliente creado.
::fin

@recuerda
Un `except` no «arregla» el problema por arte de magia. Tú decides qué hacer en él: mostrar un mensaje, usar un valor por defecto, anotar el error o volver a lanzarlo.
@fin

### ¿Qué pasa con el orden de los except?

En `gestores/gestor_reservas.py` el método `crear` tiene tres `except` seguidos. Léelos como una escalera que va de lo más específico a lo más general:

::codigo gestores/gestor_reservas.py 38-57 | Método crear de GestorReservas: tres except ordenados de lo específico a lo general
::lineas
39-46 | Dentro del `try` se busca el cliente, se preparan los porcentajes, se verifica que el servicio esté habilitado y tenga cupo, y se crea la reserva. Cualquiera de esos pasos puede fallar.
47-48 | Primer escalón: si el cliente o el servicio no existen, simplemente se relanza, porque el método `obtener` del gestor ya lo anotó en el registro (así no se escribe dos veces).
49-51 | Segundo escalón: cualquier otro error del proyecto (dato inválido, sin cupo, cálculo inconsistente) se anota como «Reserva fallida» y se relanza.
52-54 | Último escalón: cualquier error imprevisto de Python (`Exception` atrapa casi todo) se anota y se transforma en una `ReservaError` con un mensaje comprensible. El `from error` conserva la causa original (sección 9.8).
55-57 | Si se llegó hasta aquí es porque no hubo excepción: se guarda la reserva, se registra y se devuelve.
::fin

@atencion
Si pusieras `except Exception` en primer lugar, atraparía **todo** y los `except` de abajo nunca se usarían, porque Python se detiene en el primero que coincide. El orden importa.
@fin

## 9.4 else: lo que se hace solo si todo salió bien

@nivel1
Cuando envías un paquete por mensajería, primero se intenta la entrega (`try`). Si el destinatario no está, se deja un aviso (`except`). Solo si la entrega fue exitosa se envía el mensaje «Tu paquete fue entregado» (`else`). No tendría sentido enviar ese mensaje si la entrega falló.
@fin

@nivel2
El bloque **else** («si no», «de lo contrario») va después de todos los `except` y se ejecuta **únicamente cuando el `try` terminó sin excepciones**. ¿Por qué no poner ese código al final del `try`? Porque así dejamos claro qué parte es «riesgosa» y qué parte es «la consecuencia del éxito». Además, si el código del `else` fallara, ese fallo no sería atrapado por accidente por los `except` de arriba.
@fin

```python
try:
    edad = int(input("Edad: "))
except ValueError:
    print("Eso no es un número.")
else:
    print("En diez años tendrás", edad + 10)
```

@nivel3
Ya viste el `else` del método `registrar` (líneas 20-23 de `gestor_clientes.py`): el cliente solo se agrega a la lista si su creación no lanzó ninguna excepción. Otro `else` muy didáctico está en la simulación de 15 operaciones: la variable `ok` solo se vuelve verdadera en el `else`.
@fin

::codigo simulacion.py 70-89 | La simulación ejecuta cada operación dentro de try/except/else/finally
::lineas
70 | Se recorren las 15 operaciones, numeradas desde 1.
71 | Se parte suponiendo que la operación fallará (`ok = False`) y sin detalle.
72-73 | Se intenta ejecutar la operación.
74-75 | Si fue un error del proyecto, el detalle será el mensaje del error, con su código (por ejemplo «[FJ-201] Ya existe…»).
76-78 | Si fue un error inesperado de Python, se registra como crítico y se describe en el detalle. La simulación no se detiene.
79-83 | `else`: solo si la operación funcionó se marca `ok = True` y se arma un detalle con la descripción del resultado.
84-89 | `finally`: pase lo que pase, se guarda la fila del resultado y se informa a la ventana (la sección 9.5 explica `finally`).
::fin

## 9.5 finally: lo que se hace siempre

@nivel1
Al salir de la cocina, cocines bien o se te queme el arroz, siempre apagas la estufa. Esa acción no depende del resultado: se hace *siempre*.
@fin

@nivel2
El bloque **finally** («finalmente») se ejecuta **siempre**: si no hubo error, si hubo un error atrapado e incluso si hubo un error que se volvió a lanzar. Se usa para tareas de cierre o de constancia: cerrar un archivo, liberar un recurso, escribir en el registro que «se intentó» algo.
@fin

::img d_try | Recorrido de un bloque try / except / else / finally: el camino verde es el del éxito, el rojo el del error, y finally está en ambos.

| Bloque | ¿Cuándo se ejecuta? | Pregunta que responde |
|---|---|---|
| `try` | Siempre se intenta | ¿Qué quiero hacer? |
| `except` | Solo si hubo una excepción de ese tipo | ¿Qué hago si sale mal? |
| `else` | Solo si NO hubo excepción | ¿Qué hago si sale bien? |
| `finally` | Siempre, al final | ¿Qué hago pase lo que pase? |

@nivel3
El método `procesar` de la clase `Reserva` fue escrito precisamente para mostrar los cuatro bloques juntos. Procesar significa «facturar» una reserva confirmada.
@fin

::codigo modelos/reserva.py 102-127 | Reserva.procesar: el ejemplo completo de try, except, else y finally
::lineas
102-108 | Se define el método y su comentario de documentación explica qué hace cada bloque.
109 | `resultado` empieza vacío (`None` significa «nada»). Si todo sale bien, guardará el total facturado.
110 | Empieza el intento.
111-112 | Si la reserva no está confirmada, no se puede facturar: se lanza `OperacionNoPermitidaError`.
113 | Se vuelve a calcular el costo con los mismos datos, como una auditoría.
114-116 | Si el total guardado y el recalculado difieren en más de un centavo, se lanza `CalculoInconsistenteError`.
117-118 | Si el problema fue de estado (operación no permitida), se relanza tal cual: el mensaje ya es claro.
119-121 | Cualquier otro error del proyecto se registra y se reemplaza por una `ReservaError` más general, conservando la causa con `from error`.
122-124 | `else`: solo si no hubo problemas se cambia el estado a «Procesada» y se guarda el total.
125-126 | `finally`: haya funcionado o no, se deja constancia del intento en el registro, con el estado en que quedó la reserva.
127 | Se devuelve el total facturado (o `None` si no se llegó al `else`).
::fin

@ejemplo: Qué ves en el registro
Cuando en la captura del manual se procesó la reserva R-0002, el `finally` escribió esta línea en `software_fj.log`: «Intento de procesamiento de R-0002 -> estado Procesada». Si el intento hubiera fallado, la línea igual aparecería, pero con el estado anterior.
@fin

### Otro finally: al cerrar el programa

::codigo main.py 21-33 | La función main también usa try / except / finally
::lineas
21-26 | Se intenta importar y crear la ventana principal; `mainloop()` mantiene la ventana abierta hasta que el usuario sale.
27-30 | Si la ventana no pudo crearse (por ejemplo, porque falta Tkinter), se registra como error crítico, se avisa en la consola y la función devuelve 1, que por convención significa «terminó con error».
31-32 | Pase lo que pase, al final se escribe «Fin de la ejecución de Software FJ» en el registro.
33 | Si todo salió bien, se devuelve 0, que significa «terminó correctamente».
::fin

## 9.6 raise: lanzar una excepción a propósito

@nivel1
El salvavidas de una piscina ve a alguien corriendo en el borde y toca el silbato. Nadie se ha caído todavía, pero él *decide* avisar porque se está rompiendo una regla. Ese silbatazo voluntario es `raise`.
@fin

@nivel2
Hasta ahora las excepciones las lanzaba Python solo. Con la palabra **raise** («levantar», «elevar») tú mismo lanzas una excepción cuando detectas que algo no cumple las reglas de tu programa. Se escribe `raise` seguido del objeto excepción, por ejemplo `raise ValueError("La edad no puede ser negativa")`. En cuanto se ejecuta, la función se interrumpe y la excepción viaja hacia arriba buscando un `except` que la atrape. Un `raise` solo, sin nada a la derecha, dentro de un `except`, significa «vuelve a lanzar la misma excepción que acabo de atrapar».
@fin

```python
def validar_edad(edad):
    if edad < 0:
        raise ValueError("La edad no puede ser negativa")
    return edad

try:
    validar_edad(-5)
except ValueError as error:
    print("Problema:", error)
```

```salida
Problema: La edad no puede ser negativa
```

@nivel3
Las reglas de los clientes viven en `modelos/cliente.py`. Cada regla incumplida termina en un `raise`. Mira la validación de la identificación y del correo:
@fin

::codigo modelos/cliente.py 21-32 | Validaciones que usan raise en la clase Cliente
::lineas
21-22 | `_obligatorio` es un método de apoyo que revisa que un campo no esté vacío.
23-24 | Si el valor no existe o solo tiene espacios, se lanza `ParametroFaltanteError`. El mensaje será «El campo 'nombre' es obligatorio.» (o el campo que corresponda).
25 | Si el campo sí tiene contenido, se devuelve sin espacios sobrantes.
27-29 | `_validar_identificacion` primero exige que no esté vacía (reutiliza `_obligatorio`).
30-31 | Si contiene algo que no sea dígito, o tiene menos de 5 o más de 12 caracteres, se lanza `DatoInvalidoError` con el motivo.
32 | Si pasó todas las pruebas, se devuelve el valor validado.
::fin

::codigo modelos/cliente.py 54-59 | Validación del correo con raise
::lineas
56 | Se exige el correo y se convierte a minúsculas con `lower()`.
57-58 | Si no cumple el patrón «usuario@dominio.ext», se lanza `DatoInvalidoError` con el motivo «formato de correo no válido». Esta es exactamente la excepción que produjo la ventana de la figura del correo «maria.ruiz@».
59 | Si es válido, se guarda en el atributo privado.
::fin

## 9.7 Excepciones personalizadas

@nivel1
En un hospital no basta con decir «el paciente está mal». Hay categorías: urgencia, consulta externa, cirugía; y dentro de urgencias hay niveles de gravedad. Clasificar los problemas permite que cada uno llegue a la persona correcta. Las excepciones personalizadas son eso: categorías de problemas con nombre propio.
@fin

@nivel2
Python trae muchas excepciones (`ValueError`, `TypeError`…), pero son genéricas. Una **excepción personalizada** es una clase que tú creas y que **hereda** (capítulo 4) de `Exception`, la clase madre de casi todas las excepciones. Al heredar, tu clase ya «sabe» comportarse como excepción y tú le agregas lo que necesites: un mensaje más claro, un código, el nombre del campo que falló. Además, como las clases forman familias, puedes atrapar a toda una familia con un solo `except`: si atrapas la clase madre, atrapas también a todas sus hijas.
@fin

```python
class SaldoInsuficienteError(Exception):
    pass   # "pass" significa "no agrego nada más por ahora"

try:
    raise SaldoInsuficienteError("No hay fondos suficientes")
except SaldoInsuficienteError as error:
    print("Aviso:", error)
```

@nivel3
Software FJ define su propia familia de excepciones en el archivo `excepciones.py`. La «abuela» de todas es `SoftwareFJError`. Gracias a eso, la interfaz puede escribir un solo `except SoftwareFJError` y atrapar cualquier problema del negocio.
@fin

::img d_excepciones | Árbol de las excepciones personalizadas de Software FJ. Cada flecha significa «hereda de».

::codigo excepciones.py 18-27 | La excepción base SoftwareFJError
::lineas
18 | Se crea la clase `SoftwareFJError`, que hereda de `Exception`. Desde ahora es una excepción «de verdad».
19 | Texto de documentación: «Excepción base de todo el sistema».
21 | El constructor recibe un mensaje y un código. Si no se indica código, se usa «FJ-000».
22 | `super().__init__(mensaje)` le pasa el mensaje a la clase madre `Exception`, para que Python también lo conozca.
23-24 | Se guardan el mensaje y el código como atributos del objeto, para poder leerlos después (`error.mensaje`, `error.codigo`).
26-27 | `__str__` define cómo se ve la excepción cuando se convierte en texto: el código entre corchetes y luego el mensaje. Por eso en el registro aparece, por ejemplo, «[FJ-201] Ya existe un cliente…».
::fin

::codigo excepciones.py 30-51 | Las excepciones de validación
::lineas
30-35 | `ValidacionError` hereda de `SoftwareFJError` y agrega el atributo `campo`, que guarda el nombre del dato que falló («correo», «tarifa»…). Su código por defecto es FJ-100.
38-44 | `DatoInvalidoError` (FJ-101) arma el mensaje automáticamente a partir de tres piezas: el campo, el valor recibido y el motivo. `{valor!r}` muestra el valor tal como fue escrito, entre comillas si era texto.
47-51 | `ParametroFaltanteError` (FJ-102) se usa cuando falta un dato obligatorio; solo necesita saber el nombre del campo.
::fin

::codigo excepciones.py 54-81 | El resto de la familia: búsqueda, duplicados, disponibilidad, reservas y cálculos
::lineas
54-56 | `EntidadNoEncontradaError` (FJ-200): se busca un cliente, servicio o reserva que no existe.
59-61 | `EntidadDuplicadaError` (FJ-201): se intenta registrar algo con una identificación o código ya usado.
64-66 | `ServicioNoDisponibleError` (FJ-300): el servicio está deshabilitado o sin cupo.
69-71 | `ReservaError` (FJ-400): error general relacionado con reservas.
74-76 | `OperacionNoPermitidaError` (FJ-401) es hija de `ReservaError`: la acción no corresponde al estado (por ejemplo, cancelar una reserva ya procesada).
79-81 | `CalculoInconsistenteError` (FJ-500): un porcentaje inválido o un total que no cuadra.
::fin

| Código | Excepción | Ejemplo real de mensaje |
|---|---|---|
| FJ-101 | `DatoInvalidoError` | Valor inválido para 'correo' ('maria.ruiz@'): formato de correo no válido |
| FJ-102 | `ParametroFaltanteError` | El campo 'nombre' es obligatorio. |
| FJ-200 | `EntidadNoEncontradaError` | No existe un cliente con identificador '99999999'. |
| FJ-201 | `EntidadDuplicadaError` | Ya existe un cliente con identificador '1032456789'. |
| FJ-300 | `ServicioNoDisponibleError` | Servicio 'Videobeam Epson': no tiene cupos libres. |
| FJ-401 | `OperacionNoPermitidaError` | No se puede 'cancelar' una reserva en estado 'Procesada'. |
| FJ-500 | `CalculoInconsistenteError` | El descuento máximo permitido es 50%. |

@consejo
Para explicar la jerarquía en una sustentación, di: «Todas nuestras excepciones heredan de `SoftwareFJError`. Así, la interfaz las atrapa todas con un solo `except`, pero cada una conserva su propio código y mensaje».
@fin

### Una sola red para toda la familia

La ventaja de la familia se ve en la clase `VistaBase` de la interfaz. Su método `ejecutar` es el puente por el que pasan **todos** los botones antes de llegar a los gestores:

::codigo interfaz/componentes.py 342-370 | VistaBase.ejecutar: la red de seguridad de toda la interfaz
::lineas
342-343 | Se intenta ejecutar la acción pedida (registrar, crear reserva, etc.) con los datos del formulario.
344 | Primer `except`: errores de validación (hijos de `ValidacionError`).
345-350 | Se averigua qué campo falló (`error.campo`) y se marca en rojo en el formulario.
351-352 | Se muestra la ventana «Datos no válidos» con el mensaje y se escribe en la barra de estado.
353-355 | Segundo `except`: cualquier otro error del negocio (`SoftwareFJError`). Se muestra la ventana «Operación no realizada».
356-361 | Tercer `except`: cualquier error imprevisto. Se registra como crítico, se muestra «Error inesperado» y la aplicación **sigue abierta**.
362-369 | `else`: si todo salió bien, se muestra el mensaje de éxito, se actualizan todas las pantallas y se devuelve el resultado.
370 | Si hubo error, la función devuelve `None` («nada»), y la vista sabe que no debe limpiar el formulario.
::fin

@nota
Observa que `ValidacionError` va **antes** que `SoftwareFJError`. Como `ValidacionError` es hija de `SoftwareFJError`, si el orden fuera al revés el primer `except` atraparía también las validaciones y el campo nunca se marcaría en rojo.
@fin

### La última red: errores que nadie atrapó

Tkinter (la herramienta de ventanas, capítulo 5) tiene un mecanismo especial: si una función conectada a un botón lanza una excepción que nadie atrapó, llama a un método llamado `report_callback_exception`. Software FJ lo reemplaza por el suyo:

::codigo interfaz/ventana_principal.py 181-187 | Manejador global de errores de la ventana principal
::lineas
181 | El método recibe tres datos: el tipo de la excepción, la excepción en sí y el rastro (traceback).
182 | Se escribe en el registro como error crítico.
183-186 | Se muestra una ventana de error explicando que el problema quedó registrado y que la aplicación seguirá funcionando.
187 | Se pinta la barra de estado en rojo.
::fin

En la línea 64 del mismo archivo se conecta este método: `self.report_callback_exception = self._error_global`. Así, Software FJ tiene **tres redes**: los `except` de los gestores, el `ejecutar` de `VistaBase` y este manejador global.

## 9.8 Encadenar excepciones con raise ... from

@nivel1
Llevas el carro al taller porque «no prende». El mecánico revisa y escribe en la orden: «No prende **a causa de** batería descargada». Te informa el problema que tú entiendes (no prende) sin ocultar la causa técnica (la batería). Si mañana otro mecánico lee la orden, sabrá exactamente qué pasó.
@fin

@nivel2
A veces atrapas una excepción técnica de Python (por ejemplo `ValueError`) y quieres lanzar en su lugar una excepción más clara para tu programa. Si lo haces con un `raise` normal, la causa original se pierde de vista. Con **`raise NuevaExcepcion(...) from error`** le dices a Python «esta nueva excepción ocurrió *a causa de* aquella». Python guarda la excepción original en un atributo especial llamado `__cause__` («causa»). Esto se llama **encadenar excepciones**: se forma una cadena «problema visible ← causa técnica».
@fin

```python
try:
    float("abc")
except ValueError as error:
    raise RuntimeError("No se pudo leer la tarifa") from error
```

```salida
ValueError: could not convert string to float: 'abc'

The above exception was the direct cause of the following exception:

RuntimeError: No se pudo leer la tarifa
```

La frase en inglés significa «la excepción anterior fue la causa directa de la siguiente».

@nivel3
Software FJ encadena excepciones en varios lugares. El más sencillo está en la validación de números de `modelos/servicios.py`:
@fin

::codigo modelos/servicios.py 53-66 | _numero_positivo: convierte un ValueError de Python en un DatoInvalidoError del proyecto
::lineas
53-54 | Método de apoyo que valida que un valor (tarifa, cupo, capacidad, duración) sea un número positivo.
55-56 | Si está vacío, se lanza `ParametroFaltanteError`.
57-58 | Se intenta convertir el valor a número decimal con `float`.
59 | Si la conversión falla, Python lanza `ValueError` (o `TypeError`); se atrapa y se guarda en `error`.
60-61 | Se lanza en su lugar un `DatoInvalidoError` con un mensaje en español, **encadenado** a la causa original con `from error`.
62-65 | Si es cero o negativo, o supera un máximo, se lanza `DatoInvalidoError` con el motivo correspondiente.
66 | Si todo está bien, se devuelve el número.
::fin

::codigo modelos/servicios.py 23-33 | porcentaje_a_fraccion: otro encadenamiento, esta vez hacia CalculoInconsistenteError
::lineas
23-24 | Función que convierte «19», «19%» o «19,5» en la fracción 0.19, 0.195…
25-26 | Si el campo está vacío, devuelve `None` (no se aplica impuesto o descuento).
27-28 | Quita el símbolo %, cambia la coma por punto y convierte a número.
29-30 | Si no se puede convertir, lanza `CalculoInconsistenteError` encadenado al `ValueError` original.
31-33 | Si el número está fuera de 0 a 100, también es inconsistente; si no, se divide entre 100.
::fin

¿Y para qué sirve guardar la causa? La función `registrar_error` de `registro.py` la lee y la escribe en el archivo de registro. Si intentas registrar una sala con la tarifa «abc», el log muestra la cadena completa:

```salida
2026-11-05 22:20:37 | ERROR    | Registro de sala rechazado -> DatoInvalidoError: [FJ-101] Valor inválido para 'tarifa' ('abc'): debe ser numérico | causa: ValueError: could not convert string to float: 'abc'
```

El usuario ve el mensaje en español; el programador que lea el log ve además la causa técnica.

| Forma | Qué hace | Uso en Software FJ |
|---|---|---|
| `raise` (solo) | Vuelve a lanzar la misma excepción atrapada | `gestor_clientes.py`, línea 19 |
| `raise Nueva(...)` | Lanza una excepción nueva | `cliente.py`, línea 58 |
| `raise Nueva(...) from error` | Lanza una nueva y guarda la causa original | `servicios.py`, línea 61; `reserva.py`, línea 121 |

## 9.9 ¿Qué es logging?

@nivel1
Los aviones llevan una «caja negra» que anota todo lo que pasa durante el vuelo: altura, velocidad, conversaciones de la cabina. Nadie la lee mientras el vuelo va bien, pero si algo pasa, es la fuente para entender qué ocurrió. Las bitácoras de un barco o el libro de visitas de un edificio cumplen la misma función.
@fin

@nivel2
**Logging** (del inglés *log*, «bitácora») es la práctica de que un programa anote automáticamente lo que hace, con fecha y hora. Python trae un módulo llamado `logging` (un *módulo* es un archivo con herramientas listas para usar). Sus piezas básicas son:

- El **logger** («anotador»): el objeto al que le pides que anote algo.
- Los **niveles** de importancia: `DEBUG` (detalle para programadores), `INFO` (información normal), `WARNING` (advertencia), `ERROR` (algo falló) y `CRITICAL` (falla grave).
- Los **handlers** («manejadores»): deciden *dónde* se guarda cada anotación: en un archivo, en la pantalla, en memoria…
- El **formatter** («formateador»): decide *cómo* se ve cada línea.
@fin

```python
import logging
logging.basicConfig(level=logging.INFO)
logging.info("El programa inició")
logging.error("No se encontró el cliente")
```

@nivel3
Todo el registro de Software FJ está en el archivo `registro.py`. Allí se crea un único logger llamado «software_fj» con dos manejadores: uno escribe en el archivo `software_fj.log` y otro guarda en memoria los últimos 500 eventos para mostrarlos en la pantalla «Eventos y logs».
@fin

::codigo registro.py 40-54 | Configuración del logger de Software FJ
::lineas
40-41 | Se obtiene (o crea) el logger con el nombre «software_fj».
42-43 | Si ya tenía manejadores, se devuelve tal cual, para no configurarlo dos veces y evitar líneas repetidas.
44 | Nivel `DEBUG`: se aceptan anotaciones de todos los niveles.
45 | Se crea un manejador de archivo que escribe en `software_fj.log` usando UTF-8 (para que las tildes y la ñ se vean bien). Por defecto agrega líneas al final, sin borrar las anteriores.
46-47 | Se define el formato de cada línea: fecha y hora, nivel (ocupando 8 espacios) y mensaje, separados por barras.
48-49 | Se conectan los dos manejadores: el de archivo y el de memoria.
50 | `propagate = False` evita que las anotaciones se repitan en otros loggers de Python.
54 | Al importar el módulo, el logger queda configurado y guardado en la variable `logger`.
::fin

::codigo registro.py 57-75 | Las cuatro funciones que usa el resto del proyecto para anotar
::lineas
57-58 | `registrar_evento`: anota algo normal con nivel INFO.
61-62 | `registrar_advertencia`: nivel WARNING.
65-69 | `registrar_error`: si recibe una excepción, revisa si tiene causa encadenada (`__cause__`); si la tiene, la agrega al final con «| causa: …». Luego anota con nivel ERROR el mensaje, el tipo de la excepción y su texto.
70-71 | Si no se pasó excepción, anota solo el mensaje.
74-75 | `registrar_critico`: nivel CRITICAL; `exc_info` hace que en el archivo se escriba además el rastro completo del error.
::fin

@nota
Gracias a estas funciones, los demás archivos no necesitan saber cómo funciona `logging`. Solo dicen `registrar_evento("Cliente registrado…")` y listo. Esto es un buen ejemplo de **abstracción** (capítulo 4): se oculta el detalle y se ofrece una herramienta sencilla.
@fin

### El manejador en memoria

La pantalla «Eventos y logs» no lee el archivo cada vez; usa una copia en memoria. Esa copia la mantiene una clase propia que hereda de `logging.Handler`:

::codigo registro.py 15-34 | _MemoriaHandler: guarda los últimos eventos para la interfaz
::lineas
15 | La clase hereda de `logging.Handler`, así que el logger la reconoce como un manejador válido.
18-21 | Usa un `deque` con tamaño máximo 500: una lista que, al llenarse, descarta automáticamente lo más viejo. También guarda una lista de «oyentes» (funciones a las que avisar).
23-28 | `emit` es el método que `logging` llama por cada anotación. Arma un diccionario con fecha, nivel y mensaje.
29 | Lo agrega a la lista circular.
30-34 | Avisa a cada oyente. Si un oyente falla, el error se ignora (`pass`) para que un problema en la pantalla nunca rompa el registro.
::fin

## 9.10 El archivo .log

@nivel1
Un archivo `.log` es como el cuaderno de novedades de la portería de un conjunto residencial: cada línea dice a qué hora pasó algo y qué fue. Ese cuaderno no se borra al cambiar de turno; se sigue escribiendo.
@fin

@nivel2
Un archivo con extensión `.log` es un archivo de texto plano (se puede abrir con el Bloc de notas) donde un programa escribe sus anotaciones. Cada línea es un evento. Al no borrarse entre ejecuciones, permite revisar lo que pasó ayer o la semana pasada, encontrar errores difíciles de reproducir y demostrar que el sistema funcionó como se esperaba.
@fin

@nivel3
Software FJ escribe en `software_fj.log`, ubicado en la carpeta del proyecto (la ruta la calcula la línea 12 de `registro.py`). Este es un fragmento real del archivo, generado mientras se tomaban las capturas del manual de usuario:
@fin

```salida
2026-11-05 21:54:45 | INFO     | Interfaz gráfica iniciada
2026-11-05 21:54:48 | INFO     | Cliente registrado: Cliente Laura Gómez (ID 1032456789)
2026-11-05 21:54:51 | ERROR    | Registro de cliente rechazado -> DatoInvalidoError: [FJ-101] Valor inválido para 'correo' ('maria.ruiz@'): formato de correo no válido
2026-11-05 21:54:55 | ERROR    | Registro de cliente rechazado -> EntidadDuplicadaError: [FJ-201] Ya existe un cliente con identificador '1032456789'.
2026-11-05 21:55:07 | ERROR    | Registro de sala rechazado -> DatoInvalidoError: [FJ-101] Valor inválido para 'tarifa' ('-20000'): debe ser mayor que cero
2026-11-05 21:55:16 | INFO     | Reserva creada: Reserva R-0001: Laura Gómez - Sala Ejecutiva (3 horas) - $160,650.00 - Pendiente
2026-11-05 21:55:18 | ERROR    | Reserva fallida -> DatoInvalidoError: [FJ-101] Valor inválido para 'duración' ('40'): para Equipo debe estar entre 1 y 30 días
2026-11-05 21:55:20 | INFO     | Reserva R-0001 -> Confirmada
2026-11-05 21:55:25 | INFO     | Intento de procesamiento de R-0002 -> estado Procesada
2026-11-05 21:55:25 | INFO     | Reserva R-0002 -> Procesada
2026-11-05 21:55:28 | INFO     | Reserva R-0004 -> Cancelada
```

### Cómo leer una línea

| Parte | Ejemplo | Significado |
|---|---|---|
| Fecha y hora | `2026-11-05 21:54:51` | Cuándo ocurrió (año-mes-día hora:minuto:segundo) |
| Nivel | `ERROR` | Qué tan importante es |
| Mensaje | `Registro de cliente rechazado -> …` | Qué pasó, quién lo anotó y, si es un error, su tipo y código |

Fíjate en la cadena de responsables de una línea de error: «Registro de cliente rechazado» lo escribió el gestor (`gestor_clientes.py`, línea 18); «DatoInvalidoError» es el tipo de la excepción; «[FJ-101] Valor inválido…» es el texto que produjo el método `__str__` de `SoftwareFJError`.

::img 50_archivo_log | La ventana «software_fj.log» de la aplicación muestra el archivo real; las líneas de error aparecen en rojo.

::img 48_eventos_errores | En la pantalla «Eventos y logs», el filtro «Errores» muestra solo los eventos ERROR y CRITICAL guardados en memoria.

### Leer el archivo sin que el programa se caiga

Incluso la función que lee el archivo está protegida:

::codigo registro.py 90-95 | leer_archivo_log maneja el caso de que el archivo todavía no exista
::lineas
91-93 | Se intenta abrir el archivo en modo lectura con UTF-8 y devolver todo su contenido. La palabra `with` asegura que el archivo se cierre al terminar, aunque ocurra un error.
94-95 | Si el archivo no existe (`FileNotFoundError`), en lugar de fallar se devuelve un texto explicativo.
::fin

## 9.11 Todo junto: el viaje de un error

Para cerrar, sigamos el recorrido completo de un error real: el usuario escribe el correo «maria.ruiz@» y pulsa **Guardar**.

1. El botón llama a `VistaClientes.guardar`, que pide a `VistaBase.ejecutar` llamar a `GestorClientes.registrar`.
2. Dentro del `try` de `registrar`, se crea `Cliente(...)`.
3. El *setter* del correo (`cliente.py`, línea 58) ejecuta `raise DatoInvalidoError("correo", "maria.ruiz@", "formato de correo no válido")`.
4. La excepción sube hasta el `except SoftwareFJError` del gestor, que llama a `registrar_error` y la escribe en `software_fj.log` con nivel ERROR.
5. El `raise` del gestor la relanza hacia arriba.
6. En `VistaBase.ejecutar`, el `except ValidacionError` la atrapa, marca en rojo el campo «correo» y muestra la ventana «Datos no válidos».
7. La función devuelve `None`; el formulario no se limpia para que el usuario corrija.
8. La aplicación sigue abierta, lista para el siguiente intento.

@recuerda
Las tres capas trabajan juntas: el **modelo** detecta el problema y lanza la excepción; el **gestor** la anota en el registro; la **interfaz** la muestra al usuario. Ninguna capa hace el trabajo de las otras.
@fin

@ejercicio: Practica con la consola
Abre una terminal en la carpeta del proyecto, escribe `python` y luego prueba:
```python
from modelos.cliente import Cliente
Cliente("123", "Ana", "ana@mail.com", "3001234567")
```
¿Qué excepción aparece? ¿Qué código FJ tiene? Ahora corrige la identificación a «12345» y vuelve a intentarlo.
@fin

@resumen
- Un **error de sintaxis** impide que el programa arranque; una **excepción** aparece mientras el programa funciona.
- `try` contiene lo que puede fallar; `except` dice qué hacer si falla; `else` qué hacer si todo salió bien; `finally` lo que se hace siempre.
- Los `except` se revisan en orden: los más específicos primero.
- `raise` lanza una excepción a propósito; `raise` solo la relanza; `raise ... from error` encadena una nueva excepción con su causa.
- Software FJ tiene su propia familia de excepciones, todas hijas de `SoftwareFJError`, con códigos FJ-101 a FJ-500.
- `VistaBase.ejecutar` y `_error_global` garantizan que ningún error cierre la aplicación.
- El módulo `logging` anota lo que pasa; Software FJ lo configura en `registro.py` y escribe en `software_fj.log` con el formato «fecha | nivel | mensaje».
@fin
