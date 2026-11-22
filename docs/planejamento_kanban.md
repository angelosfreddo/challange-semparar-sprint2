# Planejamento Ágil e Quadro Kanban — Challenge Sem Parar

**Projeto:** Calculadora de Redução de Custos de Frota  
**Parceria:** Sem Parar Empresas (Corpay) & FIAP  
**Aluno:** Angelo Guilherme Sfreddo (RM: 566580) — Turma: 1TIAO  
**Ferramenta de Gestão:** Trello (Metodologia Kanban / Scrum Adaptado)

---

## 1. Visão Geral dos Ciclos de Entrega

```text
[Sprint 1: Concepção & Arquitetura] (Concluída)
       │
       ▼
[Sprint 2: Inteligência & Diagnóstico] (Entregue Nesta Etapa)
       │
       ▼
[Sprint 3: Recomendações & Economia Financeira em R$] (Próxima Etapa)
```

---

## 2. Quadro Kanban Detalhado por Colunas

### Coluna 1: Concluído na Sprint 1 (Fase 1 a 3)
- [x] Mapeamento das 20 User Stories e definição das 3 Personas (Gestor de Frota, CFO e Sem Parar);
- [x] Modelagem conceitual da Calculadora de Custos de Frota;
- [x] Definição dos níveis de maturidade de dados (Bronze, Prata e Ouro);
- [x] Especificação da arquitetura lógica integrando as disciplinas da Fase 3;
- [x] Catálogo de soluções e integrações da Sem Parar Empresas;
- [x] Repositório oficial e documentação inicial no GitHub (`challange-semparar-sprint1`).

---

### Coluna 2: Concluído na Sprint 2 (Entrega Atual — Inteligência e Diagnóstico)
- [x] **AI Computer Systems & Sensors (ESP32):**
  - [x] Firmware C/C++ desenvolvido no Wokwi (`src/iot_esp32/sketch.ino`);
  - [x] Telemetria de 4 variáveis críticas (velocidade, RPM, temperatura do motor e combustível);
  - [x] Detecção de anomalias operacionais (superaquecimento >= 105°C, giro excessivo >= 3800 RPM, excesso de velocidade >= 115 km/h);
  - [x] Atuação física com LEDs semafóricos, alarme sonoro com Buzzer e interface LCD 16x2 I2C;
  - [x] Exportação de 5.000 leituras de telemetria em CSV (`data/telemetria/telemetria_esp32_amostra.csv`).
- [x] **Computational Thinking with Python:**
  - [x] Módulo de ingestão multiformato (`src/ingestion/normalizador.py`) para CSV, JSON e TXT posicional/pipe;
  - [x] Normalização de taxonomia de custos, unidades monetárias e datas em padrão ISO-8601;
  - [x] Base normalizada exportada em CSV e JSON (`data/processed/base_custos_normalizada.*`).
- [x] **Cognitive Data Science:**
  - [x] Motor de auditoria de consistência (`src/quality/auditoria_qualidade.py`);
  - [x] Detecção e descarte/tratamento de 9 inconsistências intencionais (valores negativos, duplicidades, campos nulos, chaves órfãs e consumos impossíveis);
  - [x] Relatório técnico de auditoria emitido (`docs/relatorio_qualidade_dados.md`);
  - [x] Base transacional limpa e base agregada por veículo (`data/processed/frota_consolidada_mes.csv`).
- [x] **Statistical Computing:**
  - [x] Segmentação da frota em 3 grupos homogêneos (`LEVE_URBANO`, `MEDIO_DISTRIBUICAO`, `PESADO_RODOVIARIO`);
  - [x] Cálculo dos benchmarks estatísticos com mediana, média, quartis Q1/Q3 e desvio padrão (`data/processed/tabela_benchmarks_grupos.csv`);
  - [x] Mensuração dos Gaps de Eficiência (absoluto em R$/km e percentual) com ranking geral de ineficiência (`docs/benchmark_e_gaps.md`).
- [x] **Machine Learning & Modelling:**
  - [x] Treinamento comparativo de 4 modelos supervisionados (Árvore de Decisão, Random Forest, Regressão Logística e Rede Neural MLP);
  - [x] Acurácia de até 100% no conjunto de teste estratificado (80/20);
  - [x] Confronto analítico: Diagnóstico Heurístico por Regras vs. Modelo de Aprendizado de Máquina com 100% de concordância (`docs/diagnostico_regras_vs_ml.md`);
  - [x] Serialização dos artefatos treinados com `joblib`.
- [x] **Ir Além (Bônus):**
  - [x] Rede Neural Artificial MLP (`MLPClassifier`) implementada e avaliada;
  - [x] Módulo de parsing OCR de comprovantes de pedágio e abastecimento (`src/ingestion/extrator_faturas.py`).
- [x] **Analytics Visual & Executável:**
  - [x] 5 painéis visuais em alta resolução e diagrama de arquitetura (`assets/diagramas/`);
  - [x] Aplicação executável CLI (`src/app.py --auto` e modo interativo);
  - [x] Jupyter Notebook completo (`notebooks/02_inteligencia_e_diagnostico_frota.ipynb`).

---

### Coluna 3: Backlog Planejado para a Sprint 3 (Próxima Fase)
- [ ] Motor de Recomendação Prescritiva por Veículo (ações corretivas de manutenção, treinamento de condutor e readequação de rotas);
- [ ] Estimativa de Economia Financeira Projetada em Reais (R$/ano) caso os veículos atinjam o benchmark do seu grupo;
- [ ] Simulador de ROI (Retorno sobre Investimento) das soluções Sem Parar Empresas (Tag Pedágio, Cartão Combustível, Gestão de Abastecimento);
- [ ] Relatório executivo consolidado em formato PDF / Dashboard web para tomada de decisão do CFO e Gestor de Frota.

