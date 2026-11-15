# Dicionário de Dados — Challenge Sem Parar (Sprint 2)

Este documento descreve detalhadamente a estrutura, origem, tipos de dados, unidades de medida e regras de negócio aplicadas a todas as bases de dados do projeto **Calculadora de Redução de Custos de Frota**.

---

## 1. Cadastro da Frota (`data/raw/cadastro_frota.csv`)
Base mestra cadastral contendo os 25 veículos monitorados pela Sem Parar Empresas.

| Campo | Tipo | Unidade | Descrição | Exemplo |
| :--- | :---: | :---: | :--- | :--- |
| `veiculo_id` | String | - | Identificador unívoco do veículo (Chave Primária) | `SP-V01` |
| `placa` | String | - | Placa do veículo no padrão Mercosul | `BRA0124` |
| `modelo` | String | - | Fabricante e modelo comercial do veículo | `Fiorino 1.4 EVO` |
| `perfil_operacao` | String | - | Grupo homogêneo de benchmark (`LEVE_URBANO`, `MEDIO_DISTRIBUICAO`, `PESADO_RODOVIARIO`) | `LEVE_URBANO` |
| `combustivel_padrao` | String | - | Tipo de combustível homologado (`Flex`, `Diesel S10`) | `Flex` |
| `capacidade_tanque_litros` | Float | Litros (L) | Volume nominal do tanque de combustível | `55.0` |
| `kml_referencia_fabrica` | Float | km/l | Consumo médio de referência fornecido pelo fabricante | `11.5` |
| `ano_fabricacao` | Inteiro | Ano | Ano de fabricação do veículo | `2023` |
| `motorista_responsavel` | String | - | Identificador do condutor principal alocado | `Motorista_01` |
| `tag_semparar` | String | - | Código numérico da tag RFID Sem Parar instalada | `TAG-SP-100001` |

---

## 2. Custos de Combustível (`data/raw/custos_combustivel.csv`)
Registros de abastecimentos integrados via cartões de combustível corporativos e notas fiscais.

| Campo | Tipo | Unidade | Descrição | Exemplo |
| :--- | :---: | :---: | :--- | :--- |
| `transacao_id` | String | - | Código único do comprovante de abastecimento | `COMB-10001` |
| `data_abastecimento` | Data | YYYY-MM-DD | Data em que o abastecimento foi realizado | `2026-07-04` |
| `veiculo_id` | String | - | Identificador do veículo abastecido | `SP-V01` |
| `odometro_km` | Inteiro | km | Quilometragem registrada no hodômetro no momento da compra | `45200` |
| `km_percorrido` | Inteiro | km | Distância percorrida desde o abastecimento anterior | `380` |
| `combustivel` | String | - | Tipo de combustível abastecido | `Flex` |
| `litros_abastecidos` | Float | Litros (L) | Quantidade de litros faturada na bomba | `34.50` |
| `preco_unitario_litro` | Float | R$/L | Valor do litro cobrado no posto parceiro | `5.89` |
| `valor_total_reais` | Float | Reais (R$) | Valor total pago (`litros * preco_unitario`) | `203.21` |
| `posto_combustivel` | String | - | Nome da rede/posto de abastecimento | `Shell Box Express` |

---

## 3. Custos de Pedágio Sem Parar (`data/raw/custos_pedagio_semparar.json`)
Passagens automáticas registradas nas praças de pedágio rodoviárias pela tag Sem Parar.

| Campo | Tipo | Unidade | Descrição | Exemplo |
| :--- | :---: | :---: | :--- | :--- |
| `passagem_id` | String | - | Identificador único da transação de pedágio | `PED-50001` |
| `data_hora_passagem` | Timestamp | ISO-8601 | Data e hora da transposição da cancela | `2026-07-05 14:22:10` |
| `veiculo_id` | String | - | Identificador do veículo associado | `SP-V01` |
| `tag_semparar` | String | - | Código da tag RFID Sem Parar | `TAG-SP-100001` |
| `praca_pedagio` | String | - | Nome oficial da praça de cobrança | `Praça Caieiras` |
| `rodovia` | String | - | Rodovia concedida onde se localiza a praça | `SP-348 Bandeirantes` |
| `concessionaria` | String | - | Concessionária responsável pela administração | `AutoBAn` |
| `numero_eixos` | Inteiro | Eixos | Quantidade de eixos faturados na passagem | `2` |
| `valor_tarifa_reais` | Float | Reais (R$) | Valor da tarifa debitada na fatura Sem Parar | `11.80` |
| `status_cobranca` | String | - | Status do débito (`PROCESSADO_AUTOMATICO`) | `PROCESSADO_AUTOMATICO` |

---

## 4. Custos de Manutenção (`data/raw/custos_manutencao.txt`)
Ordens de serviço de oficinas e centros automotivos credenciados (formato posicional/delimitado por pipes).

| Posição | Campo | Tipo | Unidade | Descrição |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `tipo_registro` | String | - | Marcador de linha fixa (`REG`) |
| 2 | `id_manutencao` | String | - | Identificador da Ordem de Serviço (`MAN-70001`) |
| 3 | `data_manutencao` | Data | YYYY-MM-DD | Data de execução do serviço |
| 4 | `veiculo_id` | String | - | Identificador do veículo manutenido |
| 5 | `tipo_manutencao` | String | - | Natureza do reparo (`PREVENTIVA` ou `CORRETIVA`) |
| 6 | `valor_reais` | Float | Reais (R$) | Custo total da intervenção (peças + mão de obra) |
| 7 | `descricao` | String | - | Discriminação dos itens trocados ou reparados |
| 8 | `oficina_parceira` | String | - | Razão social ou nome fantasia do estabelecimento |

---

## 5. Custos de Multas e Impostos (`data/raw/custos_multas_impostos.csv`)
Despesas legais, autuações de trânsito e tributos veiculares (IPVA, licenciamento e DPVAT).

| Campo | Tipo | Unidade | Descrição | Exemplo |
| :--- | :---: | :---: | :--- | :--- |
| `infracao_id` | String | - | Código de autuação ou guia de recolhimento | `INF-80001` |
| `data_ocorrencia` | Data | YYYY-MM-DD | Data da infração ou do vencimento do imposto | `2026-07-12` |
| `veiculo_id` | String | - | Veículo autuado ou tributado | `SP-V01` |
| `categoria_despesa` | String | - | Classificação fiscal (`MULTA` ou `IMPOSTO`) | `MULTA` |
| `descricao` | String | - | Motivo legal ou tributo recolhido | `Excesso de velocidade até 20%` |
| `valor_reais` | Float | Reais (R$) | Valor nominal pago | `130.16` |
| `orgao_emissor` | String | - | Entidade arrecadadora | `DETRAN-SP / DER` |

---

## 6. Telemetria de Borda ESP32 (`data/telemetria/telemetria_esp32_amostra.csv`)
Amostras coletadas pelo módulo microcontrolado simulado no Wokwi em intervalos regulares.

| Campo | Tipo | Unidade | Descrição | Limites Críticos |
| :--- | :---: | :---: | :--- | :--- |
| `timestamp_ms` | Inteiro | ms | Tempo decorrido de inicialização do microcontrolador | - |
| `veiculo_id` | String | - | Veículo em trânsito | - |
| `velocidade_kmh` | Float | km/h | Velocidade instantânea | Alerta >= 95, Crítico >= 115 |
| `rpm` | Inteiro | RPM | Rotação do virabrequim | Alerta >= 3100, Crítico >= 3800 |
| `temperatura_motor_c` | Float | °C | Temperatura do fluido de arrefecimento | Alerta >= 98, Crítico >= 105 |
| `combustivel_pct` | Float | % | Nível do reservatório | Alerta <= 15 |
| `status_operacional` | String | - | Classificação de bordo (`NORMAL`, `ATENCAO`, `CRITICO`) | - |
| `alerta_ativo` | Inteiro | Binário | Sinalizador booleano de alarme (0 ou 1) | - |
| `codigo_anomalia` | String | - | Motivo principal do disparo do alarme | `SUPERAQUECIMENTO_MOTOR`, etc. |

---

## 7. Base Consolidada de Indicadores (`data/processed/frota_consolidada_mes.csv`)
Base agregada final resultante dos processos de normalização, auditoria e cruzamento de custos com telemetria.

| Indicador | Unidade | Fórmula de Cálculo | Propósito Analítico |
| :--- | :---: | :--- | :--- |
| `km_total_rodado` | km | $\sum \text{km\_percorrido}$ | Volume de operação do veículo |
| `custo_combustivel` | R$ | $\sum \text{custo de combustíveis}$ | Principal despesa variável |
| `custo_manutencao` | R$ | $\sum \text{custo de intervenções}$ | Desgaste e confiabilidade mecânica |
| `custo_pedagio` | R$ | $\sum \text{tarifas Sem Parar}$ | Custo de mobilidade rodoviária |
| `custo_multas_impostos` | R$ | $\sum \text{multas e tributos}$ | Custos regulatórios e conformidade |
| `custo_total` | R$ | $\sum \text{todos os custos}$ | TCO operacional consolidado |
| `custo_por_km` | R$/km | $\text{custo\_total} / \text{km\_total\_rodado}$ | **Indicador central de eficiência de custos** |
| `consumo_medio_kml` | km/l | $\text{km\_total\_rodado} / \text{litros\_totais}$ | Eficiência energética do veículo |
| `pct_combustivel` | % | $(\text{custo\_combustivel} / \text{custo\_total}) \times 100$ | Peso relativo do combustível |
| `pct_manutencao` | % | $(\text{custo\_manutencao} / \text{custo\_total}) \times 100$ | Peso relativo da oficina |
| `pct_pedagio` | % | $(\text{custo\_pedagio} / \text{custo\_total}) \times 100$ | Peso relativo do pedágio |
| `total_anomalias_telemetria` | Ocorrências | Contagem de alertas no ESP32 | Comportamento agressivo ou falhas mecânicas |
| `anomalias_por_1000km` | Ocorrências/1000km | $(\text{total\_anomalias} / \text{km\_total}) \times 1000$ | Densidade de falhas e risco |
| `gap_custo_km_pct` | % | $((\text{custo\_km} - \text{benchmark\_km}) / \text{benchmark\_km}) \times 100$ | **Gap de ineficiência contra o grupo** |
| `diagnostico_regras` | Categórico | Regra baseada no corte do gap percentual | `EFICIENTE`, `ATENCAO`, `INEFICIENTE` |
| `diagnostico_ml` | Categórico | Predição da Árvore de Decisão / Random Forest | `EFICIENTE`, `ATENCAO`, `INEFICIENTE` |
