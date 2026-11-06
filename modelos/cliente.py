"""Clase Cliente con validaciones y encapsulación de datos personales."""
import re

from excepciones import DatoInvalidoError, ParametroFaltanteError
from modelos.entidad import Entidad

_PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)*\.[A-Za-z]{2,}$")
_PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' ]+$")


class Cliente(Entidad):
    """Cliente de Software FJ. Todos sus datos se validan al asignarse."""

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(self._validar_identificacion(identificacion))
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # ---------- validaciones (estáticas, reutilizables) ----------
    @staticmethod
    def _obligatorio(campo, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError(campo)
        return str(valor).strip()

    @classmethod
    def _validar_identificacion(cls, valor):
        valor = cls._obligatorio("identificación", valor)
        if not valor.isdigit() or not 5 <= len(valor) <= 12:
            raise DatoInvalidoError("identificación", valor, "debe tener entre 5 y 12 dígitos")
        return valor

    # ---------- propiedades encapsuladas ----------
    @property
    def identificacion(self):
        return self._identificador

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor = self._obligatorio("nombre", valor)
        if len(valor) < 3 or not _PATRON_NOMBRE.match(valor):
            raise DatoInvalidoError("nombre", valor, "solo letras y mínimo 3 caracteres")
        self.__nombre = " ".join(p.capitalize() for p in valor.split())

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        valor = self._obligatorio("correo", valor).lower()
        if not _PATRON_CORREO.match(valor):
            raise DatoInvalidoError("correo", valor, "formato de correo no válido")
        self.__correo = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        valor = self._obligatorio("teléfono", valor).replace(" ", "").replace("-", "")
        if not valor.isdigit() or not 7 <= len(valor) <= 10:
            raise DatoInvalidoError("teléfono", valor, "debe tener entre 7 y 10 dígitos")
        self.__telefono = valor

    @property
    def correo_oculto(self):
        """Muestra el correo parcialmente para proteger el dato personal."""
        usuario, dominio = self.__correo.split("@")
        return f"{usuario[:2]}***@{dominio}"

    # ---------- implementación de la abstracción ----------
    def describir(self):
        return f"Cliente {self.nombre} (ID {self.identificacion})"

    def a_diccionario(self):
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "telefono": self.telefono,
        }
