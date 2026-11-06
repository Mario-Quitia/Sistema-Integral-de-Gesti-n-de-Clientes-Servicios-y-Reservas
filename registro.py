"""
Registro de eventos y errores en el archivo software_fj.log.

Además de escribir en disco, guarda los últimos eventos en memoria para que
la interfaz pueda mostrarlos sin volver a leer el archivo.
"""
import logging
import os
from collections import deque
from datetime import datetime

RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "software_fj.log")


class _MemoriaHandler(logging.Handler):
    """Handler que conserva los últimos N registros en una lista circular."""

    def __init__(self, capacidad=500):
        super().__init__()
        self.registros = deque(maxlen=capacidad)
        self.oyentes = []

    def emit(self, record):
        entrada = {
            "fecha": datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S"),
            "nivel": record.levelname,
            "mensaje": record.getMessage(),
        }
        self.registros.append(entrada)
        for oyente in list(self.oyentes):
            try:
                oyente(entrada)
            except Exception:  # un oyente defectuoso nunca debe romper el log
                pass


_memoria = _MemoriaHandler()


def _configurar():
    logger = logging.getLogger("software_fj")
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)
    archivo = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    archivo.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(archivo)
    logger.addHandler(_memoria)
    logger.propagate = False
    return logger


logger = _configurar()


def registrar_evento(mensaje):
    logger.info(mensaje)


def registrar_advertencia(mensaje):
    logger.warning(mensaje)


def registrar_error(mensaje, excepcion=None):
    if excepcion is not None:
        causa = excepcion.__cause__
        detalle = f" | causa: {type(causa).__name__}: {causa}" if causa else ""
        logger.error(f"{mensaje} -> {type(excepcion).__name__}: {excepcion}{detalle}")
    else:
        logger.error(mensaje)


def registrar_critico(mensaje, excepcion=None):
    logger.critical(mensaje, exc_info=excepcion)


def eventos_recientes(nivel=None):
    """Devuelve los eventos en memoria (más recientes primero)."""
    datos = list(_memoria.registros)
    if nivel:
        datos = [d for d in datos if d["nivel"] in nivel]
    return list(reversed(datos))


def suscribir(oyente):
    _memoria.oyentes.append(oyente)


def leer_archivo_log():
    try:
        with open(RUTA_LOG, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "(El archivo de log aún no existe)"
