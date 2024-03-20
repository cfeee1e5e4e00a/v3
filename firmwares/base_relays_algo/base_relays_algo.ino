#include <GyverPID.h>
#include <ACS712.h>
#include <DHT.h>
#include "EspMQTTClient.h"

//номер еспшки
#define CLIENT_ID "1"
#define FLAT_NO_1 "1"
#define FLAT_NO_2 "2"

#define CALIBRATION_PERIOD 1000

float flat_1_setpoint_temp = 25.0;
float flat_2_setpoint_temp = 27.0;
float tau = 2.0;

typedef enum {
    CONSTANT,
    EFFECTIVE,
    TIME_DEPENDENT
} Mode;
Mode flat_1_mode;
Mode flat_2_mode;

//кв. 1, реле 1; кв. 1, реле 2; кв. 2 реле 1; кв. 2, реле 1.
int relay_pins[4] = {5, 18, 19, 21};
bool relay_states[4] = {0, 0, 0, 0}; //все выкл

#define PERIOD 5000

#define DHT_1 27
#define DHT_2 26
#define CURR_1 35
#define CURR_2 34

DHT dht_1(DHT_1, DHT11);
DHT dht_2(DHT_2, DHT11);
ACS712  acs1(CURR_1, 3.3, 4095, 100);
ACS712  acs2(CURR_2, 3.3, 4095, 100);

GyverPID regulator(0.1, 0.05, 0.01, CALIBRATION_PERIOD);

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

    flat_1_mode = CONSTANT;
    flat_2_mode = CONSTANT;

    regulator.setDirection(NORMAL);
    regulator.setLimits(0, 1000);
    regulator.setpoint = flat_1_setpoint_temp;

}

unsigned long last_publish = 0;
unsigned long last_calibrated = 0;
unsigned long last_switched = 0;

int t_heat_1 = 2500;
int pid_1 = 50;
bool is_on_1 = 0;

double c1, c2;
double t1, t2;
void loop()
{
	client.loop();

    t1 = dht_1.readTemperature();
    t2 = dht_2.readTemperature();

    unsigned long m = millis();
    //SENSORS POLL AND PUBLISH 
    if(m - last_publish > PERIOD){
        last_publish = m;
        //temp 1
        client.publish("/sensors", String("temp,flat=" + String(FLAT_NO_1) + String(" value=")) + t1);
        //temp 2
        client.publish("/sensors", String("temp,flat=" + String(FLAT_NO_2) + String(" value=")) + t2);
        // humidity 1
        client.publish("/sensors", String("humd,flat=" + String(FLAT_NO_1) + String(" value=")) + dht_1.readHumidity());
        // humidity 2
        client.publish("/sensors", String("humd,flat=" + String(FLAT_NO_2) + String(" value=")) + dht_2.readHumidity()); 
        // CURR 1
        c1 = acs1.mA_DC()/1000.0;
        client.publish("/sensors", String("curr,flat=" + String(FLAT_NO_1) + String(" value=")) + max(c1, 0.0));
        // CURR 2
        c2 = acs2.mA_DC()/1000.0;
        client.publish("/sensors", String("curr,flat=" + String(FLAT_NO_2) + String(" value=")) + max(c2, 0.0));
    }

    //SETTING HEATING PERIOD DEPENDING ON STRATEGY
    if (m - last_calibrated > CALIBRATION_PERIOD) {
        last_calibrated = m;
        if (flat_1_mode == CONSTANT) {
            regulator.input = t1;
            pid1 = regulator.getResultTimer();
            if (pid1 < 500) {
                t_heat_1 = pid1 * 10 //[мс]
                relay_states[0] = 1; //on
                relay_states[1] = 0; //off
            } else {
                t_heat_1 = 2500 + (x - 500) * 10
                relay_states[0] = 1;
                relay_states[1] = 1;
            }
        }
    }

    //SWITCHING RELAYS DEPENDING ON PERIODS
    m = millis();
    if (m - last_switched < t_heat_1 && is_on_1 == 0) {
        //Включаем активные реле
        for (int i = 0; i++; i<2) {
            if (relay_states[i]) { 
                digitalWrite(relay_pins[i], 0); 
                } else {
                digitalWrite(relay_pins[i], 1);
            }
        }
        is_on_1 = 1;
    } else if (m - last_switched > t_heat_1 && m - last_switched < 5000 && is_on_1 == 1) {
        //Выключаем все реле
        digitalWrite(relay_pins[0], 1);
        digitalWrite(relay_pins[1], 1);
        is_on_1 = 0;
    } else if (m - last_switched > 5000) {
        last_switched = m;
    }
}