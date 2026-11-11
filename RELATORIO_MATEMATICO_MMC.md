# Relatório Técnico: Modelagem Matemática e Computacional (MMC)
**Global Solution 2026.2 — CitizenTech**  
**Tema:** Mobilidade Urbana Inteligente: Modelagem Matemática para a Gestão do Transporte Público  
**Curso:** 1º Ano de Ciência da Computação (1CC) — FIAP

---

## ETAPA 1 — Diagnóstico e Modelagem da Situação Atual

### 1.a) Identificação das Variáveis do Problema
Para representar a quantidade de ônibus alocados em cada um dos quatro centros operacionais da empresa municipal durante o período analisado, definimos as quatro variáveis reais (restritas ao conjunto dos números inteiros não negativos $\mathbb{Z}_{\ge 0}$):

* $x_N$: quantidade de ônibus alocados na região **Norte**;
* $x_S$: quantidade de ônibus alocados na região **Sul**;
* $x_L$: quantidade de ônibus alocados na região **Leste**;
* $x_O$: quantidade de ônibus alocados na região **Oeste**.

Restrições físicas do modelo:
$$x_N, x_S, x_L, x_O \in \mathbb{Z}_{\ge 0}$$

---

### 1.b) Construção do Modelo Matemático (Sistema de Equações Lineares)
A partir dos quatro indicadores consolidados preservados no **Relatório I**, traduzimos cada afirmação em uma equação linear:

1. *"A frota disponível para a operação regular é composta por 72 ônibus"*:
   $$x_N + x_S + x_L + x_O = 72 \quad \text{(Equação 1)}$$

2. *"A soma dos veículos da região Norte com os da região Oeste e com o dobro dos veículos da região Sul corresponde a 76 unidades"*:
   $$x_N + 2x_S + 0x_L + x_O = 76 \quad \text{(Equação 2)}$$

3. *"O número de veículos da região Sul, somado ao dobro da quantidade de veículos da região Leste, corresponde a 52 unidades"*:
   $$0x_N + x_S + 2x_L + 0x_O = 52 \quad \text{(Equação 3)}$$

4. *"A quantidade de veículos da região Norte, somada à quantidade da região Leste e ao dobro dos veículos da região Oeste, corresponde a 76 unidades"*:
   $$x_N + 0x_S + x_L + 2x_O = 76 \quad \text{(Equação 4)}$$

Reunindo as quatro equações, obtemos o sistema linear $4 \times 4$:
$$\begin{cases}
x_N + x_S + x_L + x_O = 72 \\
x_N + 2x_S + x_O = 76 \\
x_S + 2x_L = 52 \\
x_N + x_L + 2x_O = 76
\end{cases}$$

---

### 1.c) Representação por meio de um Sistema Matricial
O sistema linear pode ser escrito na forma matricial $A\mathbf{x} = \mathbf{b}$, onde $A \in \mathbb{R}^{4\times 4}$ é a matriz dos coeficientes, $\mathbf{x} \in \mathbb{R}^{4\times 1}$ é o vetor-coluna das incógnitas e $\mathbf{b} \in \mathbb{R}^{4\times 1}$ é o vetor-coluna dos termos independentes:

$$\underbrace{\begin{bmatrix}
1 & 1 & 1 & 1 \\
1 & 2 & 0 & 1 \\
0 & 1 & 2 & 0 \\
1 & 0 & 1 & 2
\end{bmatrix}}_{A}
\underbrace{\begin{bmatrix}
x_N \\
x_S \\
x_L \\
x_O
\end{bmatrix}}_{\mathbf{x}}
=
\underbrace{\begin{bmatrix}
72 \\
76 \\
52 \\
76
\end{bmatrix}}_{\mathbf{b}}$$

A matriz aumentada $[A \mid \mathbf{b}]$ associada ao sistema é:
$$[A \mid \mathbf{b}] = \left[\begin{array}{cccc|c}
1 & 1 & 1 & 1 & 72 \\
1 & 2 & 0 & 1 & 76 \\
0 & 1 & 2 & 0 & 52 \\
1 & 0 & 1 & 2 & 76
\end{array}\right]$$

---

### 1.d) Investigação Matemática de Existência e Unicidade da Solução (Álgebra Linear)

Para investigar se os indicadores preservados permitem determinar uma **única** distribuição de veículos, utilizamos três conceitos equivalentes da Álgebra Linear: **Escalonamento de Gauss (Posto e Teorema de Rouché-Capelli)**, **Determinante** e **Independência Linear das Colunas de $A$**.

#### 1) Escalonamento por Operações Elementares sobre Linhas
Partindo da matriz aumentada $[A \mid \mathbf{b}]$:
* Fazendo $L_2 \leftarrow L_2 - L_1$ e $L_4 \leftarrow L_4 - L_1$:
  $$\left[\begin{array}{cccc|c}
  1 & 1 & 1 & 1 & 72 \\
  0 & 1 & -1 & 0 & 4 \\
  0 & 1 & 2 & 0 & 52 \\
  0 & -1 & 0 & 1 & 4
  \end{array}\right]$$
* Fazendo $L_3 \leftarrow L_3 - L_2$ e $L_4 \leftarrow L_4 + L_2$:
  $$\left[\begin{array}{cccc|c}
  1 & 1 & 1 & 1 & 72 \\
  0 & 1 & -1 & 0 & 4 \\
  0 & 0 & 3 & 0 & 48 \\
  0 & 0 & -1 & 1 & 8
  \end{array}\right]$$
* Fazendo $L_4 \leftarrow L_4 + \frac{1}{3}L_3$:
  $$\left[\begin{array}{cccc|c}
  1 & 1 & 1 & 1 & 72 \\
  0 & 1 & -1 & 0 & 4 \\
  0 & 0 & 3 & 0 & 48 \\
  0 & 0 & 0 & 1 & 24
  \end{array}\right]$$

Observando a matriz escalonada superior $U$:
* Existem **4 pivôs não nulos** ($1, 1, 3, 1$), um em cada linha e coluna de $A$.
* Portanto, o **posto da matriz de coeficientes** é $\text{posto}(A) = 4$ e o **posto da matriz aumentada** é $\text{posto}([A \mid \mathbf{b}]) = 4$.
* Como o número de incógnitas é $n = 4$, temos:
  $$\text{posto}(A) = \text{posto}([A \mid \mathbf{b}]) = n = 4$$
  Pelo **Teorema de Rouché-Capelli**, o sistema é **Possível e Determinado (SPD)**, possuindo **uma única solução** (grau de liberdade $n - \text{posto}(A) = 4 - 4 = 0$).

#### 2) Cálculo do Determinante de $A$
Como as operações elementares de substituição ($L_i \leftarrow L_i + k L_j$) preservam o determinante, o determinante de $A$ é igual ao produto dos elementos da diagonal principal da matriz triangular superior $U$:
$$\det(A) = \det(U) = 1 \times 1 \times 3 \times 1 = 3 \neq 0$$
Como $\det(A) = 3 \neq 0$, a matriz $A$ é **não-singular (invertível)**, suas colunas são **linearmente independentes (LI)** em $\mathbb{R}^4$ e para qualquer vetor $\mathbf{b} \in \mathbb{R}^4$ existe um único vetor $\mathbf{x} = A^{-1}\mathbf{b}$.

#### 3) Resolução Algébrica por Retro-substituição
A partir da matriz escalonada:
* Da 4ª linha: $x_O = 24$;
* Da 3ª linha: $3x_L = 48 \implies x_L = \frac{48}{3} = 16$;
* Da 2ª linha: $x_S - x_L = 4 \implies x_S = 4 + 16 = 20$;
* Da 1ª linha: $x_N + x_S + x_L + x_O = 72 \implies x_N + 20 + 16 + 24 = 72 \implies x_N = 72 - 60 = 12$.

Portanto, a única distribuição atual de ônibus é:
$$\mathbf{x} = \begin{bmatrix} x_N \\ x_S \\ x_L \\ x_O \end{bmatrix} = \begin{bmatrix} 12 \\ 20 \\ 16 \\ 24 \end{bmatrix}$$

---

### 1.e) Implementação Computacional em Python
A resolução computacional completa está implementada no arquivo [`modelo_frota_onibus.py`](modelo_frota_onibus.py), que realiza o escalonamento de Gauss-Jordan com aritmética racional exata (`fractions.Fraction`), calcula $\det(A) = 3$, $\text{posto}(A) = 4$ e resolve o sistema linear (também compatível com `numpy.linalg.solve`), encontrando:
* **Região Norte ($x_N$):** $12\text{ ônibus}$ ($480\text{ lugares}$)
* **Região Sul ($x_S$):** $20\text{ ônibus}$ ($800\text{ lugares}$)
* **Região Leste ($x_L$):** $16\text{ ônibus}$ ($640\text{ lugares}$)
* **Região Oeste ($x_O$):** $24\text{ ônibus}$ ($960\text{ lugares}$)

---

### 1.f) Verificação dos Registros Operacionais Fornecidos
Substituindo $x_N = 12$, $x_S = 20$, $x_L = 16$ e $x_O = 24$ nas quatro condições do Relatório I e nas restrições do problema:

1. **Registro 1 (Frota total de 72 ônibus):**
   $$12 + 20 + 16 + 24 = 72 \quad (\text{Verificado } \checkmark)$$
2. **Registro 2 ($\text{Norte} + \text{Oeste} + 2 \times \text{Sul} = 76$):**
   $$12 + 24 + 2(20) = 36 + 40 = 76 \quad (\text{Verificado } \checkmark)$$
3. **Registro 3 ($\text{Sul} + 2 \times \text{Leste} = 52$):**
   $$20 + 2(16) = 20 + 32 = 52 \quad (\text{Verificado } \checkmark)$$
4. **Registro 4 ($\text{Norte} + \text{Leste} + 2 \times \text{Oeste} = 76$):**
   $$12 + 16 + 2(24) = 28 + 48 = 76 \quad (\text{Verificado } \checkmark)$$
5. **Restrições físicas:** Todos os valores ($12, 20, 16, 24$) são números inteiros e não negativos ($\checkmark$).

---

## ETAPA 2 — Desenvolvimento de uma Política de Redistribuição

### 2.a) Estimativa da Quantidade de Ônibus Necessária por Região (Relatório II)
Sabendo que cada ônibus possui capacidade para atender $C = 40\text{ passageiros}$ no horário de pico, a quantidade mínima necessária de ônibus na região $i$ é dada por $n_i = \frac{\text{Demanda}_i}{40}$:

* **Região Norte:** $n_N = \frac{560}{40} = 14\text{ ônibus}$
* **Região Sul:** $n_S = \frac{760}{40} = 19\text{ ônibus}$
* **Região Leste:** $n_L = \frac{720}{40} = 18\text{ ônibus}$
* **Região Oeste:** $n_O = \frac{840}{40} = 21\text{ ônibus}$
* **Demanda Total da Cidade:** $560 + 760 + 720 + 840 = 2.880\text{ passageiros}$, exigindo um total de $14 + 19 + 18 + 21 = \mathbf{72\text{ ônibus}}$ (exatamente igual à frota total disponível!).

---

### 2.b) Identificação dos Desequilíbrios entre Frota Disponível e Necessidade Estimada

Comparando o vetor da frota atual $\mathbf{x} = [12, 20, 16, 24]^T$ com o vetor da frota necessária $\mathbf{y}_{\text{ideal}} = [14, 19, 18, 21]^T$:

| Região | Passageiros (Pico) | Frota Atual ($x_i$) | Capacidade Atual (Vagas) | Frota Necessária ($y_i$) | Saldo ($x_i - y_i$) | Taxa de Ocupação Atual | Diagnóstico de Desequilíbrio |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Norte** | 560 | 12 | 480 | **14** | **$-2$ ônibus** | $116,67\%$ | **Déficit de 2 ônibus** (80 passageiros sem vaga / superlotação) |
| **Sul** | 760 | 20 | 800 | **19** | **$+1$ ônibus** | $95,00\%$ | **Superávit de 1 ônibus** (40 vagas ociosas) |
| **Leste** | 720 | 16 | 640 | **18** | **$-2$ ônibus** | $112,50\%$ | **Déficit de 2 ônibus** (80 passageiros sem vaga / superlotação) |
| **Oeste** | 840 | 24 | 960 | **21** | **$+3$ ônibus** | $87,50\%$ | **Superávit de 3 ônibus** (120 vagas ociosas) |
| **TOTAL** | **2.880** | **72** | **2.880** | **72** | **$0$** | $100,00\%$ *(média)* | Capacidade global suficiente, porém mal distribuída |

---

### 2.c) Proposta de Política de Redistribuição da Frota e Critérios Adotados

**Critérios adotados pela equipe:**
1. **Eliminação integral da superlotação (Atendimento de 100% da demanda em todas as regiões):** Como a soma dos superávits das regiões Sul ($+1$) e Oeste ($+3$) é de $+4\text{ ônibus}$, exatamente igual à soma dos déficits das regiões Norte ($-2$) e Leste ($-2$), é possível atingir o equilíbrio ótimo $\mathbf{y} = [14, 19, 18, 21]^T$ sem adquirir novos veículos.
2. **Retenção máxima nas regiões deficitárias:** Os centros operacionais com déficit (**Norte** e **Leste**) mantêm $100\%$ de seus ônibus atuais ($12$ e $16$ ônibus, respectivamente) e apenas recebem veículos excedentes.
3. **Transferência proporcional a partir das regiões superavitárias:**
   * O centro **Sul** (que possui $20$ ônibus e precisa de $19$) retém $\frac{19}{20} = 95\%$ de sua frota ($19$ ônibus) e transfere $\frac{1}{20} = 5\%$ de sua frota ($1$ ônibus) para o centro **Leste**.
   * O centro **Oeste** (que possui $24$ ônibus e precisa de $21$) retém $\frac{21}{24} = \frac{7}{8} = 87,5\%$ de sua frota ($21$ ônibus), transfere $\frac{2}{24} = \frac{1}{12} \approx 8,33\%$ de sua frota ($2$ ônibus) para o centro **Norte** e transfere $\frac{1}{24} \approx 4,17\%$ de sua frota ($1$ ônibus) para o centro **Leste**.

---

### 2.d) Representação Matemática por meio de uma Transformação Linear

Definimos a transformação linear $T: \mathbb{R}^4 \to \mathbb{R}^4$ que leva o vetor de estado atual da frota $\mathbf{x} = (x_N, x_S, x_L, x_O)^T$ ao novo vetor de frota redistribuída $\mathbf{y} = (y_N, y_S, y_L, y_O)^T$:

$$T\begin{pmatrix} x_N \\ x_S \\ x_L \\ x_O \end{pmatrix} =
\begin{pmatrix}
1 \cdot x_N + 0 \cdot x_S + 0 \cdot x_L + \frac{2}{24} x_O \\[4pt]
0 \cdot x_N + \frac{19}{20} x_S + 0 \cdot x_L + 0 \cdot x_O \\[4pt]
0 \cdot x_N + \frac{1}{20} x_S + 1 \cdot x_L + \frac{1}{24} x_O \\[4pt]
0 \cdot x_N + 0 \cdot x_S + 0 \cdot x_L + \frac{21}{24} x_O
\end{pmatrix}
= M \mathbf{x}$$

*(Nota: Como $T(\mathbf{u} + \mathbf{v}) = M(\mathbf{u} + \mathbf{v}) = M\mathbf{u} + M\mathbf{v} = T(\mathbf{u}) + T(\mathbf{v})$ e $T(\alpha \mathbf{u}) = M(\alpha \mathbf{u}) = \alpha M\mathbf{u} = \alpha T(\mathbf{u})$ para quaisquer $\mathbf{u}, \mathbf{v} \in \mathbb{R}^4$ e $\alpha \in \mathbb{R}$, $T$ é de fato uma transformação linear.)*

---

### 2.e) Construção da Matriz Associada $M$ e Significado de seus Coeficientes

A matriz canônica $M = [m_{ij}]_{4\times 4}$ associada à transformação linear $T$ na base ordenada $\{N, S, L, O\}$ é:

$$M = \begin{bmatrix}
1 & 0 & 0 & \frac{2}{24} \\[4pt]
0 & \frac{19}{20} & 0 & 0 \\[4pt]
0 & \frac{1}{20} & 1 & \frac{1}{24} \\[4pt]
0 & 0 & 0 & \frac{21}{24}
\end{bmatrix}
=
\begin{bmatrix}
1 & 0 & 0 & \frac{1}{12} \\[4pt]
0 & \frac{19}{20} & 0 & 0 \\[4pt]
0 & \frac{1}{20} & 1 & \frac{1}{24} \\[4pt]
0 & 0 & 0 & \frac{7}{8}
\end{bmatrix}
\approx
\begin{bmatrix}
1,0000 & 0,0000 & 0,0000 & 0,0833 \\
0,0000 & 0,9500 & 0,0000 & 0,0000 \\
0,0000 & 0,0500 & 1,0000 & 0,0417 \\
0,0000 & 0,0000 & 0,0000 & 0,8750
\end{bmatrix}$$

#### Significado Operacional dos Coeficientes $m_{ij}$
* Cada elemento $m_{ij}$ (linha $i$, coluna $j$) representa a **fração (ou proporção) da frota originalmente alocada na região $j$ que passa a operar na região $i$** após a redistribuição:
  * **Elementos da diagonal principal ($m_{ii}$):** representam a **taxa de retenção** de cada centro operacional ($m_{11} = 100\%$ no Norte; $m_{22} = 95\%$ no Sul; $m_{33} = 100\%$ no Leste; $m_{44} = 87,5\%$ no Oeste).
  * **Elementos fora da diagonal ($m_{ij}$, com $i \neq j$):** representam a **taxa de transferência (compartilhamento)** do centro $j$ para o centro $i$:
    * $m_{32} = \frac{1}{20} = 0,05$: $5\%$ da frota do Sul ($1$ ônibus) é compartilhada com o Leste;
    * $m_{14} = \frac{2}{24} = \frac{1}{12} \approx 0,0833$: $8,33\%$ da frota do Oeste ($2$ ônibus) é compartilhada com o Norte;
    * $m_{34} = \frac{1}{24} \approx 0,0417$: $4,17\%$ da frota do Oeste ($1$ ônibus) é compartilhada com o Leste;
    * Os demais $m_{ij} = 0$ indicam ausência de transferência entre os respectivos pares de regiões.

Aplicando $M$ ao vetor atual $\mathbf{x} = [12, 20, 16, 24]^T$:
$$\mathbf{y} = M\mathbf{x} =
\begin{bmatrix}
1(12) + 0(20) + 0(16) + \frac{2}{24}(24) \\[4pt]
0(12) + \frac{19}{20}(20) + 0(16) + 0(24) \\[4pt]
0(12) + \frac{1}{20}(20) + 1(16) + \frac{1}{24}(24) \\[4pt]
0(12) + 0(20) + 0(16) + \frac{21}{24}(24)
\end{bmatrix}
=
\begin{bmatrix}
12 + 2 \\
19 \\
1 + 16 + 1 \\
21
\end{bmatrix}
=
\begin{bmatrix}
14 \\
19 \\
18 \\
21
\end{bmatrix}$$

---

### 2.f) Demonstração Matemática de Conservação da Frota Total e Não-Negatividade

Queremos demonstrar rigorosamente que a transformação linear $\mathbf{y} = T(\mathbf{x}) = M\mathbf{x}$:
1. **Preserva a quantidade total de ônibus** ($\sum_{i=1}^4 y_i = \sum_{j=1}^4 x_j$); e
2. **Não produz alocações negativas** ($y_i \ge 0$ para todo $i \in \{1, 2, 3, 4\}$).

#### Demonstração 1: Preservação da Quantidade Total de Ônibus
A matriz $M$ foi construída como uma **matriz coluna-estocástica (matriz de transição de Markov)**, isto é, a soma dos elementos de cada coluna $j \in \{1, 2, 3, 4\}$ é exatamente igual a $1$:
* Coluna 1 (Norte): $\sum_{i=1}^4 m_{i1} = 1 + 0 + 0 + 0 = 1$
* Coluna 2 (Sul): $\sum_{i=1}^4 m_{i2} = 0 + \frac{19}{20} + \frac{1}{20} + 0 = \frac{20}{20} = 1$
* Coluna 3 (Leste): $\sum_{i=1}^4 m_{i3} = 0 + 0 + 1 + 0 = 1$
* Coluna 4 (Oeste): $\sum_{i=1}^4 m_{i4} = \frac{2}{24} + 0 + \frac{1}{24} + \frac{21}{24} = \frac{24}{24} = 1$

Seja $\mathbf{1}^T = [1, 1, 1, 1]$. Como $\sum_{i=1}^4 m_{ij} = 1$ para todo $j$, vale a identidade matricial $\mathbf{1}^T M = \mathbf{1}^T$. Assim, para qualquer vetor de frota $\mathbf{x} \in \mathbb{R}^4$:
$$\sum_{i=1}^4 y_i = \mathbf{1}^T \mathbf{y} = \mathbf{1}^T (M\mathbf{x}) = (\mathbf{1}^T M)\mathbf{x} = \mathbf{1}^T \mathbf{x} = \sum_{j=1}^4 x_j$$
Em particular, para a nossa frota inicial $\sum_{j=1}^4 x_j = 72$:
$$y_N + y_S + y_L + y_O = 14 + 19 + 18 + 21 = 72 \quad \blacksquare$$

#### Demonstração 2: Ausência de Alocações Negativas ($y_i \ge 0$)
Por construção, todos os coeficientes da matriz $M$ são não negativos:
$$m_{ij} \ge 0, \quad \forall i, j \in \{1, 2, 3, 4\}$$
Além disso, o vetor de frota inicial possui componentes não negativas ($x_j \ge 0, \forall j$). Pela definição do produto matriz-vetor, cada componente $y_i$ do vetor redistribuído é dada por:
$$y_i = \sum_{j=1}^4 m_{ij} x_j = m_{i1}x_N + m_{i2}x_S + m_{i3}x_L + m_{i4}x_O$$
Como o conjunto dos números reais não negativos $\mathbb{R}_{\ge 0}$ é fechado sob adição e multiplicação ($m_{ij} \ge 0$ e $x_j \ge 0 \implies m_{ij}x_j \ge 0 \implies \sum_{j=1}^4 m_{ij}x_j \ge 0$), conclui-se que:
$$y_i \ge 0, \quad \forall i \in \{1, 2, 3, 4\}$$
No caso concreto avaliado, obtemos $\mathbf{y} = [14, 19, 18, 21]^T > \mathbf{0}$, com todas as alocações inteiras, positivas e atendendo a $100\%$ da demanda em todas as regiões. $\blacksquare$
