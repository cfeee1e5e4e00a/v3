#include <DHT.h>
#include "EspMQTTClient.h"

//номер еспшки
#define CLIENT_ID "1"

//квартира 1 реле 1
#define REL_1 5
//квартира 1 реле 2
#define REL_2 18
//квартира 2 реле 1
#define REL_3 19
//квартира 2 реле 2
#define REL_4 21

#define PERIOD 5000


#define DHT_1 27
#define DHT_2 26
#define CURR_1 35
#define CURR_2 34

DHT dht_1(DHT_1, DHT11);
DHT dht_2(DHT_2, DHT11);

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
  "1",     // Client name that uniquely identify your device
  mqttPort              // The MQTT port, default to 1883. this line can be omitted
);


void onConnectionEstablished() {
    
}


void setup()
{
    //digital
	pinMode(REL_1, OUTPUT);
    pinMode(REL_2, OUTPUT);
    pinMode(REL_3, OUTPUT);
    pinMode(REL_4, OUTPUT);

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
String temp1 = "";
String temp2 = "";

/*String get_dht_temp(DHT dht) {
    switch(dht.getState()) {
    // всё OK
    case DHT_OK:
      // выводим показания влажности и температуры
      return(String(dht.getTemperatureC()));
    // ошибка контрольной суммы
    case DHT_ERROR_CHECKSUM:
      return(String("Checksum error"));
    // превышение времени ожидания
    case DHT_ERROR_TIMEOUT:
      return(String("Time out error"));
    // данных нет, датчик не реагирует или отсутствует
    case DHT_ERROR_NO_REPLY:
      return(String("Sensor not connected"));
  }
}
*/

/*String get_dht_humidity(DHT dht) {
    switch(dht.getState()) {
    // всё OK
    case DHT_OK:
      // выводим показания влажности и температуры
      return(String(dht.getHumidity()));
    // ошибка контрольной суммы
    case DHT_ERROR_CHECKSUM:
      return(String("Checksum error"));
    // превышение времени ожидания
    case DHT_ERROR_TIMEOUT:
      return(String("Time out error"));
    // данных нет, датчик не реагирует или отсутствует
    case DHT_ERROR_NO_REPLY:
      return(String("Sensor not connected"));
  }
}
*/

String get_current(int pin) {
    int i = analogRead(pin);
    //TODO: formula
    return String(i);
}

void loop()
{
	client.loop();
    Serial.println(dht_1.readTemperature());
    unsigned long m = millis();

    //SENSORS POLL AND PUBLISH 
    if(m - last_publish > PERIOD){
        last_publish = m;
        //temp 1
        client.publish("/sensors", String("temp,flat=1 value=") + dht_1.readTemperature());
        //client.publish("/sensors", String("temp,flat=1 value=") + dht_1.getTemperatureC());
        //temp 2
        client.publish("/sensors", String("temp,flat=2 value=") + dht_2.readTemperature());
        // humidity 1
        client.publish("/sensors", String("humd,flat=1 value=") + dht_1.readHumidity());
        // humidity 2
        client.publish("/sensors", String("humd,flat=2 value=") + dht_2.readHumidity()); 
        // CURR 1
        client.publish("/sensors", String("curr,flat=1 value=") + get_current(CURR_1));
        // CURR 2
        client.publish("/sensors", String("curr,flat=2 value=") + get_current(CURR_2));
    }

    //RELAY ALGO
    //----------
}