"""Pruebas de las tres versiones de la LCS.

Se ejecutan solas con:  python3 -m unittest discover -s tests -t .
(main.py también las ejecuta antes de medir).
"""
import random
import unittest

from lcs import (VERSIONES, lcs_hirschberg, lcs_recursiva, lcs_tabular,
                 llamadas_peor_caso, llamadas_recursiva, tabla_lcs)
from lcs.utilidades import es_subsecuencia, pareja_peor_caso


def comprobar(prueba, a, b, longitud_esperada, versiones="ABC"):
    """Cada versión devuelve una subsecuencia común de la longitud dada."""
    for clave in versiones:
        resultado = VERSIONES[clave](a, b)
        with prueba.subTest(version=clave, a=a, b=b):
            prueba.assertEqual(len(resultado), longitud_esperada)
            prueba.assertTrue(es_subsecuencia(resultado, a))
            prueba.assertTrue(es_subsecuencia(resultado, b))


class EjemplosDelMaterial(unittest.TestCase):
    """Casos con solución conocida en el material del curso."""

    def test_tema3_entrenamiento3(self):
        # Tema 3, Entrenamiento 3: LCS = GTCGTCGGAAGCCGGCCGAA (20).
        # La versión A no se prueba: con 29 y 28 símbolos tardaría mucho.
        a = "ACCGGTCGAGTGCGCGGAAGCCGGCCGAA"
        b = "GTCGTTCGGAATGCCGTTGCTCTGTAAA"
        comprobar(self, a, b, 20, versiones="BC")
        self.assertEqual(lcs_tabular(a, b), "GTCGTCGGAAGCCGGCCGAA")

    def test_lectura_seccion_5_4(self):
        # Guerequeta y Vallecillo (1998), §5.4: longitud 6.
        comprobar(self, "10010101", "010110110", 6)

    def test_casa_cama(self):
        for clave in "ABC":
            with self.subTest(version=clave):
                self.assertEqual(VERSIONES[clave]("CASA", "CAMA"), "CAA")

    def test_tabla_casa_cama(self):
        esperada = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1],
            [0, 1, 2, 2, 2],
            [0, 1, 2, 2, 2],
            [0, 1, 2, 2, 3],
        ]
        self.assertEqual(tabla_lcs("CASA", "CAMA"), esperada)


class CasosLimite(unittest.TestCase):

    def test_cadenas_vacias(self):
        for a, b in [("", ""), ("", "ACGT"), ("ACGT", "")]:
            comprobar(self, a, b, 0)

    def test_cadenas_iguales(self):
        for clave in "ABC":
            with self.subTest(version=clave):
                self.assertEqual(VERSIONES[clave]("GATTACA", "GATTACA"),
                                 "GATTACA")

    def test_sin_simbolos_en_comun(self):
        comprobar(self, "AAAA", "CCC", 0)
        comprobar(self, "ACAC", "GTTG", 0)

    def test_una_contenida_en_la_otra(self):
        for clave in "ABC":
            with self.subTest(version=clave):
                self.assertEqual(VERSIONES[clave]("ACE", "ABCDE"), "ACE")
                self.assertEqual(VERSIONES[clave]("ABCDE", "ACE"), "ACE")

    def test_un_solo_simbolo(self):
        comprobar(self, "A", "A", 1)
        comprobar(self, "A", "C", 0)
        comprobar(self, "A", "CGTA", 1)
        comprobar(self, "CGTA", "T", 1)


class ValidacionAleatoria(unittest.TestCase):
    """Como la validación aleatoria del Lab 1 (§7.4): 200 parejas."""

    def test_las_tres_versiones_coinciden(self):
        generador = random.Random(2026)
        for _ in range(200):
            alfabeto = generador.choice(["AB", "ACGT", "ABCDEFGH"])
            a = "".join(generador.choice(alfabeto)
                        for _ in range(generador.randint(0, 9)))
            b = "".join(generador.choice(alfabeto)
                        for _ in range(generador.randint(0, 9)))
            comprobar(self, a, b, len(lcs_tabular(a, b)))

    def test_hirschberg_y_tabular_con_cadenas_largas(self):
        generador = random.Random(7)
        for m, n in [(300, 250), (257, 31), (64, 400)]:
            a = "".join(generador.choice("ACGT") for _ in range(m))
            b = "".join(generador.choice("ACGT") for _ in range(n))
            comprobar(self, a, b, len(lcs_tabular(a, b)), versiones="BC")


class LlamadasDeLaVersionA(unittest.TestCase):
    """La cuenta de llamadas es 2·C(m+n, n) - 1 en el peor caso."""

    def test_formula_del_peor_caso(self):
        for m, n in [(0, 0), (1, 1), (2, 3), (5, 5), (8, 6), (9, 9)]:
            a, b = pareja_peor_caso(max(m, n), semilla=m * 31 + n)
            a, b = a[:m], b[:n]
            with self.subTest(m=m, n=n):
                self.assertEqual(llamadas_recursiva(a, b),
                                 llamadas_peor_caso(m, n))

    def test_con_coincidencias_hay_menos_llamadas(self):
        a, b = "ACGTACGTAC", "CAGTTGCAAC"
        self.assertLess(llamadas_recursiva(a, b),
                        llamadas_peor_caso(len(a), len(b)))
        self.assertEqual(len(lcs_recursiva(a, b)),
                         len(lcs_hirschberg(a, b)))


if __name__ == "__main__":
    unittest.main()
