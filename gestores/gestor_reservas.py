
"""
Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas
Empresa: Software FJ
Módulo: Gestión de Reservas
Autora: July Viviana Matabanchoy Guacas

Descripción:
Este módulo permite administrar el ciclo de vida de las reservas,
incluyendo su creación, confirmación, cancelación, procesamiento
y consulta.
"""

# Importación de las excepciones personalizadas que permiten
# controlar los diferentes errores que pueden presentarse
# durante la gestión de las reservas.
from excepciones import (
    CalculoInconsistenteError,
    EntidadNoEncontradaError,
    ReservaError,
    ServicioNoDisponibleError,
    SoftwareFJError
)

# Importación de la clase Reserva y del enumerador EstadoReserva,
# que permiten crear reservas y controlar sus diferentes estados.
from modelos.reserva import EstadoReserva, Reserva

# Importación de la función que convierte porcentajes a fracciones.
# Se utiliza para realizar correctamente los cálculos de impuestos
# y descuentos.
from modelos.servicios import porcentaje_a_fraccion

# Importación de las funciones encargadas de registrar
# los errores y los eventos importantes del sistema en los logs.
from registro import registrar_error, registrar_evento


# Constante que establece el descuento máximo permitido
# para una reserva: 0.50 equivale al 50 %.
DESCUENTO_MAXIMO = 0.50


# Clase encargada de administrar todas las operaciones
# relacionadas con las reservas del sistema.
class GestorReservas:

    # Constructor de la clase.
    # Recibe los gestores de clientes y servicios para poder
    # relacionar las reservas con los clientes y servicios registrados.
    def __init__(self, gestor_clientes, gestor_servicios):

        # Guarda la referencia al gestor de clientes.
        self._clientes = gestor_clientes

        # Guarda la referencia al gestor de servicios.
        self._servicios = gestor_servicios

        # Crea una lista vacía donde se almacenarán las reservas.
        self._reservas = []

        # Asigna al gestor de servicios la función que permite
        # consultar cuántas reservas activas tiene cada servicio.
        gestor_servicios.contador_ocupacion = self.contar_activas


    # ---------- UTILIDADES ----------

    # Cuenta cuántas reservas activas existen para un servicio.
    def contar_activas(self, servicio):

        # Recorre las reservas registradas y cuenta únicamente
        # aquellas que pertenecen al servicio indicado y están activas.
        return sum(
            1 for r in self._reservas
            if r.servicio is servicio and r.activa
        )


    # Prepara y valida los datos necesarios antes de realizar
    # una cotización o crear una reserva.
    def _preparar(self, codigo_servicio, duracion, impuesto, descuento):

        # Busca el servicio utilizando su código.
        # Los impuestos y descuentos se reciben en porcentaje,
        # por ejemplo, 19 representa el 19 %.
        servicio = self._servicios.obtener(codigo_servicio)

        # Convierte el porcentaje del impuesto a una fracción decimal.
        impuesto = porcentaje_a_fraccion("impuesto", impuesto)

        # Convierte el porcentaje del descuento a una fracción decimal.
        descuento = porcentaje_a_fraccion("descuento", descuento)

        # Comprueba que el descuento no supere el máximo permitido.
        if descuento is not None and descuento > DESCUENTO_MAXIMO:

            # Genera una excepción cuando el descuento supera el 50 %.
            raise CalculoInconsistenteError(
                f"El descuento máximo permitido es {DESCUENTO_MAXIMO:.0%}."
            )

        # Devuelve el servicio y los porcentajes ya convertidos
        # para utilizarlos en los cálculos posteriores.
        return servicio, impuesto, descuento


    # ---------- OPERACIONES ----------

    # Calcula el costo de una reserva sin crearla.
    # Este método permite mostrar una cotización previa al usuario.
    def cotizar(self, codigo_servicio, duracion, impuesto=None, descuento=None):

        # Prepara y valida los datos del servicio, impuesto y descuento.
        servicio, impuesto, descuento = self._preparar(
            codigo_servicio, duracion, impuesto, descuento
        )

        # Solicita al servicio el cálculo detallado del costo,
        # teniendo en cuenta la duración, el impuesto y el descuento.
        return servicio.calcular_costo_detallado(
            duracion, impuesto, descuento
        )


    # Crea una nueva reserva relacionando un cliente con un servicio.
    def crear(self, id_cliente, codigo_servicio, duracion,
              impuesto=None, descuento=None):

        # Inicia el bloque de control de errores para evitar
        # que una operación incorrecta interrumpa inesperadamente
        # el funcionamiento del sistema.
        try:

            # Busca al cliente mediante su número de identificación.
            cliente = self._clientes.obtener(id_cliente)

            # Busca el servicio y prepara los valores del cálculo.
            servicio, impuesto, descuento = self._preparar(
                codigo_servicio, duracion, impuesto, descuento
            )

            # Verifica que el servicio esté habilitado.
            if not servicio.disponible:

                # Genera un error si el servicio está deshabilitado.
                raise ServicioNoDisponibleError(
                    servicio.nombre, "está deshabilitado"
                )

            # Comprueba que el servicio tenga cupos disponibles.
            if self.contar_activas(servicio) >= servicio.cupo:

                # Genera un error cuando ya no existen cupos libres.
                raise ServicioNoDisponibleError(
                    servicio.nombre, "no tiene cupos libres"
                )

            # Crea el objeto reserva con los datos del cliente,
            # servicio, duración, impuesto y descuento.
            reserva = Reserva(
                cliente, servicio, duracion, impuesto, descuento
            )

        # Captura los errores relacionados con entidades no encontradas.
        # Se vuelve a generar el error porque el método obtener
        # del gestor ya se encarga de registrarlo.
        except EntidadNoEncontradaError:
            raise

        # Captura los errores personalizados del sistema.
        # Registra el error y lo vuelve a generar para que pueda
        # ser atendido por el nivel superior del programa.
        except SoftwareFJError as error:
            registrar_error("Reserva fallida", error)
            raise

        # Captura cualquier otro error inesperado que no haya
        # sido contemplado en las excepciones anteriores.
        except Exception as error:

            # Registra el error inesperado en el archivo de logs.
            registrar_error("Error inesperado al crear reserva", error)

            # Genera una excepción propia de reservas y conserva
            # el error original como causa mediante "from error".
            raise ReservaError(
                "Ocurrió un error inesperado al crear la reserva."
            ) from error

        # Agrega la reserva creada a la lista de reservas del sistema.
        # Esta instrucción se ejecuta cuando no se produjo ningún error.
        self._reservas.append(reserva)

        # Registra en el archivo de eventos la creación de la reserva.
        registrar_evento(f"Reserva creada: {reserva.describir()}")

        # Devuelve el objeto reserva creado.
        return reserva


    # Método interno que permite ejecutar una acción sobre una reserva.
    # Recibe el código de la reserva, el nombre de la acción
    # y los argumentos adicionales que pueda necesitar.
    def _transicion(self, codigo, accion, *args):

        # Busca la reserva correspondiente al código indicado.
        reserva = self.obtener(codigo)

        # Controla los errores que puedan presentarse al ejecutar
        # la acción solicitada sobre la reserva.
        try:

            # Ejecuta dinámicamente el método solicitado.
            # getattr obtiene el método de la reserva cuyo nombre
            # se recibe en el parámetro accion.
            # *args permite enviar argumentos adicionales si son necesarios.
            getattr(reserva, accion)(*args)

        # Captura los errores personalizados que puedan producirse
        # durante la confirmación, cancelación o procesamiento.
        except SoftwareFJError as error:

            # Registra el error indicando la acción y el código
            # de la reserva en la que ocurrió.
            registrar_error(
                f"No se pudo {accion} {reserva.codigo}", error
            )

            # Vuelve a generar el error para que sea atendido
            # por el programa que llamó este método.
            raise

        # Registra el nuevo estado de la reserva después
        # de ejecutar correctamente la operación.
        registrar_evento(
            f"Reserva {reserva.codigo} -> {reserva.estado}"
        )

        # Devuelve la reserva con su estado actualizado.
        return reserva


    # Confirma una reserva previamente registrada.
    def confirmar(self, codigo):

        # Utiliza el método interno para ejecutar la acción confirmar.
        return self._transicion(codigo, "confirmar")


    # Cancela una reserva y permite indicar el motivo de cancelación.
    # Si no se proporciona un motivo, utiliza uno predeterminado.
    def cancelar(self, codigo, motivo="Cancelada por el usuario"):

        # Ejecuta la acción cancelar y envía el motivo correspondiente.
        return self._transicion(codigo, "cancelar", motivo)


    # Procesa una reserva de acuerdo con las reglas definidas
    # en la clase Reserva.
    def procesar(self, codigo):

        # Utiliza el método interno para ejecutar la acción procesar.
        return self._transicion(codigo, "procesar")


    # ---------- CONSULTAS ----------

    # Busca una reserva utilizando su código.
    def obtener(self, codigo):

        # Convierte el código a texto, elimina espacios innecesarios
        # y lo transforma a mayúsculas para facilitar su búsqueda.
        codigo = str(codigo or "").strip().upper()

        # Recorre todas las reservas almacenadas.
        for reserva in self._reservas:

            # Compara el código solicitado con el código de cada reserva.
            if reserva.codigo == codigo:

                # Devuelve la reserva cuando encuentra una coincidencia.
                return reserva

        # Si termina el recorrido y no encuentra la reserva,
        # crea una excepción indicando que no existe.
        error = EntidadNoEncontradaError("una reserva", codigo)

        # Registra el error de consulta en el archivo de logs.
        registrar_error("Consulta de reserva", error)

        # Genera la excepción para informar que la reserva no existe.
        raise error


    # Devuelve la lista de reservas.
    # Si se indica un estado, muestra únicamente las reservas
    # que coincidan con dicho estado.
    def listar(self, estado=None):

        # Cuando se especifica un estado, filtra las reservas.
        if estado:
            return [
                r for r in self._reservas
                if r.estado == estado
            ]

        # Cuando no se especifica un estado, devuelve todas
        # las reservas mediante una copia de la lista.
        return list(self._reservas)


    # Calcula la cantidad de reservas registradas.
    # También permite contar las reservas de un estado específico.
    def total(self, estado=None):

        # Obtiene la lista correspondiente y cuenta sus elementos.
        return len(self.listar(estado))


    # Calcula los ingresos generados por las reservas.
    def ingresos(self):

        # Suma el total de las reservas que se encuentran
        # confirmadas o procesadas.
        # Las reservas pendientes o canceladas no se incluyen.
        # round(..., 2) limita el resultado a dos decimales.
        return round(
            sum(
                r.total for r in self._reservas
                if r.estado in (
                    EstadoReserva.CONFIRMADA,
                    EstadoReserva.PROCESADA
                )
            ),
            2
        )
