#!/usr/bin/env python3
"""
Módulo gerador de bases brutas multiformato (CSV, JSON, TXT) para o Challenge Sem Parar.
Gera dados realistas de 25 veículos da frota corporativa ao longo de 90 dias,
incluindo inconsistências propositais para validação dos filtros de qualidade de dados.
"""

import os
import json
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def gerar_bases_brutas(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    os.makedirs("data/raw", exist_ok=True)

    # 1. Cadastro da Frota (25 veículos com 3 perfis homogêneos)
    modelos = {
        "LEVE_URBANO": [
            ("Fiorino 1.4 EVO", 55, "Flex", 11.5),
            ("Kangoo Maxi 1.6", 60, "Flex", 10.8),
            ("Strada Endurance 1.4", 55, "Flex", 12.0)
        ],
        "MEDIO_DISTRIBUICAO": [
            ("VW Delivery Express", 80, "Diesel S10", 6.8),
            ("Mercedes-Benz Accelo 815", 150, "Diesel S10", 6.2),
            ("Iveco Daily 35S15", 100, "Diesel S10", 7.0)
        ],
        "PESADO_RODOVIARIO": [
            ("Scania R450 6x2", 400, "Diesel S10", 2.6),
            ("Volvo FH 540 6x4", 500, "Diesel S10", 2.4),
            ("Mercedes-Benz Actros 2651", 450, "Diesel S10", 2.5)
        ]
    }

    veiculos_cadastro = []
    # 10 Leves, 8 Médios, 7 Pesados
    distribuicao = [("LEVE_URBANO", 10), ("MEDIO_DISTRIBUICAO", 8), ("PESADO_RODOVIARIO", 7)]
    v_id = 1

    for perfil, qtd in distribuicao:
        for _ in range(qtd):
            mod, tanq, comb_tipo, kml_ref = random.choice(modelos[perfil])
            veiculos_cadastro.append({
                "veiculo_id": f"SP-V{v_id:02d}",
                "placa": f"BRA{v_id:02d}{random.randint(10, 99)}",
                "modelo": mod,
                "perfil_operacao": perfil,
                "combustivel_padrao": comb_tipo,
                "capacidade_tanque_litros": tanq,
                "kml_referencia_fabrica": kml_ref,
                "ano_fabricacao": random.randint(2020, 2024),
                "motorista_responsavel": f"Motorista_{v_id:02d}",
                "tag_semparar": f"TAG-SP-{100000 + v_id}"
            })
            v_id += 1

    df_frota = pd.DataFrame(veiculos_cadastro)
    df_frota.to_csv("data/raw/cadastro_frota.csv", index=False)
    print("1. Cadastro da frota gerado: 25 veiculos em data/raw/cadastro_frota.csv")

    # Datas base (90 dias)
    data_inicio = datetime(2026, 7, 1)
    
    # 2. Custos de Combustível (CSV)
    combustivel_transacoes = []
    trans_id = 10001

    preco_litro = {"Flex": 5.89, "Diesel S10": 6.19}

    for veic in veiculos_cadastro:
        vid = veic["veiculo_id"]
        perfil = veic["perfil_operacao"]
        kml_ref = veic["kml_referencia_fabrica"]
        comb_tipo = veic["combustivel_padrao"]
        preco = preco_litro[comb_tipo]

        # Comportamento: alguns veículos são ineficientes propositalmente
        fator_eficiencia = 1.0
        if vid in ["SP-V03", "SP-V14", "SP-V22"]: # 3 veículos com ineficiência severa
            fator_eficiencia = 0.72 # gasta ~38% mais combustível
        elif vid in ["SP-V08", "SP-V16"]: # 2 veículos com atenção
            fator_eficiencia = 0.88

        odometro_acumulado = random.randint(20000, 80000)

        # Frequência de abastecimentos (a cada 3-5 dias)
        dias_abastecimento = random.randint(18, 25)
        for _ in range(dias_abastecimento):
            dias_delta = random.randint(1, 89)
            data_trans = data_inicio + timedelta(days=dias_delta)
            
            # Km percorrido no ciclo
            if perfil == "LEVE_URBANO":
                km_rodado = random.randint(250, 480)
            elif perfil == "MEDIO_DISTRIBUICAO":
                km_rodado = random.randint(450, 850)
            else: # PESADO_RODOVIARIO
                km_rodado = random.randint(900, 1600)

            odometro_acumulado += km_rodado
            kml_real = max(1.0, kml_ref * fator_eficiencia * random.uniform(0.92, 1.05))
            litros = round(km_rodado / kml_real, 2)
            valor_total = round(litros * preco, 2)

            combustivel_transacoes.append({
                "transacao_id": f"COMB-{trans_id}",
                "data_abastecimento": data_trans.strftime("%Y-%m-%d"),
                "veiculo_id": vid,
                "odometro_km": odometro_acumulado,
                "km_percorrido": km_rodado,
                "combustivel": comb_tipo,
                "litros_abastecidos": litros,
                "preco_unitario_litro": preco,
                "valor_total_reais": valor_total,
                "posto_combustivel": random.choice(["Posto Ipiranga Rodo", "Shell Box Express", "Petrobras Rede Siga Bem"])
            })
            trans_id += 1

    # Inserção proposital de inconsistências em combustível:
    # 1. Valor negativo indevido
    combustivel_transacoes.append({
        "transacao_id": "COMB-99901",
        "data_abastecimento": "2026-08-15",
        "veiculo_id": "SP-V02",
        "odometro_km": 45100,
        "km_percorrido": 320,
        "combustivel": "Flex",
        "litros_abastecidos": -45.0, # negativo!
        "preco_unitario_litro": 5.89,
        "valor_total_reais": -265.05, # negativo!
        "posto_combustivel": "Posto Shell Auditoria"
    })
    # 2. Campo obrigatório nulo (veiculo_id ausente)
    combustivel_transacoes.append({
        "transacao_id": "COMB-99902",
        "data_abastecimento": "2026-08-18",
        "veiculo_id": "", # nulo!
        "odometro_km": 38900,
        "km_percorrido": 410,
        "combustivel": "Flex",
        "litros_abastecidos": 38.5,
        "preco_unitario_litro": 5.89,
        "valor_total_reais": 226.77,
        "posto_combustivel": "Posto Ipiranga Sem ID"
    })
    # 3. Chave órfã (veículo inexistente no cadastro)
    combustivel_transacoes.append({
        "transacao_id": "COMB-99903",
        "data_abastecimento": "2026-08-20",
        "veiculo_id": "SP-V99", # Veículo não existe no cadastro!
        "odometro_km": 120500,
        "km_percorrido": 500,
        "combustivel": "Diesel S10",
        "litros_abastecidos": 80.0,
        "preco_unitario_litro": 6.19,
        "valor_total_reais": 495.20,
        "posto_combustivel": "Posto Fantasma"
    })
    # 4. Registro duplicado idêntico
    combustivel_transacoes.append(combustivel_transacoes[10].copy())
    # 5. Incoerência física de consumo (km/l absurdo de 98 km/l)
    combustivel_transacoes.append({
        "transacao_id": "COMB-99904",
        "data_abastecimento": "2026-08-22",
        "veiculo_id": "SP-V21",
        "odometro_km": 150000,
        "km_percorrido": 980,
        "combustivel": "Diesel S10",
        "litros_abastecidos": 10.0, # 98 km/l para caminhão pesado Scania!
        "preco_unitario_litro": 6.19,
        "valor_total_reais": 61.90,
        "posto_combustivel": "Posto Erro Sensor"
    })

    df_comb = pd.DataFrame(combustivel_transacoes)
    df_comb.to_csv("data/raw/custos_combustivel.csv", index=False)
    print(f"2. Custos de combustível gerados: {len(df_comb)} registros em data/raw/custos_combustivel.csv")

    # 3. Custos de Pedágio Sem Parar (JSON)
    pedagio_transacoes = []
    pracas = [
        ("Praça Caieiras", "SP-348 Rodovia dos Bandeirantes", "AutoBAn", 11.80),
        ("Praça Campo Limpo", "SP-330 Rodovia Anhanguera", "AutoBAn", 12.20),
        ("Praça Itaquaquecetuba", "SP-070 Ayrton Senna", "Ecopistas", 5.60),
        ("Praça Diadema", "SP-160 Rodovia dos Imigrantes", "Ecovias", 18.40),
        ("Praça Barueri", "SP-280 Rodovia Castello Branco", "CCR ViaOeste", 6.10),
        ("Praça Moreira César", "BR-116 Presidente Dutra", "CCR RioSP", 17.50)
    ]

    ped_id = 50001
    for veic in veiculos_cadastro:
        vid = veic["veiculo_id"]
        tag = veic["tag_semparar"]
        perfil = veic["perfil_operacao"]

        # Frequência de pedágios conforme perfil
        if perfil == "LEVE_URBANO":
            qtd_pedagios = random.randint(8, 20)
            eixos = 2
        elif perfil == "MEDIO_DISTRIBUICAO":
            qtd_pedagios = random.randint(25, 55)
            eixos = 3
        else: # PESADO_RODOVIARIO
            qtd_pedagios = random.randint(60, 110)
            eixos = 6

        for _ in range(qtd_pedagios):
            dias_delta = random.randint(1, 89)
            data_passagem = data_inicio + timedelta(days=dias_delta, hours=random.randint(6, 21), minutes=random.randint(0, 59))
            praca, rod, conc, tarifa_base = random.choice(pracas)
            valor_pedagio = round(tarifa_base * (eixos / 2.0), 2)

            pedagio_transacoes.append({
                "passagem_id": f"PED-{ped_id}",
                "data_hora_passagem": data_passagem.strftime("%Y-%m-%d %H:%M:%S"),
                "veiculo_id": vid,
                "tag_semparar": tag,
                "praca_pedagio": praca,
                "rodovia": rod,
                "concessionaria": conc,
                "numero_eixos": eixos,
                "valor_tarifa_reais": valor_pedagio,
                "status_cobranca": "PROCESSADO_AUTOMATICO"
            })
            ped_id += 1

    # Inconsistência proposital em pedágio:
    # Registro duplicado e tarifa negativa
    pedagio_transacoes.append(pedagio_transacoes[5].copy())
    pedagio_transacoes.append({
        "passagem_id": "PED-99901",
        "data_hora_passagem": "2026-07-28 14:22:00",
        "veiculo_id": "SP-V10",
        "tag_semparar": "TAG-SP-100010",
        "praca_pedagio": "Praça Estorno Incorreto",
        "rodovia": "SP-280",
        "concessionaria": "CCR ViaOeste",
        "numero_eixos": 2,
        "valor_tarifa_reais": -15.50, # Tarifa negativa indevida!
        "status_cobranca": "ERRO_ESTORNO"
    })

    with open("data/raw/custos_pedagio_semparar.json", "w", encoding="utf-8") as f:
        json.dump(pedagio_transacoes, f, indent=2, ensure_ascii=False)
    print(f"3. Custos de pedágio Sem Parar gerados: {len(pedagio_transacoes)} passagens em data/raw/custos_pedagio_semparar.json")

    # 4. Custos de Manutenção (TXT Estruturado com delimitador de pipes)
    manutencoes = []
    tipos_manut = [
        ("PREVENTIVA", "Troca de oleo, filtros e revisao periodica", (350, 1200)),
        ("PREVENTIVA", "Alinhamento, balanceamento e rodizio de pneus", (250, 600)),
        ("PREVENTIVA", "Substituicao de pastilhas de freio", (400, 1100)),
        ("CORRETIVA", "Reparo do sistema de freios / ABS", (800, 3200)),
        ("CORRETIVA", "Substituicao de embreagem desgastada", (1200, 4800)),
        ("CORRETIVA", "Reparo emergencial no sistema de arrefecimento / radiador", (650, 2900)),
        ("CORRETIVA", "Manutencao corretiva de suspensao e amortecedores", (1100, 3800))
    ]

    manut_id = 70001
    linhas_txt = ["# REGISTRO DE MANUTENCAO DE FROTA - FORMATO PIPE DELIMITED",
                  "# REG|ID_MANUTENCAO|DATA|VEICULO_ID|TIPO_MANUTENCAO|VALOR_REAIS|DESCRICAO|OFICINA_PARCEIRA"]

    for veic in veiculos_cadastro:
        vid = veic["veiculo_id"]
        # Veículos ineficientes sofrem muito mais manutenções corretivas
        if vid in ["SP-V03", "SP-V14", "SP-V22"]:
            qtd_manut = random.randint(4, 7)
            prob_corretiva = 0.80
        elif vid in ["SP-V08", "SP-V16"]:
            qtd_manut = random.randint(2, 4)
            prob_corretiva = 0.50
        else:
            qtd_manut = random.randint(1, 3)
            prob_corretiva = 0.20

        for _ in range(qtd_manut):
            dias_delta = random.randint(3, 88)
            data_m = data_inicio + timedelta(days=dias_delta)
            
            tipo = "CORRETIVA" if random.random() < prob_corretiva else "PREVENTIVA"
            candidatos = [item for item in tipos_manut if item[0] == tipo]
            _, desc, faixa_preco = random.choice(candidatos)
            valor = round(random.uniform(faixa_preco[0], faixa_preco[1]), 2)
            oficina = random.choice(["Oficina Central Bosch Car", "Mecânica RodoDiesel", "Auto Center Porto Seguro"])

            linhas_txt.append(f"REG|MAN-{manut_id}|{data_m.strftime('%Y-%m-%d')}|{vid}|{tipo}|{valor:.2f}|{desc}|{oficina}")
            manut_id += 1

    # Inconsistência proposital em manutenção:
    # 1. Campo de data corrompido / vazio
    linhas_txt.append("REG|MAN-99901||SP-V05|CORRETIVA|1250.00|Reparo sem data registrada|Mecanica Desconhecida")
    # 2. Veículo inexistente
    linhas_txt.append("REG|MAN-99902|2026-08-11|SP-V88|PREVENTIVA|450.00|Revisao de veiculo fantasma|Oficina Rapida")

    with open("data/raw/custos_manutencao.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(linhas_txt) + "\n")
    print(f"4. Custos de manutenção gerados: {len(linhas_txt) - 2} registros em data/raw/custos_manutencao.txt")

    # 5. Custos de Multas e Impostos (CSV)
    multas_impostos = []
    multa_id = 80001
    
    infracoes = [
        ("MULTA", "Excesso de velocidade ate 20% acima do limite", 130.16),
        ("MULTA", "Excesso de velocidade entre 20% e 50% acima", 195.23),
        ("MULTA", "Avanco de sinal vermelho do semaforo", 293.47),
        ("MULTA", "Transitar em faixa ou via exclusiva de onibus", 293.47),
        ("IMPOSTO", "Parcela IPVA e Taxa de Licenciamento Anual", 650.00),
        ("IMPOSTO", "Seguro Obrigatorio e Emissao DPVAT/Taxa", 180.00)
    ]

    for veic in veiculos_cadastro:
        vid = veic["veiculo_id"]
        # Veículos com condutores agressivos têm mais multas
        if vid in ["SP-V03", "SP-V14", "SP-V22"]:
            qtd_ocorrencias = random.randint(3, 6)
        else:
            qtd_ocorrencias = random.randint(1, 2)

        for _ in range(qtd_ocorrencias):
            dias_delta = random.randint(5, 87)
            data_o = data_inicio + timedelta(days=dias_delta)
            tipo_desp, desc, val = random.choice(infracoes)
            multas_impostos.append({
                "infracao_id": f"INF-{multa_id}",
                "data_ocorrencia": data_o.strftime("%Y-%m-%d"),
                "veiculo_id": vid,
                "categoria_despesa": tipo_desp,
                "descricao": desc,
                "valor_reais": val,
                "orgao_emissor": "DETRAN-SP / DER / CET"
            })
            multa_id += 1

    df_multas = pd.DataFrame(multas_impostos)
    df_multas.to_csv("data/raw/custos_multas_impostos.csv", index=False)
    print(f"5. Custos de multas e impostos gerados: {len(df_multas)} registros em data/raw/custos_multas_impostos.csv")

if __name__ == "__main__":
    gerar_bases_brutas()
