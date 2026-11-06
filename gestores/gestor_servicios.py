"""Gestión del catálogo de servicios (salas, equipos y asesorías)."""
from excepciones import EntidadDuplicadaError, EntidadNoEncontradaError, SoftwareFJError
from modelos.servicios import AlquilerEquipo, Asesoria, ReservaSala, porcentaje_a_fraccion
from registro import registrar_error, registrar_evento


class GestorServicios:
    def __init__(self):
        self._servicios = []
        # Función que devuelve cuántas reservas activas tiene un servicio.
        # La asigna el sistema al conectar con el gestor de reservas.
        self.contador_ocupacion = lambda servicio: 0

    # ---------- registro (un método por tipo) ----------
    def _agregar(self, fabrica, descripcion):
        try:
            servicio = fabrica()
            if any(s.codigo == servicio.codigo for s in self._servicios):
                raise EntidadDuplicadaError("un servicio", servicio.codigo)
        except SoftwareFJError as error:
            registrar_error(f"Registro de {descripcion} rechazado", error)
            raise
        self._servicios.append(servicio)
        registrar_evento(f"Servicio registrado: {servicio.describir()}")
        return servicio

    def registrar_sala(self, codigo, nombre, tarifa_hora, capacidad, cupo=2):
        return self._agregar(lambda: ReservaSala(codigo, nombre, tarifa_hora, capacidad, cupo), "sala")

    def registrar_equipo(self, codigo, nombre, tarifa_dia, tipo_equipo, unidades=1):
        return self._agregar(lambda: AlquilerEquipo(codigo, nombre, tarifa_dia, tipo_equipo, unidades),
                             "equipo")

    def registrar_asesoria(self, codigo, nombre, tarifa_hora, especialidad, nivel="Básico", cupo=1):
        return self._agregar(lambda: Asesoria(codigo, nombre, tarifa_hora, especialidad, nivel, cupo),
                             "asesoría")

    # ---------- consultas ----------
    def obtener(self, codigo):
        codigo = str(codigo or "").strip().upper()
        for servicio in self._servicios:
            if servicio.codigo == codigo:
                return servicio
        error = EntidadNoEncontradaError("un servicio", codigo)
        registrar_error("Consulta de servicio", error)
        raise error

    def listar(self, tipo=None):
        if tipo:
            return [s for s in self._servicios if s.tipo == tipo]
        return list(self._servicios)

    def total(self):
        return len(self._servicios)

    def consultar_disponibilidad(self, codigo):
        servicio = self.obtener(codigo)
        ocupados = self.contador_ocupacion(servicio)
        libres = max(servicio.cupo - ocupados, 0)
        return {
            "servicio": servicio,
            "habilitado": servicio.disponible,
            "ocupados": ocupados,
            "libres": libres,
            "disponible": servicio.disponible and libres > 0,
        }

    def cambiar_habilitacion(self, codigo, habilitado):
        servicio = self.obtener(codigo)
        if habilitado:
            servicio.habilitar()
        else:
            servicio.deshabilitar()
        registrar_evento(f"Servicio {servicio.codigo} {'habilitado' if habilitado else 'deshabilitado'}")
        return servicio

    def calcular_tarifa(self, codigo, duracion, impuesto=None, descuento=None):
        """impuesto y descuento en porcentaje (19 = 19 %)."""
        servicio = self.obtener(codigo)
        try:
            return servicio.calcular_costo_detallado(
                duracion,
                porcentaje_a_fraccion("impuesto", impuesto),
                porcentaje_a_fraccion("descuento", descuento))
        except SoftwareFJError as error:
            registrar_error(f"Cálculo de tarifa para {servicio.codigo}", error)
            raise
