"""Utilidades: comprobar subsecuencias y generar parejas de cadenas."""
import random
from typing import Tuple

ALFABETO_ADN = "ACGT"


def es_subsecuencia(s: str, t: str) -> bool:
    """True si los símbolos de s aparecen en t en el mismo orden."""
    posicion = 0
    for simbolo in s:
        posicion = t.find(simbolo, posicion)
        if posicion == -1:
            return False
        posicion += 1
    return True


def cadena_aleatoria(longitud: int, generador: random.Random,
                     alfabeto: str = ALFABETO_ADN) -> str:
    """Cadena con símbolos elegidos al azar del alfabeto."""
    return "".join(generador.choice(alfabeto) for _ in range(longitud))


def pareja_aleatoria(longitud: int, semilla: int,
                     alfabeto: str = ALFABETO_ADN) -> Tuple[str, str]:
    """Dos cadenas aleatorias de la misma longitud, reproducibles."""
    generador = random.Random(semilla)
    return (cadena_aleatoria(longitud, generador, alfabeto),
            cadena_aleatoria(longitud, generador, alfabeto))


def pareja_peor_caso(longitud: int, semilla: int) -> Tuple[str, str]:
    """Dos cadenas sin símbolos en común: peor caso de la versión A.

    Una usa el alfabeto {A, C} y la otra {G, T}.
    """
    generador = random.Random(semilla)
    return (cadena_aleatoria(longitud, generador, "AC"),
            cadena_aleatoria(longitud, generador, "GT"))
