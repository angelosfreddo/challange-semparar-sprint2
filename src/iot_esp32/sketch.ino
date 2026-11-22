/*
 * ==============================================================================
 * FIAP - GRADUAÇÃO EM INTELIGÊNCIA ARTIFICIAL
 * CHALLENGE SEM PARAR EMPRESAS (CORPAY) - SPRINT 2
 * MÓDULO: TELEMETRIA VEICULAR E DETECÇÃO DE ANOMALIAS DE BORDA (ESP32)
 *
 * Aluno: Angelo Guilherme Sfreddo (RM: 566580) - Turma: 1TIAO
 *
 * Arquitetura de Borda:
 *   - Microcontrolador: ESP32 DevKit V4
 *   - Entradas Analógicas:
 *       GPIO 34: Velocidade do Veículo (0 a 140 km/h)
 *       GPIO 35: Rotação do Motor / RPM (800 a 4500 RPM)
 *       GPIO 32: Temperatura do Motor (60 a 130 °C)
 *       GPIO 33: Nível de Combustível (0 a 100 %)
 *   - Entrada Digital:
 *       GPIO 27: Botão seletor de Veículo (V01 a V05) com interrupção
 *   - Atuadores e Sinalizadores:
 *       GPIO 2:  LED Verde (Operação Normal / Eficiente)
 *       GPIO 4:  LED Amarelo (Atenção / Limite Operacional)
 *       GPIO 5:  LED Vermelho (Anomalia Crítica / Ineficiência Severa)
 *       GPIO 18: Buzzer Piezoelétrico (Alarme Acústico em Anomalia Crítica)
 *       I2C (SDA 21, SCL 22): Display LCD 16x2 (Endereço 0x27)
 *   - Comunicação:
 *       Serial UART (115200 bps) emitindo telemetria padronizada em CSV
 * ==============================================================================
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Definição de Pinos Analógicos (ADC1)
#define PIN_VELOCIDADE 34
#define PIN_RPM 35
#define PIN_TEMP_MOTOR 32
#define PIN_COMBUSTIVEL 33

// Definição de Pinos Digitais
#define PIN_BOTAO_VEICULO 27
#define PIN_LED_VERDE 2
#define PIN_LED_AMARELO 4
#define PIN_LED_VERMELHO 5
#define PIN_BUZZER 18

// Inicialização do Display LCD 16x2 (I2C)
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Identificadores de Veículos monitorados
const char* VEICULOS[] = {"SP-V01", "SP-V02", "SP-V03", "SP-V04", "SP-V05"};
const int TOTAL_VEICULOS = 5;
volatile int indiceVeiculoAtual = 0;
volatile unsigned long ultimoDebounceBotao = 0;
const unsigned long TEMPO_DEBOUNCE_MS = 250;

// Temporização de Telemetria
unsigned long ultimoEnvioTelemetria = 0;
const unsigned long INTERVALO_TELEMETRIA_MS = 2000; // Envio a cada 2 segundos

// Interrupção para alternar veículo monitorado
void IRAM_ATTR alternarVeiculo() {
  unsigned long agora = millis();
  if (agora - ultimoDebounceBotao > TEMPO_DEBOUNCE_MS) {
    indiceVeiculoAtual = (indiceVeiculoAtual + 1) % TOTAL_VEICULOS;
    ultimoDebounceBotao = agora;
  }
}

void setup() {
  Serial.begin(115200);
  delay(500);

  // Configuração dos pinos digitais
  pinMode(PIN_BOTAO_VEICULO, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PIN_BOTAO_VEICULO), alternarVeiculo, FALLING);

  pinMode(PIN_LED_VERDE, OUTPUT);
  pinMode(PIN_LED_AMARELO, OUTPUT);
  pinMode(PIN_LED_VERMELHO, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);

  digitalWrite(PIN_LED_VERDE, LOW);
  digitalWrite(PIN_LED_AMARELO, LOW);
  digitalWrite(PIN_LED_VERMELHO, LOW);
  digitalWrite(PIN_BUZZER, LOW);

  // Inicialização do LCD
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Sem Parar Frotas");
  lcd.setCursor(0, 1);
  lcd.print("Telemetria Borda");
  delay(1500);
  lcd.clear();

  // Cabeçalho da Telemetria Serial em CSV
  Serial.println("==========================================================================================");
  Serial.println("INICIALIZACAO DO MODULO DE BORDA IOT - TELEMETRIA E DETECCAO DE ANOMALIAS SEM PARAR");
  Serial.println("Aluno: Angelo Guilherme Sfreddo (RM566580) - Turma: 1TIAO");
  Serial.println("Formato dos dados transmitidos (CSV):");
  Serial.println("timestamp_ms,veiculo_id,velocidade_kmh,rpm,temperatura_motor_c,combustivel_pct,status_operacional,alerta_ativo,codigo_anomalia");
  Serial.println("==========================================================================================");
}

void loop() {
  unsigned long agora = millis();

  if (agora - ultimoEnvioTelemetria >= INTERVALO_TELEMETRIA_MS) {
    ultimoEnvioTelemetria = agora;

    // Leitura das entradas analógicas (ADC 12 bits: 0 a 4095)
    int adcVel = analogRead(PIN_VELOCIDADE);
    int adcRpm = analogRead(PIN_RPM);
    int adcTemp = analogRead(PIN_TEMP_MOTOR);
    int adcComb = analogRead(PIN_COMBUSTIVEL);

    // Mapeamento para grandezas de engenharia veicular
    float velocidade = (float)adcVel * (140.0 / 4095.0);          // 0 a 140 km/h
    int rpm = 800 + (int)((float)adcRpm * (3700.0 / 4095.0));     // 800 a 4500 RPM
    float tempMotor = 60.0 + (float)adcTemp * (70.0 / 4095.0);    // 60 a 130 °C
    float combustivel = (float)adcComb * (100.0 / 4095.0);        // 0 a 100 %

    // Regras de Detecção de Anomalias Operacionais
    String statusOperacional = "NORMAL";
    int alertaAtivo = 0;
    String codigoAnomalia = "NENHUMA";
    bool alarmeSonoro = false;

    // Verificação de Limites Críticos
    if (tempMotor >= 105.0) {
      statusOperacional = "CRITICO";
      alertaAtivo = 1;
      codigoAnomalia = "SUPERAQUECIMENTO_MOTOR";
      alarmeSonoro = true;
    } else if (rpm >= 3800) {
      statusOperacional = "CRITICO";
      alertaAtivo = 1;
      codigoAnomalia = "ROTACAO_EXCESSIVA";
      alarmeSonoro = true;
    } else if (velocidade >= 115.0) {
      statusOperacional = "CRITICO";
      alertaAtivo = 1;
      codigoAnomalia = "EXCESSO_VELOCIDADE";
      alarmeSonoro = true;
    }
    // Verificação de Limites de Atenção
    else if (tempMotor >= 98.0 || rpm >= 3100 || velocidade >= 95.0 || combustivel <= 15.0) {
      statusOperacional = "ATENCAO";
      alertaAtivo = 1;
      if (combustivel <= 15.0) {
        codigoAnomalia = "NIVEL_BAIXO_COMBUSTIVEL";
      } else if (tempMotor >= 98.0) {
        codigoAnomalia = "TEMPERATURA_ELEVADA";
      } else if (rpm >= 3100) {
        codigoAnomalia = "ROTACAO_ELEVADA";
      } else {
        codigoAnomalia = "VELOCIDADE_ELEVADA";
      }
    }

    // Controle dos Atuadores e Sinalizadores
    if (statusOperacional == "CRITICO") {
      digitalWrite(PIN_LED_VERDE, LOW);
      digitalWrite(PIN_LED_AMARELO, LOW);
      digitalWrite(PIN_LED_VERMELHO, HIGH);
      tone(PIN_BUZZER, 1200, 250);
    } else if (statusOperacional == "ATENCAO") {
      digitalWrite(PIN_LED_VERDE, LOW);
      digitalWrite(PIN_LED_AMARELO, HIGH);
      digitalWrite(PIN_LED_VERMELHO, LOW);
      noTone(PIN_BUZZER);
    } else {
      digitalWrite(PIN_LED_VERDE, HIGH);
      digitalWrite(PIN_LED_AMARELO, LOW);
      digitalWrite(PIN_LED_VERMELHO, LOW);
      noTone(PIN_BUZZER);
    }

    const char* veiculoAtual = VEICULOS[indiceVeiculoAtual];

    // Atualização da Interface Visual do Motorista (LCD 16x2)
    lcd.setCursor(0, 0);
    lcd.print(veiculoAtual);
    lcd.print(" ");
    lcd.print((int)velocidade);
    lcd.print("km/h ");
    lcd.print((int)tempMotor);
    lcd.print("C  ");

    lcd.setCursor(0, 1);
    lcd.print("RPM:");
    lcd.print(rpm);
    lcd.print(" ");
    if (statusOperacional == "CRITICO") {
      lcd.print("!CRIT!");
    } else if (statusOperacional == "ATENCAO") {
      lcd.print("!ATEN!");
    } else {
      lcd.print("OK    ");
    }

    // Transmissão da Telemetria Serial Formatada em CSV
    Serial.print(agora);
    Serial.print(",");
    Serial.print(veiculoAtual);
    Serial.print(",");
    Serial.print(velocidade, 1);
    Serial.print(",");
    Serial.print(rpm);
    Serial.print(",");
    Serial.print(tempMotor, 1);
    Serial.print(",");
    Serial.print(combustivel, 1);
    Serial.print(",");
    Serial.print(statusOperacional);
    Serial.print(",");
    Serial.print(alertaAtivo);
    Serial.print(",");
    Serial.println(codigoAnomalia);
  }
}

