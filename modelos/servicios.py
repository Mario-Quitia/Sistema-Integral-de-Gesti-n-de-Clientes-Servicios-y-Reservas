"""
Clase abstracta Servicio y sus especializaciones:
ReservaSala, AlquilerEquipo y Asesoria.

Polimorfismo: cada subclase sobrescribe calcular_costo_base, describir,
validar_parametros, unidad y tipo.

Sobrecarga: calcular_costo admite tres variantes de llamada
    calcular_costo(duracion)
    calcular_costo(duracion, impuesto)
    calcular_costo(duracion, impuesto, descuento)
y calcular_costo_detallado devuelve el desglose completo.
"""
from abc import abstractmethod

from excepciones import (CalculoInconsistenteError, DatoInvalidoError,
                         ParametroFaltanteError)
from modelos.entidad import Entidad

IMPUESTO_POR_DEFECTO = 19   # IVA Colombia, en porcentaje


def porcentaje_a_fraccion(campo, valor):
    """Convierte un porcentaje (19, '19', '19%') en fracción (0.19). Vacío -> None."""
    if valor is None or str(valor).strip() == "":
        return None
    try:
        porcentaje = float(str(valor).replace("%", "").replace(",", ".").strip())
    except ValueError as error:
        raise CalculoInconsistenteError(f"El {campo} '{valor}' no es un número.") from error
    if not 0 <= porcentaje <= 100:
        raise CalculoInconsistenteError(f"El {campo} debe estar entre 0 y 100 % (recibido {valor}).")
    return porcentaje / 100


class Servicio(Entidad):
    """Servicio genérico ofrecido por Software FJ."""

    def __init__(self, codigo, nombre, tarifa, cupo):
        codigo = str(codigo or "").strip().upper()
        if not codigo:
            raise ParametroFaltanteError("código")
        super().__init__(codigo)
        nombre = str(nombre or "").strip()
        if len(nombre) < 3:
            raise DatoInvalidoError("nombre", nombre, "mínimo 3 caracteres")
        self._nombre = nombre
        self._tarifa = self._numero_positivo("tarifa", tarifa)
        self._cupo = int(self._numero_positivo("cupo", cupo))
        self._disponible = True

    # ---------- utilidades de validación ----------
    @staticmethod
    def _numero_positivo(campo, valor, maximo=None):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError(campo)
        try:
            numero = float(valor)
        except (TypeError, ValueError) as error:
            # Encadenamiento: se conserva el error original como causa
            raise DatoInvalidoError(campo, valor, "debe ser numérico") from error
        if numero <= 0:
            raise DatoInvalidoError(campo, valor, "debe ser mayor que cero")
        if maximo is not None and numero > maximo:
            raise DatoInvalidoError(campo, valor, f"no puede superar {maximo}")
        return numero

    # ---------- propiedades ----------
    @property
    def codigo(self):
        return self._identificador

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa(self):
        return self._tarifa

    @property
    def cupo(self):
        return self._cupo

    @property
    def disponible(self):
        return self._disponible

    def habilitar(self):
        self._disponible = True

    def deshabilitar(self):
        self._disponible = False

    # ---------- contrato abstracto (polimorfismo) ----------
    @property
    @abstractmethod
    def tipo(self):
        """Nombre legible del tipo de servicio."""

    @property
    @abstractmethod
    def unidad(self):
        """Unidad de la duración (horas, días...)."""

    @abstractmethod
    def validar_parametros(self, duracion):
        """Valida la duración y devuelve el valor normalizado."""

    @abstractmethod
    def calcular_costo_base(self, duracion):
        """Costo sin impuestos ni descuentos."""

    @abstractmethod
    def detalle(self):
        """Atributos específicos del servicio en texto."""

    # ---------- métodos "sobrecargados" ----------
    def calcular_costo(self, duracion, impuesto=None, descuento=None):
        """
        Variantes:
          calcular_costo(d)            -> costo base
          calcular_costo(d, i)         -> base + impuesto i
          calcular_costo(d, i, desc)   -> (base - descuento) + impuesto
        """
        return self.calcular_costo_detallado(duracion, impuesto, descuento)["total"]

    def calcular_costo_detallado(self, duracion, impuesto=None, descuento=None):
        duracion = self.validar_parametros(duracion)
        base = self.calcular_costo_base(duracion)
        tasa_imp = 0.0 if impuesto is None else self._tasa("impuesto", impuesto)
        tasa_desc = 0.0 if descuento is None else self._tasa("descuento", descuento)
        valor_descuento = round(base * tasa_desc, 2)
        neto = base - valor_descuento
        valor_impuesto = round(neto * tasa_imp, 2)
        total = round(neto + valor_impuesto, 2)
        if total < 0 or base <= 0:
            raise CalculoInconsistenteError(
                f"Resultado inválido para {self.codigo}: base={base}, total={total}")
        return {
            "duracion": duracion,
            "subtotal": round(base, 2),
            "descuento": valor_descuento,
            "impuesto": valor_impuesto,
            "total": total,
        }

    @staticmethod
    def _tasa(campo, valor):
        """Valida una tasa expresada como fracción (0.19 = 19 %)."""
        try:
            tasa = float(valor)
        except (TypeError, ValueError) as error:
            raise DatoInvalidoError(campo, valor, "debe ser numérico") from error
        if not 0 <= tasa <= 1:
            raise CalculoInconsistenteError(f"El {campo} debe estar entre 0% y 100% (recibido {valor}).")
        return tasa

    def _validar_rango(self, duracion, minimo, maximo):
        valor = self._numero_positivo("duración", duracion)
        if not minimo <= valor <= maximo:
            raise DatoInvalidoError("duración", duracion,
                                    f"para {self.tipo} debe estar entre {minimo} y {maximo} {self.unidad}")
        return valor

    def describir(self):
        estado = "Disponible" if self._disponible else "No disponible"
        return f"{self.tipo} '{self.nombre}' [{self.codigo}] - {self.detalle()} - " \
               f"${self.tarifa:,.0f}/{self.unidad[:-1] if self.unidad.endswith('s') else self.unidad} - {estado}"

    def a_diccionario(self):
        return {
            "codigo": self.codigo,
            "tipo": self.tipo,
            "nombre": self.nombre,
            "detalle": self.detalle(),
            "tarifa": self.tarifa,
            "unidad": self.unidad,
            "cupo": self.cupo,
            "disponible": self.disponible,
        }


class ReservaSala(Servicio):
    """Reserva de salas por horas. Salas grandes tienen recargo del 10 %."""

    def __init__(self, codigo, nombre, tarifa_hora, capacidad, cupo=2):
        super().__init__(codigo, nombre, tarifa_hora, cupo)
        self._capacidad = int(self._numero_positivo("capacidad", capacidad, maximo=500))

    tipo = "Sala"
    unidad = "horas"

    @property
    def capacidad(self):
        return self._capacidad

    def validar_parametros(self, duracion):
        return self._validar_rango(duracion, 1, 12)

    def calcular_costo_base(self, duracion):
        recargo = 1.10 if self._capacidad > 20 else 1.0
        return self.tarifa * duracion * recargo

    def detalle(self):
        return f"Capacidad {self._capacidad} personas"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos por días. Incluye seguro del 5 % sobre el subtotal."""

    TASA_SEGURO = 0.05

    def __init__(self, codigo, nombre, tarifa_dia, tipo_equipo, unidades=1):
        super().__init__(codigo, nombre, tarifa_dia, unidades)
        tipo_equipo = str(tipo_equipo or "").strip()
        if not tipo_equipo:
            raise ParametroFaltanteError("tipo de equipo")
        self._tipo_equipo = tipo_equipo

    tipo = "Equipo"
    unidad = "días"

    @property
    def tipo_equipo(self):
        return self._tipo_equipo

    def validar_parametros(self, duracion):
        valor = self._validar_rango(duracion, 1, 30)
        if valor != int(valor):
            raise DatoInvalidoError("duración", duracion, "los equipos se alquilan por días completos")
        return int(valor)

    def calcular_costo_base(self, duracion):
        return self.tarifa * duracion * (1 + self.TASA_SEGURO)

    def detalle(self):
        return f"{self._tipo_equipo}, {self.cupo} unidad(es), seguro 5%"


class Asesoria(Servicio):
    """Asesoría especializada por horas, con multiplicador según el nivel."""

    NIVELES = {"Básico": 1.0, "Intermedio": 1.3, "Experto": 1.6}

    def __init__(self, codigo, nombre, tarifa_hora, especialidad, nivel="Básico", cupo=1):
        super().__init__(codigo, nombre, tarifa_hora, cupo)
        especialidad = str(especialidad or "").strip()
        if not especialidad:
            raise ParametroFaltanteError("especialidad")
        if nivel not in self.NIVELES:
            raise DatoInvalidoError("nivel", nivel, f"use uno de {', '.join(self.NIVELES)}")
        self._especialidad = especialidad
        self._nivel = nivel

    tipo = "Asesoría"
    unidad = "horas"

    @property
    def especialidad(self):
        return self._especialidad

    @property
    def nivel(self):
        return self._nivel

    def validar_parametros(self, duracion):
        return self._validar_rango(duracion, 0.5, 8)

    def calcular_costo_base(self, duracion):
        return self.tarifa * duracion * self.NIVELES[self._nivel]

    def detalle(self):
        return f"{self._especialidad} (nivel {self._nivel})"
