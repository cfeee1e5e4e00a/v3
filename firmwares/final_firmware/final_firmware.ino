#include <ACS712.h>
#include <DHT.h>
#include "EspMQTTClient.h"
#include <GyverPID.h>

#include "config.h"

#define R_OFF 1
#define R_ON 0

// #define CALIBRATION_PERIOD 1000
#define MEASUREMENT_PERIOD 500
#define SWITCH_PERIOD 1000


const char* ssid = "tochka_dostupa";
const char* password =  "ntisosatnampizdets";
const char* mqttServer = "mqtt.cfeee1e5e4e00a.ru";
const int mqttPort = 1883;
const char* mqttUser = "nti";
const char* mqttPassword = "nti";



EspMQTTClient* client;

DHT *dhts;
ACS712 *acss;
GyverPID *pids;

typedef enum {
    CONSTANT = 0,
    CONSTANT_ECONOMY,
    PROFILE,
    OFF
} Mode;

// TODO: do not hardcode modes
Mode modes[N_ROOMS];
float setpoints[N_ROOMS];

bool relay_states[N_ROOMS*N_RELAYS];
bool rooms_states[N_ROOMS];
unsigned long int switch_timer = 0;
int heat_times[N_ROOMS];

void setup_constant_mode(int room, float setpoint);
void switch_relays(int room);

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
        float k = 100;
        float kp = 1000;
        new(&pids[i]) GyverPID(1000, 0, 0, SWITCH_PERIOD);
        pids[i].setDirection(NORMAL);
        pids[i].setLimits(0, SWITCH_PERIOD*2);

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
        setup_off_mode(i);
    }


    // setup_constant_mode(0, 50);
}

void onConnectionEstablished() {
    Serial.println("Connected to mqtt");
    client->publish("/init", String("power,esp=") + config.client_id + " value=1");
    for(int i = 0; i < N_ROOMS; i++){
        // client->subscribe(String("/relays/")+config.rooms[i].id, [=](String msg){
        //     for(int r  =0; r < N_RELAYS; r++){
        //         digitalWrite(config.rooms[i].relay_pins[r], msg[r] - '0' ? R_ON : R_OFF);
        //     }
        // });

        client->subscribe(String("/mode/") + config.rooms[i].id, [=](String msg){
            Serial.println("Changing mode...");
            int space1 = msg.indexOf(' ');
            int space2 =  msg.indexOf(' ', space1 + 1); 
            int mode = msg.toInt();
            int arg1 = atoi(msg.c_str() + space1 + 1);
            switch (mode)
            {
            case OFF:
                setup_off_mode(i);
                break;
            case CONSTANT:
                setup_constant_mode(i, arg1);
                break;
            default:
                Serial.printf("Unsupported mode for room %d: %d\n", i, modes[i]);
                break;
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
    // TODO: uncomment this
    client->loop();


    


    // send new data
    unsigned long m = millis();
    if (m - last_publish > MEASUREMENT_PERIOD){
        last_publish = m;

        for(int i = 0; i < N_ROOMS; i++){
            float temp = dhts[i].readTemperature();
            float hum = dhts[i].readHumidity();
            room_temps[i] = temp;
            float curr = abs(acss[i].mA_DC(10))/1000.0;

            publish_measurement("temp", i, temp);
            publish_measurement("humd", i, hum);
            publish_measurement("curr", i, curr);

            publish_measurement("mode", i, modes[i]);
            publish_measurement("set_temp", i, setpoints[i]);
            publish_measurement("pid_out", i, pids[i].output);
        }
    }

    

    for (int i = 0; i < N_ROOMS; i++) {
        switch (modes[i])
        {
        case OFF:
            run_off_mode(i);
            break;
        case CONSTANT:
            run_constant_mode(i);
            break;
        default:
            Serial.printf("Unsupported mode for room %d: %d\n", i, modes[i]);
            break;
        }

        switch_relays(i);
    }
    



    // calibrate_constant_mode(0);
    // switch_relays(0);
    
}

int run_constant_mode(int room) {
    pids[room].input = room_temps[room];
    int out = pids[room].getResultTimer();
    // Serial.println(String("Temp = ") + room_temps[room] + ", pid_out = " + out);
    int t;
    // if (out < SWITCH_PERIOD) {
    //     t = out; //[мс]
    //     relay_states[room * 2] = 1; //on
    //     relay_states[room * 2 + 1] = 0; //off
    // } else  {
    //     t = out/2; //[мс]
    //     relay_states[room * 2] = 1;
    //     relay_states[room * 2 + 1] = 1;
    // }
    t = out/2;
    relay_states[room * 2] = 1;
    relay_states[room * 2 + 1] = 1;
    if(out < 5){
        t = 10;
        relay_states[room * 2] = 0;
        relay_states[room * 2 + 1] = 0;
    }
    heat_times[room] = t;
    return t;
}

void run_off_mode(int room){

}

void setup_constant_mode(int room, float setpoint) {
    modes[room] = CONSTANT;
    setpoints[room] = setpoint;
    pids[room].setpoint = setpoint;
    pids[room].integral = 0;
}

void setup_off_mode(int room){
    modes[room] = OFF;
    for(int i = 0; i < N_RELAYS; i++){
        relay_states[room * N_RELAYS + i] = 0;
    }
    heat_times[room] = 0;
    rooms_states[room] = 0;
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
            rooms_states[room] = 0;
            if (m - switch_timer > heat_times[room]) {
                //выключаем все нагреватели в комнате
                for (int j = 0; j < N_RELAYS; j++) {
                    digitalWrite(config.rooms[room].relay_pins[j], R_OFF);
                }
        }
    }

}