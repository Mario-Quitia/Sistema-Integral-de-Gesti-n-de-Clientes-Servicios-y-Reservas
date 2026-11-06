"""Capa de gestores: punto de entrada de la interfaz hacia la lógica de negocio."""
from gestores.gestor_clientes import GestorClientes
from gestores.gestor_servicios import GestorServicios
from gestores.gestor_reservas import GestorReservas
from modelos.reserva import EstadoReserva


class SistemaFJ:
    """Fachada que agrupa los tres gestores y ofrece estadísticas globales."""

    def __init__(self):
        self.clientes = GestorClientes()
        self.servicios = GestorServicios()
        self.reservas = GestorReservas(self.clientes, self.servicios)

    def estadisticas(self):
        return {
            "clientes": self.clientes.total(),
            "servicios": self.servicios.total(),
            "servicios_disponibles": sum(
                1 for s in self.servicios.listar()
                if self.servicios.consultar_disponibilidad(s.codigo)["disponible"]),
            "reservas": self.reservas.total(),
            "pendientes": self.reservas.total(EstadoReserva.PENDIENTE),
            "confirmadas": self.reservas.total(EstadoReserva.CONFIRMADA),
            "procesadas": self.reservas.total(EstadoReserva.PROCESADA),
            "canceladas": self.reservas.total(EstadoReserva.CANCELADA),
            "ingresos": self.reservas.ingresos(),
        }


__all__ = ["GestorClientes", "GestorServicios", "GestorReservas", "SistemaFJ"]
