//you can ignore this part, just for the temperature sensor
#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin(); //start the temp reading (agian only for temperature sensor
}

void loop() {
  //read the temperature and humidity (temperature sensor specific code)
  float h = dht.readHumidity(); //read humidity
  float t = dht.readTemperature(); //read temperature (C)
 
  // check if returns are valid
  if (isnan(t) || isnan(h)) {
    Serial.println("Failed to read from DHT");
  } else {  //if it read correctly
    Serial.print(h);     //humidity
    Serial.print(" \t"); //tab
    Serial.println(t);   //temperature (C)
  }
}
