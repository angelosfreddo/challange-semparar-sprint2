# Relatório de Auditoria e Verificações de Qualidade de Dados

Este documento registra a aplicação das regras de integridade e auditoria sobre os dados integrados de custos, cadastro e telemetria da Sem Parar Empresas.

## 1. Resumo Executivo da Auditoria

- **Total de Transações Ingeridas:** 1669
- **Transações Válidas Homologadas:** 1661 (99.5%)
- **Inconsistências Detectadas:** 9
- **Transações Descartadas por Inviabilidade:** 8
- **Transações Corrigidas por Imputação Técnica:** 1

## 2. Detalhamento das Inconsistências por Categoria

| ID Transação | Tipo de Inconsistência | Descrição da Ocorrência | Tratamento Aplicado |
| :--- | :--- | :--- | :--- |
| `COMB-10011` | **DUPLICIDADE_TRANSACAO** | Registro duplicado da transacao COMB-10011 no canal CSV_CARTAO_COMBUSTIVEL | `DESCARTE_REGISTRO_DUPLICADO` |
| `PED-50006` | **DUPLICIDADE_TRANSACAO** | Registro duplicado da transacao PED-50006 no canal JSON_TAG_SEMPARAR | `DESCARTE_REGISTRO_DUPLICADO` |
| `COMB-99902` | **CAMPO_OBRIGATORIO_NULO** | Campo veiculo_id, data ou valor_reais ausente | `DESCARTE_INVIABILIDADE_RASTREABILIDADE` |
| `MAN-99901` | **CAMPO_OBRIGATORIO_NULO** | Campo veiculo_id, data ou valor_reais ausente | `DESCARTE_INVIABILIDADE_RASTREABILIDADE` |
| `COMB-99901` | **VALOR_NEGATIVO_INDEVIDO** | Valor total (R$ -265.05) ou quantidade (-45.0) negativo | `DESCARTE_ERRO_ESTORNO_FINANCEIRO` |
| `PED-99901` | **VALOR_NEGATIVO_INDEVIDO** | Valor total (R$ -15.5) ou quantidade (2.0) negativo | `DESCARTE_ERRO_ESTORNO_FINANCEIRO` |
| `COMB-99903` | **CHAVE_ESTRANGEIRA_ORFA** | Veiculo SP-V99 nao cadastrado no registro mestre de frota | `ISOLAMENTO_EM_QUARANTENA_AUDITORIA` |
| `MAN-99902` | **CHAVE_ESTRANGEIRA_ORFA** | Veiculo SP-V88 nao cadastrado no registro mestre de frota | `ISOLAMENTO_EM_QUARANTENA_AUDITORIA` |
| `COMB-99904` | **CONSUMO_FISICAMENTE_IMPOSSIVEL** | Eficiencia calculada de 98.0 km/l excede limites de engenharia veicular | `IMPUTACAO_PELA_MEDIANA_DO_VEICULO` |

## 3. Justificativa Técnica dos Tratamentos Aplicados

1. **Valores Negativos:** Em faturas de combustíveis e pedágios, valores negativos decorrem comumente de estornos operacionais não conciliados ou falhas de integração no ponto de venda (PDV). Foram descartados para evitar distorção da média de custos por km da frota;
2. **Campos Obrigatórios Nulos:** A ausência de `veiculo_id` ou data inviabiliza a rastreabilidade fiscal e impede o cálculo do TCO por ativo, resultando em descarte auditado;
3. **Chaves Órfãs:** Transações atribuídas a veículos inexistentes na base mestra (`SP-V99`, `SP-V88`) foram isoladas para investigação de possível fraude ou erro de digitação de placas em postos;
4. **Duplicidades:** Deduplicação por chave unívoca de evento (`transacao_id` e `passagem_id`), mantendo a primeira ocorrência;
5. **Incoerências de Consumo:** Registros de consumo discrepantes das leis de conservação de energia e consumo de motores a combustão foram reajustados pela mediana de fábrica do respectivo modelo, preservando a quilometragem real percorrida.
