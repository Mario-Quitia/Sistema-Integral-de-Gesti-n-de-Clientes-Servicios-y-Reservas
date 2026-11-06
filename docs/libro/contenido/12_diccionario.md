# Diccionario para principiantes
> Las palabras raras dejan de asustar cuando se explican con ejemplos de todos los días.

@objetivos
- Consultar rápidamente el significado de los términos de programación usados en el libro.
- Relacionar cada término con una situación cotidiana y con una línea de Python.
- Usar este capítulo como apoyo para estudiar la sustentación.
@fin

## 12.1 Cómo usar este diccionario

Los términos están en orden alfabético. Cada uno tiene cuatro partes: la **palabra**, un **significado sencillo**, un **ejemplo cotidiano** que lo conecta con algo conocido y un **ejemplo de Python**, casi siempre tomado o inspirado en Software FJ. Cuando una palabra viene del inglés, se indica su traducción.

@consejo
No intentes memorizar el diccionario de una vez. Vuelve a él cada vez que en otro capítulo encuentres una palabra que no recuerdes.
@fin

## 12.2 Términos de la A a la Z

### A

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| Abstracción | Mostrar solo lo importante y ocultar los detalles. | Usas el control del televisor sin saber cómo funciona por dentro. | `class Servicio(Entidad)` define qué debe hacer todo servicio sin decir cómo. |
| Abstracta (clase) | Clase que sirve de modelo y no se puede usar para crear objetos directamente. | El plano general de «vehículo»: nadie maneja un «vehículo» genérico, maneja un carro o una moto. | `class Entidad(ABC):` |
| Algoritmo | Lista ordenada de pasos para resolver un problema. | Una receta de cocina. | Los cinco pasos de `calcular_costo_detallado`. |
| Argumento | Valor concreto que se entrega a una función al llamarla. | El dato que le das al cajero: «retire 50.000». | `registrar_evento("Inicio")` |
| Atributo | Dato que pertenece a un objeto. | El color y la placa de un carro. | `self.codigo` |

### B

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| Biblioteca (librería) | Conjunto de herramientas ya escritas que se pueden reutilizar. | Una caja de herramientas comprada. | `import tkinter` |
| Booleano | Dato que solo puede ser verdadero o falso. | Un interruptor: encendido o apagado. | `self._disponible = True` |
| Bucle (ciclo) | Instrucción que repite un bloque varias veces. | Dar vueltas a la cancha hasta completar diez. | `for cliente in self._clientes:` |
| Botón | Elemento de la ventana que ejecuta una acción al hacer clic. | El timbre de una casa. | `ttk.Button(barra, text="Buscar", command=self.buscar)` |

### C

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| Cadena (string) | Texto: letras, números o símbolos entre comillas. | Lo que escribes en un mensaje de texto. | `nombre = "Laura Gómez"` |
| Clase | Molde que define cómo serán ciertos objetos. | El molde para hacer arepas. | `class Cliente(Entidad):` |
| Clave | Nombre con el que se busca un valor en un diccionario. | La palabra que buscas en un diccionario de español. | `costos["total"]` |
| Código fuente | Texto con las instrucciones del programa. | La partitura de una canción. | El contenido de `main.py`. |
| Comentario | Nota para personas que Python ignora. | Una nota adhesiva en un libro. | `# IVA Colombia, en porcentaje` |
| Commit | Fotografía guardada de los cambios en Git. | Guardar una versión de un documento con fecha. | `git commit -m "cambios actualizados"` |
| Condicional | Instrucción que decide qué hacer según una condición. | «Si llueve, llevo paraguas». | `if numero <= 0:` |
| Constante | Valor que no debería cambiar. | La cantidad de días de la semana. | `IMPUESTO_POR_DEFECTO = 19` |
| Constructor | Método que prepara un objeto recién creado. | Llenar la ficha de inscripción de un estudiante nuevo. | `def __init__(self, codigo, nombre, tarifa, cupo):` |
| Consola (terminal) | Ventana de texto donde se escriben órdenes. | Hablar con el computador por escrito. | `python main.py --consola` |

### D

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| Decorador | Etiqueta con `@` que cambia el comportamiento de una función. | Ponerle un sello a un documento para darle otro uso. | `@property` |
| Depurar | Buscar y corregir errores. | Revisar una receta que salió mal para saber qué falló. | Leer el `software_fj.log`. |
| Diccionario | Colección de datos con nombre (clave) y valor. | Una agenda: nombre → teléfono. | `{"subtotal": 150000, "total": 160650}` |
| Docstring | Texto entre triples comillas que explica una función o clase. | La etiqueta con instrucciones de un electrodoméstico. | `"""Excepción base de todo el sistema."""` |

### E

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| Encadenar excepciones | Lanzar un error nuevo guardando el error que lo causó. | «No prende a causa de la batería». | `raise DatoInvalidoError(...) from error` |
| Encapsulación | Proteger los datos de un objeto para que solo se cambien por caminos controlados. | El dinero del banco solo se mueve por el cajero, no metiendo la mano en la bóveda. | `self.__correo` |
| Entero (int) | Número sin decimales. | La cantidad de personas en un salón. | `cupo = 2` |
| Evento | Algo que pasa en la ventana: un clic, una tecla. | Que suene el timbre. | `"<<TreeviewSelect>>"` |
| Excepción | Aviso de que algo impidió continuar normalmente. | El pitazo del árbitro cuando hay falta. | `raise ServicioNoDisponibleError(...)` |
| Ejecutar | Poner a funcionar un programa. | Darle *play* a una canción. | `python main.py` |
| Except | Bloque que dice qué hacer si ocurre una excepción. | La red debajo del trapecista. | `except SoftwareFJError as error:` |

### F

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| Fachada | Clase que reúne varias piezas y ofrece una sola puerta de entrada. | La recepción de un hotel que te comunica con todos los servicios. | `class SistemaFJ:` |
| Finally | Bloque que se ejecuta siempre al final de un `try`. | Apagar la estufa, se queme o no el arroz. | `finally: registrar_evento(...)` |
| Flotante (float) | Número con decimales. | Un precio de 2,5 kilos. | `tasa = 0.19` |
| For | Ciclo que recorre los elementos de una colección. | Revisar uno por uno los cuadernos de un salón. | `for servicio in self._servicios:` |
| Función | Bloque de código con nombre que realiza una tarea. | Una licuadora: le das frutas y devuelve jugo. | `def registrar_evento(mensaje):` |
| f-string | Texto con valores insertados entre llaves. | Una plantilla «Hola, ___». | `f"Reserva {self.codigo}"` |

### G

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| Gestor | En Software FJ, clase que administra una lista de clientes, servicios o reservas. | El administrador de un edificio. | `class GestorReservas:` |
| Git | Programa que guarda el historial de cambios de un proyecto. | Un álbum con todas las versiones de un trabajo. | `git log` |
| GitHub | Sitio web que guarda repositorios Git en Internet. | Una nube para compartir el álbum con el equipo. | `git push origin main` |
| Getter | Método que permite leer un atributo protegido. | La ventanilla donde consultas tu saldo. | `@property def nombre(self):` |

### H

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| Handler | Pieza de `logging` que decide dónde se guardan los mensajes. | El cartero que decide a qué buzón va cada carta. | `logging.FileHandler(RUTA_LOG)` |
| Herencia | Una clase recibe los atributos y métodos de otra. | Un hijo hereda rasgos de sus padres. | `class ReservaSala(Servicio):` |

### I

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| If / elif / else | Palabras para tomar decisiones: si, si no si, si no. | «Si hace sol, voy a la playa; si llueve, al cine; si no, me quedo». | `if tipo == "Sala": ... elif tipo == "Equipo": ... else: ...` |
| Import | Traer herramientas de otro archivo o módulo. | Pedir prestada una herramienta al vecino. | `from modelos.cliente import Cliente` |
| Indentación (sangría) | Espacios al inicio de la línea que indican qué código está dentro de qué. | Los subtítulos de un índice que van corridos a la derecha. | Las líneas dentro de un `def` van con 4 espacios. |
| Input | Función que pide un dato al usuario por teclado. | Preguntar «¿cómo te llamas?». | `nombre = input("Nombre: ")` |
| Instancia | Un objeto concreto creado a partir de una clase. | Una arepa específica salida del molde. | `laura = Cliente("1032456789", ...)` |
| Intérprete | Programa que lee el código Python y lo ejecuta línea por línea. | Un traductor simultáneo. | `python` |

### L

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| Lambda | Función pequeña sin nombre, escrita en una línea. | Una nota rápida en lugar de una carta. | `lambda servicio: 0` |
| Lista | Colección ordenada de elementos. | La lista del mercado. | `self._clientes = []` |
| Log | Registro de eventos con fecha y hora. | La bitácora de un barco. | `software_fj.log` |
| Logger | Objeto que se encarga de anotar en el log. | El secretario que toma el acta. | `logging.getLogger("software_fj")` |

### M

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| Mainloop | Ciclo que mantiene la ventana abierta esperando acciones. | Un portero que espera, todo el día, a que alguien toque. | `app.mainloop()` |
| Merge | Unir los cambios de una rama con otra en Git. | Juntar las partes de un trabajo grupal en un solo documento. | `git merge Vanesa` |
| Messagebox | Ventanita emergente de Tkinter con un mensaje. | Una notificación en el celular. | `messagebox.showinfo("Operación exitosa", texto)` |
| Método | Función que pertenece a una clase. | Lo que sabe hacer un objeto: un carro sabe «arrancar». | `def confirmar(self):` |
| Módulo | Archivo `.py` con código que se puede importar. | Un capítulo de un libro. | `registro.py` |

### O

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| Objeto | Algo concreto con datos y acciones, creado a partir de una clase. | Tu celular: tiene marca (dato) y puede llamar (acción). | `reserva = Reserva(cliente, servicio, 3)` |
| Operador | Símbolo que realiza una operación. | Los signos de una calculadora. | `base * tasa_desc` |

### P

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| Parámetro | Nombre de un dato que una función espera recibir. | El espacio en blanco de un formulario. | `def cancelar(self, motivo="Cancelada por el usuario"):` |
| Polimorfismo | Varias clases responden al mismo mensaje cada una a su manera. | «Haz sonido»: el perro ladra, el gato maúlla. | `calcular_costo_base` distinto en sala, equipo y asesoría. |
| POO | Programación orientada a objetos: organizar el programa en clases y objetos. | Organizar una empresa en departamentos con funciones claras. | `Cliente`, `Servicio`, `Reserva` |
| Print | Función que muestra texto en la consola. | Hablar en voz alta. | `print(f"{r['numero']:>2}. [{marca}]")` |
| Property | Decorador que convierte un método en algo que se lee como atributo. | Una ventanilla que muestra un dato sin abrir la bóveda. | `@property def total(self):` |
| Pull | Traer a tu computador los cambios que están en GitHub. | Descargar la última versión del trabajo grupal. | `git pull origin main` |
| Pull Request | Solicitud en GitHub para unir una rama a otra, con revisión. | Entregar tu parte al coordinador para que la revise antes de unirla. | Se crea desde la página de GitHub. |
| Push | Enviar tus commits a GitHub. | Subir tu versión a la nube. | `git push origin Kathe` |

### R

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| Raise | Lanzar una excepción a propósito. | Tocar el silbato cuando alguien rompe una regla. | `raise ParametroFaltanteError(campo)` |
| Rama (branch) | Línea de trabajo paralela en Git. | Cada integrante escribe su capítulo en un borrador aparte. | `git checkout -b Sebastian` |
| Repositorio | Carpeta del proyecto con todo su historial en Git. | El archivo histórico de una empresa. | `git clone https://github.com/...` |
| Return | Palabra que devuelve un resultado y termina la función. | La licuadora entrega el jugo. | `return cliente` |

### S

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| Self | Palabra con la que un objeto se refiere a sí mismo. | Decir «yo» o «mi». | `self._estado = EstadoReserva.PENDIENTE` |
| Setter | Método que controla cómo se cambia un atributo. | El cajero que verifica tu clave antes de cambiar tu saldo. | `@correo.setter` |
| Sintaxis | Reglas de escritura del lenguaje. | La ortografía y gramática del español. | Olvidar `:` después de `if` es un error de sintaxis. |
| Sobrecarga | Llamar un mismo método de varias formas. Python la imita con valores por defecto. | Pedir un café solo, con leche o con leche y azúcar en la misma caja. | `calcular_costo(d)`, `calcular_costo(d, i)`, `calcular_costo(d, i, desc)` |
| Sobrescritura | Una clase hija redefine un método heredado. | El hijo aprende la receta familiar pero le cambia un ingrediente. | `def calcular_costo_base(self, duracion):` en `Asesoria` |
| Super | Función para usar el código de la clase madre. | Pedirle ayuda a tus padres con algo que ellos ya saben hacer. | `super().__init__(codigo)` |

### T

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| Tipo de dato | Clase de información: texto, entero, decimal, booleano… | No es lo mismo un número de teléfono que una edad. | `type(19)` devuelve `int` |
| Tkinter | Biblioteca de Python para crear ventanas. | Un kit de piezas para armar tableros. | `import tkinter as tk` |
| Traceback | Informe que muestra dónde ocurrió un error no atrapado. | El rastro de huellas que lleva hasta el problema. | `Traceback (most recent call last): ...` |
| Treeview | Tabla de Tkinter para mostrar filas y columnas. | Una hoja de cálculo pequeña. | `ttk.Treeview(self, columns=self._claves)` |
| Try | Bloque con el código que podría fallar. | El trapecista que intenta la acrobacia. | `try: numero = float(valor)` |
| Tupla | Colección ordenada que no se puede modificar. | Las coordenadas de un lugar en un mapa. | `ACTIVOS = (PENDIENTE, CONFIRMADA)` |

### V

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| Validar | Verificar que un dato cumple las reglas. | El portero que revisa tu carné antes de dejarte entrar. | `if not valor.isdigit():` |
| Variable | Nombre que guarda un valor. | Una caja con etiqueta. | `total = round(neto + valor_impuesto, 2)` |
| Ventana emergente | Ventana pequeña que aparece sobre la principal. | Un aviso que sale en la pantalla del cajero. | `messagebox.askyesno("Salir", "¿Desea cerrar Software FJ?")` |
| Visual Studio Code | Editor de texto para escribir código. | Un procesador de palabras especial para programar. | Abrir la carpeta del proyecto con `code .` |

### W

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| While | Ciclo que se repite mientras una condición sea verdadera. | «Mientras haya platos sucios, sigo lavando». | `while intentos < 3:` |
| Widget | Cualquier pieza visual de una ventana: botón, etiqueta, campo… | Las piezas de un tablero de control. | `ttk.Label`, `ttk.Entry`, `ttk.Combobox` |
| With | Abre un recurso y lo cierra automáticamente al terminar. | Abrir la llave del agua y cerrarla al salir. | `with open(RUTA_LOG, encoding="utf-8") as f:` |

### Símbolos

| Palabra | Significado sencillo | Ejemplo cotidiano | Ejemplo de Python |
|---|---|---|---|
| `__init__` | Nombre especial del constructor. | La ficha de bienvenida. | `def __init__(self, identificador):` |
| `__str__` | Método especial que define cómo se ve un objeto como texto. | La forma de presentarse: «Soy…». | `return f"[{self.codigo}] {self.mensaje}"` |
| `#` | Inicio de un comentario. | Una nota al margen. | `# rollback` |
| `@` | Indica un decorador. | Un sello en un documento. | `@staticmethod` |
| `==` | Compara si dos valores son iguales. | Preguntar «¿son iguales?». | `if s.codigo == codigo:` |
| `=` | Asigna un valor a una variable. | Poner algo dentro de la caja. | `libres = max(servicio.cupo - ocupados, 0)` |

@resumen
- Este diccionario reúne más de 90 términos de programación, Python, POO, Tkinter, excepciones y Git.
- Cada término se explica con un significado sencillo, una comparación cotidiana y un ejemplo de código.
- Muchos ejemplos de código provienen directamente de Software FJ: úsalos para reconocer los términos cuando leas el proyecto.
- Vuelve a este capítulo cada vez que una palabra técnica te detenga.
@fin
