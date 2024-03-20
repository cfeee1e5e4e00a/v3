#pragma once

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




extern config_t config;

void load_config();

// linker does some shit so not ccp file

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