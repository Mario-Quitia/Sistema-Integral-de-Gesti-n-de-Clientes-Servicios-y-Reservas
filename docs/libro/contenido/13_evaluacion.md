# Evaluación y aprendizaje
> Aprender no es leer: es poder explicar, predecir y construir. Aquí pones a prueba las tres cosas.

@objetivos
- Comprobar cuánto has aprendido sobre Python, POO, Tkinter, excepciones y Git.
- Practicar la lectura de código real de Software FJ y predecir lo que hace.
- Aplicar lo aprendido modificando el proyecto con ejercicios pequeños.
- Prepararte para responder preguntas en la sustentación con tus propias palabras.
@fin

## 13.1 Instrucciones

Este capítulo tiene cinco tipos de actividades:

| Sección | Tipo | Cantidad | Código |
|---|---|---|---|
| 13.2 | Selección múltiple | 30 | P1 a P30 |
| 13.3 | Verdadero o falso | 20 | VF1 a VF20 |
| 13.4 | Interpretación de código | 10 | IC1 a IC10 |
| 13.5 | Ejercicios prácticos | 8 | EP1 a EP8 |
| 13.6 | Explica con tus palabras | 12 | EC1 a EC12 |

Responde primero sin mirar el libro. Luego revisa tus respuestas en el capítulo «Respuestas de la evaluación», al final del libro. Si fallas una pregunta, vuelve a la sección indicada en la respuesta.

@consejo
Para los ejercicios de interpretación, intenta predecir el resultado en un papel **antes** de ejecutar el código. Después ejecútalo en la consola de Python desde la carpeta del proyecto y compara.
@fin

## 13.2 Preguntas de selección múltiple

Elige **una** respuesta.

**P1.** ¿Qué es un programa?
a) Un computador muy rápido. b) Un conjunto de instrucciones que el computador sigue para realizar una tarea. c) Un archivo de imagen. d) Una conexión a Internet.

**P2.** ¿Qué hace el intérprete de Python?
a) Dibuja ventanas. b) Traduce y ejecuta el código Python instrucción por instrucción. c) Guarda los archivos en GitHub. d) Corrige automáticamente los errores.

**P3.** ¿Qué extensión tienen los archivos de código Python?
a) `.txt` b) `.exe` c) `.py` d) `.log`

**P4.** ¿Qué tipo de dato es `19` en `IMPUESTO_POR_DEFECTO = 19`?
a) Cadena de texto. b) Número entero. c) Número decimal. d) Booleano.

**P5.** ¿Qué estructura usa Software FJ para guardar los clientes en memoria dentro de `GestorClientes`?
a) Un diccionario. b) Una tupla. c) Una lista. d) Un archivo de texto.

**P6.** En `costos["total"]`, ¿qué es `"total"`?
a) Una función. b) Una clave de diccionario. c) Una clase. d) Un parámetro.

**P7.** ¿Qué palabra se usa para devolver un resultado desde una función?
a) `print` b) `input` c) `return` d) `import`

**P8.** ¿Qué es una clase?
a) Un objeto concreto. b) Un molde que define atributos y métodos de los objetos. c) Una variable global. d) Un archivo de registro.

**P9.** ¿Qué representa `self` dentro de un método?
a) La clase madre. b) El objeto que está ejecutando el método. c) El archivo actual. d) La ventana principal.

**P10.** ¿Cuándo se ejecuta el método `__init__`?
a) Al cerrar el programa. b) Cada vez que se crea un objeto de esa clase. c) Solo cuando hay un error. d) Al presionar un botón.

**P11.** ¿De qué clase heredan `ReservaSala`, `AlquilerEquipo` y `Asesoria`?
a) `Entidad` directamente. b) `Cliente`. c) `Servicio`. d) `Reserva`.

**P12.** ¿Qué pilar de la POO se aplica cuando `Cliente` guarda su correo en `self.__correo` y solo permite cambiarlo a través de un *setter* que valida?
a) Herencia. b) Encapsulación. c) Polimorfismo. d) Sobrecarga.

**P13.** Cada tipo de servicio calcula su costo base de forma distinta con el mismo método `calcular_costo_base`. Eso es:
a) Encapsulación. b) Abstracción. c) Polimorfismo. d) Encadenamiento.

**P14.** ¿Cómo imita Software FJ la sobrecarga del método `calcular_costo`?
a) Escribiendo tres métodos con el mismo nombre. b) Usando parámetros con valores por defecto (`impuesto=None`, `descuento=None`). c) Usando herencia múltiple. d) No la imita.

**P15.** ¿Qué ocurre si intentas crear un objeto con `Entidad("x")`?
a) Se crea normalmente. b) Python lanza `TypeError` porque `Entidad` es abstracta. c) Se crea un cliente. d) Se cierra la ventana.

**P16.** ¿Qué widget de Tkinter usa Software FJ para mostrar tablas?
a) `Label` b) `Entry` c) `ttk.Treeview` d) `Canvas`

**P17.** ¿Qué hace `app.mainloop()` en `main.py`?
a) Cierra la aplicación. b) Mantiene la ventana abierta esperando las acciones del usuario. c) Ejecuta la simulación. d) Borra el log.

**P18.** ¿Qué parámetro de un botón de Tkinter indica la función que se ejecuta al hacer clic?
a) `text` b) `style` c) `command` d) `cursor`

**P19.** ¿Qué método de `VistaBase` atrapa los errores de todos los botones?
a) `refrescar` b) `ejecutar` c) `mostrar` d) `salir`

**P20.** ¿Qué bloque se ejecuta solo si el `try` terminó sin excepciones?
a) `except` b) `finally` c) `else` d) `raise`

**P21.** ¿Qué bloque se ejecuta siempre?
a) `try` b) `except` c) `else` d) `finally`

**P22.** ¿Qué hace `raise DatoInvalidoError(...) from error`?
a) Ignora el error. b) Lanza un nuevo error y guarda el error original como causa. c) Cierra el programa. d) Imprime el error en pantalla.

**P23.** ¿Cuál es la excepción base de todo Software FJ?
a) `Exception` b) `ValidacionError` c) `SoftwareFJError` d) `ReservaError`

**P24.** ¿Qué código tiene `EntidadDuplicadaError`?
a) FJ-101 b) FJ-200 c) FJ-201 d) FJ-500

**P25.** ¿En qué archivo se configura el registro de eventos?
a) `main.py` b) `registro.py` c) `excepciones.py` d) `simulacion.py`

**P26.** ¿Cuál es el formato de cada línea de `software_fj.log`?
a) mensaje · fecha b) fecha | nivel | mensaje c) nivel - código d) usuario | contraseña

**P27.** Una reserva en estado «Pendiente» puede pasar a:
a) Procesada directamente. b) Confirmada o Cancelada. c) Solo Cancelada. d) Ningún otro estado.

**P28.** Si una sala de 60 personas cuesta $ 80.000 por hora, ¿cuál es su subtotal por 4 horas?
a) $ 320.000 b) $ 336.000 c) $ 352.000 d) $ 384.000

**P29.** En Git, ¿qué es un *commit*?
a) Una rama nueva. b) Una fotografía guardada de los cambios del proyecto. c) Un servidor. d) Un error.

**P30.** ¿Cuántas ramas tiene el repositorio de Software FJ en GitHub?
a) Una. b) Tres. c) Cinco: `main`, `Jully`, `Kathe`, `Sebastian` y `Vanesa`. d) Diez.

## 13.3 Verdadero o falso

Escribe V si la afirmación es verdadera o F si es falsa.

**VF1.** Python necesita que cada instrucción termine con punto y coma.

**VF2.** La sangría (indentación) en Python indica qué líneas pertenecen a un bloque.

**VF3.** Una lista puede cambiar después de creada, pero una tupla no.

**VF4.** `"5" + 3` da como resultado 8.

**VF5.** Software FJ guarda los clientes en una base de datos que se conserva al cerrar el programa.

**VF6.** Un objeto es una instancia concreta creada a partir de una clase.

**VF7.** `super().__init__(...)` llama al constructor de la clase madre.

**VF8.** Python permite escribir tres métodos con el mismo nombre en una clase y escoge automáticamente uno según el número de parámetros.

**VF9.** La clase `Servicio` no puede usarse directamente para crear objetos porque tiene métodos abstractos.

**VF10.** En Software FJ, la interfaz gráfica contiene las reglas de cálculo de los costos.

**VF11.** El descuento se aplica antes del impuesto.

**VF12.** Los equipos pueden alquilarse por 2,5 días.

**VF13.** Una reserva procesada todavía ocupa cupo del servicio.

**VF14.** Si un `except` más general se escribe antes que uno específico, el específico nunca se usará.

**VF15.** `finally` se ejecuta incluso cuando el `except` vuelve a lanzar la excepción.

**VF16.** `OperacionNoPermitidaError` es hija de `ReservaError`.

**VF17.** El archivo `software_fj.log` se borra cada vez que se abre el programa.

**VF18.** El manejador `_error_global` evita que un error no atrapado cierre la ventana de Software FJ.

**VF19.** En el repositorio, las ramas `Jully`, `Kathe`, `Sebastian` y `Vanesa` ya contienen commits propios distintos del primero.

**VF20.** `git push` envía tus commits locales a GitHub.

## 13.4 Interpretación de código

Lee cada fragmento y responde. Los fragmentos que vienen del proyecto se muestran con su archivo y número de línea reales.

**IC1.** Observa el método `__str__` de la excepción base:

::codigo excepciones.py 18-27 | Clase SoftwareFJError

¿Qué imprime `print(EntidadDuplicadaError("un cliente", "1032456789"))`? (Pista: mira también las líneas 59-61 de `excepciones.py`).

**IC2.** ¿Qué imprime este programa?

```python
precios = [50000, 35000, 120000]
total = 0
for p in precios:
    if p > 40000:
        total += p
print(total)
```

**IC3.** Observa el cálculo detallado del costo:

::codigo modelos/servicios.py 128-146 | Servicio.calcular_costo_detallado

Una sala de 12 personas tiene tarifa de $ 50.000 por hora. ¿Qué diccionario devuelve `calcular_costo_detallado(3, 0.19, 0.10)`? ¿Y qué devuelve `calcular_costo(3)`?

**IC4.** Observa el método `cancelar`:

::codigo modelos/reserva.py 97-100 | Reserva.cancelar

Si la reserva ya está en estado «Procesada» y se llama a `reserva.cancelar()`, ¿qué excepción se lanza y cuál es su mensaje completo (con código)?

**IC5.** ¿Qué imprime este programa? Escribe las letras en orden.

```python
def prueba(valor):
    try:
        n = int(valor)
    except ValueError:
        print("A")
    else:
        print("B")
    finally:
        print("C")

prueba("7")
prueba("siete")
```

**IC6.** Observa los *setters* del nombre, correo y teléfono:

::codigo modelos/cliente.py 43-70 | Setters de Cliente

Se ejecuta `c = Cliente("80123456", "andrés   pérez", "APEREZ@Empresa.co", "601-765-4321")`. ¿Qué valores tienen `c.nombre`, `c.correo` y `c.telefono`?

**IC7.** Observa la función de porcentajes:

::codigo modelos/servicios.py 23-33 | porcentaje_a_fraccion

¿Qué devuelve `porcentaje_a_fraccion("descuento", "19,5%")`? ¿Qué pasa con `porcentaje_a_fraccion("impuesto", "120")`?

**IC8.** Observa la clase `Asesoria`:

::codigo modelos/servicios.py 241-271 | Clase Asesoria

Para `a = Asesoria("A1", "Asesoría X", 100000, "Contabilidad", "Intermedio")`, ¿qué devuelve `a.calcular_costo(2)`? ¿Qué ocurre con `a.calcular_costo(0.25)`?

**IC9.** ¿Qué imprime este programa?

```python
costos = {"subtotal": 150000, "descuento": 15000}
costos["impuesto"] = 25650
print(len(costos), costos.get("total", 0))
```

**IC10.** Observa la validación de los equipos:

::codigo modelos/servicios.py 228-235 | AlquilerEquipo.validar_parametros y calcular_costo_base

Para `e = AlquilerEquipo("E1", "Videobeam", 35000, "Proyector")`, ¿qué pasa con `e.calcular_costo(2.5)`? ¿Cuánto da `e.calcular_costo(2, 0.19)`?

## 13.5 Ejercicios prácticos

Antes de modificar el proyecto, haz una copia de la carpeta. Después de cada cambio, ejecuta `python main.py --consola` para verificar que la simulación sigue funcionando.

**EP1. Nueva regla para el nombre.** Modifica el *setter* `nombre` de `modelos/cliente.py` para que el nombre tenga como máximo 60 caracteres. Si se supera, debe lanzar `DatoInvalidoError` con el motivo «máximo 60 caracteres».

**EP2. Teléfono celular.** Agrega una regla para que, si el teléfono tiene 10 dígitos, deba empezar por «3» (celulares en Colombia). Usa `DatoInvalidoError`.

**EP3. Nuevo nivel de asesoría.** Agrega el nivel «Senior» con multiplicador 2.0 a la clase `Asesoria`. ¿Qué otro archivo muestra los niveles en la interfaz? ¿Necesitas cambiarlo?

**EP4. Contar clientes por dominio.** Escribe una función `contar_por_dominio(gestor)` que reciba un `GestorClientes` y devuelva un diccionario con cuántos clientes tiene cada dominio de correo (por ejemplo `{"mail.com": 2, "empresa.co": 1}`).

**EP5. Método `eliminar` de clientes.** Agrega a `GestorClientes` un método `eliminar(identificacion)` que busque el cliente con `obtener`, lo quite de la lista y registre el evento «Cliente eliminado: …». ¿Qué debería pasar si el cliente tiene reservas activas? Propón y escribe la regla.

**EP6. Nueva excepción.** Crea en `excepciones.py` la excepción `ClienteConReservasError` (código FJ-202), hija de `SoftwareFJError`, y úsala en el método del ejercicio EP5.

**EP7. Advertencia en el log.** Cuando se crea una reserva con descuento mayor o igual al 30 %, registra una advertencia (`registrar_advertencia`) con el texto «Descuento alto en …». ¿En qué archivo y método lo harías?

**EP8. Nueva tarjeta en el panel.** Agrega a `SistemaFJ.estadisticas()` la clave `"ticket_promedio"`: el promedio del total de las reservas confirmadas y procesadas (0 si no hay). Luego indica qué archivo de la interfaz tendrías que tocar para mostrarla.

## 13.6 Explica con tus palabras

Responde en voz alta o por escrito, como si se lo explicaras a un compañero que nunca ha programado. Usa una comparación cotidiana y un ejemplo de Software FJ.

**EC1.** ¿Qué es programar y por qué Python es un buen lenguaje para empezar?

**EC2.** ¿Cuál es la diferencia entre una clase y un objeto?

**EC3.** ¿Para qué sirve el constructor `__init__` y qué significa `self`?

**EC4.** ¿Qué es la abstracción y dónde aparece en Software FJ?

**EC5.** ¿Qué es la encapsulación y por qué protege los datos del cliente?

**EC6.** Explica la herencia con las clases de servicios.

**EC7.** Explica el polimorfismo con el cálculo del costo base.

**EC8.** ¿Qué diferencia hay entre sobrescritura y sobrecarga? ¿Cómo maneja Python la sobrecarga?

**EC9.** ¿Por qué el proyecto separa la interfaz, los gestores y los modelos?

**EC10.** ¿Qué pasa, paso a paso, cuando el usuario pulsa «Crear reserva»?

**EC11.** ¿Para qué sirven `try`, `except`, `else` y `finally` en Software FJ?

**EC12.** ¿Para qué sirven las ramas de Git en un trabajo de cinco personas?

@resumen
- Este capítulo te propuso 80 actividades: 30 de selección múltiple, 20 de verdadero o falso, 10 de interpretación de código, 8 ejercicios prácticos y 12 preguntas para explicar.
- Los ejercicios de interpretación usan código real del proyecto: predice antes de ejecutar.
- Los ejercicios prácticos extienden Software FJ respetando su arquitectura: reglas en los modelos, registro en los gestores, presentación en la interfaz.
- Las respuestas, con su justificación, están en el capítulo «Respuestas de la evaluación».
@fin
