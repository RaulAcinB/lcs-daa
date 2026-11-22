# Resultados de los experimentos

## Equipo
| Dato | Valor |
|---|---|
| sistema | macOS-26.5.2-arm64-arm-64bit |
| arquitectura | arm64 |
| python | 3.9.6 |
| implementacion | CPython |
| procesador | Apple M1 |
| modelo | MacBookPro17,1 |
| memoria_total_gb | 8.0 |
| nucleos | 8 |

## Serie corta: versiones A, B y C (aleatorias, ACGT)
| n | LCS | Tiempo A | Tiempo B | Tiempo C | Memoria A | Memoria B | Memoria C | Llamadas A |
|---|---|---|---|---|---|---|---|---|
| 4 | 2 | 11,1 µs | 14,9 µs | 7,7 µs | 4,0 kB | 1,7 kB | 928 B | 42 |
| 6 | 4 | 37,8 µs | 29,7 µs | 12,7 µs | 5,5 kB | 2,2 kB | 1,2 kB | 139 |
| 8 | 3 | 423,7 µs | 36,8 µs | 18,2 µs | 7,9 kB | 2,2 kB | 1,7 kB | 1.704 |
| 10 | 4 | 5,94 ms | 58,4 µs | 27,0 µs | 9,9 kB | 2,6 kB | 2,1 kB | 25.028 |
| 12 | 5 | 13,37 ms | 74,4 µs | 34,4 µs | 11,5 kB | 2,6 kB | 2,6 kB | 57.029 |
| 14 | 6 | 561,63 ms | 109,0 µs | 45,6 µs | 13,5 kB | 2,9 kB | 3,2 kB | 2.297.166 |
| 16 | 9 | 434,95 ms | 129,9 µs | 56,0 µs | 15,0 kB | 2,8 kB | 3,8 kB | 1.688.636 |
| 18 | 9 | 3,18 s | 168,5 µs | 69,2 µs | 16,9 kB | 3,5 kB | 4,5 kB | 13.604.192 |

## Peor caso de la versión A (sin símbolos en común)
| n | Llamadas contadas | 2·C(2n, n) − 1 | Tiempo | ns por llamada |
|---|---|---|---|---|
| 1 | 3 | 3 | 1,5 µs | 507 |
| 2 | 11 | 11 | 3,5 µs | 316 |
| 3 | 39 | 39 | 9,9 µs | 253 |
| 4 | 139 | 139 | 32,5 µs | 234 |
| 5 | 503 | 503 | 115,6 µs | 230 |
| 6 | 1.847 | 1.847 | 420,3 µs | 228 |
| 7 | 6.863 | 6.863 | 1,56 ms | 227 |
| 8 | 25.739 | 25.739 | 5,83 ms | 226 |
| 9 | 97.239 | 97.239 | 21,99 ms | 226 |
| 10 | 369.511 | 369.511 | 83,49 ms | 226 |
| 11 | 1.410.863 | 1.410.863 | 319,14 ms | 226 |
| 12 | 5.408.311 | 5.408.311 | 1,22 s | 226 |

## Serie larga: versiones B y C (aleatorias, ACGT)
| n | LCS | Tiempo B | Tiempo C | B/C | Memoria B | Memoria C | C/B | A (peor caso, estimado) |
|---|---|---|---|---|---|---|---|---|
| 250 | 160 | 22,11 ms | 10,53 ms | 2,10 | 8,7 kB | 522,0 kB | 60 | 10^135 años |
| 500 | 322 | 92,81 ms | 45,18 ms | 2,05 | 12,7 kB | 2,2 MB | 171 | 10^286 años |
| 1.000 | 650 | 390,90 ms | 189,36 ms | 2,06 | 54,2 kB | 11,5 MB | 212 | 10^586 años |
| 2.000 | 1.291 | 1,64 s | 779,23 ms | 2,10 | 131,5 kB | 53,0 MB | 403 | 10^1188 años |
| 4.000 | 2.590 | 6,97 s | 3,16 s | 2,21 | 281,2 kB | 226,1 MB | 804 | 10^2392 años |

## Pendientes en escala log-log (serie larga)
| Medida | Versión B | Versión C | Teoría (B y C) |
|---|---|---|---|
| Tiempo | 2,07 | 2,06 | 2 y 2 |
| Memoria | 1,34 | 2,21 | 1 y 2 |
| Memoria (3 mayores) | 1,19 | 2,15 | 1 y 2 |
