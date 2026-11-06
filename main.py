"""
SOFTWARE FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas.

Uso:
    python main.py            -> abre la interfaz gráfica
    python main.py --demo     -> abre la interfaz y ejecuta la demostración
    python main.py --consola  -> ejecuta solo la simulación de 15 operaciones en consola
"""
import sys

from registro import registrar_critico, registrar_evento


def main():
    argumentos = set(sys.argv[1:])
    if "--consola" in argumentos:
        import runpy
        runpy.run_module("simulacion", run_name="__main__")
        return 0

    try:
        from interfaz import VentanaPrincipal
        app = VentanaPrincipal()
        if "--demo" in argumentos:
            app.after(600, app.ejecutar_demostracion)
        app.mainloop()
    except Exception as error:   # error fatal al iniciar: se registra antes de salir
        registrar_critico("No fue posible iniciar la interfaz gráfica", error)
        print(f"Error al iniciar Software FJ: {error}. Revise software_fj.log", file=sys.stderr)
        return 1
    finally:
        registrar_evento("Fin de la ejecución de Software FJ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
