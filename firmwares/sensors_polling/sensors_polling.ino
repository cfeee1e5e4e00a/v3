#include <ACS712.h>
#include <DHT.h>
#include "EspMQTTClient.h"

//номер еспшки
#define CLIENT_ID "1"
#define FLAT_NO_1 "1"
#define FLAT_NO_2 "2"

//кв. 1, реле 1; кв. 1, реле 2; кв. 2 реле 1; кв. 2, реле 1.
int relay_pins[4] = {5, 18, 19, 21};

#define PERIOD 5000

#define DHT_1 27
#define DHT_2 26
#define CURR_1 35
#define CURR_2 34

DHT dht_1(DHT_1, DHT11);
DHT dht_2(DHT_2, DHT11);
ACS712  acs1(CURR_1, 3.3, 4095, 100);
ACS712  acs2(CURR_2, 3.3, 4095, 100);

const char* ssid = "TP-Link_4F90";
const char* password =  "NTOContest202324";
const char* mqttServer = "mqtt.cfeee1e5e4e00a.ru";
const int mqttPort = 1883;
const char* mqttUser = "nti";
const char* mqttPassword = "nti";

EspMQTTClient client(
  ssid,
  password,
  mqttServer,  // MQTT Broker server ip
  "nti",   // Can be omitted if not needed
  "nti",   // Can be omitted if not needed
  CLIENT_ID,     // Client name that uniquely identify your device
  mqttPort              // The MQTT port, default to 1883. this line can be omitted
);

void onConnectionEstablished() {
    client.publish("/init", String("privet ya esp ") + String(CLIENT_ID));
}

void setup()
{
    //digital
    for (int i = 0; i < 4; i++){
        pinMode(relay_pins[i], OUTPUT);
        digitalWrite(relay_pins[i], 1);
    }
    delay(100);

    acs1.autoMidPointDC();
    acs2.autoMidPointDC();

    pinMode(DHT_1, INPUT);
    pinMode(DHT_2, INPUT);
    //analog
    pinMode(CURR_1, INPUT);
    pinMode(CURR_2, INPUT);

    Serial.begin(115200);
    dht_1.begin();
    dht_2.begin();
}

unsigned long last_publish = 0;

void loop()
{
	client.loop();
    Serial.println(dht_1.readTemperature());
    unsigned long m = millis();

    //SENSORS POLL AND PUBLISH 
    if(m - last_publish > PERIOD){
        last_publish = m;
        //temp 1
        client.publish("/sensors", String("temp,flat=" + String(FLAT_NO_1) + String(" value=")) + dht_1.readTemperature());
        //temp 2
        client.publish("/sensors", String("temp,flat=" + String(FLAT_NO_2) + String(" value=")) + dht_2.readTemperature());
        // humidity 1
        client.publish("/sensors", String("humd,flat=" + String(FLAT_NO_1) + String(" value=")) + dht_1.readHumidity());
        // humidity 2
        client.publish("/sensors", String("humd,flat=" + String(FLAT_NO_2) + String(" value=")) + dht_2.readHumidity()); 
        // CURR 1
        client.publish("/sensors", String("curr,flat=" + String(FLAT_NO_1) + String(" value=")) + acs1.mA_DC()/1000.0);
        // CURR 2
        client.publish("/sensors", String("curr,flat=" + String(FLAT_NO_2) + String(" value=")) + acs2.mA_DC()/1000.0);
    }

    //RELAY ALGO
    
}