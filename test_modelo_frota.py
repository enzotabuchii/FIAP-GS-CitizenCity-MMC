#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes automatizados para a entrega de Modelagem Matemática e Computacional (MMC).
"""

import unittest
from modelo_frota_onibus import (
    analisar_demanda_e_redistribuicao_etapa2,
    avaliar_resultados,
    resolver_sistema_linear_etapa1,
)


class TestModeloFrotaMMC(unittest.TestCase):
    def test_etapa1_solucao_unica_e_determinante(self) -> None:
        res1 = resolver_sistema_linear_etapa1()
        self.assertEqual(res1["determinante_A"], 3)
        self.assertEqual(res1["posto_A"], 4)
        self.assertEqual(res1["posto_Ab"], 4)
        self.assertTrue(res1["sistema_unico_spd"])
        self.assertEqual(res1["vetor_solucao_x"], [12, 20, 16, 24])

    def test_etapa1_verificacao_relatorio_1(self) -> None:
        res1 = resolver_sistema_linear_etapa1()
        for info in res1["verificacoes_relatorio_1"].values():
            self.assertTrue(info["ok"])

    def test_etapa2_transformacao_linear_redistribuicao(self) -> None:
        res2 = analisar_demanda_e_redistribuicao_etapa2([12, 20, 16, 24])
        self.assertEqual(res2["vetor_necessario"], [14, 19, 18, 21])
        self.assertEqual(res2["vetor_redistribuido_y"], [14, 19, 18, 21])
        self.assertTrue(res2["colunas_somam_1"])
        self.assertTrue(res2["coeficientes_nao_negativos"])
        self.assertTrue(res2["preserva_frota_total"])
        self.assertTrue(res2["sem_alocacoes_negativas"])

    def test_avaliacao_resultados(self) -> None:
        aval = avaliar_resultados([12, 20, 16, 24], [14, 19, 18, 21])
        self.assertEqual(aval["sem_vaga_antes"], 160)
        self.assertEqual(aval["sem_vaga_depois"], 0)
        self.assertEqual(aval["ociosas_antes"], 160)
        self.assertEqual(aval["ociosas_depois"], 0)
        self.assertEqual(aval["onibus_movidos"], 4)


if __name__ == "__main__":
    unittest.main()
