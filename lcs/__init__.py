"""Subsecuencia común más larga (LCS) de dos cadenas: tres versiones.

- Versión A, recursiva directa sin memorización: lcs_recursiva.
- Versión B, divide y conquista de Hirschberg: lcs_hirschberg.
- Versión C, programación dinámica tabular: lcs_tabular.

Las tres devuelven una subsecuencia común de longitud máxima. Puede haber
varias distintas con esa longitud, así que dos versiones pueden devolver
cadenas diferentes, pero siempre de la misma longitud.
"""
from .hirschberg import lcs_hirschberg
from .recursiva import lcs_recursiva, llamadas_peor_caso, llamadas_recursiva
from .tabular import lcs_tabular, reconstruir, tabla_lcs

VERSIONES = {
    "A": lcs_recursiva,
    "B": lcs_hirschberg,
    "C": lcs_tabular,
}

__all__ = [
    "lcs_recursiva",
    "lcs_hirschberg",
    "lcs_tabular",
    "llamadas_recursiva",
    "llamadas_peor_caso",
    "tabla_lcs",
    "reconstruir",
    "VERSIONES",
]
