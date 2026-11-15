#!/usr/bin/env python3
"""
Módulo "Ir Além": Extrator de Faturas e Comprovantes Fiscais (OCR / Parsing Sintético).
Demonstra a capacidade de extrair comprovantes não estruturados de pedágio e abastecimento,
convertendo-os para o esquema unificado de dados do pipeline de normalização.
"""

import os
import re
import json

def extrair_dados_comprovante_texto(texto_comprovante):
    """
    Parser baseado em expressões regulares e heurísticas de extração para
    comprovantes fiscais digitalizados (DANFE / Ticket de Pedágio / Cupom de Posto).
    """
    # Padrões de extração
    padrao_valor = re.search(r"(?:TOTAL|VALOR|R\$)\s*[:=]?\s*R?\$?\s*([0-9]+[.,][0-9]{2})", texto_comprovante, re.IGNORECASE)
    padrao_placa_ou_veic = re.search(r"(?:VEICULO|PLACA|TAG)\s*[:=]?\s*([A-Z0-9\-]+)", texto_comprovante, re.IGNORECASE)
    padrao_data = re.search(r"(\d{2}[/\-]\d{2}[/\-]\d{4}|\d{4}[/\-]\d{2}[/\-]\d{2})", texto_comprovante)
    padrao_litros = re.search(r"([0-9]+[.,][0-9]{1,3})\s*(?:L|LITROS)", texto_comprovante, re.IGNORECASE)

    valor = float(padrao_valor.group(1).replace(",", ".")) if padrao_valor else None
    identificador = padrao_placa_ou_veic.group(1) if padrao_placa_ou_veic else "NAO_IDENTIFICADO"
    
    data_bruta = padrao_data.group(1) if padrao_data else "2026-08-01"
    if "/" in data_bruta:
        partes = data_bruta.split("/")
        if len(partes[0]) == 4:
            data_iso = f"{partes[0]}-{partes[1]}-{partes[2]}"
        else:
            data_iso = f"{partes[2]}-{partes[1]}-{partes[0]}"
    else:
        data_iso = data_bruta

    litros = float(padrao_litros.group(1).replace(",", ".")) if padrao_litros else None

    tipo_despesa = "COMBUSTIVEL" if litros or "POSTO" in texto_comprovante.upper() else "PEDAGIO"

    return {
        "transacao_id": f"OCR-{abs(hash(texto_comprovante)) % 100000}",
        "data": data_iso,
        "veiculo_id": identificador,
        "categoria_custo": tipo_despesa,
        "subcategoria": "DOCUMENTO_DIGITALIZADO",
        "valor_reais": valor,
        "quantidade": litros if litros else 1.0,
        "unidade_medida": "LITROS" if litros else "TARIFA_UNITARIA",
        "km_odometro": None,
        "km_percorrido": None,
        "origem_dado": "OCR_COMPROVANTE_DIGITAL",
        "estabelecimento_oficina": "EXTRACAO_AUTOMATICA_COMPROVANTE"
    }

def demonstrar_extracao():
    print("Executando demonstracao do modulo 'Ir Alem' (Extracao OCR/Parsing de Comprovantes)...")

    amostra_comprovante_posto = """
    =======================================================
    CUPOM FISCAL ELETRONICO - SAT
    POSTO IPIRANGA RODOVIA ANHANGUERA KM 38
    DATA: 14/08/2026 18:32:00
    PLACA: SP-V04
    PRODUTO: DIESEL S10
    QTDE: 75,40 LITROS
    PRECO UNIT: R$ 6,19
    VALOR TOTAL: R$ 466,73
    FORMA DE PAGAMENTO: CARTAO SEM PARAR EMPRESAS
    =======================================================
    """

    amostra_ticket_pedagio = """
    =======================================================
    CONCESSIONARIA AUTOBAN S.A.
    PRACA DE PEDAGIO CAMPO LIMPO PAULISTA - KM 39
    DATA: 2026-08-15 11:20:14
    TAG: SP-V12
    CATEGORIA: 3 EIXOS
    TARIFA PAGA: R$ 36,60
    COBRANCA AUTOMATICA SEM PARAR
    =======================================================
    """

    r1 = extrair_dados_comprovante_texto(amostra_comprovante_posto)
    r2 = extrair_dados_comprovante_texto(amostra_ticket_pedagio)

    print("Comprovante 1 Extraido com Sucesso:")
    print(json.dumps(r1, indent=2, ensure_ascii=False))
    print("\nComprovante 2 Extraido com Sucesso:")
    print(json.dumps(r2, indent=2, ensure_ascii=False))

    return [r1, r2]

if __name__ == "__main__":
    demonstrar_extracao()
