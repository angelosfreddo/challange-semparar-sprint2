#!/usr/bin/env python3
"""
Aplicação Central Executável — Calculadora de Redução de Custos de Frota (Sprint 2).
Permite executar o pipeline completo em modo automatizado (--auto) ou navegar
interativamente para inspecionar veículos, benchmarks, anomalias e diagnósticos.
"""

import os
import sys

# Garante inclusão da raiz do projeto no PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
import pandas as pd
from src.ingestion.normalizador import executar_normalizacao
from src.quality.auditoria_qualidade import executar_auditoria_qualidade
from src.benchmark.calculador_benchmark import calcular_benchmark_e_gaps
from src.ml.classificador_eficiencia import treinar_e_avaliar_modelos
from src.analytics.gerar_graficos_sprint2 import gerar_todos_os_graficos

def exibir_cabecalho():
    print("=" * 90)
    print("FIAP - GRADUACAO EM INTELIGENCIA ARTIFICIAL (FASE 4)")
    print("CHALLENGE SEM PARAR EMPRESAS (CORPAY) - SPRINT 2: INTELIGENCIA E DIAGNOSTICO")
    print("PROJETO: CALCULADORA DE REDUCAO DE CUSTOS DE FROTA")
    print("Aluno: Angelo Guilherme Sfreddo | RM: 566580 | Turma: 1TIAO")
    print("=" * 90)

def executar_pipeline_completo():
    exibir_cabecalho()
    print("\n>>> ETAPA 1/5: INGESTAO E NORMALIZACAO DE FONTES HETEROGENEAS (CSV, JSON, TXT)")
    executar_normalizacao()

    print("\n>>> ETAPA 2/5: AUDITORIA DE QUALIDADE DE DADOS E INTEGRACAO (COGNITIVE DATA SCIENCE)")
    executar_auditoria_qualidade()

    print("\n>>> ETAPA 3/5: COMPUTACAO ESTATISTICA E BENCHMARK POR GRUPO HOMOGENEO")
    calcular_benchmark_e_gaps()

    print("\n>>> ETAPA 4/5: MACHINE LEARNING & DIAGNOSTICO DE EFICIENCIA")
    treinar_e_avaliar_modelos()

    print("\n>>> ETAPA 5/5: ANALYTICS VISUAL E GERACAO DE GRAFICOS EXECUTIVOS")
    gerar_todos_os_graficos()

    print("\n" + "=" * 90)
    print("PIPELINE EXECUTADO COM SUCESSO! RESUMO DOS INDICADORES CONSOLIDADOS:")
    print("=" * 90)
    
    df_final = pd.read_csv("data/processed/frota_com_benchmark_e_ml.csv")
    cols_view = ["veiculo_id", "modelo", "perfil_operacao", "custo_por_km", "benchmark_custo_km",
                 "gap_percentual_custo_km", "diagnostico_regras", "diagnostico_ml"]
    print(df_final[cols_view].to_string(index=False))
    
    print("\nDistribuição dos Diagnósticos nos 25 Veículos da Frota:")
    print(df_final["diagnostico_regras"].value_counts().to_string())

def inspecionar_veiculo_interativo():
    df = pd.read_csv("data/processed/frota_com_benchmark_e_ml.csv")
    print("\nVeiculos disponiveis: " + ", ".join(df["veiculo_id"].tolist()))
    vid = input("Digite o ID do veiculo para inspecionar (ex: SP-V03): ").strip().upper()
    
    veic = df[df["veiculo_id"] == vid]
    if veic.empty:
        print(f"Veiculo {vid} nao encontrado.")
        return

    row = veic.iloc[0]
    print("\n" + "-" * 70)
    print(f"FICHA TECNICA E DIAGNOSTICO: {row['veiculo_id']} ({row['modelo']})")
    print("-" * 70)
    print(f"Perfil de Operacao:          {row['perfil_operacao']}")
    print(f"Placa / Motorista:            {row['placa']} / {row['motorista_responsavel']}")
    print(f"Quilometragem no Periodo:    {row['km_total_rodado']:,.0f} km")
    print(f"Consumo Medio Real:          {row['consumo_medio_kml']:.2f} km/l (Fabrica: {row['kml_referencia_fabrica']:.2f} km/l)")
    print(f"Custo Total da Operacao:     R$ {row['custo_total']:,.2f}")
    print(f"  - Combustivel:             R$ {row['COMBUSTIVEL']:,.2f} ({row['pct_combustivel']:.1f}%)")
    print(f"  - Manutencao:              R$ {row['MANUTENCAO']:,.2f} ({row['pct_manutencao']:.1f}%)")
    print(f"  - Pedagio Sem Parar:       R$ {row['PEDAGIO']:,.2f} ({row['pct_pedagio']:.1f}%)")
    print(f"  - Multas e Impostos:       R$ {row['MULTAS_IMPOSTOS']:,.2f} ({row['pct_multas_impostos']:.1f}%)")
    print(f"Custo Real por KM:           R$ {row['custo_por_km']:.3f} / km")
    print(f"Benchmark do Grupo:          R$ {row['benchmark_custo_km']:.3f} / km")
    print(f"Gap de Eficiencia:           {'+' if row['gap_percentual_custo_km'] > 0 else ''}{row['gap_percentual_custo_km']:.1f}%")
    print(f"Anomalias no ESP32:          {row['total_anomalias_telemetria']} alertas ({row['anomalias_por_1000km']:.2f} por 1.000 km)")
    print(f"DIAGNOSTICO POR REGRAS:      {row['diagnostico_regras']}")
    print(f"DIAGNOSTICO POR ML (IA):     {row['diagnostico_ml']}")
    print("-" * 70)

def main():
    parser = argparse.ArgumentParser(description="Calculadora de Custos de Frota Sem Parar - Sprint 2")
    parser.add_argument("--auto", action="store_true", help="Executa o pipeline completo ponta a ponta sem paradas")
    args = parser.parse_args()

    if args.auto or not sys.stdin.isatty():
        executar_pipeline_completo()
        return

    while True:
        exibir_cabecalho()
        print("\nMENU PRINCIPAL - SPRINT 2 (INTELIGENCIA E DIAGNOSTICO)")
        print("1. Executar Pipeline Completo (Ingestao, Auditoria, Benchmark, ML e Graficos)")
        print("2. Inspecionar Diagnostico Detalhado de um Veiculo")
        print("3. Visualizar Tabela de Benchmarks por Grupo Homogeneo")
        print("4. Visualizar Ranking Geral de Gaps de Ineficiencia")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opcao: ").strip()
        if opcao == "1":
            executar_pipeline_completo()
        elif opcao == "2":
            inspecionar_veiculo_interativo()
        elif opcao == "3":
            if os.path.exists("data/processed/tabela_benchmarks_grupos.csv"):
                df_b = pd.read_csv("data/processed/tabela_benchmarks_grupos.csv")
                print("\n" + df_b.to_string(index=False))
            else:
                print("Execute a opcao 1 primeiro para calcular os benchmarks.")
        elif opcao == "4":
            if os.path.exists("data/processed/frota_com_benchmark_e_ml.csv"):
                df_f = pd.read_csv("data/processed/frota_com_benchmark_e_ml.csv")
                df_r = df_f.sort_values(by="gap_percentual_custo_km", ascending=False)
                cols = ["veiculo_id", "modelo", "perfil_operacao", "custo_por_km", "benchmark_custo_km", "gap_percentual_custo_km", "diagnostico_regras"]
                print("\n" + df_r[cols].to_string(index=False))
            else:
                print("Execute a opcao 1 primeiro para calcular os gaps.")
        elif opcao == "0":
            print("Encerrando aplicacao Sem Parar.")
            break
        else:
            print("Opcao invalida. Tente novamente.")
        input("\nPressione [Enter] para continuar...")

if __name__ == "__main__":
    main()
