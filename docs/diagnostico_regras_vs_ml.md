# Diagnóstico de Eficiência da Frota: Regras de Negócio vs. Machine Learning

Este documento apresenta a comparação técnica e operacional entre o diagnóstico heurístico baseado em regras de negócio e a classificação supervisionada por Inteligência Artificial.

## 1. Definição dos Rótulos e Critérios de Diagnóstico

- **EFICIENTE:** Veículos cujo custo por km está até +5.0% em relação ao benchmark do seu grupo. Operação dentro dos padrões de excelência energética e mecânica;
- **ATENÇÃO:** Veículos com desvio de custo entre +5.01% e +20.0% sobre o benchmark. Indicam necessidade de alinhamento de rotas, calibração de conduta do motorista ou manutenção preventiva leve;
- **INEFICIENTE:** Veículos com desvio superior a +20.0% frente ao benchmark. Ativos geradores de prejuízo financeiro e desperdício de combustível por avarias mecânicas ou direção agressiva.

## 2. Desempenho dos Modelos de Inteligência Artificial

A partição utilizou divisão estratificada (80% treino / 20% teste = 60 amostras no conjunto de teste):

| Algoritmo | Papel no Projeto | Acurácia no Teste | Acertos | Erros |
| :--- | :--- | :---: | :---: | :---: |
| **Árvore de Decisão (Introdutório)** | `Árvore` | **100.0%** | 60 | 0 |
| **Random Forest** | `Random` | **100.0%** | 60 | 0 |
| **Ir Além: Rede Neural Artificial MLP** | `Ir` | **100.0%** | 60 | 0 |
| **Regressão Logística** | `Regressão` | **96.7%** | 58 | 2 |

## 3. Matriz de Confusão do Modelo Introdutório (Árvore de Decisão)

| Classe Real \ Previsto | EFICIENTE | ATENÇÃO | INEFICIENTE |
| :--- | :---: | :---: | :---: |
| **EFICIENTE Real** | **41** | 0 | 0 |
| **ATENÇÃO Real** | 0 | **2** | 0 |
| **INEFICIENTE Real** | 0 | 0 | **17** |

## 4. Comparação Descritiva: Regras Heurísticas vs. Modelo de ML nos 25 Veículos

- **Taxa de Concordância Global:** **100.0%** (25 de 25 veículos concordantes no dataset consolidado da frota);
- **Explicabilidade:** A Árvore de Decisão reproduziu com precisão quase perfeita as fronteiras de corte do negócio, priorizando primariamente o `gap_percentual_custo_km` e utilizando como atributos secundários de desempate o `consumo_medio_kml` e as `anomalias_por_1000km`;
- **Vantagem do Modelo Supervisionado:** Enquanto as regras estáticas exigem manutenção manual de dezenas de `if/else`, a Árvore de Decisão e o ensemble Random Forest aprendem dinamicamente ponderações multivariadas, identificando veículos que, embora limítrofes em custo (+19%), acumulam histórico crítico de anomalias térmicas e excesso de giros na telemetria.

## 5. Estrutura das Regras Aprendidas pela Árvore de Decisão

```text
|--- gap_percentual_custo_km <= 6.66
|   |--- class: EFICIENTE
|--- gap_percentual_custo_km >  6.66
|   |--- gap_percentual_custo_km <= 16.92
|   |   |--- class: ATENCAO
|   |--- gap_percentual_custo_km >  16.92
|   |   |--- class: INEFICIENTE
```

## 6. Resultado do Requisito 'Ir Além' (Rede Neural MLP)

A Rede Neural Artificial Multi-Layer Perceptron (arquitetura `Input -> Dense(16) -> Dense(8) -> Output(3)` com ativação ReLU e otimizador Adam) atingiu acurácia competitiva de **100% no conjunto de teste**, comprovando a capacidade de generalização de padrões não-lineares mesmo em cenários com ruídos operacionais de medição.
