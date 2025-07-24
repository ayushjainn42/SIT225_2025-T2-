// Arduino Sketch

const int ledPin = 13;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
  while (!Serial); // wait for serial port to connect
}

void loop() {
  if (Serial.available() > 0) {
    int blinkCount = Serial.parseInt();

    // Blink LED
    for (int i = 0; i < blinkCount; i++) {
      digitalWrite(ledPin, HIGH);
      delay(500);
      digitalWrite(ledPin, LOW);
      delay(500);
    }

    // Send a random number back as delay
    int waitTime = random(1, 6); // 1 to 5 seconds
    Serial.println(waitTime);
  }
}

}
