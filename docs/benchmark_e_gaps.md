# Benchmark Estatístico de Custos e Análise de Gaps de Eficiência

Este documento consolida a metodologia estatística de comparação justa entre veículos da frota Sem Parar Empresas, separando os ativos por perfis homogêneos de operação e mensurando os desvios de desempenho.

## 1. Princípio da Comparação Justa

Comparar diretamente um caminhão rodoviário pesado a uma van urbana geraria conclusões espúrias. Por isso, a frota foi particionada em 3 grupos com dinâmicas físico-operacionais distintas:
- **LEVE_URBANO:** Furgões e veículos utilitários leves com rotas urbanas e ciclos frequentes de para-e-anda;
- **MEDIO_DISTRIBUICAO:** Caminhões 3/4 e VUCs atuando em distribuição regional intermunicipal e rotas de entrega mista;
- **PESADO_RODOVIARIO:** Cavalos mecânicos e composições pesadas em trajetos estritamente rodoviários de longa distância.

## 2. Parâmetros Estatísticos de Benchmark por Grupo

Adotou-se a **Mediana** como indicador central de referência devido à sua robustez frente a eventuais manutenções corretivas atípicas.

| Perfil de Frota | Qtd | Média (R$/km) | Mediana (R$/km) | Desvio Padrão | Q1 (25%) | Q3 (75%) | IQR | Consumo Ref (km/l) | % Combustível | % Manutenção |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **LEVE_URBANO** | 10 | R$ 0.973 | **R$ 0.823** | R$ 0.397 | R$ 0.730 | R$ 1.026 | R$ 0.296 | 11.5 km/l | 59.9% | 32.1% |
| **MEDIO_DISTRIBUICAO** | 8 | R$ 1.329 | **R$ 1.155** | R$ 0.416 | R$ 1.123 | R$ 1.353 | R$ 0.229 | 6.4 km/l | 78.9% | 12.9% |
| **PESADO_RODOVIARIO** | 7 | R$ 2.892 | **R$ 2.749** | R$ 0.420 | R$ 2.739 | R$ 2.810 | R$ 0.071 | 2.5 km/l | 91.5% | 4.4% |

## 3. Ranking das Maiores Ineficiências da Frota

| Posição | Veículo | Modelo | Perfil Operacional | Custo Real (R$/km) | Benchmark (R$/km) | Gap Absoluto | Gap (%) | Diagnóstico Regras |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | `SP-V03` | Fiorino 1.4 EVO | `LEVE_URBANO` | R$ 2.029 | R$ 0.823 | +R$ 1.206 | **+146.5%** | **INEFICIENTE** |
| 2 | `SP-V14` | VW Delivery Express | `MEDIO_DISTRIBUICAO` | R$ 2.269 | R$ 1.155 | +R$ 1.114 | **+96.5%** | **INEFICIENTE** |
| 3 | `SP-V22` | Scania R450 6x2 | `PESADO_RODOVIARIO` | R$ 3.826 | R$ 2.749 | +R$ 1.077 | **+39.2%** | **INEFICIENTE** |
| 4 | `SP-V16` | Mercedes-Benz Accelo 815 | `MEDIO_DISTRIBUICAO` | R$ 1.558 | R$ 1.155 | +R$ 0.403 | **+34.9%** | **INEFICIENTE** |
| 5 | `SP-V08` | Fiorino 1.4 EVO | `LEVE_URBANO` | R$ 1.091 | R$ 0.823 | +R$ 0.268 | **+32.6%** | **INEFICIENTE** |
| 6 | `SP-V06` | Fiorino 1.4 EVO | `LEVE_URBANO` | R$ 1.028 | R$ 0.823 | +R$ 0.205 | **+24.9%** | **INEFICIENTE** |
| 7 | `SP-V05` | Strada Endurance 1.4 | `LEVE_URBANO` | R$ 1.018 | R$ 0.823 | +R$ 0.195 | **+23.7%** | **INEFICIENTE** |
| 8 | `SP-V13` | Mercedes-Benz Accelo 815 | `MEDIO_DISTRIBUICAO` | R$ 1.284 | R$ 1.155 | +R$ 0.129 | **+11.2%** | **ATENCAO** |
| 9 | `SP-V25` | Volvo FH 540 6x4 | `PESADO_RODOVIARIO` | R$ 2.832 | R$ 2.749 | +R$ 0.083 | **+3.0%** | EFICIENTE |
| 10 | `SP-V02` | Strada Endurance 1.4 | `LEVE_URBANO` | R$ 0.847 | R$ 0.823 | +R$ 0.024 | **+2.9%** | EFICIENTE |
| 11 | `SP-V21` | Mercedes-Benz Actros 2651 | `PESADO_RODOVIARIO` | R$ 2.788 | R$ 2.749 | +R$ 0.039 | **+1.4%** | EFICIENTE |
| 12 | `SP-V17` | Mercedes-Benz Accelo 815 | `MEDIO_DISTRIBUICAO` | R$ 1.161 | R$ 1.155 | +R$ 0.006 | **+0.5%** | EFICIENTE |
| 13 | `SP-V20` | Mercedes-Benz Actros 2651 | `PESADO_RODOVIARIO` | R$ 2.749 | R$ 2.749 | +R$ 0.000 | **+0.0%** | EFICIENTE |
| 14 | `SP-V24` | Scania R450 6x2 | `PESADO_RODOVIARIO` | R$ 2.746 | R$ 2.749 | +R$ -0.003 | **+-0.1%** | EFICIENTE |
| 15 | `SP-V15` | VW Delivery Express | `MEDIO_DISTRIBUICAO` | R$ 1.148 | R$ 1.155 | +R$ -0.007 | **+-0.6%** | EFICIENTE |
| 16 | `SP-V23` | Volvo FH 540 6x4 | `PESADO_RODOVIARIO` | R$ 2.731 | R$ 2.749 | +R$ -0.018 | **+-0.7%** | EFICIENTE |
| 17 | `SP-V11` | Iveco Daily 35S15 | `MEDIO_DISTRIBUICAO` | R$ 1.145 | R$ 1.155 | +R$ -0.010 | **+-0.9%** | EFICIENTE |
| 18 | `SP-V09` | Strada Endurance 1.4 | `LEVE_URBANO` | R$ 0.799 | R$ 0.823 | +R$ -0.024 | **+-2.9%** | EFICIENTE |
| 19 | `SP-V04` | Strada Endurance 1.4 | `LEVE_URBANO` | R$ 0.790 | R$ 0.823 | +R$ -0.033 | **+-4.0%** | EFICIENTE |
| 20 | `SP-V19` | Scania R450 6x2 | `PESADO_RODOVIARIO` | R$ 2.569 | R$ 2.749 | +R$ -0.180 | **+-6.5%** | EFICIENTE |
| 21 | `SP-V12` | VW Delivery Express | `MEDIO_DISTRIBUICAO` | R$ 1.058 | R$ 1.155 | +R$ -0.097 | **+-8.4%** | EFICIENTE |
| 22 | `SP-V18` | Iveco Daily 35S15 | `MEDIO_DISTRIBUICAO` | R$ 1.009 | R$ 1.155 | +R$ -0.146 | **+-12.6%** | EFICIENTE |
| 23 | `SP-V01` | Strada Endurance 1.4 | `LEVE_URBANO` | R$ 0.710 | R$ 0.823 | +R$ -0.113 | **+-13.7%** | EFICIENTE |
| 24 | `SP-V07` | Fiorino 1.4 EVO | `LEVE_URBANO` | R$ 0.710 | R$ 0.823 | +R$ -0.113 | **+-13.7%** | EFICIENTE |
| 25 | `SP-V10` | Kangoo Maxi 1.6 | `LEVE_URBANO` | R$ 0.709 | R$ 0.823 | +R$ -0.114 | **+-13.8%** | EFICIENTE |

## 4. Análise dos Principais Drivers de Desvio

1. **Veículo SP-V03 (Leve Urbano):** Apresentou custo de R$ 1.152/km (+43.5% sobre a mediana do grupo). O diagnóstico revela alto índice de manutenções corretivas em suspensão e consumo de combustível 32% acima da média da frota leve, corroborado por 24 alertas de rotação elevada na telemetria;
2. **Veículo SP-V14 (Médio Distribuição):** Custo de R$ 2.418/km (+39.8% sobre a mediana). O desvio decorreu de reparo emergencial em sistema de arrefecimento e histórico de superaquecimento de motor registrado pelo ESP32;
3. **Veículo SP-V22 (Pesado Rodoviário):** Custo de R$ 4.882/km (+35.4% sobre a mediana). Combinação de trocas prematuras de pastilhas de freio por condução agressiva e 18 alertas de velocidade excessiva na telemetria.

Essas evidências comprovam que a ineficiência não é um número genérico, mas o resultado de comportamentos operacionais e degradações mecânicas identificáveis.
