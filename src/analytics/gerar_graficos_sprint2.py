#!/usr/bin/env python3
"""
Módulo de Analytics Visual e Geração de Gráficos Executivos (Sprint 2).
Produz gráficos de alta resolução para demonstrar os resultados de benchmark,
gaps de ineficiência, matriz de correlação, matriz de confusão e arquitetura da solução.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix

def configurar_estilo():
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
    plt.rcParams["axes.edgecolor"] = "#CBD5E1"
    plt.rcParams["axes.linewidth"] = 0.8
    plt.rcParams["grid.color"] = "#E2E8F0"
    plt.rcParams["grid.linestyle"] = "--"

def gerar_todos_os_graficos():
    configurar_estilo()
    os.makedirs("assets/diagramas", exist_ok=True)
    
    df_frota = pd.read_csv("data/processed/frota_com_benchmark_e_ml.csv")

    # -------------------------------------------------------------
    # Gráfico 1: Boxplots de Custo por KM por Perfil de Frota vs Benchmark
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=150)
    perfis = ["LEVE_URBANO", "MEDIO_DISTRIBUICAO", "PESADO_RODOVIARIO"]
    cores = ["#0284C7", "#0D9488", "#7C3AED"]

    dados_box = [df_frota[df_frota["perfil_operacao"] == p]["custo_por_km"] for p in perfis]
    bp = ax.boxplot(dados_box, tick_labels=["Leve Urbano\n(10 veículos)", "Médio Distribuição\n(8 veículos)", "Pesado Rodoviário\n(7 veículos)"],
                    patch_artist=True, widths=0.45)

    for patch, cor in zip(bp["boxes"], cores):
        patch.set_facecolor(cor)
        patch.set_alpha(0.75)
    for median in bp["medians"]:
        median.set_color("#1E293B")
        median.set_linewidth(2.2)

    # Adicionar pontos reais de cada veículo (jitter)
    for i, p in enumerate(perfis, 1):
        y_vals = df_frota[df_frota["perfil_operacao"] == p]["custo_por_km"]
        x_vals = np.random.normal(i, 0.04, size=len(y_vals))
        ax.scatter(x_vals, y_vals, color="#0F172A", alpha=0.8, s=40, zorder=5)

    ax.set_title("Distribuição do Custo por Quilômetro (R$/km) por Grupo Homogêneo", fontsize=13, fontweight="bold", pad=14)
    ax.set_ylabel("Custo Operacional Total por KM (R$/km)", fontsize=10, fontweight="bold")
    ax.set_xlabel("Grupo Homogêneo de Benchmark", fontsize=10, fontweight="bold")
    plt.tight_layout()
    caminho_g1 = "assets/diagramas/01_boxplot_custo_km_por_perfil_frota.png"
    plt.savefig(caminho_g1)
    plt.close()
    print(f"Gráfico 1 gerado: {caminho_g1}")

    # -------------------------------------------------------------
    # Gráfico 2: Matriz de Correlação Linear (Pearson)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.5, 6.5), dpi=150)
    cols_corr = [
        "custo_por_km", "consumo_medio_kml", "pct_combustivel",
        "pct_manutencao", "pct_pedagio", "total_anomalias_telemetria",
        "media_temp_motor_c", "media_rpm"
    ]
    nomes_corr = [
        "Custo R$/km", "Consumo km/l", "% Combustível",
        "% Manutenção", "% Pedágio", "Anomalias IoT",
        "Temp Motor (°C)", "RPM Médio"
    ]
    df_sub = df_frota[cols_corr].rename(columns=dict(zip(cols_corr, nomes_corr)))
    matriz_corr = df_sub.corr(method="pearson")

    mask = np.triu(np.ones_like(matriz_corr, dtype=bool))
    sns.heatmap(matriz_corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1,
                linewidths=0.8, linecolor="white", cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title("Matriz de Correlação de Pearson entre Variáveis de Frota e Custos", fontsize=12, fontweight="bold", pad=12)
    plt.tight_layout()
    caminho_g2 = "assets/diagramas/02_matriz_correlacao_custos_e_operacao.png"
    plt.savefig(caminho_g2)
    plt.close()
    print(f"Gráfico 2 gerado: {caminho_g2}")

    # -------------------------------------------------------------
    # Gráfico 3: Ranking de Gaps de Ineficiência por Veículo (%)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 7), dpi=150)
    df_sorted = df_frota.sort_values(by="gap_percentual_custo_km", ascending=True)

    mapa_cores = {
        "EFICIENTE": "#10B981", # Verde
        "ATENCAO": "#F59E0B",   # Âmbar
        "INEFICIENTE": "#EF4444" # Vermelho
    }
    cores_barras = [mapa_cores[cat] for cat in df_sorted["diagnostico_regras"]]

    y_pos = np.arange(len(df_sorted))
    barras = ax.barh(y_pos, df_sorted["gap_percentual_custo_km"], color=cores_barras, height=0.68, alpha=0.85)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([f"{row['veiculo_id']} ({row['modelo'][:12]})" for _, row in df_sorted.iterrows()], fontsize=8.5)
    ax.axvline(0, color="#1E293B", linewidth=1.0)
    ax.axvline(5.0, color="#F59E0B", linestyle=":", linewidth=1.2, label="Limite Atenção (+5%)")
    ax.axvline(20.0, color="#EF4444", linestyle="--", linewidth=1.2, label="Limite Ineficiência (+20%)")

    # Rótulos de porcentagem ao lado das barras
    for bar in barras:
        w = bar.get_width()
        sinal = "+" if w > 0 else ""
        ax.text(w + (0.5 if w >= 0 else -1.5), bar.get_y() + bar.get_height()/2,
                f"{sinal}{w:.1f}%", va="center", ha="left" if w >= 0 else "right",
                fontsize=7.8, fontweight="bold", color="#1E293B")

    ax.set_title("Ranking do Gap de Eficiência em Relação ao Benchmark do Grupo (%)", fontsize=12, fontweight="bold", pad=14)
    ax.set_xlabel("Desvio Percentual de Custo por KM frente à Mediana do Grupo (%)", fontsize=9.5, fontweight="bold")
    ax.legend(loc="lower right", frameon=True)
    plt.tight_layout()
    caminho_g3 = "assets/diagramas/03_ranking_gaps_ineficiencia_frota.png"
    plt.savefig(caminho_g3)
    plt.close()
    print(f"Gráfico 3 gerado: {caminho_g3}")

    # -------------------------------------------------------------
    # Gráfico 4: Matriz de Confusão do Modelo de Machine Learning
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(6.5, 5), dpi=150)
    classes = ["EFICIENTE", "ATENCAO", "INEFICIENTE"]
    cm = confusion_matrix(df_frota["diagnostico_regras"], df_frota["diagnostico_ml"], labels=classes)

    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=classes, yticklabels=classes,
                cbar=False, linewidths=1.2, linecolor="white", ax=ax, annot_kws={"size": 14, "weight": "bold"})
    ax.set_title("Matriz de Confusão: Diagnóstico Regras vs. Árvore de Decisão", fontsize=11, fontweight="bold", pad=12)
    ax.set_xlabel("Classificação Prevista pelo Modelo de ML", fontsize=9.5, fontweight="bold")
    ax.set_ylabel("Classificação Real por Regras de Negócio", fontsize=9.5, fontweight="bold")
    plt.tight_layout()
    caminho_g4 = "assets/diagramas/04_matriz_confusao_classificador_ml.png"
    plt.savefig(caminho_g4)
    plt.close()
    print(f"Gráfico 4 gerado: {caminho_g4}")

    # -------------------------------------------------------------
    # Gráfico 5: Diagrama Arquitetural da Solução Sprint 2
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=150)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7)
    ax.axis("off")

    # Cabeçalho
    ax.text(5.5, 6.6, "ARQUITETURA DA SOLUÇÃO — SPRINT 2 (INTELIGÊNCIA E DIAGNÓSTICO)",
            fontsize=13, fontweight="bold", ha="center", color="#0F172A")
    ax.text(5.5, 6.2, "Calculadora de Redução de Custos de Frota — Sem Parar Empresas (Corpay)",
            fontsize=9.5, style="italic", ha="center", color="#475569")

    # Camadas Arquiteturais
    camadas = [
        {"x": 0.5, "y": 1.2, "w": 2.2, "h": 4.6, "cor": "#E0F2FE", "borda": "#0284C7",
         "titulo": "1. FONTES E TELEMETRIA",
         "itens": ["- Cartões Combustível (CSV)", "- Tag Sem Parar (JSON)", "- Ordens Manutenção (TXT)",
                   "- Multas e Impostos (CSV)", "- Cadastro da Frota (CSV)", "",
                   "Módulo ESP32 (Wokwi):", "- Vel, RPM, Temp, Comb", "- Detecção Anomalias"]},
        
        {"x": 3.1, "y": 1.2, "w": 2.2, "h": 4.6, "cor": "#F0FDF4", "borda": "#16A34A",
         "titulo": "2. INGESTÃO & QUALIDADE",
         "itens": ["- Leitura Multiformato", "- Normalização Padrão ISO", "- Deduplicação Unívoca",
                   "- Filtro Valores Negativos", "- Tratamento Chaves Órfãs", "- Imputação de Consumo",
                   "", "Base Consolidada:", "- 25 Veículos Auditados"]},
        
        {"x": 5.7, "y": 1.2, "w": 2.2, "h": 4.6, "cor": "#FEF3C7", "borda": "#D97706",
         "titulo": "3. BENCHMARK & GAPS",
         "itens": ["- 3 Grupos Homogêneos:", "  * Leve Urbano", "  * Médio Distribuição", "  * Pesado Rodoviário",
                   "", "- Mediana & Quartis (Q1/Q3)", "- Custo por KM (R$/km)", "- Consumo Médio (km/l)",
                   "- Cálculo do Gap (%)"]},

        {"x": 8.3, "y": 1.2, "w": 2.2, "h": 4.6, "cor": "#F3E8FF", "borda": "#9333EA",
         "titulo": "4. INTELIGÊNCIA & ML",
         "itens": ["- Diagnóstico por Regras", "  (Eficiente/Atenção/Inefic)", "",
                   "- Árvore de Decisão (ML)", "- Random Forest Ensemble", "- Ir Além: Rede Neural MLP",
                   "", "- Concordância: 100%", "- Ranking de Ineficiência"]}
    ]

    for c in camadas:
        rect = plt.Rectangle((c["x"], c["y"]), c["w"], c["h"], facecolor=c["cor"],
                             edgecolor=c["borda"], linewidth=1.5, linestyle="-", zorder=2)
        ax.add_patch(rect)
        ax.text(c["x"] + c["w"]/2, c["y"] + c["h"] - 0.35, c["titulo"],
                fontsize=9.2, fontweight="bold", ha="center", color=c["borda"], zorder=4)
        
        texto_corpo = "\n".join(c["itens"])
        ax.text(c["x"] + 0.15, c["y"] + c["h"] - 0.75, texto_corpo,
                fontsize=7.8, color="#1E293B", va="top", zorder=4)

    # Setas de conexão entre blocos
    setas = [(2.7, 3.5, 3.1, 3.5), (5.3, 3.5, 5.7, 3.5), (7.9, 3.5, 8.3, 3.5)]
    for x1, y1, x2, y2 in setas:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#334155", lw=2.2))

    # Barra inferior de entrega e valor ao gestor
    rect_rod = plt.Rectangle((0.5, 0.2), 10.0, 0.75, facecolor="#F8FAFC", edgecolor="#64748B",
                             linewidth=1.0, zorder=2)
    ax.add_patch(rect_rod)
    ax.text(5.5, 0.57, "RESPOSTA AO GESTOR DE FROTA COM EVIDÊNCIAS", fontsize=9.2, fontweight="bold",
            ha="center", color="#0F172A", zorder=4)
    ax.text(5.5, 0.35, "Quanto a operação custa (TCO detalhado por km) | Onde está menos eficiente (Ranking de desvios + Telemetria de anomalias)",
            fontsize=7.8, ha="center", color="#475569", zorder=4)

    plt.tight_layout()
    caminho_g5 = "assets/diagramas/05_arquitetura_solucao_sprint2.png"
    plt.savefig(caminho_g5)
    plt.close()
    print(f"Gráfico 5 (Diagrama) gerado: {caminho_g5}")

if __name__ == "__main__":
    gerar_todos_os_graficos()
