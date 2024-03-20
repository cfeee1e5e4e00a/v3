#include <ACS712.h>
#include <DHT.h>
// #include "EspMQTTClient.h"

//номер еспшки
#define CLIENT_ID "FUCK"
#define FLAT_NO_1 "1"
#define FLAT_NO_2 "2"

//кв. 1, реле 1; кв. 1, реле 2; кв. 2 реле 1; кв. 2, реле 1.
int relay_pins[2] = {5, 18};

#define PERIOD 500

#define DHT_1 27
// #define DHT_2 26
#define CURR_1 34
// #define CURR_2 34

DHT dht_1(DHT_1, DHT11);
// DHT dht_2(DHT_2, DHT11);
ACS712  acs1(CURR_1, 3.3, 4095, 100);
// ACS712  acs2(CURR_2, 3.3, 4095, 100);

const char* ssid = "TP-Link_4F90";
const char* password =  "NTOContest202324";
const char* mqttServer = "mqtt.cfeee1e5e4e00a.ru";
const int mqttPort = 1883;
const char* mqttUser = "nti";
const char* mqttPassword = "nti";

#define N_ROOMS 2
#define N_RELAYS 2

typedef struct __attribute__ ((packed)) {
    byte id;
    byte dht_pin;
    byte acs_pin;
    byte relay_pins[N_RELAYS];
    
} flat_config_t;


typedef struct __attribute__ ((packed)) {
    char client_id[16];
    byte send_external_temp;
    byte external_temp_pin;
    flat_config_t rooms[N_ROOMS];
} config_t;


config_t config;

void dump_config(){
    Serial.println(String("I identify myself as ") + config.client_id);
    Serial.printf("Send external temp: %d\nExternal dgt pin: %d\n", config.send_external_temp, config.external_temp_pin);
    for (int i = 0; i < N_ROOMS; i++){
        Serial.printf("Room #%d\n", config.rooms[i].id);
        Serial.printf("\tDHT pin: %d\n\tACS pin: %d\n\tRelay pins: ", config.rooms[i].dht_pin, config.rooms[i].acs_pin);
        for(int j = 0; j < N_RELAYS; j++){
            Serial.print(config.rooms[i].relay_pins[j]);
            Serial.print(' ');
        }
        Serial.println();
    }
    Serial.println("End of config");
}

void load_config(){
    Serial.println("Loading config...");
    const esp_partition_t * cfg_part = esp_partition_find_first(ESP_PARTITION_TYPE_ANY, ESP_PARTITION_SUBTYPE_ANY, "nticfg");
    if(!cfg_part){
        Serial.println("Config partition not found");
        while (1);
    }
    Serial.println("Got config partition");
    esp_partition_read(cfg_part, 0, &config, sizeof(config));
    Serial.println("Loaded config!");
    dump_config();
}

// EspMQTTClient client(
//   ssid,
//   password,
//   mqttServer,  // MQTT Broker server ip
//   "nti",   // Can be omitted if not needed
//   "nti",   // Can be omitted if not needed
//   CLIENT_ID,     // Client name that uniquely identify your device
//   mqttPort              // The MQTT port, default to 1883. this line can be omitted
// );

int relay_states[2] = {0,0};

// void onConnectionEstablished() {
//     client.publish("/init", String("privet ya esp ") + String(CLIENT_ID));
//     // client.
//     client.subscribe("/test_control", [](const String &topicStr, const String &message){
//         for(int i = 0; i < 2; i++){
//             relay_states[i] = message[i] - '0';
//             digitalWrite(relay_pins[i], !relay_states[i]);
//         }
//     });
// }

void setup()
{
    Serial.begin(115200);
    load_config();
    Serial.println("Different firmware");
    // //digital
    // for (int i = 0; i < 2; i++){
    //     pinMode(relay_pins[i], OUTPUT);
    //     digitalWrite(relay_pins[i], 1);
    // }
    // delay(100);

    // acs1.autoMidPointDC();
    // // acs2.autoMidPointDC();

    // pinMode(DHT_1, INPUT);
    // // pinMode(DHT_2, INPUT);
    // //analog
    // pinMode(CURR_1, INPUT);
    // // pinMode(CURR_2, INPUT);

    // Serial.begin(115200);
    // dht_1.begin();
    // // dht_2.begin();
    // client.enableDebuggingMessages(true);
    
}

unsigned long last_publish = 0;



void loop()
{
	// client.loop();
    // // Serial.println(dht_1.readTemperature());
    // unsigned long m = millis();

    // //SENSORS POLL AND PUBLISH 
    // if(m - last_publish > PERIOD){
    //     last_publish = m;
    //     //temp 1
    //     client.publish("/sensors", String("test_measure" + String(" temp=")) + dht_1.readTemperature() + ",relay1=" + relay_states[0] + ",relay2=" + relay_states[1] + ",curr=" +acs1.mA_DC(30)/1000.0);
    //     //temp 2
    //     // client.publish("/sensors", String("temp,flat=" + String(FLAT_NO_2) + String(" value=")) + dht_2.readTemperature());
    //     // // humidity 1
    //     // client.publish("/sensors", String("humd,flat=" + String(FLAT_NO_1) + String(" value=")) + dht_1.readHumidity());
    //     // // humidity 2
    //     // client.publish("/sensors", String("humd,flat=" + String(FLAT_NO_2) + String(" value=")) + dht_2.readHumidity()); 
    //     // // CURR 1
    //     // client.publish("/sensors", String("curr,flat=" + String(FLAT_NO_1) + String(" value=")) + acs1.mA_DC()/1000.0);
    //     // // CURR 2
    //     // client.publish("/sensors", String("curr,flat=" + String(FLAT_NO_2) + String(" value=")) + acs2.mA_DC()/1000.0);
    // }

    // //RELAY ALGO
    
}