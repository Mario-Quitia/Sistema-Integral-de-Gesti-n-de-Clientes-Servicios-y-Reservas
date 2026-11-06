"""Gestión del ciclo de vida de las reservas."""
from excepciones import (CalculoInconsistenteError, EntidadNoEncontradaError,
                         ReservaError, ServicioNoDisponibleError, SoftwareFJError)
from modelos.reserva import EstadoReserva, Reserva
from modelos.servicios import porcentaje_a_fraccion
from registro import registrar_error, registrar_evento

DESCUENTO_MAXIMO = 0.50


class GestorReservas:
    def __init__(self, gestor_clientes, gestor_servicios):
        self._clientes = gestor_clientes
        self._servicios = gestor_servicios
        self._reservas = []
        gestor_servicios.contador_ocupacion = self.contar_activas

    # ---------- utilidades ----------
    def contar_activas(self, servicio):
        return sum(1 for r in self._reservas if r.servicio is servicio and r.activa)

    def _preparar(self, codigo_servicio, duracion, impuesto, descuento):
        """impuesto y descuento llegan en porcentaje (19 = 19 %)."""
        servicio = self._servicios.obtener(codigo_servicio)
        impuesto = porcentaje_a_fraccion("impuesto", impuesto)
        descuento = porcentaje_a_fraccion("descuento", descuento)
        if descuento is not None and descuento > DESCUENTO_MAXIMO:
            raise CalculoInconsistenteError(
                f"El descuento máximo permitido es {DESCUENTO_MAXIMO:.0%}.")
        return servicio, impuesto, descuento

    # ---------- operaciones ----------
    def cotizar(self, codigo_servicio, duracion, impuesto=None, descuento=None):
        """Calcula el costo sin crear la reserva (para la vista previa)."""
        servicio, impuesto, descuento = self._preparar(codigo_servicio, duracion, impuesto, descuento)
        return servicio.calcular_costo_detallado(duracion, impuesto, descuento)

    def crear(self, id_cliente, codigo_servicio, duracion, impuesto=None, descuento=None):
        try:
            cliente = self._clientes.obtener(id_cliente)
            servicio, impuesto, descuento = self._preparar(codigo_servicio, duracion, impuesto, descuento)
            if not servicio.disponible:
                raise ServicioNoDisponibleError(servicio.nombre, "está deshabilitado")
            if self.contar_activas(servicio) >= servicio.cupo:
                raise ServicioNoDisponibleError(servicio.nombre, "no tiene cupos libres")
            reserva = Reserva(cliente, servicio, duracion, impuesto, descuento)
        except SoftwareFJError as error:
            registrar_error("Reserva fallida", error)
            raise
        except Exception as error:
            registrar_error("Error inesperado al crear reserva", error)
            raise ReservaError("Ocurrió un error inesperado al crear la reserva.") from error
        self._reservas.append(reserva)
        registrar_evento(f"Reserva creada: {reserva.describir()}")
        return reserva

    def _transicion(self, codigo, accion, *args):
        reserva = self.obtener(codigo)
        try:
            getattr(reserva, accion)(*args)
        except SoftwareFJError as error:
            registrar_error(f"No se pudo {accion} {reserva.codigo}", error)
            raise
        registrar_evento(f"Reserva {reserva.codigo} -> {reserva.estado}")
        return reserva

    def confirmar(self, codigo):
        return self._transicion(codigo, "confirmar")

    def cancelar(self, codigo, motivo="Cancelada por el usuario"):
        return self._transicion(codigo, "cancelar", motivo)

    def procesar(self, codigo):
        return self._transicion(codigo, "procesar")

    # ---------- consultas ----------
    def obtener(self, codigo):
        codigo = str(codigo or "").strip().upper()
        for reserva in self._reservas:
            if reserva.codigo == codigo:
                return reserva
        error = EntidadNoEncontradaError("una reserva", codigo)
        registrar_error("Consulta de reserva", error)
        raise error

    def listar(self, estado=None):
        if estado:
            return [r for r in self._reservas if r.estado == estado]
        return list(self._reservas)

    def total(self, estado=None):
        return len(self.listar(estado))

    def ingresos(self):
        return round(sum(r.total for r in self._reservas
                         if r.estado in (EstadoReserva.CONFIRMADA, EstadoReserva.PROCESADA)), 2)
