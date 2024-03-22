#include <ACS712.h>
#include <DHT.h>
#include "EspMQTTClient.h"
#include <GyverPID.h>

#include "config.h"

#define R_OFF 1
#define R_ON 0

// #define CALIBRATION_PERIOD 1000
#define MEASUREMENT_PERIOD 500
#define PUBLISH_PERIOD 5000
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

float trend_target_temps[N_ROOMS];
float trend_target_times[N_ROOMS];
float trend_start_times[N_ROOMS];
float trend_start_temps[N_ROOMS];


void setup_constant_mode(int room, float setpoint);
void switch_relays(int room);

bool is_rising[N_ROOMS];

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
    //__________________TEST PID___________________
    //pids[0] = GyverPID(800, 5, 0, SWITCH_PERIOD);
    //pids[0].setDirection(NORMAL);
    //pids[0].setLimits(0, SWITCH_PERIOD*2);

    // setup_constant_mode(0, 50);
}

void onConnectionEstablished() {
    Serial.println("Connected to mqtt");
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
            case CONSTANT_ECONOMY:
                setup_constant_mode(i, arg1);
                break;
            case PROFILE:
               setup_trend_mode(i, atof(msg.c_str() + space1 + 1), atoi(msg.c_str() + space2 + 1));
               break;
            default:
                Serial.printf("Unsupported mode for room %d: %d\n", i, modes[i]);
                break;
            }
        });
    }
    client->publish(String("/startup/") + config.rooms[0].id, "1");
    client->publish(String("/startup/") + config.rooms[1].id, "1");
}

volatile float room_temps[N_ROOMS];


unsigned long last_publish = 0;
unsigned long last_measured = 0;


void publish_measurement(String name, int flat, float value){
    client->publish("/sensors", name+",flat="+config.rooms[flat].id+" value="+value);
}

float t;

void loop(){    
    // TODO: uncomment this
    client->loop();

    // send new data
    unsigned long m = millis();

    if (m - last_measured > MEASUREMENT_PERIOD) {
        last_measured = m;
        for(int i = 0; i < N_ROOMS; i++) {
            t = dhts[i].readTemperature();
            if (t - room_temps[i] > 0) {
                is_rising[i] = 1;
            } else if (t - room_temps[i] < 0){
                is_rising[i] = 0;
            }
            room_temps[i] = t;
        }
    }
    if (m - last_publish > PUBLISH_PERIOD){
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
        case CONSTANT_ECONOMY:
            run_constant_mode(i);
            break;
        case PROFILE:
            run_trend_mode(i);
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
    //-----------------ПОМЕНЯЛА УСЛОВИЕ 
    float threshold = (setpoints[room]/10) * 2;
    if (setpoints[room] > 45) {
        threshold = 4.5;
    }
    if (modes[room] == PROFILE) {
        threshold = 3;
    }
    // TODO: calibrate this costyl
    threshold = threshold > 8 ? 8 : threshold;
    if(out < SWITCH_PERIOD/100 || (is_rising[room] && abs(setpoints[room] - room_temps[room]) < threshold ) || (room_temps[room] - setpoints[room] >= threshold)){
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
}

void setup_off_mode(int room){
    modes[room] = OFF;
    for(int i = 0; i < N_RELAYS; i++){
        relay_states[room * N_RELAYS + i] = 0;
    }
    heat_times[room] = 0;
    rooms_states[room] = 0;
    pids[room].integral = 0;
}

void setup_trend_mode(int room, float target_temp, int time_interval_s){
    trend_target_temps[room] = target_temp;
    trend_start_times[room] = millis();
    trend_target_times[room] = millis() + time_interval_s * 1000;
    trend_start_temps[room] = room_temps[room];
    modes[room] = PROFILE;
}


void run_trend_mode(int room){
    float current_setpoint = map(min((float)millis(), trend_target_times[room]), trend_start_times[room], trend_target_times[room], trend_start_temps[room], trend_target_temps[room]);
    setpoints[room] = current_setpoint;
    pids[room].setpoint = current_setpoint;
    run_constant_mode(room);
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
    if (room_temps[room] > 60) {
        for (int j = 0; j < N_RELAYS; j++) {
                    digitalWrite(config.rooms[room].relay_pins[j], R_OFF);
        }
    }

}