#include <Arduino_LSM6DS3.h>  
const float CRASH_THRESHOLD = 0.8; // g, low for testing
const unsigned long CRASH_DURATION = 1000; // keep crash HIGH for 1 second
unsigned long crashStartTime = 0;
int crash = 0;
void setup() {
  Serial.begin(115200);
  while (!Serial);
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  Serial.println("Arduino Crash Detection Started");
}
void loop() {
  float ax, ay, az;
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(ax, ay, az);
    float g = sqrt(ax*ax + ay*ay + az*az)/9.81;

    // Detect crash
    if (g > CRASH_THRESHOLD) {
      crash = 1;
      crashStartTime = millis();
    }
    // Keep crash HIGH for CRASH_DURATION
    if (crash == 1 && (millis() - crashStartTime > CRASH_DURATION)) {
      crash = 0;
    }
    // Send data to Python
    Serial.print(ax); Serial.print(",");
    Serial.print(ay); Serial.print(",");
    Serial.print(az); Serial.print(",");
    Serial.println(crash);
    delay(50); // faster update
  }
}


