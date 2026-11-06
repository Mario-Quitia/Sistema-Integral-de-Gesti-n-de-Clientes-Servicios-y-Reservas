"""Clase abstracta base para todas las entidades del sistema."""
from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):
    """Representa cualquier entidad identificable de Software FJ."""

    def __init__(self, identificador):
        self._identificador = identificador
        self._fecha_creacion = datetime.now()

    @property
    def identificador(self):
        return self._identificador

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def describir(self):
        """Devuelve una descripción legible de la entidad."""

    @abstractmethod
    def a_diccionario(self):
        """Representación plana, útil para tablas e informes."""

    def __eq__(self, otro):
        return isinstance(otro, Entidad) and type(self) is type(otro) \
            and self._identificador == otro._identificador

    def __hash__(self):
        return hash((type(self).__name__, self._identificador))

    def __repr__(self):
        return f"{type(self).__name__}({self._identificador!r})"
