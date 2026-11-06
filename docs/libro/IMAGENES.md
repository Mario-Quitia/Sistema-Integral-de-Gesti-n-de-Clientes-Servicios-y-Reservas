# Imágenes disponibles para `::img nombre | pie`

## Capturas reales de la aplicación (copiadas de docs/manual/capturas y docs/manual/anotadas)
01_panel_vacio, 02_clientes_vacio, 03_cliente_formulario, 04_cliente_registrado, 05_error_correo,
06_campo_invalido, 07_error_duplicado, 08_clientes_tabla, 09_cliente_edicion, 10_cliente_actualizado,
11_busqueda, 12_sin_resultados, 13_servicios_vacio, 14_form_sala, 15_servicio_registrado,
16_form_equipo, 17_form_asesoria, 18_error_tarifa, 19_campo_tarifa_invalido, 20_catalogo,
21_servicio_seleccionado, 22_disponibilidad, 23_calcular_tarifa, 24_confirmar_deshabilitar,
25_servicio_deshabilitado, 26_catalogo_deshabilitado, 27_reservas_vacio, 28_reserva_cotizacion,
29_reserva_creada, 30_aviso_duracion, 31_error_duracion, 32_aviso_descuento, 33_reserva_seleccionada,
34_confirmar_pregunta, 35_confirmada, 36_confirmada_botones, 37_procesar_pregunta, 38_procesada,
39_cancelar_pregunta, 40_motivo, 41_cancelada, 42_reservas_tabla, 43_filtro_pendiente, 44_historial,
45_servicios_ocupacion, 46_panel_con_datos, 47_eventos, 48_eventos_errores, 49_detalle_evento,
50_archivo_log, 51_acerca_de, 52_salir, 53_demo_pregunta, 54_demo_resultados, 55_panel_tras_demo
Diálogo recortado: añadir `_dlg` (p. ej. 05_error_correo_dlg, 44_historial_dlg, 40_motivo_dlg)
Anotadas con números rojos: a_ventana, a_clientes, a_servicios, a_reservas, a_eventos
Widgets Tkinter anotados (nuevas): t_widgets_clientes (Label, Entry, Button, Treeview, Frame),
t_widgets_reservas (Combobox, Entry, Label de resumen, Button), t_menu (menú lateral)

## Capturas reales del editor Visual Studio Code
vscode_main, vscode_cliente, vscode_ventana   (NO existe vscode_servicios: usar ::codigo)

## Diagramas (generados para el libro)
d_programa      entrada → proceso → salida
d_interprete    archivo .py → intérprete de Python → computador
d_variable      variables como cajas con etiqueta
d_lista_dic     lista (posiciones) frente a diccionario (claves)
d_molde         clase = molde, objetos = piezas fabricadas (Cliente → laura, andres)
d_capas         arquitectura en capas (interfaz → gestores → modelos; excepciones y registro transversales)
d_uml_modelos   UML: Entidad, Cliente, Servicio, ReservaSala, AlquilerEquipo, Asesoria, Reserva, EstadoReserva
d_uml_gestores  UML: SistemaFJ, GestorClientes, GestorServicios, GestorReservas
d_uml_interfaz  UML: VentanaPrincipal, VistaBase y las cinco vistas, componentes
d_herencia      árbol de herencia Servicio → ReservaSala / AlquilerEquipo / Asesoria
d_excepciones   jerarquía de excepciones personalizadas (SoftwareFJError ...)
d_try           flujo try / except / else / finally
d_estados       ciclo de vida de una reserva
d_costo         cálculo del costo en cinco pasos
d_recorrido     recorrido completo de 12 pasos con el archivo que interviene en cada uno
d_evento        clic → evento → método de la vista → ejecutar → gestor → resultado
d_tk_arbol      árbol de widgets de la ventana principal
d_imports       qué archivo importa a cuál
d_git_flujo     commit → push → pull request → merge (concepto general)
d_git_ramas     ramas reales del repositorio (main, Jully, Kathe, Sebastian, Vanesa)
