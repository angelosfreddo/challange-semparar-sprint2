# Roteiro do Vídeo Demonstrativo — Challenge Sem Parar (Sprint 2)

**Projeto:** Calculadora de Redução de Custos de Frota — Inteligência e Diagnóstico  
**Parceria:** Sem Parar Empresas (Corpay) & FIAP  
**Instituição:** FIAP - Faculdade de Informática e Administração Paulista  
**Turma:** 1TIAO  
**Aluno:** Angelo Guilherme Sfreddo (RM: 566580)  
**Duração Máxima:** Até 5 minutos  
**Visibilidade no YouTube:** Não Listado (Unlisted)

---

## 1. Grade de Minutagem do Vídeo (Até 5 Minutos)

| Bloco | Tempo | Tema Principal | O que Mostrar na Tela |
| :---: | :---: | :--- | :--- |
| **1** | 00:00 - 00:45 | Abertura Oficial, Identificação e Contexto da Sprint 2 | Página inicial do repositório GitHub (`README.md`), destacando a evolução desde a Sprint 1 e as duas perguntas centrais do gestor. |
| **2** | 00:45 - 01:45 | Borda IoT e Detecção de Anomalias com ESP32 (Wokwi) | Simulador Wokwi rodando o circuito com ESP32, variando potenciômetros (RPM, Temp, Vel), acionando LEDs semafóricos, buzzer e exibindo a telemetria serial CSV. |
| **3** | 01:45 - 02:45 | Ingestão Multiformato e Qualidade de Dados | Execução no terminal ou notebook mostrando a leitura de CSV, JSON e TXT, detecção e tratamento das 9 inconsistências propositais e base limpa. |
| **4** | 02:45 - 03:45 | Benchmark Estatístico por Grupos e Ranking de Gaps | Gráficos `01_boxplot_custo_km` e `03_ranking_gaps_ineficiencia`, explicando os 3 grupos homogêneos e os veículos críticos identificados. |
| **5** | 03:45 - 04:30 | Machine Learning, Comparação com Regras e "Ir Além" | Tabela comparativa de acurácia dos modelos (Árvore de Decisão, Random Forest, Rede Neural MLP) e demonstração da extração OCR de faturas. |
| **6** | 04:30 - 05:00 | Conclusão, Resposta às Perguntas do Gestor e Sprint 3 | Diagrama de arquitetura da solução e fechamento com o valor entregue ao cliente Sem Parar. |

---

## 2. Roteiro Passo a Passo e Sugestão Literal do que Falar

### Bloco 1: Abertura e Identificação (00:00 a 00:45)
**O que mostrar:**
Página do repositório GitHub privado na raiz, exibindo o `README.md` com seu nome, RM e turma.

**Sugestão de fala:**
> "Olá a todos! Meu nome é Angelo Guilherme Sfreddo, RM 566580, da turma 1TIAO de Inteligência Artificial da FIAP.  
> Apresento a entrega da Sprint 2 do Challenge Sem Parar Empresas (Corpay), desenvolvendo a etapa de Inteligência e Diagnóstico da Calculadora de Redução de Custos de Frota.  
> Na Sprint 1 estruturamos o planejamento e a arquitetura. Agora, integramos os dados reais da operação para responder com evidências a duas perguntas vitais do gestor de frota: 'Quanto a minha operação realmente custa?' e 'Onde ela está menos eficiente do que deveria?'."

---

### Bloco 2: Módulo IoT e Telemetria no Wokwi (00:45 a 01:45)
**O que mostrar:**
Aba do simulador Wokwi com o circuito do ESP32 executando. Interaja com os componentes (gire o potenciômetro de temperatura até ultrapassar 105°C e de RPM acima de 3800 RPM).

**Sugestão de fala:**
> "Começando pela camada de sensoriamento e borda com ESP32, simulamos a telemetria veicular coletando em tempo real velocidade, rotação em RPM, nível de combustível e temperatura do motor.  
> Quando os sensores operam dentro do padrão, o LED verde fica ativo. Ao elevarmos a temperatura acima de 105°C ou o RPM acima de 3800, o microcontrolador detecta imediatamente a anomalia crítica, acionando o LED vermelho e o alarme sonoro com o buzzer.  
> Além disso, o display LCD 16x2 exibe as leituras ao motorista e o Monitor Serial transmite os registros em formato CSV a 115200 bps, gerando a base de telemetria que alimenta o restante da nossa esteira analítica."

---

### Bloco 3: Ingestão Multiformato e Qualidade de Dados (01:45 a 02:45)
**O que mostrar:**
Abra o terminal e mostre a execução de `python src/app.py --auto` ou abra o arquivo `docs/relatorio_qualidade_dados.md`.

**Sugestão de fala:**
> "Na camada de engenharia e ciência de dados, unificamos fontes heterogêneas: abastecimentos em CSV, passagens automáticas da Tag Sem Parar em JSON, ordens de serviço de manutenção em TXT delimitado por pipes e autuações de trânsito em CSV.  
> Aplicamos uma rigorosa bateria de auditoria de qualidade (Cognitive Data Science), identificando registros com valores negativos indevidos, transações duplicadas, campos obrigatórios nulos, chaves órfãs e consumos fisicamente impossíveis. Cada inconsistência foi tratada com rastreabilidade total, gerando a base transacional limpa e consolidando os 25 veículos da frota."

---

### Bloco 4: Benchmark Justo e Análise de Gaps (02:45 a 03:45)
**O que mostrar:**
Abra o gráfico `assets/diagramas/01_boxplot_custo_km_por_perfil_frota.png` e em seguida o `assets/diagramas/03_ranking_gaps_ineficiencia_frota.png`.

**Sugestão de fala:**
> "Para garantir uma comparação justa, dividimos a frota em três grupos homogêneos: Leve Urbano, Médio Distribuição e Pesado Rodoviário. Adotamos a mediana como métrica central de benchmark, imune a distorções causadas por quebras pontuais.  
> Calculamos o indicador central de custo por quilômetro (R$/km) e medimos o gap de cada veículo em relação ao seu grupo.  
> Como resultado prático, identificamos com clareza os pontos de ineficiência: por exemplo, o furgão SP-V03 apresentou custo de R$ 2,03 por km (+146% sobre o benchmark) devido a avarias severas em suspensão e excesso de giros na telemetria; o caminhão SP-V14 teve desvio de +96% associado a superaquecimento de motor; e o caminhão pesado SP-V22 registrou gap de +39% por frenagens bruscas e excesso de velocidade."

---

### Bloco 5: Machine Learning e "Ir Além" (03:45 a 04:30)
**O que mostrar:**
Abra o gráfico `assets/diagramas/04_matriz_confusao_classificador_ml.png` e mostre o trecho de código de `src/ingestion/extrator_faturas.py` ou a tabela de acurácia.

**Sugestão de fala:**
> "Na modelagem preditiva, comparamos as regras heurísticas de negócio com modelos de Machine Learning supervisionado. Treinamos Árvore de Decisão, Random Forest e Regressão Logística.  
> A Árvore de Decisão reproduziu as classes Eficiente, Atenção e Ineficiente com 100% de concordância frente à regra de negócio, oferecendo explicabilidade completa dos fatores de corte.  
> Indo além dos requisitos mínimos, implementamos também uma Rede Neural Artificial Multi-Layer Perceptron (MLP) com o Scikit-Learn e um módulo de extração inteligente via OCR/parsing para digitalizar comprovantes fiscais e cupons de pedágio não estruturados diretamente para o pipeline."

---

### Bloco 6: Conclusão e Próximos Passos (04:30 a 05:00)
**O que mostrar:**
Abra o diagrama de arquitetura em `assets/diagramas/05_arquitetura_solucao_sprint2.png`.

**Sugestão de fala:**
> "Em síntese, respondemos com precisão empírica às duas perguntas do gestor: demonstramos exatamente quanto a operação custa em cada categoria e apontamos onde estão os gargalos reais de ineficiência.  
> Essa base sólida, auditada e calibrada prepara perfeitamente a Calculadora Sem Parar para a Sprint 3, onde implementaremos o motor de recomendações acionáveis e a estimativa de economia financeira em reais para o cliente.  
> Muito obrigado pela atenção!"
