#!/usr/bin/env python3
"""
Módulo de Ingestão e Normalização de Fontes Heterogêneas.
Lê dados em CSV, JSON e TXT posicional/pipe, padronizando campos, datas ISO-8601,
unidades monetárias e taxonomia unificada de despesas de frota.
"""

import os
import json
import pandas as pd
from datetime import datetime

def normalizar_combustivel(caminho_csv="data/raw/custos_combustivel.csv"):
    df = pd.read_csv(caminho_csv)
    registros = []
    for _, row in df.iterrows():
        registros.append({
            "transacao_id": str(row.get("transacao_id", "")).strip(),
            "data": str(row.get("data_abastecimento", "")).strip(),
            "veiculo_id": str(row.get("veiculo_id", "")).strip(),
            "categoria_custo": "COMBUSTIVEL",
            "subcategoria": str(row.get("combustivel", "INDEFINIDO")).strip(),
            "valor_reais": float(row.get("valor_total_reais", 0.0)) if pd.notnull(row.get("valor_total_reais")) else None,
            "quantidade": float(row.get("litros_abastecidos", 0.0)) if pd.notnull(row.get("litros_abastecidos")) else None,
            "unidade_medida": "LITROS",
            "km_odometro": float(row.get("odometro_km", 0.0)) if pd.notnull(row.get("odometro_km")) else None,
            "km_percorrido": float(row.get("km_percorrido", 0.0)) if pd.notnull(row.get("km_percorrido")) else None,
            "origem_dado": "CSV_CARTAO_COMBUSTIVEL",
            "estabelecimento_oficina": str(row.get("posto_combustivel", "")).strip()
        })
    return registros

def normalizar_pedagio(caminho_json="data/raw/custos_pedagio_semparar.json"):
    with open(caminho_json, "r", encoding="utf-8") as f:
        dados = json.load(f)
    registros = []
    for row in dados:
        data_hora = str(row.get("data_hora_passagem", "")).strip()
        data_iso = data_hora.split(" ")[0] if " " in data_hora else data_hora
        registros.append({
            "transacao_id": str(row.get("passagem_id", "")).strip(),
            "data": data_iso,
            "veiculo_id": str(row.get("veiculo_id", "")).strip(),
            "categoria_custo": "PEDAGIO",
            "subcategoria": str(row.get("praca_pedagio", "PRACA_RODOVIA")).strip(),
            "valor_reais": float(row.get("valor_tarifa_reais", 0.0)) if row.get("valor_tarifa_reais") is not None else None,
            "quantidade": float(row.get("numero_eixos", 2)),
            "unidade_medida": "EIXOS",
            "km_odometro": None,
            "km_percorrido": None,
            "origem_dado": "JSON_TAG_SEMPARAR",
            "estabelecimento_oficina": f"{row.get('concessionaria', '')} - {row.get('rodovia', '')}"
        })
    return registros

def normalizar_manutencao(caminho_txt="data/raw/custos_manutencao.txt"):
    registros = []
    with open(caminho_txt, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            partes = linha.split("|")
            if len(partes) >= 8 and partes[0] == "REG":
                _, man_id, data_str, veic_id, tipo_manut, valor_str, desc, oficina = partes[:8]
                try:
                    valor = float(valor_str) if valor_str else None
                except ValueError:
                    valor = None
                registros.append({
                    "transacao_id": man_id.strip(),
                    "data": data_str.strip(),
                    "veiculo_id": veic_id.strip(),
                    "categoria_custo": "MANUTENCAO",
                    "subcategoria": tipo_manut.strip(),
                    "valor_reais": valor,
                    "quantidade": 1.0,
                    "unidade_medida": "ORDEM_SERVICO",
                    "km_odometro": None,
                    "km_percorrido": None,
                    "origem_dado": "TXT_ORDEM_SERVICO_OFICINA",
                    "estabelecimento_oficina": f"{oficina.strip()} ({desc.strip()})"
                })
    return registros

def normalizar_multas_impostos(caminho_csv="data/raw/custos_multas_impostos.csv"):
    df = pd.read_csv(caminho_csv)
    registros = []
    for _, row in df.iterrows():
        registros.append({
            "transacao_id": str(row.get("infracao_id", "")).strip(),
            "data": str(row.get("data_ocorrencia", "")).strip(),
            "veiculo_id": str(row.get("veiculo_id", "")).strip(),
            "categoria_custo": "MULTAS_IMPOSTOS",
            "subcategoria": str(row.get("categoria_despesa", "TAXA_LEGAL")).strip(),
            "valor_reais": float(row.get("valor_reais", 0.0)) if pd.notnull(row.get("valor_reais")) else None,
            "quantidade": 1.0,
            "unidade_medida": "AUTUACAO_GUIA",
            "km_odometro": None,
            "km_percorrido": None,
            "origem_dado": "CSV_ORGAO_TRANSITO",
            "estabelecimento_oficina": f"{row.get('orgao_emissor', '')} - {row.get('descricao', '')}"
        })
    return registros

def executar_normalizacao():
    print("Iniciando ingestao e normalizacao de fontes heterogeneas...")
    lista_geral = []
    lista_geral.extend(normalizar_combustivel())
    lista_geral.extend(normalizar_pedagio())
    lista_geral.extend(normalizar_manutencao())
    lista_geral.extend(normalizar_multas_impostos())

    df_consolidado = pd.DataFrame(lista_geral)
    
    os.makedirs("data/processed", exist_ok=True)
    caminho_csv = "data/processed/base_custos_normalizada.csv"
    caminho_json = "data/processed/base_custos_normalizada.json"

    df_consolidado.to_csv(caminho_csv, index=False)
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(lista_geral, f, indent=2, ensure_ascii=False)

    print(f"Normalizacao concluida: {len(df_consolidado)} registros unificados.")
    print(f"Saidas salvas em:\n - {caminho_csv}\n - {caminho_json}")
    return df_consolidado

if __name__ == "__main__":
    executar_normalizacao()

