#include <Arduino_LSM6DS3.h>

float x, y, z;

void setup() {
  Serial.begin(9600); // match baud rate with Python
  while (!Serial);    // wait for serial port to connect

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.println("X, Y, Z");  // header for CSV
}

void loop() {
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    Serial.print(x, 3);
    Serial.print(", ");
    Serial.print(y, 3);
    Serial.print(", ");
    Serial.println(z, 3);
  }

  delay(1000); // read every 1 second
}
