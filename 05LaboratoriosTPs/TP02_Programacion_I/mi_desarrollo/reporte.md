# Reporte del TP02 – Programación I

**Trabajo:** Controlador de misiones  
**Archivo:** `tp02_uberti_abril.py`  
**Comisión:** 582918

**Integrantes:**
- Federico Mara
- Abril Uberti
- Mariana Bogarin
- Franco Fernandez
- Tiziano Ginel
- Luciana Olivieri

---

## 1. Modalidad de desarrollo

La modalidad de desarrollo fue **mixta (programación manual con asistencia de inteligencia artificial)**.

El grupo elaboró una primera versión de las cuatro funciones principales del controlador: `comando_es_valido`, `ejecutar_comando`, `ejecutar_mision` y `generar_reporte`. Posteriormente, el código fue revisado y mejorado mediante una conversación con una herramienta de inteligencia artificial, que también colaboró en la preparación de pruebas y en la interpretación de sus resultados.

La ejecución de las pruebas en el simulador estuvo a cargo del grupo.

## 2. Tiempo empleado

A continuación, se detalla el tiempo aproximado dedicado a cada etapa del trabajo.

| Actividad | Tiempo (minutos) |
|---|---:|
| Análisis | 15 |
| Programación | 30 |
| Pruebas | 10 |
| Presentación del trabajo y elaboración del reporte | 10 |
| **Tiempo total** | **65** |

## 3. Uso de inteligencia artificial

### 3.1. Herramienta utilizada

| Ítem | Detalle |
|---|---|
| Herramienta | Claude (Anthropic) |
| Plataforma | Chat web de [claude.ai](https://claude.ai/) |
| Modelo | Claude Sonnet |
| Modalidad de uso | Asistente conversacional |
| Integración con el editor | No se utilizó integración con el editor ni autocompletado de código. |

### 3.2. Material proporcionado

Para trabajar con la herramienta se utilizaron los siguientes materiales:

- La guía del TP02.
- El archivo base `mi_tp02.py` del repositorio.
- El archivo `misiones.py`.
- Las salidas de consola obtenidas durante las ejecuciones del programa.

### 3.3. Aportes de la inteligencia artificial

La herramienta colaboró en la revisión y mejora de distintos aspectos de la implementación:

- **Validación de comandos:** revisión de los tipos de datos, la cantidad de parámetros y los límites de velocidad y tiempo, incluyendo casos especiales como `nan`, `inf` y valores booleanos.
- **Manejo de errores:** adecuación de `ejecutar_comando` para que devuelva un texto, de acuerdo con su *docstring*, y capture la excepción `ErrorDeSeguridad`.
- **Continuidad de las misiones:** incorporación de un bloque `try/except` adicional en `ejecutar_mision`, con el objetivo de evitar que un error inesperado interrumpa la ejecución completa de la misión.
- **Documentación del código:** elaboración de *docstrings* para las funciones auxiliares, siguiendo el formato del apunte: Objetivo, Parámetros y Retorna.
- **Selección de misiones:** incorporación de la posibilidad de seleccionar una misión mediante un argumento de línea de comandos, manteniendo `MISION_BASICA` como opción predeterminada.
- **Pruebas adicionales:** creación de una misión propia denominada `MISION_BORDES`, destinada a evaluar casos límite.

### 3.4. Verificación de los resultados

Las modificaciones propuestas se verificaron mediante la ejecución del programa en el simulador, utilizando las cuatro misiones proporcionadas en el material original y la misión propia `MISION_BORDES`.

Se compararon los resultados de los reportes obtenidos en cada ejecución con los resultados esperados, con el propósito de comprobar el comportamiento del controlador y la gestión de los comandos válidos e inválidos.

## 4. Resultados de las pruebas

Las pruebas se realizaron en el simulador con los robots G1 y Go2.

| Misión | Comandos ejecutados | Comandos rechazados | Total de comandos | Resultado |
|---|---:|---:|---:|---|
| `MISION_BASICA` | 4 | 0 | 4 | Correcto |
| `MISION_CUADRADO` | 9 | 0 | 9 | Correcto |
| `MISION_CON_ERRORES` | 4 | 7 | 11 | Correcto |
| `MISION_LARGA` | 9 | 0 | 9 | Correcto |
| `MISION_BORDES` (propia) | 3 | 7 | 10 | Correcto |

### 4.1. Prueba de comandos inválidos

En la misión `MISION_CON_ERRORES` se rechazaron siete comandos inválidos por los siguientes motivos:

1. Velocidad de `0.9 m/s`.
2. Tiempo de ejecución de `50 s`.
3. Velocidad de giro de `3.0 rad/s`.
4. Comando inexistente: `volar`.
5. Velocidad con un valor no numérico.
6. Comando sin especificación del tiempo requerido.
7. Tiempo de ejecución negativo.

La misión continuó después de cada rechazo, lo que permitió comprobar que los comandos inválidos eran gestionados sin interrumpir la secuencia completa.

## 5. Observaciones y limitaciones

- **Visualización del saludo:** el simulador no muestra visualmente la acción de saludo con ninguno de los dos robots probados (G1 y Go2). Sin embargo, el reporte registra el comando `saludar` como ejecutado y sin errores.
- **Alcance de las pruebas:** las verificaciones se realizaron exclusivamente en el simulador. Por lo tanto, los resultados permiten evaluar la lógica del controlador, pero no garantizan que el comportamiento sea idéntico en un robot físico real.

## 6. Conclusión

A partir de las pruebas realizadas, se verificó el funcionamiento del controlador con las misiones proporcionadas y con una misión adicional destinada a evaluar casos límite. Los resultados registrados muestran que los comandos válidos se ejecutaron y que los comandos inválidos fueron rechazados según los casos evaluados.

Asimismo, se comprobó que la misión podía continuar después del rechazo de un comando inválido. Las pruebas permitieron evaluar la lógica de validación y el manejo de errores del programa dentro de las condiciones del simulador.