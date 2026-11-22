"""Versión A: recursión directa sobre la recurrencia, sin memorización.

Sea L(i, j) la longitud de la LCS de los prefijos a[:i] y b[:j]
(tema 3, Entrenamiento 3; Guerequeta y Vallecillo, 1998, §5.4):

    L(i, j) = 0                            si i = 0 o j = 0
    L(i, j) = L(i-1, j-1) + 1              si a[i-1] = b[j-1]
    L(i, j) = max(L(i-1, j), L(i, j-1))    en otro caso

La versión A programa la recurrencia tal cual. Como no guarda resultados,
resuelve muchas veces los mismos subproblemas, igual que Fibonacci
recursivo (tema 3, Entrenamiento 1).

Peor caso (a y b sin símbolos en común): cada llamada genera dos,
T(m, n) = T(m-1, n) + T(m, n-1) + c. Con N = m + n queda
T(N) <= 2·T(N-1) + c, que según el tema 1 (a·T(n-b) + c·n^k con a = 2)
es O(2^N) = O(2^(m+n)). El número exacto de llamadas es 2·C(m+n, n) - 1
(función llamadas_peor_caso).

Memoria: la pila de llamadas, de profundidad <= m + n.
Solo es utilizable con cadenas cortas (del orden de 15 símbolos).
"""
from math import comb


def lcs_recursiva(a: str, b: str) -> str:
    """Devuelve una subsecuencia común más larga de a y b (versión A)."""

    def resolver(i: int, j: int) -> str:
        # Caso base: uno de los dos prefijos está vacío.
        if i == 0 or j == 0:
            return ""
        # Los últimos símbolos coinciden: forman parte de la LCS.
        if a[i - 1] == b[j - 1]:
            return resolver(i - 1, j - 1) + a[i - 1]
        # No coinciden: se quita el último de a o el último de b
        # y se queda la subsecuencia más larga de las dos.
        sin_ultimo_de_a = resolver(i - 1, j)
        sin_ultimo_de_b = resolver(i, j - 1)
        if len(sin_ultimo_de_a) >= len(sin_ultimo_de_b):
            return sin_ultimo_de_a
        return sin_ultimo_de_b

    return resolver(len(a), len(b))


def llamadas_recursiva(a: str, b: str) -> int:
    """Número de llamadas que hace la versión A con a y b.

    Recorre el mismo árbol de recursión que lcs_recursiva, pero sin
    construir la subsecuencia: solo cuenta los nodos del árbol.
    """
    total = 0

    def contar(i: int, j: int) -> None:
        nonlocal total
        total += 1
        if i == 0 or j == 0:
            return
        if a[i - 1] == b[j - 1]:
            contar(i - 1, j - 1)
        else:
            contar(i - 1, j)
            contar(i, j - 1)

    contar(len(a), len(b))
    return total


def llamadas_peor_caso(m: int, n: int) -> int:
    """Llamadas de la versión A sin símbolos en común: 2·C(m+n, n) - 1.

    Sea N(i, j) el número de llamadas: N(i, 0) = N(0, j) = 1 y, si i, j > 0,
    N(i, j) = 1 + N(i-1, j) + N(i, j-1). Con U = N + 1 queda la regla de
    Pascal U(i, j) = U(i-1, j) + U(i, j-1), con U = 2 en los bordes
    (tema 3, Entrenamiento 2), cuya solución es U(i, j) = 2·C(i+j, i).
    Para m = n crece como 4^n / sqrt(pi·n).
    """
    return 2 * comb(m + n, n) - 1
