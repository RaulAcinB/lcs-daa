"""Medición del tiempo de CPU y de la memoria máxima de una llamada."""
import gc
import statistics
import time
import tracemalloc


def tiempo_cpu(funcion, a, b, repeticiones=5, minimo=0.05):
    """Mediana del tiempo de CPU, en segundos, de una llamada funcion(a, b).

    - time.process_time() cuenta solo el tiempo de CPU del proceso, no el
      tiempo de reloj (que incluye esperas y otros programas).
    - En cada repetición la función se ejecuta las veces necesarias para
      sumar al menos `minimo` segundos y se divide entre el número de
      ejecuciones; así se miden bien también los casos de microsegundos.
    - El recolector de ciclos se desactiva durante la medida, como timeit.
    """
    muestras = []
    for _ in range(repeticiones):
        gc.collect()
        gc.disable()
        try:
            ejecuciones = 0
            inicio = time.process_time()
            while True:
                funcion(a, b)
                ejecuciones += 1
                transcurrido = time.process_time() - inicio
                if transcurrido >= minimo:
                    break
        finally:
            gc.enable()
        muestras.append(transcurrido / ejecuciones)
    return statistics.median(muestras)


def memoria_pico(funcion, a, b):
    """Memoria máxima, en bytes, que reserva funcion(a, b) (tracemalloc).

    tracemalloc solo cuenta lo reservado después de start(): no incluye
    las cadenas de entrada, sino la memoria adicional del algoritmo.
    Se mide en una ejecución aparte porque ralentiza mucho el programa.
    """
    gc.collect()
    tracemalloc.start()
    try:
        funcion(a, b)
        _, pico = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return pico
