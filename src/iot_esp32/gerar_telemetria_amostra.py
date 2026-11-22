#!/usr/bin/env python3
"""
Módulo gerador de telemetria simulada ESP32 (Wokwi) para a frota Sem Parar.
Gera leituras representativas em conformidade exata com o firmware sketch.ino.
"""

import os
import random
import pandas as pd
import numpy as np

def gerar_telemetria_frota(num_registros=5000, seed=42):
    random.seed(seed)
    np.random.seed(seed)

    veiculos = [f"SP-V{i:02d}" for i in range(1, 26)] # 25 veículos da frota
    
    registros = []
    tempo_base_ms = 1000

    for i in range(num_registros):
        veic = random.choice(veiculos)
        tempo_base_ms += random.randint(1500, 3000)

        # 88% operação normal, 8% atenção, 4% crítica/anômala
        tipo_comportamento = np.random.choice(["NORMAL", "ATENCAO", "CRITICO"], p=[0.88, 0.08, 0.04])

        if tipo_comportamento == "NORMAL":
            velocidade = round(float(np.random.normal(65, 15)), 1)
            velocidade = max(0.0, min(90.0, velocidade))
            rpm = int(np.random.normal(2100, 300))
            rpm = max(800, min(2900, rpm))
            temp_motor = round(float(np.random.normal(87, 4)), 1)
            temp_motor = max(75.0, min(94.0, temp_motor))
            combustivel = round(float(np.random.uniform(25.0, 95.0)), 1)
            status = "NORMAL"
            alerta = 0
            codigo_anomalia = "NENHUMA"

        elif tipo_comportamento == "ATENCAO":
            subtipo = random.choice(["RPM_ALTO", "VEL_ALTA", "TEMP_ALTA", "COMB_BAIXO"])
            if subtipo == "RPM_ALTO":
                velocidade = round(float(np.random.uniform(70, 92)), 1)
                rpm = int(np.random.uniform(3100, 3600))
                temp_motor = round(float(np.random.uniform(90, 97)), 1)
                combustivel = round(float(np.random.uniform(20, 80)), 1)
                codigo_anomalia = "ROTACAO_ELEVADA"
            elif subtipo == "VEL_ALTA":
                velocidade = round(float(np.random.uniform(95, 110)), 1)
                rpm = int(np.random.uniform(2800, 3400))
                temp_motor = round(float(np.random.uniform(88, 96)), 1)
                combustivel = round(float(np.random.uniform(20, 80)), 1)
                codigo_anomalia = "VELOCIDADE_ELEVADA"
            elif subtipo == "TEMP_ALTA":
                velocidade = round(float(np.random.uniform(50, 85)), 1)
                rpm = int(np.random.uniform(2200, 3200))
                temp_motor = round(float(np.random.uniform(98, 104)), 1)
                combustivel = round(float(np.random.uniform(20, 80)), 1)
                codigo_anomalia = "TEMPERATURA_ELEVADA"
            else:
                velocidade = round(float(np.random.uniform(40, 80)), 1)
                rpm = int(np.random.uniform(1800, 2600))
                temp_motor = round(float(np.random.uniform(84, 92)), 1)
                combustivel = round(float(np.random.uniform(5, 14.9)), 1)
                codigo_anomalia = "NIVEL_BAIXO_COMBUSTIVEL"
            status = "ATENCAO"
            alerta = 1

        else: # CRITICO
            subtipo = random.choice(["SUPERAQUECIMENTO", "ROTACAO_EXCESSIVA", "EXCESSO_VELOCIDADE"])
            if subtipo == "SUPERAQUECIMENTO":
                velocidade = round(float(np.random.uniform(60, 100)), 1)
                rpm = int(np.random.uniform(2800, 3900))
                temp_motor = round(float(np.random.uniform(105.1, 122.0)), 1)
                combustivel = round(float(np.random.uniform(15, 70)), 1)
                codigo_anomalia = "SUPERAQUECIMENTO_MOTOR"
            elif subtipo == "ROTACAO_EXCESSIVA":
                velocidade = round(float(np.random.uniform(75, 115)), 1)
                rpm = int(np.random.uniform(3850, 4400))
                temp_motor = round(float(np.random.uniform(95, 104)), 1)
                combustivel = round(float(np.random.uniform(15, 70)), 1)
                codigo_anomalia = "ROTACAO_EXCESSIVA"
            else:
                velocidade = round(float(np.random.uniform(115.1, 138.0)), 1)
                rpm = int(np.random.uniform(3400, 4200))
                temp_motor = round(float(np.random.uniform(92, 103)), 1)
                combustivel = round(float(np.random.uniform(15, 70)), 1)
                codigo_anomalia = "EXCESSO_VELOCIDADE"
            status = "CRITICO"
            alerta = 1

        registros.append({
            "timestamp_ms": tempo_base_ms,
            "veiculo_id": veic,
            "velocidade_kmh": velocidade,
            "rpm": rpm,
            "temperatura_motor_c": temp_motor,
            "combustivel_pct": combustivel,
            "status_operacional": status,
            "alerta_ativo": alerta,
            "codigo_anomalia": codigo_anomalia
        })

    df = pd.DataFrame(registros)
    os.makedirs("data/telemetria", exist_ok=True)
    caminho_saida = "data/telemetria/telemetria_esp32_amostra.csv"
    df.to_csv(caminho_saida, index=False)
    print(f"Telemetria gerada com sucesso: {len(df)} registros em {caminho_saida}")
    return df

if __name__ == "__main__":
    gerar_telemetria_frota()

