#include <ArduinoIoTCloud.h>              // Make sure the library is installed
#include <Arduino_ConnectionHandler.h>    // Make sure the library is installed
#include "arduino_secrets.h"              // Loads SECRET_SSID and SECRET_PASS

void onRandomTemperatureChange();

float randomTemperature;

void initProperties() {
  ArduinoCloud.addProperty(randomTemperature, READWRITE, ON_CHANGE, onRandomTemperatureChange);
}

// Use secrets defined in arduino_secrets.h
WiFiConnectionHandler ArduinoIoTPreferredConnection(SECRET_SSID, SECRET_PASS);
