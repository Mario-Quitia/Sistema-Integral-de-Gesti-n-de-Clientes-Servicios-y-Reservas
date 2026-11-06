# Formato de los archivos de contenido del libro

Cada capítulo es un archivo UTF-8 en `docs/libro/contenido/NN_nombre.md`.
El constructor (`construir_libro.py`) lo convierte a PDF y DOCX. Reglas:

## Estructura
```
# Título del capítulo
> Frase de presentación del capítulo (una línea, opcional)

@objetivos
- Al terminar este capítulo podrás ...
@fin

## 1.1 Sección (numerar a mano: capítulo.sección)
### Subsección (sin número)
Párrafo normal. Inline: **negrita**, *cursiva*, `código corto`.
Los párrafos se separan con una línea en blanco. Una línea = un párrafo (no partir con saltos).

- viñeta
1. lista numerada

@resumen
- punto clave
@fin
```
Cada capítulo DEBE empezar con `@objetivos` y terminar con `@resumen`.

## Recuadros (bloques que terminan con `@fin`)
`@nivel1`  → «Nivel 1 · Explicación cotidiana»  
`@nivel2`  → «Nivel 2 · Explicación informática»  
`@nivel3`  → «Nivel 3 · En Software FJ»  
`@nota`, `@consejo`, `@importante`, `@atencion`, `@ejemplo`, `@recuerda`, `@ejercicio`, `@pregunta`  
Título opcional: `@ejemplo: Una tienda de barrio`. Dentro de un recuadro se permiten párrafos,
viñetas, bloques de código y `::codigo`.

## Código
Código didáctico (NO del proyecto), escrito a mano:
````
```python
nombre = "Laura"
print(nombre)
```
````
Salida de consola: bloque con lenguaje `salida`. Comandos de terminal: lenguaje `consola`.

Código REAL del proyecto (nunca copiarlo a mano; el constructor lo lee del archivo):
```
::codigo modelos/cliente.py 13-27 | Constructor de la clase Cliente
```
(ruta relativa a la raíz del proyecto, rango de líneas inclusive, pie opcional).
Para explicar línea por línea, justo después:
```
::lineas
13 | Se define la clase Cliente, que hereda de Entidad.
16-19 | El constructor recibe los cuatro datos y ...
::fin
```

## Imágenes
`::img nombre | Pie de figura`  (nombre sin extensión; ver lista en IMAGENES.md)

## Tablas (estilo Markdown)
```
| Columna A | Columna B |
|---|---|
| dato | dato |
```

## Otros
`\salto` en una línea sola = salto de página.
No usar emojis. Usar comillas «» en el texto. Tono: profesor paciente, tuteo («tú»).
