"""Versión B: divide y conquista de Hirschberg (1975), en espacio lineal.

Esquema de divide y vencerás (tema 2) aplicado a la LCS:

1. Dividir: se parte a por la mitad, a = a1 + a2.
2. Buscar el corte: con solo dos filas de la tabla de la versión C (la
   idea del reto del Lab 1: cada fila depende solo de la anterior) se
   calculan, hacia delante, la LCS de a1 con cada prefijo de b y, hacia
   atrás, la LCS de a2 con cada sufijo de b. La posición k de b que
   maximiza la suma es por donde la LCS cruza la fila central:
   LCS(a, b) = LCS(a1, b[:k]) + LCS(a2, b[k:]).
3. Resolver las dos mitades de forma recursiva.
4. Combinar: concatenar los dos resultados.

Coste: el primer nivel recorre (m/2)·n + (m/2)·n = m·n casillas; el
segundo, la mitad: (m/2)·k + (m/2)·(n-k) = m·n/2; y así sucesivamente.
En total m·n·(1 + 1/2 + 1/4 + ...) <= 2·m·n, luego el tiempo es O(m·n),
unas dos veces las operaciones de la versión C. Memoria: O(m + n), con
unas pocas filas de longitud n + 1 y una pila de profundidad O(log m).

Para no copiar subcadenas en cada llamada, las funciones trabajan con
índices: a[i0:i1] y b[j0:j1] indican el trozo que se está resolviendo.
"""
from typing import List


def _fila_hacia_delante(a: str, i0: int, i1: int,
                        b: str, j0: int, j1: int) -> List[int]:
    """F[j] = LCS de a[i0:i1] y el prefijo b[j0:j0+j], para j = 0..n.

    Es la última fila de la tabla de la versión C, con solo dos filas.
    """
    n = j1 - j0
    anterior = [0] * (n + 1)
    actual = [0] * (n + 1)
    for i in range(i0, i1):
        simbolo = a[i]
        for j in range(1, n + 1):
            if simbolo == b[j0 + j - 1]:
                actual[j] = anterior[j - 1] + 1
            elif anterior[j] >= actual[j - 1]:
                actual[j] = anterior[j]
            else:
                actual[j] = actual[j - 1]
        anterior, actual = actual, anterior   # la nueva pasa a anterior
    return anterior


def _fila_hacia_atras(a: str, i0: int, i1: int,
                      b: str, j0: int, j1: int) -> List[int]:
    """R[j] = LCS de a[i0:i1] y el sufijo de b[j0:j1] de longitud j.

    Igual que la anterior, pero recorriendo a y b de atrás hacia delante.
    """
    n = j1 - j0
    anterior = [0] * (n + 1)
    actual = [0] * (n + 1)
    for i in range(i1 - 1, i0 - 1, -1):
        simbolo = a[i]
        for j in range(1, n + 1):
            if simbolo == b[j1 - j]:
                actual[j] = anterior[j - 1] + 1
            elif anterior[j] >= actual[j - 1]:
                actual[j] = anterior[j]
            else:
                actual[j] = actual[j - 1]
        anterior, actual = actual, anterior
    return anterior


def _mejor_corte(a: str, i0: int, mitad: int, i1: int,
                 b: str, j0: int, j1: int) -> int:
    """Posición k de b por la que la LCS pasa de la mitad 1 a la 2."""
    delante = _fila_hacia_delante(a, i0, mitad, b, j0, j1)
    atras = _fila_hacia_atras(a, mitad, i1, b, j0, j1)
    n = j1 - j0
    mejor_j, mejor_valor = 0, -1
    for j in range(n + 1):
        # LCS(a1, primeros j de b) + LCS(a2, resto de b)
        valor = delante[j] + atras[n - j]
        if valor > mejor_valor:
            mejor_j, mejor_valor = j, valor
    return j0 + mejor_j


def _resolver(a: str, i0: int, i1: int, b: str, j0: int, j1: int,
              salida: List[str]) -> None:
    """Añade a salida, en orden, una LCS de a[i0:i1] y b[j0:j1]."""
    m, n = i1 - i0, j1 - j0
    if m == 0 or n == 0:                  # caso base: un trozo vacío
        return
    if m == 1:                            # caso base: un símbolo en a
        if b.find(a[i0], j0, j1) != -1:
            salida.append(a[i0])
        return
    if n == 1:                            # caso base: un símbolo en b
        if a.find(b[j0], i0, i1) != -1:
            salida.append(b[j0])
        return
    mitad = i0 + m // 2                   # 1. dividir a por la mitad
    k = _mejor_corte(a, i0, mitad, i1, b, j0, j1)   # 2. corte en b
    _resolver(a, i0, mitad, b, j0, k, salida)       # 3. primera mitad
    _resolver(a, mitad, i1, b, k, j1, salida)       # 3. segunda mitad
    # 4. combinar: las dos llamadas escriben en salida en orden


def lcs_hirschberg(a: str, b: str) -> str:
    """Devuelve una subsecuencia común más larga de a y b (versión B)."""
    salida: List[str] = []
    _resolver(a, 0, len(a), b, 0, len(b), salida)
    return "".join(salida)
