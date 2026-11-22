"""Versión C: programación dinámica tabular.

Se rellena la tabla L de (m+1) x (n+1) con la misma recurrencia que la
versión A, por filas y de izquierda a derecha, de modo que cada
subproblema se calcula una sola vez (tema 3, Entrenamiento 3; Guerequeta
y Vallecillo, 1998, §5.4). L[m][n] es la longitud de la LCS.

Para obtener la subsecuencia se recorre la tabla hacia atrás desde
L[m][n]. La dirección de cada paso se deduce comparando valores de la
tabla, así que no hace falta una segunda tabla de decisiones.

Coste: tiempo O(m·n) para la tabla y O(m + n) para la reconstrucción.
Memoria: O(m·n), porque la reconstrucción necesita la tabla entera.
"""
from typing import List


def tabla_lcs(a: str, b: str) -> List[List[int]]:
    """Tabla completa: L[i][j] = longitud de la LCS de a[:i] y b[:j]."""
    m, n = len(a), len(b)
    L = [[0] * (n + 1) for _ in range(m + 1)]   # fila y columna 0 a cero
    for i in range(1, m + 1):
        simbolo = a[i - 1]
        fila, fila_anterior = L[i], L[i - 1]
        for j in range(1, n + 1):
            if simbolo == b[j - 1]:
                fila[j] = fila_anterior[j - 1] + 1   # diagonal + 1
            elif fila_anterior[j] >= fila[j - 1]:
                fila[j] = fila_anterior[j]           # viene de arriba
            else:
                fila[j] = fila[j - 1]                # viene de la izquierda
    return L


def reconstruir(a: str, b: str, L: List[List[int]]) -> str:
    """Recorre la tabla desde L[m][n] y devuelve la LCS, en O(m + n)."""
    i, j = len(a), len(b)
    simbolos = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:            # diagonal: es de la LCS
            simbolos.append(a[i - 1])
            i -= 1
            j -= 1
        elif L[i - 1][j] >= L[i][j - 1]:    # el valor viene de arriba
            i -= 1
        else:                               # viene de la izquierda
            j -= 1
    simbolos.reverse()                      # se recorrió al revés
    return "".join(simbolos)


def lcs_tabular(a: str, b: str) -> str:
    """Devuelve una subsecuencia común más larga de a y b (versión C)."""
    return reconstruir(a, b, tabla_lcs(a, b))
