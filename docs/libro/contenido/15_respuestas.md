# Respuestas de la evaluación
> Revisa cada respuesta y, si fallaste, vuelve a la sección indicada.

Las respuestas de interpretación de código (IC) fueron comprobadas ejecutando cada fragmento con Python 3.14 desde la carpeta raíz del proyecto.

## Selección múltiple (P1 a P30)

| Pregunta | Respuesta | Justificación |
|---|---|---|
| P1 | b | Un programa es una lista de instrucciones que el computador sigue (capítulo 1). |
| P2 | b | El intérprete lee el código `.py` y lo ejecuta instrucción por instrucción. |
| P3 | c | Los archivos de Python terminan en `.py`, como `main.py`. |
| P4 | b | `19` no tiene decimales ni comillas: es un entero (`int`). |
| P5 | c | `self._clientes = []` crea una lista vacía en `GestorClientes`. |
| P6 | b | `"total"` es la clave con la que se busca un valor en el diccionario de costos. |
| P7 | c | `return` entrega el resultado y termina la función. |
| P8 | b | La clase es el molde; los objetos se fabrican con ella. |
| P9 | b | `self` es el propio objeto que ejecuta el método. |
| P10 | b | `__init__` se ejecuta automáticamente al crear cada objeto. |
| P11 | c | Las tres clases se declaran como `class ReservaSala(Servicio)`, etc. |
| P12 | b | Ocultar el dato y controlar su cambio con validación es encapsulación. |
| P13 | c | Un mismo método con comportamiento distinto en cada clase es polimorfismo. |
| P14 | b | Los parámetros opcionales permiten llamar `calcular_costo(d)`, `(d, i)` o `(d, i, desc)`. |
| P15 | b | `Entidad` hereda de `ABC` y tiene métodos abstractos; Python lanza `TypeError`. |
| P16 | c | La clase `Tabla` de `componentes.py` usa `ttk.Treeview`. |
| P17 | b | `mainloop()` mantiene viva la ventana y atiende los eventos. |
| P18 | c | `command=self.buscar` conecta el botón con su función. |
| P19 | b | `VistaBase.ejecutar` envuelve cada llamada a los gestores en `try/except`. |
| P20 | c | `else` solo corre si el `try` no lanzó excepciones. |
| P21 | d | `finally` se ejecuta siempre. |
| P22 | b | `from error` encadena la nueva excepción con su causa original. |
| P23 | c | Todas las excepciones del proyecto heredan de `SoftwareFJError`. |
| P24 | c | `EntidadDuplicadaError` usa el código FJ-201. |
| P25 | b | El logger «software_fj» se configura en `registro.py`. |
| P26 | b | Cada línea tiene fecha, nivel y mensaje separados por barras verticales. |
| P27 | b | Desde Pendiente se puede confirmar o cancelar. |
| P28 | c | 80.000 × 4 = 320.000, más 10 % de recargo por superar 20 personas = 352.000. |
| P29 | b | Un commit es una fotografía guardada del proyecto. |
| P30 | c | `git ls-remote origin` muestra cinco ramas: main, Jully, Kathe, Sebastian y Vanesa. |

## Verdadero o falso (VF1 a VF20)

| Afirmación | Respuesta | Justificación |
|---|---|---|
| VF1 | F | Python no usa punto y coma al final de cada línea; el salto de línea basta. |
| VF2 | V | La sangría define los bloques en Python. |
| VF3 | V | Las listas son modificables; las tuplas, como `ACTIVOS`, no. |
| VF4 | F | Mezclar texto y número produce `TypeError`. |
| VF5 | F | Todo se guarda en memoria y se pierde al cerrar; solo persiste el log. |
| VF6 | V | Un objeto es una instancia de una clase. |
| VF7 | V | `super()` da acceso a la clase madre. |
| VF8 | F | Python no tiene sobrecarga por firma: el último método con ese nombre reemplaza a los anteriores. |
| VF9 | V | `Servicio("X", "abc", 1, 1)` lanza `TypeError` por sus métodos abstractos. |
| VF10 | F | Las reglas de cálculo están en `modelos/servicios.py`; la interfaz solo muestra resultados. |
| VF11 | V | `neto = base - valor_descuento` y luego el impuesto se calcula sobre `neto`. |
| VF12 | F | `AlquilerEquipo.validar_parametros` exige días completos. |
| VF13 | F | Solo las reservas Pendientes y Confirmadas (`ACTIVOS`) ocupan cupo. |
| VF14 | V | Python usa el primer `except` que coincide. |
| VF15 | V | `finally` se ejecuta aunque la excepción se relance. |
| VF16 | V | `class OperacionNoPermitidaError(ReservaError)`. |
| VF17 | F | `FileHandler` agrega líneas al final; el archivo conserva todas las sesiones. |
| VF18 | V | `_error_global` registra el error, lo muestra y deja la aplicación abierta. |
| VF19 | F | Las cuatro ramas apuntan al primer commit (`1199503`); solo `main` tiene el segundo commit. |
| VF20 | V | `push` sube los commits locales al repositorio remoto. |

## Interpretación de código (IC1 a IC10)

**IC1.** Imprime:

```salida
[FJ-201] Ya existe un cliente con identificador '1032456789'.
```

`EntidadDuplicadaError` arma el mensaje y le pasa el código FJ-201 a `SoftwareFJError`, cuyo `__str__` pone el código entre corchetes antes del mensaje.

**IC2.** Imprime `170000`. Solo 50000 y 120000 superan 40000; 35000 se salta.

**IC3.** Devuelve:

```salida
{'duracion': 3.0, 'subtotal': 150000.0, 'descuento': 15000.0, 'impuesto': 25650.0, 'total': 160650.0}
```

Subtotal 50.000 × 3 = 150.000 (sin recargo, 12 personas); descuento 10 % = 15.000; neto 135.000; impuesto 19 % = 25.650; total 160.650. En cambio, `calcular_costo(3)` devuelve `150000.0`, porque sin impuesto ni descuento el total es igual al subtotal.

**IC4.** Se lanza `OperacionNoPermitidaError` con el mensaje:

```salida
[FJ-401] No se puede 'cancelar' una reserva en estado 'Procesada'.
```

«Procesada» no está en `EstadoReserva.ACTIVOS`, así que la línea 98 es verdadera y se ejecuta el `raise` de la línea 99.

**IC5.** Imprime, en orden: `B`, `C`, `A`, `C`. Con «7» la conversión funciona (else y finally); con «siete» falla (except y finally).

**IC6.** `c.nombre` es `"Andrés Pérez"` (se quitan los espacios repetidos y se pone mayúscula inicial); `c.correo` es `"aperez@empresa.co"` (minúsculas); `c.telefono` es `"6017654321"` (se eliminan los guiones).

**IC7.** `porcentaje_a_fraccion("descuento", "19,5%")` devuelve `0.195`: quita el «%», cambia la coma por punto y divide entre 100. Con «120» se lanza `CalculoInconsistenteError`: «[FJ-500] El impuesto debe estar entre 0 y 100 % (recibido 120).».

**IC8.** `a.calcular_costo(2)` devuelve `260000.0` (100.000 × 2 × 1,3 del nivel Intermedio). `a.calcular_costo(0.25)` lanza `DatoInvalidoError`: «[FJ-101] Valor inválido para 'duración' (0.25): para Asesoría debe estar entre 0.5 y 8 horas».

**IC9.** Imprime `3 0`. El diccionario queda con tres claves y `get("total", 0)` devuelve el valor por defecto 0 porque la clave «total» no existe.

**IC10.** `e.calcular_costo(2.5)` lanza `DatoInvalidoError`: «[FJ-101] Valor inválido para 'duración' (2.5): los equipos se alquilan por días completos». `e.calcular_costo(2, 0.19)` devuelve `87465.0`: 35.000 × 2 × 1,05 (seguro) = 73.500; más 19 % (13.965) = 87.465.

## Ejercicios prácticos (EP1 a EP8)

Estas son soluciones modelo; puede haber otras correctas. Ninguna forma parte del código original de Software FJ.

**EP1.** En el *setter* `nombre` de `modelos/cliente.py`, después de la validación existente:

```python
if len(valor) > 60:
    raise DatoInvalidoError("nombre", valor, "máximo 60 caracteres")
```

**EP2.** En el *setter* `telefono`, después de validar los dígitos:

```python
if len(valor) == 10 and not valor.startswith("3"):
    raise DatoInvalidoError("teléfono", valor, "un celular de 10 dígitos debe empezar por 3")
```

Nota: esta regla rechazaría el fijo de 10 dígitos «6017654321» usado en los ejemplos; es una decisión de negocio que debe discutirse con el equipo.

**EP3.** Basta con cambiar el diccionario en `modelos/servicios.py`:

```python
NIVELES = {"Básico": 1.0, "Intermedio": 1.3, "Experto": 1.6, "Senior": 2.0}
```

No hay que tocar la interfaz: `interfaz/vista_servicios.py` (línea 21) construye la lista desplegable con `list(Asesoria.NIVELES)`, así que el nuevo nivel aparece solo.

**EP4.**

```python
def contar_por_dominio(gestor):
    conteo = {}
    for cliente in gestor.listar():
        dominio = cliente.correo.split("@")[1]
        conteo[dominio] = conteo.get(dominio, 0) + 1
    return conteo
```

Con tres clientes de prueba devolvió `{'mail.com': 2, 'empresa.co': 1}`.

**EP5 y EP6.** En `excepciones.py`:

```python
class ClienteConReservasError(SoftwareFJError):
    def __init__(self, identificacion):
        super().__init__(f"El cliente '{identificacion}' tiene reservas activas.", "FJ-202")
```

En `GestorClientes` se necesita saber si hay reservas activas; como el gestor de clientes no conoce las reservas, una opción es recibir una función que las cuente (igual que `contador_ocupacion` en `GestorServicios`):

```python
def eliminar(self, identificacion, tiene_reservas_activas=lambda c: False):
    cliente = self.obtener(identificacion)
    if tiene_reservas_activas(cliente):
        error = ClienteConReservasError(identificacion)
        registrar_error("Eliminación de cliente rechazada", error)
        raise error
    self._clientes.remove(cliente)
    registrar_evento(f"Cliente eliminado: {cliente.describir()}")
```

**EP7.** En `gestores/gestor_reservas.py`, método `crear`, después de crear la reserva (después de la línea 56):

```python
if descuento is not None and descuento >= 0.30:
    registrar_advertencia(f"Descuento alto en {reserva.codigo}: {descuento:.0%}")
```

Hay que importar `registrar_advertencia` desde `registro`. Se pone en el gestor porque es quien registra los eventos de negocio.

**EP8.** En `gestores/__init__.py`, dentro de `estadisticas()`:

```python
validas = [r for r in self.reservas.listar()
           if r.estado in (EstadoReserva.CONFIRMADA, EstadoReserva.PROCESADA)]
"ticket_promedio": round(sum(r.total for r in validas) / len(validas), 2) if validas else 0,
```

(La lista `validas` se calcula antes del `return`, y la clave se agrega al diccionario). Para mostrarla hay que agregar una tarjeta en `interfaz/dashboard.py`: una tupla nueva en `TARJETAS` y una línea `actualizar` en `refrescar`.

## Explica con tus palabras (EC1 a EC12)

**EC1.** Programar es escribirle al computador una receta exacta de pasos. Python es bueno para empezar porque se lee casi como inglés sencillo, no exige símbolos innecesarios y trae muchas herramientas listas, como Tkinter para las ventanas de Software FJ.

**EC2.** La clase es el molde y el objeto es lo que sale del molde. `Cliente` es la clase; Laura Gómez, con su identificación 1032456789, es un objeto.

**EC3.** `__init__` es el constructor: prepara cada objeto nuevo, como llenar la ficha de inscripción. `self` es la forma en que el objeto dice «yo»: `self.nombre` es «mi nombre».

**EC4.** Abstracción es quedarse con lo esencial. `Entidad` y `Servicio` definen qué debe saber hacer todo servicio (describirse, calcular su costo) sin decir cómo; cada tipo concreto completa los detalles.

**EC5.** Encapsular es guardar los datos bajo llave. El correo de un cliente está en `self.__correo` y solo se cambia por el *setter*, que verifica el formato; así nadie puede guardar «maria.ruiz@» por error.

**EC6.** Herencia es recibir lo de los padres. `ReservaSala`, `AlquilerEquipo` y `Asesoria` heredan de `Servicio` el código, el nombre, la tarifa, el cupo y el cálculo de impuestos y descuentos; cada una solo agrega lo suyo.

**EC7.** Polimorfismo es que la misma orden produzca resultados distintos según quién la recibe. Todos los servicios responden a `calcular_costo_base`, pero la sala aplica recargo, el equipo suma el seguro y la asesoría multiplica por el nivel.

**EC8.** Sobrescribir es que la hija redefina un método de la madre (como `calcular_costo_base`). Sobrecargar es tener varias formas de llamar un método. Python no permite varios métodos con el mismo nombre; lo imita con parámetros opcionales, como `calcular_costo(duracion, impuesto=None, descuento=None)`.

**EC9.** Por orden y responsabilidad, como en un restaurante: el mesero (interfaz) toma el pedido, el administrador (gestores) coordina y la cocina (modelos) sigue las recetas. Si cambia la decoración, la cocina no se entera.

**EC10.** El botón llama a `VistaReservas.crear`; esta usa `ejecutar` para llamar a `GestorReservas.crear`; el gestor busca el cliente y el servicio, revisa disponibilidad y cupo, y crea un objeto `Reserva`, que calcula el costo con el servicio. Si todo sale bien, se registra el evento, se muestra «Operación exitosa» y se refrescan las pantallas; si no, se muestra el error y se anota en el log.

**EC11.** `try` intenta la operación; `except` atrapa los errores y los convierte en mensajes; `else` hace lo que corresponde al éxito, como guardar el cliente; `finally` deja constancia siempre, como en `Reserva.procesar`. Gracias a eso ningún error cierra el programa.

**EC12.** Las ramas son borradores separados: cada integrante trabaja en la suya sin dañar el trabajo de los demás y, cuando su parte está lista, se une a `main`. En el repositorio existen las ramas `Jully`, `Kathe`, `Sebastian` y `Vanesa` además de `main`.
