"""Series de experimentos: qué se mide, con qué cadenas y cómo se resume."""
import csv
import math
import os
import platform
import subprocess
import sys

from lcs import VERSIONES, llamadas_peor_caso, llamadas_recursiva
from lcs.utilidades import pareja_aleatoria, pareja_peor_caso

from .medicion import memoria_pico, tiempo_cpu

SEMILLA_BASE = 1000      # la pareja de longitud n usa la semilla 1000 + n
SEGUNDOS_POR_ANIO = 365.25 * 24 * 3600

CONFIGURACIONES = {
    # La de la memoria: python3 main.py
    "completa": {
        "corta": [4, 6, 8, 10, 12, 14, 16, 18],
        "peor_caso": list(range(1, 13)),
        "larga": [250, 500, 1000, 2000, 4000],
        "repeticiones": 5,
        "repeticiones_larga": 3,
    },
    # Comprobación rápida (unos segundos): python3 main.py --rapido
    "rapida": {
        "corta": [4, 6, 8, 10],
        "peor_caso": list(range(1, 9)),
        "larga": [100, 200, 300, 500, 1000],
        "repeticiones": 3,
        "repeticiones_larga": 1,
    },
}


def serie_corta(longitudes, repeticiones, informar=print):
    """Versiones A, B y C con parejas aleatorias cortas sobre ACGT."""
    filas = []
    for n in longitudes:
        a, b = pareja_aleatoria(n, SEMILLA_BASE + n)
        llamadas = llamadas_recursiva(a, b)
        longitudes_lcs = set()
        for clave in "ABC":
            funcion = VERSIONES[clave]
            longitud_lcs = len(funcion(a, b))
            longitudes_lcs.add(longitud_lcs)
            tiempo = tiempo_cpu(funcion, a, b, repeticiones)
            memoria = memoria_pico(funcion, a, b)
            filas.append({
                "longitud": n, "version": clave,
                "longitud_lcs": longitud_lcs, "tiempo_s": tiempo,
                "memoria_bytes": memoria,
                "llamadas": llamadas if clave == "A" else "",
            })
            texto = (f"  n = {n:>2}  versión {clave}: "
                     f"{formatear_tiempo(tiempo):>10}  "
                     f"{formatear_memoria(memoria):>9}")
            if clave == "A":
                texto += f"  {miles(llamadas)} llamadas"
            informar(texto)
        if len(longitudes_lcs) != 1:
            raise RuntimeError(f"Las versiones no coinciden (n = {n})")
    return filas


def serie_peor_caso(longitudes, repeticiones, informar=print):
    """Versión A sin símbolos en común: llamadas frente a 2·C(2n, n) - 1."""
    filas = []
    for n in longitudes:
        a, b = pareja_peor_caso(n, SEMILLA_BASE + n)
        medidas = llamadas_recursiva(a, b)
        formula = llamadas_peor_caso(n, n)
        tiempo = tiempo_cpu(VERSIONES["A"], a, b, repeticiones)
        filas.append({
            "longitud": n, "llamadas_medidas": medidas,
            "llamadas_formula": formula, "tiempo_s": tiempo,
            "ns_por_llamada": tiempo / medidas * 1e9,
        })
        informar(f"  n = {n:>2}: {miles(medidas):>11} llamadas "
                 f"(fórmula: {miles(formula)})  {formatear_tiempo(tiempo)}")
        if medidas != formula:
            raise RuntimeError(f"Llamadas distintas de la fórmula (n = {n})")
    return filas


def serie_larga(longitudes, repeticiones, informar=print):
    """Versiones B y C con parejas aleatorias largas sobre ACGT."""
    filas = []
    for n in longitudes:
        a, b = pareja_aleatoria(n, SEMILLA_BASE + n)
        longitudes_lcs = set()
        for clave in "BC":
            funcion = VERSIONES[clave]
            longitud_lcs = len(funcion(a, b))
            longitudes_lcs.add(longitud_lcs)
            tiempo = tiempo_cpu(funcion, a, b, repeticiones)
            memoria = memoria_pico(funcion, a, b)
            filas.append({
                "longitud": n, "version": clave,
                "longitud_lcs": longitud_lcs, "tiempo_s": tiempo,
                "memoria_bytes": memoria,
            })
            informar(f"  n = {n:>4}  versión {clave}: "
                     f"{formatear_tiempo(tiempo):>10}  "
                     f"{formatear_memoria(memoria):>9}")
        if len(longitudes_lcs) != 1:
            raise RuntimeError(f"B y C no coinciden (n = {n})")
    return filas


def estimacion_version_a(longitudes, ns_por_llamada):
    """Tiempo de la versión A en el peor caso: 2·C(2n, n) - 1 llamadas."""
    filas = []
    for n in longitudes:
        llamadas = llamadas_peor_caso(n, n)
        segundos_log10 = (math.log10(llamadas)
                          + math.log10(ns_por_llamada * 1e-9))
        filas.append({
            "longitud": n,
            "llamadas_log10": round(math.log10(llamadas), 2),
            "segundos_log10": round(segundos_log10, 2),
            "anios_log10": round(
                segundos_log10 - math.log10(SEGUNDOS_POR_ANIO), 2),
        })
    return filas


def pendiente_loglog(xs, ys):
    """Pendiente de la recta de mínimos cuadrados de log(y) frente a log(x).

    Si y es proporcional a x^p, la pendiente es p.
    """
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx, my = sum(lx) / len(lx), sum(ly) / len(ly)
    numerador = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    denominador = sum((x - mx) ** 2 for x in lx)
    return numerador / denominador


def resumir(corta, peor, larga, estimacion):
    """Cifras clave para la discusión de la memoria."""
    def columna(version, campo):
        return [f[campo] for f in larga if f["version"] == version]

    ns = sorted({f["longitud"] for f in larga})
    resumen = {"longitudes_larga": ns}
    for clave in "BC":
        tiempos = columna(clave, "tiempo_s")
        memorias = columna(clave, "memoria_bytes")
        resumen[f"pendiente_tiempo_{clave}"] = round(
            pendiente_loglog(ns, tiempos), 2)
        resumen[f"pendiente_memoria_{clave}"] = round(
            pendiente_loglog(ns, memorias), 2)
        # Solo los tres tamaños mayores: ahí casi todos los valores de las
        # filas pasan de 256 y Python ya no usa su caché de enteros
        # pequeños (de -5 a 256), así que cada valor es un objeto aparte.
        resumen[f"pendiente_memoria_{clave}_mayores"] = round(
            pendiente_loglog(ns[-3:], memorias[-3:]), 2)
    resumen["cociente_tiempo_B_C"] = [
        round(tb / tc, 2)
        for tb, tc in zip(columna("B", "tiempo_s"), columna("C", "tiempo_s"))]
    resumen["cociente_memoria_C_B"] = [
        round(mc / mb, 1)
        for mb, mc in zip(columna("B", "memoria_bytes"),
                          columna("C", "memoria_bytes"))]
    resumen["ns_por_llamada_A"] = round(peor[-1]["ns_por_llamada"], 1)
    resumen["factor_llamadas_peor_caso"] = round(
        peor[-1]["llamadas_medidas"] / peor[-2]["llamadas_medidas"], 2)
    resumen["estimacion_A"] = estimacion
    resumen["llamadas_A_corta"] = {
        f["longitud"]: f["llamadas"] for f in corta if f["version"] == "A"}
    return resumen


def entorno():
    """Datos del equipo y de Python, para documentar dónde se ha medido."""
    datos = {
        "sistema": platform.platform(),
        "arquitectura": platform.machine(),
        "python": sys.version.split()[0],
        "implementacion": platform.python_implementation(),
        "procesador": platform.processor() or "",
        "modelo": "",
        "memoria_total_gb": "",
        "nucleos": os.cpu_count(),
    }
    try:
        if sys.platform == "darwin":
            def sysctl(nombre):
                return subprocess.run(
                    ["sysctl", "-n", nombre], capture_output=True,
                    text=True, timeout=5).stdout.strip()
            datos["procesador"] = (sysctl("machdep.cpu.brand_string")
                                   or datos["procesador"])
            datos["modelo"] = sysctl("hw.model")
            datos["memoria_total_gb"] = round(
                int(sysctl("hw.memsize")) / 2**30, 1)
        elif sys.platform.startswith("linux"):
            with open("/proc/cpuinfo", encoding="utf-8") as f:
                for linea in f:
                    if linea.lower().startswith(("model name", "hardware")):
                        datos["procesador"] = linea.split(":", 1)[1].strip()
                        break
            with open("/proc/meminfo", encoding="utf-8") as f:
                kb = int(f.readline().split()[1])
                datos["memoria_total_gb"] = round(kb / 2**20, 1)
    except (OSError, ValueError, subprocess.SubprocessError):
        pass
    return datos


def guardar_csv(ruta, filas):
    """Guarda una lista de diccionarios como CSV (punto decimal)."""
    if not filas:
        return
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        escritor.writeheader()
        escritor.writerows(filas)


def cargar_csv(ruta):
    """Lee un CSV de resultados y devuelve los números con su tipo."""
    enteros = {"longitud", "longitud_lcs", "memoria_bytes", "llamadas",
               "llamadas_medidas", "llamadas_formula"}
    filas = []
    with open(ruta, newline="", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            for campo, valor in fila.items():
                if valor == "" or campo == "version":
                    continue
                fila[campo] = int(valor) if campo in enteros else float(valor)
            filas.append(fila)
    return filas


def decimal(numero, decimales=2):
    """Número con coma decimal: 2.157 -> '2,16'."""
    return f"{numero:.{decimales}f}".replace(".", ",")


def miles(numero):
    """Entero con punto como separador de miles: 5408311 -> 5.408.311."""
    return f"{numero:,}".replace(",", ".")


def formatear_tiempo(segundos):
    """Tiempo legible: s, ms o µs, con coma decimal."""
    if segundos >= 1:
        return f"{decimal(segundos)} s"
    if segundos >= 1e-3:
        return f"{decimal(segundos * 1e3)} ms"
    return f"{decimal(segundos * 1e6, 1)} µs"


def formatear_memoria(octetos):
    """Memoria legible en unidades decimales: B, kB (10^3) o MB (10^6)."""
    if octetos >= 1e6:
        return f"{decimal(octetos / 1e6, 1)} MB"
    if octetos >= 1e3:
        return f"{decimal(octetos / 1e3, 1)} kB"
    return f"{octetos} B"
