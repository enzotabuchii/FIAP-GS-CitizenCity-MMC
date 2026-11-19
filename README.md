# Mobilidade Urbana Inteligente: Modelagem Matemática para a Gestão do Transporte Público (MMC)

**Global Solution 2026.2 — CitizenTech — 1º Ano de Ciência da Computação (1CC)**  
**Disciplina:** Modelagem Matemática e Computacional (MMC)

---

## 1. Visão Geral do Projeto

Este repositório contém a resolução completa (matemática e computacional em Python) do desafio de **Modelagem Matemática e Computacional** da Global Solution 2026.2. O sistema recupera a distribuição atual de uma frota de **72 ônibus** entre quatro regiões (**Norte, Sul, Leste e Oeste**) usando **Sistemas Lineares e Matrizes (Etapa 1)** e propõe uma política ótima de redistribuição de veículos baseada em **Transformações Lineares e Matrizes Coluna-Estocásticas (Etapa 2)**.

---

## Integrantes

| Integrante | RM |
| --- | ---: |
| **Enzo Seiji Delgado Tabuchi** | `573156` |
| **Luca Almeida Lucareli** | `569061` |
| **Henrique Almeida Lucareli** | `569183` |

---

## 2. Estrutura de Arquivos

* [`RELATORIO_MATEMATICO_MMC.md`](RELATORIO_MATEMATICO_MMC.md): Relatório matemático detalhado respondendo passo a passo aos itens **a, b, c, d, e, f da Etapa 1** e **a, b, c, d, e, f da Etapa 2** (com escalonamento de Gauss, determinante, Teorema de Rouché-Capelli, matriz de transformação linear $M$ e demonstrações formais), além da **avaliação dos resultados** da intervenção e das **limitações do modelo**.
* [`modelo_frota_onibus.py`](modelo_frota_onibus.py): Implementação computacional completa em Python (calcula determinante, posto, escalonamento de Gauss-Jordan exato com `fractions.Fraction`, compatibilidade automática com `numpy`, verificação dos registros do Relatório I e aplicação da transformação linear $\mathbf{y} = M\mathbf{x}$).
* [`test_modelo_frota.py`](test_modelo_frota.py): Suíte de testes unitários automatizados comprovando a exatidão matemática do modelo.

---

## 3. Resumo dos Resultados Obtidos

| Região | Demanda (Passageiros) | Frota Atual Recuperada ($\mathbf{x}$) | Capacidade Atual (Vagas) | Saldo Inicial | Frota Redistribuída ($\mathbf{y} = M\mathbf{x}$) | Nova Capacidade (Vagas) | Nova Taxa de Ocupação |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Norte** | 560 | **12 ônibus** | 480 *(116,7%)* | $-2$ ônibus | **14 ônibus** | 560 | **100,0%** |
| **Sul** | 760 | **20 ônibus** | 800 *(95,0%)* | $+1$ ônibus | **19 ônibus** | 760 | **100,0%** |
| **Leste** | 720 | **16 ônibus** | 640 *(112,5%)* | $-2$ ônibus | **18 ônibus** | 720 | **100,0%** |
| **Oeste** | 840 | **24 ônibus** | 960 *(87,5%)* | $+3$ ônibus | **21 ônibus** | 840 | **100,0%** |
| **TOTAL** | **2.880** | **72 ônibus** | **2.880** | **0** | **72 ônibus** | **2.880** | **100,0%** |

**Avaliação da intervenção:** os passageiros sem vaga no pico caem de **160 para 0** e as vagas ociosas também caem de **160 para 0**, movendo apenas **4 ônibus** (5,6% da frota), sem ampliar a frota.

---

## 4. Como Executar o Código e os Testes

```bash
# Executar a resolução computacional completa das Etapas 1 e 2
python3 modelo_frota_onibus.py

# Executar os testes automatizados de validação algébrica
python3 test_modelo_frota.py -v
```
