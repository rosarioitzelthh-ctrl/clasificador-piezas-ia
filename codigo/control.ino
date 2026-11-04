
// control.ino - Semana 8
// Sensor HC-SR04 y recepcion de ordenes desde Python

const int TRIG = 9;
const int ECHO = 10;

// ======================================
// CONFIGURACION
// ======================================

void setup() {

  Serial.begin(115200);

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  digitalWrite(TRIG, LOW);

}


// ======================================
// FUNCION PARA MEDIR DISTANCIA
// ======================================

float medirDistancia() {

  // Enviar pulso ultrasonico
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG, LOW);

  // Medir tiempo de regreso del sonido
  long tiempo = pulseIn(ECHO, HIGH, 30000);

  // Si no hay lectura, regresar un valor invalido
  if (tiempo == 0) {
    return -1;
  }

  // Convertir tiempo a centimetros
  float distancia = tiempo * 0.0343 / 2;

  return distancia;
}


// ======================================
// FUNCION PARA RECIBIR ORDENES
// ======================================

void recibirOrden() {

  while (Serial.available() > 0) {

    char orden = Serial.read();

    switch (orden) {

      case 'A':
        // Pieza tapada
        Serial.println("CLASIFICACION: TAPADO");
        break;

      case 'B':
        // Pieza mal tapada
        Serial.println("CLASIFICACION: MAL_TAPADO");
        break;

      case 'C':
        // Pieza no tapada
        Serial.println("CLASIFICACION: NO_TAPADO");
        break;

      case '0':
        // Regresar a reposo
        Serial.println("SISTEMA EN REPOSO");
        break;

    }

  }

}


// ======================================
// BUCLE PRINCIPAL
// ======================================

void loop() {

  // 1. Medir distancia
  float distancia = medirDistancia();

  // 2. Enviar lectura a Python
  if (distancia > 0 && distancia <= 400) {
    Serial.println(distancia);
  }

  // 3. Revisar si Python envio una orden
  recibirOrden();

  delay(10);

}
