"""
FIAP — Modelagem Matemática e Computacional (MMC)
Global Solution 2026.2 — CitizenTech
Mobilidade Urbana Inteligente: Modelagem Matemática para a Gestão do Transporte Público

Implementa computacionalmente em Python:
- ETAPA 1: Diagnóstico e modelagem da situação atual (Sistema Linear Ax = b,
           determinante, posto/Rouché-Capelli, matriz inversa, escalonamento
           de Gauss-Jordan e verificação dos registros operacionais).
- ETAPA 2: Análise de demanda do Relatório II, cálculo de desequilíbrios,
           política de redistribuição da frota via Transformação Linear y = T(x) = Mx
           e demonstração matemática de conservação da frota e não-negatividade.

Observação técnica: O código possui implementação completa de Álgebra Linear em
Python puro (com aritmética exata via fractions.Fraction) e também utiliza NumPy
automaticamente caso esteja instalado no ambiente.
"""

from __future__ import annotations
from fractions import Fraction
from typing import Dict, List, Tuple

try:
    import numpy as np
    POSSUI_NUMPY = True
except ImportError:
    POSSUI_NUMPY = False


REGIOES: List[str] = ["Norte", "Sul", "Leste", "Oeste"]
CAPACIDADE_POR_ONIBUS: int = 40

# Matriz de coeficientes A (Etapa 1 - Relatório I)
MATRIZ_A: List[List[int]] = [
    [1, 1, 1, 1],  # Eq 1: x_N + x_S + x_L + x_O = 72
    [1, 2, 0, 1],  # Eq 2: x_N + 2*x_S + 0*x_L + x_O = 76
    [0, 1, 2, 0],  # Eq 3: 0*x_N + x_S + 2*x_L + 0*x_O = 52
    [1, 0, 1, 2],  # Eq 4: x_N + 0*x_S + x_L + 2*x_O = 76
]

# Vetor de termos independentes b (Etapa 1 - Relatório I)
VETOR_B: List[int] = [72, 76, 52, 76]

# Demanda estimada de passageiros no horário de pico (Etapa 2 - Relatório II)
DEMANDA_PASSAGEIROS: Dict[str, int] = {
    "Norte": 560,
    "Sul": 760,
    "Leste": 720,
    "Oeste": 840,
}

# Matriz associada à Transformação Linear de Redistribuição M (Etapa 2)
# Colunas j = origem [Norte, Sul, Leste, Oeste]; Linhas i = destino [Norte, Sul, Leste, Oeste]
MATRIZ_TRANSFORMACAO_M_FRAC: List[List[Fraction]] = [
    [Fraction(1, 1), Fraction(0, 1),  Fraction(0, 1), Fraction(2, 24)],   # Destino: Norte
    [Fraction(0, 1), Fraction(19, 20), Fraction(0, 1), Fraction(0, 1)],   # Destino: Sul
    [Fraction(0, 1), Fraction(1, 20),  Fraction(1, 1), Fraction(1, 24)],  # Destino: Leste
    [Fraction(0, 1), Fraction(0, 1),  Fraction(0, 1), Fraction(21, 24)],  # Destino: Oeste
]


# ============================================================================
# FUNÇÕES DE ÁLGEBRA LINEAR (EXATAS E NUMÉRICAS)
# ============================================================================

def calcular_determinante(matriz: List[List[float | int | Fraction]]) -> Fraction:
    """Calcula o determinante exato de uma matriz quadrada n x n por expansão de Laplace."""
    n = len(matriz)
    if n == 1:
        return Fraction(matriz[0][0])
    if n == 2:
        return Fraction(matriz[0][0]) * Fraction(matriz[1][1]) - Fraction(matriz[0][1]) * Fraction(matriz[1][0])

    soma = Fraction(0)
    for col in range(n):
        submatriz = [linha[:col] + linha[col + 1:] for linha in matriz[1:]]
        sinal = 1 if col % 2 == 0 else -1
        soma += sinal * Fraction(matriz[0][col]) * calcular_determinante(submatriz)
    return soma


def escalonar_gauss_jordan(
    matriz_a: List[List[int | float | Fraction]],
    vetor_b: List[int | float | Fraction],
) -> Tuple[List[List[Fraction]], int, int]:
    """
    Aplica eliminação de Gauss-Jordan à matriz aumentada [A | b].
    Retorna (matriz_aumentada_reduzida, posto_A, posto_Ab).
    """
    n_linhas = len(matriz_a)
    n_cols = len(matriz_a[0])
    aug: List[List[Fraction]] = [
        [Fraction(matriz_a[i][j]) for j in range(n_cols)] + [Fraction(vetor_b[i])]
        for i in range(n_linhas)
    ]

    linha_pivo = 0
    for col in range(n_cols):
        if linha_pivo >= n_linhas:
            break
        # Busca pivô não nulo
        pivo = None
        for r in range(linha_pivo, n_linhas):
            if aug[r][col] != 0:
                pivo = r
                break
        if pivo is None:
            continue

        aug[linha_pivo], aug[pivo] = aug[pivo], aug[linha_pivo]
        valor_pivo = aug[linha_pivo][col]
        aug[linha_pivo] = [val / valor_pivo for val in aug[linha_pivo]]

        for r in range(n_linhas):
            if r != linha_pivo and aug[r][col] != 0:
                fator = aug[r][col]
                aug[r] = [aug[r][c] - fator * aug[linha_pivo][c] for c in range(n_cols + 1)]

        linha_pivo += 1

    posto_a = sum(1 for r in range(n_linhas) if any(aug[r][c] != 0 for c in range(n_cols)))
    posto_ab = sum(1 for r in range(n_linhas) if any(aug[r][c] != 0 for c in range(n_cols + 1)))
    return aug, posto_a, posto_ab


def resolver_sistema_linear_etapa1() -> Dict[str, object]:
    """Resolve o sistema matricial Ax = b da Etapa 1 e retorna diagnóstico completo."""
    det_a = calcular_determinante(MATRIZ_A)
    aug_reduzida, posto_a, posto_ab = escalonar_gauss_jordan(MATRIZ_A, VETOR_B)
    solucao_exata = [int(aug_reduzida[i][-1]) for i in range(len(REGIOES))]

    # Se NumPy estiver disponível, também valida com np.linalg.solve
    solucao_numpy = None
    if POSSUI_NUMPY:
        a_np = np.array(MATRIZ_A, dtype=float)
        b_np = np.array(VETOR_B, dtype=float)
        solucao_numpy = [round(float(v), 6) for v in np.linalg.solve(a_np, b_np)]

    distribuicao_atual = {REGIOES[i]: solucao_exata[i] for i in range(len(REGIOES))}
    verificacoes = verificar_registros_operacionais(distribuicao_atual)

    return {
        "determinante_A": int(det_a),
        "posto_A": posto_a,
        "posto_Ab": posto_ab,
        "sistema_unico_spd": (det_a != 0 and posto_a == posto_ab == len(REGIOES)),
        "vetor_solucao_x": solucao_exata,
        "solucao_numpy": solucao_numpy,
        "distribuicao_atual": distribuicao_atual,
        "verificacoes_relatorio_1": verificacoes,
    }


def verificar_registros_operacionais(dist: Dict[str, int]) -> Dict[str, Dict[str, int | bool]]:
    """Verifica se a distribuição encontrada satisfaz todos os 4 registros do Relatório I."""
    x_n, x_s, x_l, x_o = dist["Norte"], dist["Sul"], dist["Leste"], dist["Oeste"]

    eq1 = x_n + x_s + x_l + x_o
    eq2 = x_n + 2 * x_s + x_o
    eq3 = x_s + 2 * x_l
    eq4 = x_n + x_l + 2 * x_o
    inteiros_nao_negativos = all(isinstance(v, int) and v >= 0 for v in (x_n, x_s, x_l, x_o))

    return {
        "registro_1_frota_total": {"obtido": eq1, "esperado": 72, "ok": eq1 == 72},
        "registro_2_N_mais_O_mais_2S": {"obtido": eq2, "esperado": 76, "ok": eq2 == 76},
        "registro_3_S_mais_2L": {"obtido": eq3, "esperado": 52, "ok": eq3 == 52},
        "registro_4_N_mais_L_mais_2O": {"obtido": eq4, "esperado": 76, "ok": eq4 == 76},
        "restricao_inteiros_nao_negativos": {"ok": inteiros_nao_negativos},
    }


def multiplicar_matriz_vetor(
    matriz: List[List[Fraction]],
    vetor: List[int | Fraction],
) -> List[Fraction]:
    """Calcula o produto matricial y = M * x."""
    resultado: List[Fraction] = []
    for linha in matriz:
        soma = sum(linha[j] * Fraction(vetor[j]) for j in range(len(vetor)))
        resultado.append(soma)
    return resultado


def analisar_demanda_e_redistribuicao_etapa2(vetor_x: List[int]) -> Dict[str, object]:
    """
    Executa a Etapa 2:
    - Calcula a necessidade de ônibus por região a partir do Relatório II;
    - Identifica déficits e superávits;
    - Aplica a Transformação Linear y = T(x) = M * x;
    - Verifica as propriedades de matriz coluna-estocástica (soma das colunas = 1 e m_ij >= 0).
    """
    analise_regioes: List[Dict[str, object]] = []
    vetor_necessidade: List[int] = []

    for idx, regiao in enumerate(REGIOES):
        passageiros = DEMANDA_PASSAGEIROS[regiao]
        atual = vetor_x[idx]
        necessario = passageiros // CAPACIDADE_POR_ONIBUS
        vetor_necessidade.append(necessario)
        saldo_onibus = atual - necessario
        lugares_atuais = atual * CAPACIDADE_POR_ONIBUS
        ocupacao_atual_pct = round((passageiros / lugares_atuais) * 100.0, 2)

        if saldo_onibus < 0:
            status = f"DÉFICIT de {abs(saldo_onibus)} ônibus (Superlotação: {ocupacao_atual_pct}%)"
        elif saldo_onibus > 0:
            status = f"SUPERÁVIT de +{saldo_onibus} ônibus (Ociosidade: {ocupacao_atual_pct}%)"
        else:
            status = "EQUILIBRADO (100%)"

        analise_regioes.append(
            {
                "regiao": regiao,
                "passageiros_estimados": passageiros,
                "capacidade_onibus": CAPACIDADE_POR_ONIBUS,
                "frota_atual": atual,
                "lugares_atuais": lugares_atuais,
                "frota_necessaria": necessario,
                "saldo_onibus": saldo_onibus,
                "ocupacao_atual_pct": ocupacao_atual_pct,
                "status_diagnostico": status,
            }
        )

    # Aplica a transformação linear y = M * x
    vetor_y_frac = multiplicar_matriz_vetor(MATRIZ_TRANSFORMACAO_M_FRAC, vetor_x)
    vetor_y = [int(val) for val in vetor_y_frac]

    # Verificação matemática das propriedades da matriz M
    somas_colunas = [
        sum(MATRIZ_TRANSFORMACAO_M_FRAC[i][j] for i in range(4))
        for j in range(4)
    ]
    colunas_somam_1 = all(soma == Fraction(1, 1) for soma in somas_colunas)
    coeficientes_nao_negativos = all(
        MATRIZ_TRANSFORMACAO_M_FRAC[i][j] >= 0 for i in range(4) for j in range(4)
    )
    preserva_frota_total = sum(vetor_y) == sum(vetor_x) == 72
    sem_alocacoes_negativas = all(y >= 0 for y in vetor_y)

    return {
        "analise_regioes": analise_regioes,
        "vetor_atual_x": vetor_x,
        "vetor_necessario": vetor_necessidade,
        "vetor_redistribuido_y": vetor_y,
        "colunas_somam_1": colunas_somam_1,
        "coeficientes_nao_negativos": coeficientes_nao_negativos,
        "preserva_frota_total": preserva_frota_total,
        "sem_alocacoes_negativas": sem_alocacoes_negativas,
    }


def exibir_relatorio_mmc() -> None:
    """Imprime no terminal a resolução completa das Etapas 1 e 2 de MMC."""
    res1 = resolver_sistema_linear_etapa1()
    vetor_x = res1["vetor_solucao_x"]
    res2 = analisar_demanda_e_redistribuicao_etapa2(vetor_x)

    print("=" * 88)
    print("FIAP — MODELAGEM MATEMÁTICA E COMPUTACIONAL (MMC) — GLOBAL SOLUTION 2026.2")
    print("Mobilidade Urbana Inteligente: Modelagem Matemática para a Gestão do Transporte Público")
    print("=" * 88)

    print("\n[ETAPA 1] DIAGNÓSTICO E MODELAGEM DA SITUAÇÃO ATUAL (SISTEMA LINEAR Ax = b)")
    print("-" * 88)
    print("• Variáveis: x_N (Norte), x_S (Sul), x_L (Leste), x_O (Oeste)")
    print("• Análise de Unicidade (Álgebra Linear):")
    print(f"  - Determinante da matriz A: det(A) = {res1['determinante_A']} (diferente de zero -> A é invertível)")
    print(f"  - Posto da matriz de coeficientes: posto(A) = {res1['posto_A']}")
    print(f"  - Posto da matriz aumentada: posto([A|b]) = {res1['posto_Ab']} = n (4 incógnitas)")
    print("  - Conclusão (Teorema de Rouché-Capelli): Sistema Possível e Determinado (SPD) — Solução Única!")

    print("\n• Distribuição Atual Recuperada (Vetor x):")
    for regiao, qtd in res1["distribuicao_atual"].items():
        print(f"  - Região {regiao:<6}: {qtd:>2} ônibus ({qtd * CAPACIDADE_POR_ONIBUS} lugares)")
    print(f"  - TOTAL ATUAL  : {sum(vetor_x):>2} ônibus ({sum(vetor_x) * CAPACIDADE_POR_ONIBUS} lugares)")

    print("\n• Verificação dos Registros Operacionais (Relatório I):")
    for chave, info in res1["verificacoes_relatorio_1"].items():
        if "esperado" in info:
            status_str = "OK" if info["ok"] else "ERRO"
            print(f"  - {chave:<32}: obtido = {info['obtido']} | esperado = {info['esperado']} [{status_str}]")
        else:
            print(f"  - {chave:<32}: [{'OK' if info['ok'] else 'ERRO'}]")

    print("\n" + "=" * 88)
    print("[ETAPA 2] ANÁLISE DE DEMANDA E POLÍTICA DE REDISTRIBUIÇÃO (TRANSFORMAÇÃO LINEAR y = Mx)")
    print("-" * 88)
    print(f"{'Região':<8} | {'Passageiros':>11} | {'Atual (x)':>9} | {'Ideal (y)':>9} | {'Saldo':>6} | {'Diagnóstico Operacional'}")
    print("-" * 88)
    for item in res2["analise_regioes"]:
        sinal = "+" if item["saldo_onibus"] > 0 else ""
        print(
            f"{item['regiao']:<8} | {item['passageiros_estimados']:>11} | "
            f"{item['frota_atual']:>9} | {item['frota_necessaria']:>9} | "
            f"{sinal + str(item['saldo_onibus']):>6} | {item['status_diagnostico']}"
        )
    print("-" * 88)

    print("\n• Matriz Associada à Transformação Linear M (y = M * x):")
    for i, linha in enumerate(MATRIZ_TRANSFORMACAO_M_FRAC):
        fracs = "  ".join(f"{str(val):>6}" for val in linha)
        decs = "  ".join(f"{float(val):>6.4f}" for val in linha)
        print(f"  Destino {REGIOES[i]:<5}: [ {fracs} ]   (Em decimal: [ {decs} ])")

    print("\n• Resultado Pós-Redistribuição y = T(x) = M * x:")
    for i, regiao in enumerate(REGIOES):
        antes = vetor_x[i]
        depois = res2["vetor_redistribuido_y"][i]
        demanda = DEMANDA_PASSAGEIROS[regiao]
        ocup_nova = (demanda / (depois * CAPACIDADE_POR_ONIBUS)) * 100.0
        print(
            f"  - Região {regiao:<6}: {antes:>2} -> {depois:>2} ônibus "
            f"(Capacidade: {depois * CAPACIDADE_POR_ONIBUS} lugares p/ {demanda} passageiros | Ocupação: {ocup_nova:.1f}%)"
        )

    print("\n• Demonstração das Propriedades Matemáticas de T(x) = M * x:")
    print(f"  - Soma de cada coluna de M igual a 1 (1^T * M = 1^T)? {'SIM' if res2['colunas_somam_1'] else 'NÃO'}")
    print(f"  - Todos os coeficientes m_ij >= 0?                     {'SIM' if res2['coeficientes_nao_negativos'] else 'NÃO'}")
    print(f"  - Frota total preservada (soma(y) == soma(x) == 72)?   {'SIM' if res2['preserva_frota_total'] else 'NÃO'}")
    print(f"  - Nenhuma alocação negativa (y_i >= 0)?                {'SIM' if res2['sem_alocacoes_negativas'] else 'NÃO'}")
    print("=" * 88)


if __name__ == "__main__":
    exibir_relatorio_mmc()
