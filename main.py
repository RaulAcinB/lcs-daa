"""Actividad 1 de DAA: subsecuencia común más larga (LCS), tres algoritmos.

Único comando (desde esta carpeta):   python3 main.py

1. Ejecuta las pruebas de tests/ y se detiene si alguna falla.
2. Mide el tiempo de CPU y la memoria máxima de las versiones A, B y C.
3. Guarda en resultados/ los CSV, un resumen (resumen.md y resumen.json)
   y, si está instalado matplotlib, las gráficas.

Opciones:
  --rapido       tamaños pequeños, para comprobar en segundos que todo
                 funciona (escribe en resultados_rapido/)
  --sin-pruebas  no ejecuta las pruebas antes de medir
"""
import argparse
import json
import os
import sys
import time
import unittest

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

from experimentos import series  # noqa: E402
from experimentos.series import (decimal, formatear_memoria,  # noqa: E402
                                 formatear_tiempo, miles)


def ejecutar_pruebas():
    print("Pruebas (tests/test_lcs.py)")
    suite = unittest.TestLoader().discover(os.path.join(RAIZ, "tests"),
                                           top_level_dir=RAIZ)
    resultado = unittest.TextTestRunner(verbosity=1,
                                        stream=sys.stdout).run(suite)
    return resultado.wasSuccessful()


def tabla_markdown(cabecera, filas):
    lineas = ["| " + " | ".join(cabecera) + " |",
              "|" + "|".join("---" for _ in cabecera) + "|"]
    lineas += ["| " + " | ".join(str(c) for c in fila) + " |"
               for fila in filas]
    return "\n".join(lineas)


def escribir_resumen_md(ruta, equipo, corta, peor, larga, estimacion,
                        resumen):
    def valor(filas, n, version, campo):
        for f in filas:
            if f["longitud"] == n and f["version"] == version:
                return f[campo]
        return None

    partes = ["# Resultados de los experimentos", "", "## Equipo",
              tabla_markdown(["Dato", "Valor"],
                             [[k, v] for k, v in equipo.items()]),
              "", "## Serie corta: versiones A, B y C (aleatorias, ACGT)"]
    filas = []
    for n in sorted({f["longitud"] for f in corta}):
        fila = [n, valor(corta, n, "A", "longitud_lcs")]
        fila += [formatear_tiempo(valor(corta, n, v, "tiempo_s"))
                 for v in "ABC"]
        fila += [formatear_memoria(valor(corta, n, v, "memoria_bytes"))
                 for v in "ABC"]
        fila.append(miles(valor(corta, n, "A", "llamadas")))
        filas.append(fila)
    partes.append(tabla_markdown(
        ["n", "LCS", "Tiempo A", "Tiempo B", "Tiempo C", "Memoria A",
         "Memoria B", "Memoria C", "Llamadas A"], filas))

    partes += ["", "## Peor caso de la versión A (sin símbolos en común)"]
    partes.append(tabla_markdown(
        ["n", "Llamadas contadas", "2·C(2n, n) − 1", "Tiempo",
         "ns por llamada"],
        [[f["longitud"], miles(f["llamadas_medidas"]),
          miles(f["llamadas_formula"]), formatear_tiempo(f["tiempo_s"]),
          decimal(f["ns_por_llamada"], 0)] for f in peor]))

    partes += ["", "## Serie larga: versiones B y C (aleatorias, ACGT)"]
    filas = []
    ns = sorted({f["longitud"] for f in larga})
    for i, n in enumerate(ns):
        anios = next(e["anios_log10"] for e in estimacion
                     if e["longitud"] == n)
        filas.append([
            miles(n), miles(valor(larga, n, "B", "longitud_lcs")),
            formatear_tiempo(valor(larga, n, "B", "tiempo_s")),
            formatear_tiempo(valor(larga, n, "C", "tiempo_s")),
            decimal(resumen["cociente_tiempo_B_C"][i]),
            formatear_memoria(valor(larga, n, "B", "memoria_bytes")),
            formatear_memoria(valor(larga, n, "C", "memoria_bytes")),
            decimal(resumen["cociente_memoria_C_B"][i], 0),
            f"10^{anios:.0f} años"])
    partes.append(tabla_markdown(
        ["n", "LCS", "Tiempo B", "Tiempo C", "B/C", "Memoria B",
         "Memoria C", "C/B", "A (peor caso, estimado)"], filas))

    partes += ["", "## Pendientes en escala log-log (serie larga)",
               tabla_markdown(["Medida", "Versión B", "Versión C",
                               "Teoría (B y C)"], [
                   ["Tiempo", decimal(resumen["pendiente_tiempo_B"]),
                    decimal(resumen["pendiente_tiempo_C"]), "2 y 2"],
                   ["Memoria", decimal(resumen["pendiente_memoria_B"]),
                    decimal(resumen["pendiente_memoria_C"]), "1 y 2"],
                   ["Memoria (3 mayores)",
                    decimal(resumen["pendiente_memoria_B_mayores"]),
                    decimal(resumen["pendiente_memoria_C_mayores"]),
                    "1 y 2"],
               ])]
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(partes) + "\n")


def medir(configuracion):
    def informar(texto):
        print(texto, flush=True)

    print("[1/3] Serie corta: versiones A, B y C "
          "(cadenas aleatorias sobre ACGT)")
    corta = series.serie_corta(configuracion["corta"],
                               configuracion["repeticiones"], informar)
    print("\n[2/3] Peor caso de la versión A (sin símbolos en común)")
    peor = series.serie_peor_caso(configuracion["peor_caso"],
                                  configuracion["repeticiones"], informar)
    print("\n[3/3] Serie larga: versiones B y C "
          "(la A no es ejecutable con estos tamaños)")
    larga = series.serie_larga(configuracion["larga"],
                               configuracion["repeticiones_larga"],
                               informar)
    return corta, peor, larga


def rehacer_graficas(carpeta):
    """Vuelve a dibujar las gráficas a partir de los CSV, sin medir."""
    from experimentos import graficas
    corta = series.cargar_csv(os.path.join(carpeta, "serie_corta.csv"))
    peor = series.cargar_csv(os.path.join(carpeta, "peor_caso_A.csv"))
    larga = series.cargar_csv(os.path.join(carpeta, "serie_larga.csv"))
    for ruta in graficas.generar(corta, peor, larga, carpeta):
        print(f"Gráfica: {os.path.relpath(ruta, RAIZ)}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="LCS: pruebas y experimentos de las versiones A, B y C.")
    parser.add_argument("--rapido", action="store_true",
                        help="tamaños pequeños (unos segundos)")
    parser.add_argument("--sin-pruebas", action="store_true",
                        help="no ejecutar las pruebas antes de medir")
    parser.add_argument("--solo-graficas", action="store_true",
                        help="rehacer las gráficas con los CSV de resultados/")
    argumentos = parser.parse_args()

    if argumentos.solo_graficas:
        return rehacer_graficas(os.path.join(RAIZ, "resultados"))

    inicio = time.perf_counter()
    if not argumentos.sin_pruebas and not ejecutar_pruebas():
        print("\nHay pruebas que fallan: no se mide nada.")
        return 1

    nombre = "rapida" if argumentos.rapido else "completa"
    configuracion = series.CONFIGURACIONES[nombre]
    carpeta = os.path.join(
        RAIZ, "resultados_rapido" if argumentos.rapido else "resultados")
    os.makedirs(carpeta, exist_ok=True)

    equipo = series.entorno()
    print(f"\nEquipo: {equipo['procesador']} · {equipo['sistema']} · "
          f"Python {equipo['python']}")
    print(f"Configuración {nombre}; resultados en "
          f"{os.path.relpath(carpeta, RAIZ)}/\n")

    corta, peor, larga = medir(configuracion)
    estimacion = series.estimacion_version_a(configuracion["larga"],
                                             peor[-1]["ns_por_llamada"])
    resumen = series.resumir(corta, peor, larga, estimacion)

    for nombre_csv, filas in [("serie_corta.csv", corta),
                              ("peor_caso_A.csv", peor),
                              ("serie_larga.csv", larga),
                              ("estimacion_A.csv", estimacion)]:
        series.guardar_csv(os.path.join(carpeta, nombre_csv), filas)
    with open(os.path.join(carpeta, "resumen.json"), "w",
              encoding="utf-8") as f:
        json.dump({"entorno": equipo, "configuracion": configuracion,
                   "resumen": resumen}, f, ensure_ascii=False, indent=2)
    escribir_resumen_md(os.path.join(carpeta, "resumen.md"), equipo,
                        corta, peor, larga, estimacion, resumen)

    try:
        from experimentos import graficas
    except ImportError:
        print("\nmatplotlib no está instalado: no se generan las gráficas "
              "(se instala con: pip3 install matplotlib).")
    else:
        for ruta in graficas.generar(corta, peor, larga, carpeta):
            print(f"Gráfica: {os.path.relpath(ruta, RAIZ)}")

    print(f"\nPendiente log-log del tiempo: "
          f"B {decimal(resumen['pendiente_tiempo_B'])}, "
          f"C {decimal(resumen['pendiente_tiempo_C'])} (teoría: 2).")
    print(f"Pendiente log-log de la memoria (3 mayores): "
          f"B {decimal(resumen['pendiente_memoria_B_mayores'])} "
          f"(teoría: 1), "
          f"C {decimal(resumen['pendiente_memoria_C_mayores'])} "
          f"(teoría: 2).")
    print(f"Listo en {time.perf_counter() - inicio:.0f} s. Resumen: "
          f"{os.path.relpath(os.path.join(carpeta, 'resumen.md'), RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
