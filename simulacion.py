"""
Simulación de 15 operaciones (válidas e inválidas) sobre Software FJ.

Se puede ejecutar:
  - desde la interfaz (botón "Ejecutar demostración"), o
  - por consola:  python simulacion.py
Cada operación se ejecuta de forma aislada: si falla, se registra y se
continúa con la siguiente, demostrando que el sistema nunca se detiene.
"""
from excepciones import SoftwareFJError
from registro import registrar_critico, registrar_evento


def _operaciones(s):
    """Lista de (descripción, se_espera_exito, función)."""
    ctx = {}

    def reservar_laura():
        ctx["reserva"] = s.reservas.crear("1032456789", "SAL-01", 3, 19, 10)
        return ctx["reserva"]

    def confirmar_y_procesar():
        codigo = ctx["reserva"].codigo
        s.reservas.confirmar(codigo)
        return s.reservas.procesar(codigo)

    return [
        ("Registrar cliente válido: Laura Gómez", True,
         lambda: s.clientes.registrar("1032456789", "Laura Gómez", "laura.gomez@mail.com", "3104567890")),
        ("Registrar cliente válido: Andrés Pérez", True,
         lambda: s.clientes.registrar("80123456", "Andrés Pérez", "aperez@empresa.co", "6017654321")),
        ("Registrar cliente con correo inválido", False,
         lambda: s.clientes.registrar("52987654", "María Ruiz", "maria.ruiz@", "3001112233")),
        ("Registrar cliente duplicado (1032456789)", False,
         lambda: s.clientes.registrar("1032456789", "Laura Duplicada", "otra@mail.com", "3100000000")),
        ("Registrar sala de juntas válida", True,
         lambda: s.servicios.registrar_sala("SAL-01", "Sala Ejecutiva", 50000, 12, 2)),
        ("Registrar equipo válido: videobeam", True,
         lambda: s.servicios.registrar_equipo("EQU-01", "Videobeam Epson", 35000, "Proyector", 1)),
        ("Registrar asesoría válida (experto)", True,
         lambda: s.servicios.registrar_asesoria("ASE-01", "Asesoría en Ciberseguridad", 120000,
                                                "Seguridad informática", "Experto", 1)),
        ("Registrar servicio con tarifa negativa", False,
         lambda: s.servicios.registrar_sala("SAL-02", "Sala Mini", -20000, 4)),
        ("Reserva exitosa: Laura - Sala 3 h, IVA 19 %, desc. 10 %", True,
         reservar_laura),
        ("Reserva con duración fuera de rango (40 días de equipo)", False,
         lambda: s.reservas.crear("80123456", "EQU-01", 40, 19)),
        ("Reserva exitosa: Andrés - Videobeam 2 días", True,
         lambda: s.reservas.crear("80123456", "EQU-01", 2, 19)),
        ("Reserva sin cupo: segundo alquiler del único videobeam", False,
         lambda: s.reservas.crear("1032456789", "EQU-01", 1, 19)),
        ("Confirmar y procesar (facturar) la reserva de Laura", True,
         confirmar_y_procesar),
        ("Cancelar la reserva ya procesada (operación no permitida)", False,
         lambda: s.reservas.cancelar(ctx["reserva"].codigo)),
        ("Reserva para cliente inexistente", False,
         lambda: s.reservas.crear("99999999", "ASE-01", 2, 19)),
    ]


def ejecutar_simulacion(sistema, al_reportar=None):
    """
    Ejecuta las 15 operaciones. `al_reportar(numero, descripcion, ok, detalle)`
    se llama tras cada una (la GUI lo usa para mostrar el progreso).
    Devuelve la lista de resultados.
    """
    resultados = []
    registrar_evento("===== INICIO DE LA SIMULACIÓN DE 15 OPERACIONES =====")
    for numero, (descripcion, esperado, operacion) in enumerate(_operaciones(sistema), start=1):
        ok, detalle = False, ""
        try:
            retorno = operacion()
        except SoftwareFJError as error:
            detalle = str(error)
        except Exception as error:   # error grave inesperado: se registra y se continúa
            registrar_critico(f"Error inesperado en la operación {numero}", error)
            detalle = f"Error inesperado: {type(error).__name__}: {error}"
        else:
            ok = True
            detalle = (retorno.describir() if hasattr(retorno, "describir")
                       else f"Total facturado: ${retorno:,.2f}" if isinstance(retorno, float)
                       else f"Resultado: {retorno}")
        finally:
            fila = {"numero": numero, "descripcion": descripcion, "ok": ok,
                    "esperado": esperado, "detalle": detalle}
            resultados.append(fila)
            if al_reportar:
                al_reportar(fila)
    exitos = sum(r["ok"] for r in resultados)
    registrar_evento(f"===== FIN DE LA SIMULACIÓN: {exitos} exitosas, "
                     f"{len(resultados) - exitos} controladas con error =====")
    return resultados


if __name__ == "__main__":
    import sys
    from gestores import SistemaFJ

    sys.stdout.reconfigure(encoding="utf-8")

    for r in ejecutar_simulacion(SistemaFJ()):
        marca = "OK   " if r["ok"] else "ERROR"
        print(f"{r['numero']:>2}. [{marca}] {r['descripcion']}\n      -> {r['detalle']}")
