# SOFTWARE FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

UNAD · Programación (213023) · Fase 4. Aplicación de escritorio en Python + Tkinter,
orientada a objetos, sin base de datos (todo en memoria) y con registro de eventos en
`software_fj.log`.

## Ejecución

```bash
python main.py            # abre la interfaz gráfica
python main.py --demo     # abre la interfaz y lanza la simulación de 15 operaciones
python main.py --consola  # ejecuta solo la simulación en consola
```

Requisitos: Python 3.8+ (Tkinter viene incluido en la instalación estándar).

## Estructura

```
main.py                 Punto de entrada único
excepciones.py          Jerarquía de excepciones personalizadas (SoftwareFJError ...)
registro.py             Logging a software_fj.log + eventos en memoria para la GUI
simulacion.py           15 operaciones válidas e inválidas
modelos/                Lógica de dominio
    entidad.py          Clase abstracta Entidad
    cliente.py          Cliente con validaciones y encapsulación
    servicios.py        Servicio (abstracta) -> ReservaSala, AlquilerEquipo, Asesoria
    reserva.py          Reserva: confirmar, cancelar, procesar
gestores/               Capa que la interfaz invoca (listas internas)
    gestor_clientes.py, gestor_servicios.py, gestor_reservas.py, SistemaFJ (fachada)
interfaz/               Interfaz gráfica Tkinter (sin reglas de negocio)
    ventana_principal.py  Ventana, menú lateral, encabezado, errores globales, demostración
    dashboard.py          Panel principal + vista de eventos y logs
    vista_clientes.py     Formulario y tabla de clientes
    vista_servicios.py    Registro de salas/equipos/asesorías, disponibilidad y tarifas
    vista_reservas.py     Creación, confirmación, procesamiento y cancelación de reservas
    componentes.py        Estilos, tarjetas, tablas, formularios y VistaBase.ejecutar
```

## Conceptos aplicados

| Requisito | Dónde |
|---|---|
| Clase abstracta general | `modelos/entidad.py` (`Entidad`) |
| Herencia y polimorfismo | `Servicio` → `ReservaSala`, `AlquilerEquipo`, `Asesoria` (`calcular_costo_base`, `validar_parametros`, `detalle`) |
| Encapsulación | Propiedades con validación en `Cliente` (atributos `__nombre`, `__correo`...) |
| Métodos sobrecargados | `Servicio.calcular_costo(d)`, `(d, impuesto)`, `(d, impuesto, descuento)` |
| Excepciones personalizadas | `excepciones.py` |
| try/except/else/finally | `Reserva.procesar`, `simulacion.ejecutar_simulacion`, gestores |
| Encadenamiento (`raise ... from`) | `Servicio._numero_positivo`, `porcentaje_a_fraccion`, `Reserva.procesar` |
| Logs | `registro.py` → `software_fj.log` |

## Reglas de la interfaz

- Los botones solo llaman a los gestores mediante `VistaBase.ejecutar`, que captura
  cualquier excepción y la muestra con `messagebox` (advertencia o error).
- `VentanaPrincipal.report_callback_exception` atrapa cualquier error no previsto: se
  registra en el log y la aplicación sigue abierta.
- Tras cada operación exitosa `notificar_cambio()` refresca todas las tablas y tarjetas.

## Trabajo por ramas

| Integrante | Rama sugerida | Archivos |
|---|---|---|
| 1 | `feature/vista-clientes` | `interfaz/vista_clientes.py` |
| 2 | `feature/vista-servicios` | `interfaz/vista_servicios.py` |
| 3 | `feature/vista-reservas` | `interfaz/vista_reservas.py` |
| 4 | `feature/integracion-gestores` | `gestores/`, `interfaz/componentes.py` |
| 5 | `feature/ventana-principal` | `interfaz/ventana_principal.py`, `interfaz/dashboard.py`, `main.py`, pruebas |
