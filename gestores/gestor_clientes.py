"""Gestión de clientes en memoria (lista interna, sin base de datos)."""
from excepciones import EntidadDuplicadaError, EntidadNoEncontradaError, SoftwareFJError
from modelos.cliente import Cliente
from registro import registrar_error, registrar_evento


class GestorClientes:
    def __init__(self):
        self._clientes = []

    def registrar(self, identificacion, nombre, correo, telefono):
        try:
            identificacion = str(identificacion or "").strip()
            if any(c.identificacion == identificacion for c in self._clientes):
                raise EntidadDuplicadaError("un cliente", identificacion)
            cliente = Cliente(identificacion, nombre, correo, telefono)
        except SoftwareFJError as error:
            registrar_error("Registro de cliente rechazado", error)
            raise
        else:
            self._clientes.append(cliente)
            registrar_evento(f"Cliente registrado: {cliente.describir()}")
            return cliente

    def actualizar(self, identificacion, nombre, correo, telefono):
        cliente = self.obtener(identificacion)
        respaldo = (cliente.nombre, cliente.correo, cliente.telefono)
        try:
            cliente.nombre, cliente.correo, cliente.telefono = nombre, correo, telefono
        except SoftwareFJError as error:
            cliente.nombre, cliente.correo, cliente.telefono = respaldo   # rollback
            registrar_error(f"Actualización de cliente {identificacion} rechazada", error)
            raise
        registrar_evento(f"Cliente actualizado: {cliente.describir()}")
        return cliente

    def obtener(self, identificacion):
        identificacion = str(identificacion or "").strip()
        for cliente in self._clientes:
            if cliente.identificacion == identificacion:
                return cliente
        error = EntidadNoEncontradaError("un cliente", identificacion)
        registrar_error("Consulta de cliente", error)
        raise error

    def buscar(self, texto):
        """Busca por identificación o por parte del nombre/correo (no lanza error)."""
        texto = str(texto or "").strip().lower()
        if not texto:
            return self.listar()
        return [c for c in self._clientes
                if texto in c.identificacion or texto in c.nombre.lower() or texto in c.correo]

    def listar(self):
        return list(self._clientes)

    def total(self):
        return len(self._clientes)
