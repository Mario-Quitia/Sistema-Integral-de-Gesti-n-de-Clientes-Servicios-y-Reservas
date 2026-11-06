"""
Excepciones personalizadas del sistema Software FJ.

Jerarquía:
    SoftwareFJError
    ├── ValidacionError
    │   ├── DatoInvalidoError
    │   └── ParametroFaltanteError
    ├── EntidadNoEncontradaError
    ├── EntidadDuplicadaError
    ├── ServicioNoDisponibleError
    ├── ReservaError
    │   └── OperacionNoPermitidaError
    └── CalculoInconsistenteError
"""


class SoftwareFJError(Exception):
    """Excepción base de todo el sistema."""

    def __init__(self, mensaje, codigo="FJ-000"):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo

    def __str__(self):
        return f"[{self.codigo}] {self.mensaje}"


class ValidacionError(SoftwareFJError):
    """Error genérico de validación de datos."""

    def __init__(self, mensaje, campo=None, codigo="FJ-100"):
        super().__init__(mensaje, codigo)
        self.campo = campo


class DatoInvalidoError(ValidacionError):
    """Un dato tiene un formato o valor no permitido."""

    def __init__(self, campo, valor, motivo):
        super().__init__(f"Valor inválido para '{campo}' ({valor!r}): {motivo}",
                         campo=campo, codigo="FJ-101")
        self.valor = valor


class ParametroFaltanteError(ValidacionError):
    """Falta un parámetro obligatorio."""

    def __init__(self, campo):
        super().__init__(f"El campo '{campo}' es obligatorio.", campo=campo, codigo="FJ-102")


class EntidadNoEncontradaError(SoftwareFJError):
    def __init__(self, tipo, identificador):
        super().__init__(f"No existe {tipo} con identificador '{identificador}'.", "FJ-200")


class EntidadDuplicadaError(SoftwareFJError):
    def __init__(self, tipo, identificador):
        super().__init__(f"Ya existe {tipo} con identificador '{identificador}'.", "FJ-201")


class ServicioNoDisponibleError(SoftwareFJError):
    def __init__(self, servicio, motivo="el servicio no está disponible"):
        super().__init__(f"Servicio '{servicio}': {motivo}.", "FJ-300")


class ReservaError(SoftwareFJError):
    def __init__(self, mensaje, codigo="FJ-400"):
        super().__init__(mensaje, codigo)


class OperacionNoPermitidaError(ReservaError):
    def __init__(self, operacion, estado):
        super().__init__(f"No se puede '{operacion}' una reserva en estado '{estado}'.", "FJ-401")


class CalculoInconsistenteError(SoftwareFJError):
    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-500")
