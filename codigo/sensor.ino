const int TRIG = 9;
const int ECHO = 10;

void setup() {
  Serial.begin(115200);

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
}

void loop() {

  // Enviar pulso ultrasónico
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG, LOW);

  // Medir el tiempo que tarda en regresar el sonido
  long tiempo = pulseIn(ECHO, HIGH);

  // Convertir tiempo a distancia en centímetros
  float distancia = tiempo * 0.0343 / 2;

  // Enviar distancia a Python
  Serial.println(distancia);

  delay(10);
}