# LCS: tres algoritmos para la subsecuencia común más larga

Actividad 1 de *Diseño Avanzado de Algoritmos* (UNIPRO, curso 2026-27). El programa calcula la subsecuencia común más larga (LCS) de dos cadenas de tres maneras y compara su tiempo de CPU y su memoria máxima.

| Versión | Técnica | Tiempo | Memoria | Código |
|---|---|---|---|---|
| A | Recursión directa, sin memorización | O(2^(m+n)) | O(m + n) | `lcs/recursiva.py` |
| B | Divide y conquista de Hirschberg (1975) | O(m·n) | O(m + n) | `lcs/hirschberg.py` |
| C | Programación dinámica tabular | O(m·n) | O(m·n) | `lcs/tabular.py` |

## Requisitos

- Python 3.9 o superior. Los algoritmos solo usan la biblioteca estándar; no se usa ninguna librería de LCS.
- matplotlib, solo para las gráficas: `pip3 install matplotlib` (o `pip3 install -r requirements.txt`). Sin matplotlib se generan igualmente los CSV y el resumen.

## Ejecución: un único comando

Desde esta carpeta:

```bash
python3 main.py
```

El programa:

1. ejecuta las pruebas de `tests/` y se detiene si alguna falla;
2. mide las tres versiones (tarda unos minutos);
3. deja los resultados en `resultados/`.

Otras opciones:

| Orden | Qué hace |
|---|---|
| `python3 main.py --rapido` | Tamaños pequeños, en unos segundos. Escribe en `resultados_rapido/` |
| `python3 -m unittest discover -s tests -t . -v` | Solo las pruebas |

Uso de las funciones desde Python:

```python
from lcs import lcs_recursiva, lcs_hirschberg, lcs_tabular

lcs_tabular("CASA", "CAMA")      # 'CAA'
```

## Qué se mide

- **Tiempo de CPU** con `time.process_time()`: mediana de 5 repeticiones (3 en la serie larga). En cada repetición la función se ejecuta las veces necesarias para sumar al menos 0,05 s, y el recolector de ciclos se desactiva durante la medida, como hace `timeit`.
- **Memoria máxima** con `tracemalloc`: lo que reserva el algoritmo durante la llamada, sin contar las cadenas de entrada. Se mide en una ejecución aparte, porque `tracemalloc` ralentiza mucho el programa.
- **Series de cadenas**, aleatorias sobre {A, C, G, T}. La pareja de longitud n usa la semilla 1000 + n, así que los resultados se pueden reproducir:

| Serie | Versiones | Longitudes |
|---|---|---|
| Corta | A, B y C | 4, 6, …, 18 |
| Peor caso de A (sin símbolos en común) | A | 1 a 12 |
| Larga | B y C | 250, 500, 1 000, 2 000 y 4 000 |

La versión A no se ejecuta en la serie larga: su tiempo se estima con el número de llamadas del peor caso, 2·C(2n, n) − 1.

## Estructura

```
lcs/            las tres versiones y utilidades
  recursiva.py    versión A (y cuenta de llamadas)
  hirschberg.py   versión B
  tabular.py      versión C
  utilidades.py   comprobar subsecuencias y generar cadenas
experimentos/   medición, series y gráficas
tests/          pruebas (unittest)
main.py         el único comando
resultados/     CSV, resumen.md, resumen.json y gráficas de la última ejecución
```

## Referencias

- Guerequeta, R. y Vallecillo, A. (1998). *Técnicas de diseño de algoritmos*. Universidad de Málaga, §5.4.
- Hirschberg, D. S. (1975). A linear space algorithm for computing maximal common subsequences. *Communications of the ACM, 18*(6), 341–343.
