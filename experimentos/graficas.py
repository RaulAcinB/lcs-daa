"""Gráficas de los resultados (requiere matplotlib).

Cada versión tiene un color fijo (A azul, B naranja, C verde agua) y un
marcador distinto, para que se distingan también en blanco y negro.
"""
import os

import matplotlib

matplotlib.use("Agg")                    # sin ventanas: solo archivos
import matplotlib.pyplot as plt          # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

COLORES = {"A": "#2a78d6", "B": "#eb6834", "C": "#1baf7a"}
MARCADORES = {"A": "o", "B": "s", "C": "^"}
ETIQUETAS = {"A": "A · Recursiva", "B": "B · Hirschberg",
             "C": "C · PD tabular"}
TEXTO, TEXTO_SECUNDARIO, REJILLA = "#0b0b0b", "#52514e", "#e4e3df"

# Tamaño pensado para insertar las figuras a 17 cm de ancho sin escalarlas:
# así el texto de las gráficas se ve a 9-10 puntos en la memoria.
ANCHO = 6.7    # pulgadas (17 cm)

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 10,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "axes.edgecolor": TEXTO_SECUNDARIO,
    "axes.labelcolor": TEXTO,
    "xtick.color": TEXTO_SECUNDARIO,
    "ytick.color": TEXTO_SECUNDARIO,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.dpi": 200,
    "figure.dpi": 100,
})


def _numero(valor):
    """Número corto con coma decimal (estilo español)."""
    return f"{valor:g}".replace(".", ",")


def _miles(numero):
    return f"{numero:,}".replace(",", ".")


def _tiempo_legible(valor, _):
    if valor >= 1:
        return f"{_numero(valor)} s"
    if valor >= 1e-3:
        return f"{_numero(valor * 1e3)} ms"
    return f"{_numero(valor * 1e6)} µs"


def _memoria_legible(valor, _):
    if valor >= 1e6:
        return f"{_numero(valor / 1e6)} MB"
    if valor >= 1e3:
        return f"{_numero(valor / 1e3)} kB"
    return f"{_numero(valor)} B"


def _rejilla(eje):
    eje.grid(True, which="major", color=REJILLA, linewidth=0.8)
    eje.set_axisbelow(True)


def _serie(eje, xs, ys, clave):
    """Línea de una versión, con su etiqueta al final."""
    eje.plot(xs, ys, color=COLORES[clave], marker=MARCADORES[clave],
             markersize=5, linewidth=1.5, markeredgecolor="white",
             markeredgewidth=1.0, label=ETIQUETAS[clave])
    eje.annotate(clave, (xs[-1], ys[-1]), xytext=(6, 0),
                 textcoords="offset points", va="center", color=TEXTO,
                 fontsize=9, fontweight="bold")


def _referencia(eje, xs, ys, texto):
    """Recta de referencia teórica (gris, discontinua) con su rótulo."""
    eje.plot(xs, ys, color=TEXTO_SECUNDARIO, linewidth=1.0,
             linestyle=(0, (2, 2)))
    eje.annotate(texto, (xs[-1], ys[-1]), xytext=(4, -2),
                 textcoords="offset points", va="top",
                 color=TEXTO_SECUNDARIO, fontsize=9)


def _columna(filas, version, campo):
    return [f[campo] for f in filas if f["version"] == version]


def _eje_log_longitudes(eje, ns):
    eje.set_xscale("log")
    eje.set_xticks(ns)
    eje.set_xticklabels([_miles(n) for n in ns])
    eje.minorticks_off()


def grafica_tiempos(corta, larga, carpeta):
    """Figura 1: tiempo con cadenas cortas (A, B, C) y largas (B, C)."""
    figura, (izq, der) = plt.subplots(1, 2, figsize=(ANCHO, 2.9))
    ns_corta = sorted({f["longitud"] for f in corta})
    for clave in "ABC":
        _serie(izq, ns_corta, _columna(corta, clave, "tiempo_s"), clave)
    izq.set_yscale("log")
    izq.set_title("Cadenas cortas", loc="left", color=TEXTO)
    izq.set_xlabel("longitud n de cada cadena")
    izq.set_ylabel("tiempo de CPU (escala log.)")
    izq.yaxis.set_major_formatter(FuncFormatter(_tiempo_legible))
    izq.set_xticks(ns_corta)
    _rejilla(izq)
    izq.legend(frameon=False, loc="upper left")

    ns_larga = sorted({f["longitud"] for f in larga})
    for clave in "BC":
        _serie(der, ns_larga, _columna(larga, clave, "tiempo_s"), clave)
    base = _columna(larga, "C", "tiempo_s")[0] / ns_larga[0] ** 2 * 0.55
    _referencia(der, ns_larga, [base * n ** 2 for n in ns_larga], "∝ n²")
    _eje_log_longitudes(der, ns_larga)
    der.set_yscale("log")
    der.set_title("Cadenas largas", loc="left", color=TEXTO)
    der.set_xlabel("longitud n (escala log.)")
    der.yaxis.set_major_formatter(FuncFormatter(_tiempo_legible))
    _rejilla(der)

    figura.tight_layout()
    ruta = os.path.join(carpeta, "fig1_tiempos.png")
    figura.savefig(ruta)
    plt.close(figura)
    return ruta


def grafica_memoria(larga, carpeta):
    """Figura 2: memoria máxima de B y C con cadenas largas."""
    figura, eje = plt.subplots(figsize=(ANCHO, 2.6))
    ns = sorted({f["longitud"] for f in larga})
    for clave in "BC":
        _serie(eje, ns, _columna(larga, clave, "memoria_bytes"), clave)
    base2 = _columna(larga, "C", "memoria_bytes")[0] / ns[0] ** 2 * 0.5
    base1 = _columna(larga, "B", "memoria_bytes")[0] / ns[0] * 0.5
    _referencia(eje, ns, [base2 * n ** 2 for n in ns], "∝ n²")
    _referencia(eje, ns, [base1 * n for n in ns], "∝ n")
    _eje_log_longitudes(eje, ns)
    eje.set_yscale("log")
    eje.set_xlabel("longitud n de cada cadena (escala log.)")
    eje.set_ylabel("memoria máxima (escala log.)")
    eje.yaxis.set_major_formatter(FuncFormatter(_memoria_legible))
    _rejilla(eje)
    eje.legend(frameon=False, loc="upper left")
    figura.tight_layout()
    ruta = os.path.join(carpeta, "fig2_memoria.png")
    figura.savefig(ruta)
    plt.close(figura)
    return ruta


def grafica_llamadas(peor, carpeta):
    """Figura 3: llamadas de A en el peor caso frente a 2·C(2n, n) - 1."""
    figura, eje = plt.subplots(figsize=(ANCHO, 2.4))
    ns = [f["longitud"] for f in peor]
    eje.plot(ns, [f["llamadas_formula"] for f in peor],
             color=TEXTO_SECUNDARIO, linewidth=1.0, linestyle=(0, (2, 2)),
             label="fórmula 2·C(2n, n) − 1")
    eje.plot(ns, [f["llamadas_medidas"] for f in peor], color=COLORES["A"],
             marker=MARCADORES["A"], markersize=5, linewidth=0,
             markeredgecolor="white", markeredgewidth=1.0,
             label="llamadas contadas (versión A)")
    eje.set_yscale("log")
    eje.set_xlabel("longitud n de cada cadena (sin símbolos en común)")
    eje.set_ylabel("llamadas (escala log.)")
    eje.set_xticks(ns)
    _rejilla(eje)
    eje.legend(frameon=False, loc="upper left")
    figura.tight_layout()
    ruta = os.path.join(carpeta, "fig3_llamadas_A.png")
    figura.savefig(ruta)
    plt.close(figura)
    return ruta


def generar(corta, peor, larga, carpeta):
    """Genera las tres figuras y devuelve sus rutas."""
    return [
        grafica_tiempos(corta, larga, carpeta),
        grafica_memoria(larga, carpeta),
        grafica_llamadas(peor, carpeta),
    ]
