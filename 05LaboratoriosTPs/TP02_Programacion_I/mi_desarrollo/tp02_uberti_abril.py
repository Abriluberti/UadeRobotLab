# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones
#
#  ESTE ES EL ARCHIVO DONDE ESCRIBIS TU PROGRAMA.
#
#  Antes de ejecutarlo:
#    1. Abri INICIAR_SIMULADOR (elegi G1 o Go2)
#    2. Espera a que aparezca la ventana con el robot
#    3. Recien ahi ejecuta este archivo
#
#  Nombre y apellido:  Federico Mara, Abril Uberti, Mariana Bogarin,
#                      Franco Fernandez, Tiziano Ginel, Luciana Olivieri
#  Comision:           582918
# =====================================================================

import math
import sys

from robot import ErrorDeSeguridad, Robot

import misiones


# Limites de la materia
VEL_MAX_AVANZAR = 0.20   # m/s
VEL_MAX_GIRAR = 0.50     # rad/s
TIEMPO_MAX = 10          # segundos por orden

# Todo texto que empiece asi significa "este comando NO se ejecuto"
PREFIJO_RECHAZO = "RECHAZADO"


# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def es_numero(x):
    """Objetivo: indicar si un valor es un numero (int o float).
    Parametros:
      x: el valor a evaluar
    Retorna:
      bool: True si es un int o float finito, False en cualquier otro caso
            (los booleanos, nan e inf se excluyen a proposito)"""
    # bool es subclase de int en Python, asi que lo excluimos a mano
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return False
    return math.isfinite(x)


def motivo_invalido(comando):
    """Objetivo: decidir si un comando se puede ejecutar y, si no, por que.
    Parametros:
      comando (tuple): el comando de la mision, por ejemplo ("avanzar", 0.2, 2.0)
    Retorna:
      str o None: None si el comando es valido; si no, un texto con el motivo"""
    if not isinstance(comando, tuple) or len(comando) == 0:
        return "no es una tupla con contenido"

    nombre = comando[0]

    if nombre in ("detenerse", "saludar"):
        if len(comando) != 1:
            return f"'{nombre}' no lleva parametros"
        return None

    if nombre in ("avanzar", "girar"):
        if len(comando) != 3:
            return f"'{nombre}' necesita velocidad y tiempo"

        velocidad = comando[1]
        tiempo = comando[2]

        if not es_numero(velocidad) or not es_numero(tiempo):
            return "velocidad y tiempo deben ser numeros"

        if tiempo < 0 or tiempo > TIEMPO_MAX:
            return f"tiempo fuera de rango (0 a {TIEMPO_MAX} s)"

        limite = VEL_MAX_AVANZAR if nombre == "avanzar" else VEL_MAX_GIRAR
        if abs(velocidad) > limite:
            return f"velocidad {velocidad} supera el maximo de {limite}"

        return None

    return f"comando desconocido: {nombre}"


def comando_es_valido(comando):
    """Decide si un comando se puede ejecutar. Devuelve True o False.

    Un comando es una tupla. El primer elemento dice que hacer:
        ("avanzar", velocidad, tiempo)   velocidad en m/s, tiempo en s
        ("girar", velocidad, tiempo)     velocidad en rad/s, tiempo en s
        ("detenerse",)
        ("saludar",)

    Cosas que conviene revisar:
      - que la tupla no este vacia
      - que el nombre del comando sea uno de los cuatro validos
      - que tenga la cantidad de datos que corresponde
        (avanzar y girar llevan dos; detenerse y saludar, ninguno)
      - que velocidad y tiempo sean numeros de verdad, no textos
      - que el tiempo no sea negativo
    """
    # Ademas de lo anterior, se controlan los limites de la materia
    # (velocidad y tiempo maximos), para no mandarle al robot algo que
    # va a rechazar igual. Ver motivo_invalido().
    return motivo_invalido(comando) is None


# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    """Ejecuta UN comando en el robot. Devuelve un texto con lo que paso.

    Ordenes que podes usar:
        robot.avanzar(velocidad=..., tiempo=...)
        robot.girar(velocidad=..., tiempo=...)
        robot.detenerse()
        robot.saludar()

    Ojo: aunque el comando parezca valido, el robot puede rechazarlo
    igual (por ejemplo, si la velocidad supera el limite de la materia).
    Eso llega como un ErrorDeSeguridad y conviene atraparlo.
    """
    nombre = comando[0]

    try:
        if nombre == "avanzar":
            robot.avanzar(velocidad=comando[1], tiempo=comando[2])
        elif nombre == "girar":
            robot.girar(velocidad=comando[1], tiempo=comando[2])
        elif nombre == "detenerse":
            robot.detenerse()
        elif nombre == "saludar":
            robot.saludar()
        else:
            return f"{PREFIJO_RECHAZO}: comando desconocido '{nombre}'"

    except ErrorDeSeguridad as error:
        return f"{PREFIJO_RECHAZO} por el robot: {error}"

    return f"Comando {nombre} ejecutado correctamente"


# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================
def ejecutar_mision(robot, mision, historial):
    """Recorre la lista de comandos, uno por uno.

    Por cada comando:
      - si NO es valido, lo rechaza y sigue con el siguiente
      - si es valido, lo ejecuta
      - en los dos casos, guarda en 'historial' que fue lo que paso

    Un comando invalido NO tiene que cortar la mision.
    """
    # Cada registro del historial es un diccionario con tres claves:
    #   "comando": la tupla original
    #   "estado":  "ejecutado" o "rechazado"
    #   "motivo":  el texto que explica que paso
    for comando in mision:

        motivo = motivo_invalido(comando)
        if motivo is not None:
            historial.append({
                "comando": comando,
                "estado": "rechazado",
                "motivo": motivo,
            })
            continue

        # Red de seguridad: si algo inesperado falla al ejecutar este
        # comando (por ejemplo, un error de conexion con el simulador),
        # se registra y la mision sigue con el siguiente.
        try:
            resultado = ejecutar_comando(robot, comando)
        except Exception as error:
            resultado = (f"{PREFIJO_RECHAZO}: error inesperado "
                         f"({type(error).__name__}: {error})")

        if resultado.startswith(PREFIJO_RECHAZO):
            estado = "rechazado"
        else:
            estado = "ejecutado"

        historial.append({
            "comando": comando,
            "estado": estado,
            "motivo": resultado,
        })


# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    """Muestra por pantalla un resumen de la mision.

    Tiene que decir, como minimo:
      - cuantos comandos se ejecutaron bien
      - cuantos se rechazaron
      - cual fue el motivo de cada rechazo
    """
    ejecutados = 0
    rechazados = 0

    print("\n===== REPORTE DE LA MISION =====")

    for registro in historial:
        if registro["estado"] == "ejecutado":
            ejecutados += 1
        else:
            rechazados += 1
            print("Comando rechazado:", registro["comando"])
            print("  Motivo:", registro["motivo"])

    print("\nComandos ejecutados correctamente:", ejecutados)
    print("Comandos rechazados:", rechazados)
    print("Total de comandos:", len(historial))


# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def main():
    """Objetivo: conectar el robot, correr una mision y mostrar el reporte.
    Uso:
      python3 tp02_uberti_abril.py                      -> corre MISION_BASICA
      python3 tp02_uberti_abril.py MISION_CUADRADO      -> corre esa mision
      (tambien: MISION_CON_ERRORES, MISION_LARGA)"""
    nombre_mision = sys.argv[1] if len(sys.argv) > 1 else "MISION_BASICA"
    mision = getattr(misiones, nombre_mision, None)

    if mision is None:
        print(f"No existe {nombre_mision} en misiones.py")
        return

    print("Mision elegida:", nombre_mision)

    robot = Robot()
    robot.conectar()

    historial = []

    try:
        ejecutar_mision(robot, mision, historial)
        generar_reporte(historial)
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()