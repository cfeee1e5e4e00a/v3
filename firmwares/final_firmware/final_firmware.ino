#include <ACS712.h>
#include <DHT.h>
#include "EspMQTTClient.h"
#include <GyverPID.h>

#include "config.h"

#define R_OFF 1
#define R_ON 0

#define CALIBRATION_PERIOD 1000
#define MEASUREMENT_PERIOD 500


const char* ssid = "TP-Link_4F90";
const char* password =  "NTOContest202324";
const char* mqttServer = "mqtt.cfeee1e5e4e00a.ru";
const int mqttPort = 1883;
const char* mqttUser = "nti";
const char* mqttPassword = "nti";




EspMQTTClient client;

DHT dhts[N_ROOMS];
ACS712 acss[N_ROOMS];
GyverPID pids[2];



void setup()
{
    Serial.begin(115200);
    load_config();
    client = EspMQTTClient(
        ssid,
        password,
        mqttServer,  // MQTT Broker server ip
        mqttUser,   // Can be omitted if not needed
        mqttPassword,   // Can be omitted if not needed
        config.client_id,     // Client name that uniquely identify your device
        mqttPort              // The MQTT port, default to 1883. this line can be omitted
    );

    client.enableLastWillMessage("/init", (String("power,esp=") + config.client_id + " value=0").c_str());

    for(int i = 0; i < N_ROOMS; i++){
        // setup dhts
        dhts[i] = DHT(config.rooms[i].dht_pin, DHT11);
        dhts[i].begin();

        // setup pids
        pids[i] = GyverPID(0.1, 0.05, 0.01, CALIBRATION_PERIOD);
        pids[i].setDirection(NORMAL);
        pids[i].setLimits(0, 1000);

        // setup relay pins
        for(int j = 0; j < N_RELAYS; j++){
            pinMode(config.rooms[i].relay_pins[j], OUTPUT);
            digitalWrite(config.rooms[i].relay_pins[j], R_OFF);
        }

        delay(100);

        // setup current sensors
        acss[i] = ACS712(config.rooms[i].acs_pin, 3.3, 4095, 100);
        acss[i].autoMidPointDC();
    }

    
}

void onConnectionEstablished() {
    client.publish("/init", String("power,esp=") + config.client_id + " value=1");
}

volatile float room_temps[N_ROOMS];


unsigned long last_publish = 0;


void publish_measurement(String name, int flat, float value){
    client.publish("/sensors", name+",flat="+config.rooms[flat].id+" value="+value);
}

void loop(){    
    client.loop();

    unsigned long m = millis();
    if (m - last_publish < MEASUREMENT_PERIOD){
        return;
    }

    last_publish = m;

    for(int i = 0; i < N_ROOMS; i++){
        float temp = dhts[i].readTemperature();
        float hum = dhts[i].readHumidity();
        room_temps[i] = temp;
        float curr = abs(acss[i].mA_DC(10))/1000.0;

        publish_measurement("temp", i, temp);
        publish_measurement("humd", i, hum);
        publish_measurement("curr", i, curr);
    }
}