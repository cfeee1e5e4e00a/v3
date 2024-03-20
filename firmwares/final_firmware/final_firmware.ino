#include <ACS712.h>
#include <DHT.h>
#include "EspMQTTClient.h"
#include <GyverPID.h>

#include "config.h"

#define R_OFF 1
#define R_ON 0

#define CALIBRATION_PERIOD 1000
#define MEASUREMENT_PERIOD 500
#define SWITCH_PERIOD 5000


const char* ssid = "TP-Link_4F90";
const char* password =  "NTOContest202324";
const char* mqttServer = "mqtt.cfeee1e5e4e00a.ru";
const int mqttPort = 1883;
const char* mqttUser = "nti";
const char* mqttPassword = "nti";



EspMQTTClient* client;

DHT *dhts;
ACS712 *acss;
GyverPID *pids;

typedef enum {
    CONSTANT,
    EFFECTIVE,
    TIME_DEPENDENT,
    OFF
} Mode;
Mode modes[N_ROOMS];
float setpoints[N_ROOMS];

bool relay_states[N_ROOMS*N_RELAYS];
bool rooms_states[N_ROOMS];
unsigned long int switch_timer = 0;
int heat_times[N_ROOMS];

void setup()
{

    dhts = (DHT*)malloc(N_ROOMS * sizeof(DHT));
    acss = (ACS712*)malloc(N_ROOMS * sizeof(ACS712));
    pids = (GyverPID*)malloc(N_ROOMS * sizeof(GyverPID));

    Serial.begin(115200);
    load_config();
    client = new EspMQTTClient(
        ssid,
        password,
        mqttServer,  // MQTT Broker server ip
        mqttUser,   // Can be omitted if not needed
        mqttPassword,   // Can be omitted if not needed
        config.client_id,     // Client name that uniquely identify your device
        mqttPort              // The MQTT port, default to 1883. this line can be omitted
    );

    client->enableLastWillMessage("/init", strdup((String("power,esp=") + config.client_id + " value=0").c_str()));
    client->enableDebuggingMessages(true);
    // return;

    for(int i = 0; i < N_ROOMS; i++){
        // setup dhts
        new(&dhts[i]) DHT(config.rooms[i].dht_pin, DHT11);
        dhts[i].begin();

        // setup pids
        new(&pids[i]) GyverPID(0.1, 0.05, 0.01, CALIBRATION_PERIOD);
        pids[i].setDirection(NORMAL);
        pids[i].setLimits(0, 1000);

        // setup relay pins
        for(int j = 0; j < N_RELAYS; j++){
            pinMode(config.rooms[i].relay_pins[j], OUTPUT);
            digitalWrite(config.rooms[i].relay_pins[j], R_OFF);
        }

        delay(100);

        // setup current sensors
        new(&acss[i]) ACS712(config.rooms[i].acs_pin, 3.3, 4095, 100);
        acss[i].autoMidPointDC();

        //setup current modes
        modes[i] = OFF;
    }

    
}

void onConnectionEstablished() {
    Serial.println("Connected to mqtt");
    client->publish("/init", String("power,esp=") + config.client_id + " value=1");
    for(int i = 0; i < N_ROOMS; i++){
        client->subscribe(String("/relays/")+config.rooms[i].id, [=](String msg){
            for(int r  =0; r < N_RELAYS; r++){
                digitalWrite(config.rooms[i].relay_pins[r], msg[r] - '0' ? R_ON : R_OFF);
            }
        });
    }
}

volatile float room_temps[N_ROOMS];


unsigned long last_publish = 0;


void publish_measurement(String name, int flat, float value){
    client->publish("/sensors", name+",flat="+config.rooms[flat].id+" value="+value);
}

void loop(){    
    client->loop();

    // return;
    unsigned long m = millis();
    if (m - last_publish < MEASUREMENT_PERIOD){
        return;
    }

    last_publish = m;

    for(int i = 0; i < N_ROOMS; i++){
        float temp = dhts[i].readTemperature();
        float hum = dhts[i].readHumidity();
        room_temps[i] = temp;
        float curr = acss[i].mA_DC(10)/1000.0;
        curr = max(curr, 0.0);

        publish_measurement("temp", i, temp);
        publish_measurement("humd", i, hum);
        publish_measurement("curr", i, curr);
    }

    for (int i = 0; i < N_ROOMS; i++) {
        switch_relays(i);
    }
}

int calibrate_constant_mode(int room) {
    pids[room].input = room_temps[room];
    int out = pids[room].getResultTimer();
    int t;
    if (out < 500) {
        t = out * 10; //[мс]
        relay_states[room * 2] = 1; //on
        relay_states[room * 2 + 1] = 0; //off
    } else {
        t = 2500 + (out - 500) * 10; //[мс]
        relay_states[room * 2] = 1;
        relay_states[room * 2 + 1] = 1;
    }
    return t;
}

void setup_constant_mode(int room, float setpoint) {
    modes[room] = CONSTANT;
    setpoints[room] = setpoint;
    pids[room].setpoint = setpoint;
    calibrate_constant_mode(room);

}

void switch_relays(int room) {
    float m = millis();
    if (rooms_states[room] == 0 && m - switch_timer > SWITCH_PERIOD) {
        //Начало отсчета - включаем все активные нагреватели
        switch_timer = m;
        rooms_states[room] = 1;
        for (int i = 0; i < N_ROOMS; i++) {
            for (int j = 0; j < N_RELAYS; j++) {
                if (relay_states[i * N_RELAYS + j]) {
                    digitalWrite(config.rooms[i].relay_pins[j], R_ON);
                } else {
                    digitalWrite(config.rooms[i].relay_pins[j], R_OFF);
                }
            }
        }
    } else if (rooms_states[room] == 1 && m - switch_timer > heat_times[room]) {
            if (m - switch_timer > heat_times[room]) {
                //выключаем все нагреватели в комнате
                for (int j = 0; j < N_RELAYS; j++) {
                    digitalWrite(config.rooms[room].relay_pins[j], R_OFF);
                }
        }
    }

}