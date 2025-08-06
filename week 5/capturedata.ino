#include <Arduino_LSM6DS3.h>

void setup() {
  Serial.begin(9600);
  while (!Serial);  // Wait for serial to initialize
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  Serial.println("Gyroscope initialized!");
}

void loop() {
  float x, y, z;

  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(x, y, z);
    Serial.print(x, 2);
    Serial.print(",");
    Serial.print(y, 2);
    Serial.print(",");
    Serial.println(z, 2);
  }

  delay(100); // 10 Hz (adjust as needed)
}


