"""Clase Reserva: integra cliente, servicio, duración, costo y estado."""
from datetime import datetime
from itertools import count

from excepciones import (CalculoInconsistenteError, OperacionNoPermitidaError,
                         ReservaError, ServicioNoDisponibleError, SoftwareFJError)
from modelos.cliente import Cliente
from modelos.entidad import Entidad
from modelos.servicios import Servicio
from registro import registrar_error, registrar_evento


class EstadoReserva:
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    PROCESADA = "Procesada"
    CANCELADA = "Cancelada"
    ACTIVOS = (PENDIENTE, CONFIRMADA)


class Reserva(Entidad):
    _secuencia = count(1)

    def __init__(self, cliente, servicio, duracion, impuesto=None, descuento=None):
        if not isinstance(cliente, Cliente):
            raise ReservaError("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaError("La reserva requiere un servicio válido.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(servicio.nombre, "está deshabilitado")
        try:
            costos = servicio.calcular_costo_detallado(duracion, impuesto, descuento)
        except SoftwareFJError:
            raise
        except Exception as error:
            raise CalculoInconsistenteError("Error inesperado al calcular el costo de la reserva") from error
        # El consecutivo solo se asigna cuando la reserva es válida
        super().__init__(f"R-{next(Reserva._secuencia):04d}")
        self._cliente = cliente
        self._servicio = servicio
        self._impuesto = impuesto
        self._descuento = descuento
        self._costos = costos
        self._duracion = self._costos["duracion"]
        self._estado = EstadoReserva.PENDIENTE
        self._historial = [(datetime.now(), EstadoReserva.PENDIENTE, "Reserva creada")]

    # ---------- propiedades ----------
    @property
    def codigo(self):
        return self._identificador

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    @property
    def costos(self):
        return dict(self._costos)

    @property
    def total(self):
        return self._costos["total"]

    @property
    def historial(self):
        return list(self._historial)

    @property
    def activa(self):
        return self._estado in EstadoReserva.ACTIVOS

    # ---------- transiciones de estado ----------
    def _cambiar_estado(self, nuevo, nota):
        self._estado = nuevo
        self._historial.append((datetime.now(), nuevo, nota))

    def confirmar(self):
        if self._estado != EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError("confirmar", self._estado)
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(self._servicio.nombre, "se deshabilitó antes de confirmar")
        self._cambiar_estado(EstadoReserva.CONFIRMADA, "Reserva confirmada")

    def cancelar(self, motivo="Cancelada por el usuario"):
        if self._estado not in EstadoReserva.ACTIVOS:
            raise OperacionNoPermitidaError("cancelar", self._estado)
        self._cambiar_estado(EstadoReserva.CANCELADA, motivo or "Sin motivo")

    def procesar(self):
        """
        Procesa (factura) la reserva. Demuestra try/except/else/finally:
        - except: registra y re-lanza encadenando la causa.
        - else: solo si todo salió bien se marca como procesada.
        - finally: siempre deja constancia del intento.
        """
        resultado = None
        try:
            if self._estado != EstadoReserva.CONFIRMADA:
                raise OperacionNoPermitidaError("procesar", self._estado)
            recalculado = self._servicio.calcular_costo(self._duracion, self._impuesto, self._descuento)
            if abs(recalculado - self.total) > 0.01:
                raise CalculoInconsistenteError(
                    f"El total almacenado ({self.total}) no coincide con el recalculado ({recalculado}).")
        except OperacionNoPermitidaError:
            raise
        except SoftwareFJError as error:
            registrar_error(f"Fallo al procesar {self.codigo}", error)
            raise ReservaError(f"No fue posible procesar la reserva {self.codigo}.") from error
        else:
            self._cambiar_estado(EstadoReserva.PROCESADA, f"Facturada por ${self.total:,.2f}")
            resultado = self.total
        finally:
            registrar_evento(f"Intento de procesamiento de {self.codigo} -> estado {self._estado}")
        return resultado

    # ---------- abstracción ----------
    def describir(self):
        return (f"Reserva {self.codigo}: {self._cliente.nombre} - {self._servicio.nombre} "
                f"({self._duracion:g} {self._servicio.unidad}) - ${self.total:,.2f} - {self._estado}")

    def a_diccionario(self):
        return {
            "codigo": self.codigo,
            "cliente": self._cliente.nombre,
            "identificacion": self._cliente.identificacion,
            "servicio": self._servicio.nombre,
            "tipo": self._servicio.tipo,
            "duracion": f"{self._duracion:g} {self._servicio.unidad}",
            **self._costos,
            "estado": self._estado,
            "fecha": self.fecha_creacion.strftime("%Y-%m-%d %H:%M"),
        }
