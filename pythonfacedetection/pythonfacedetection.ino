
int facePin = 13;
int redLightPin = 12;

void setup() {
  Serial.begin(9600);
  pinMode(facePin, OUTPUT);
  pinMode(redLightPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    int data = Serial.read();
    
    if (data == 13) {
      digitalWrite(facePin, HIGH);
      digitalWrite(redLightPin, LOW);

    } else if (data == 12) {
      digitalWrite(facePin, LOW);
      digitalWrite(redLightPin, HIGH);
    }
  }
}