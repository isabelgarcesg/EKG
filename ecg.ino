#define ECG_PIN 39  // Pin analógico al que está conectado el sensor ECG

void setup() {
  Serial.begin(115200);
}

void loop() {
  int ecgValue = analogRead(ECG_PIN);  // Lee el valor analógico del sensor ECG  
  Serial.println(ecgValue);            // Envía el valor leído al monitor serial
  delay(10);                           // Aumenta la pausa para una visualización más lenta
}
