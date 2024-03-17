#include "EspMQTTClient.h"


EspMQTTClient client(
  "HEAVEN",
  "<redacted>",
  "192.168.2.228",  // MQTT Broker server ip
  "nti",   // Can be omitted if not needed
  "nti",   // Can be omitted if not needed
  "TestClient",     // Client name that uniquely identify your device
  1883              // The MQTT port, default to 1883. this line can be omitted
);

TaskHandle_t blink_task;

volatile int blink_delay = 1;
volatile int blink_brightness = 1;

void blink_task_code(void * param){
  while(1){
    ledcWrite(0, blink_brightness);
    delay(blink_delay);
    ledcWrite(0, 0);
    delay(blink_delay);
  }
  
}


void setup()
{
    pinMode(33, INPUT);
    // pinMode(32, OUTPUT);
    ledcSetup(0, 5000, 8);
    ledcAttachPin(32, 0);
    ledcWrite(0, 200);

    Serial.begin(115200);
    // client.enableDebuggingMessages(); // Enable debugging messages sent to serial output
    // client.enableHTTPWebUpdater(); // Enable the web updater. User and password default to values of MQTTUsername and MQTTPassword. These can be overridded with enableHTTPWebUpdater("user", "password").
    // client.enableOTA(); // Enable OTA (Over The Air) updates. Password defaults to MQTTPassword. Port is the default OTA port. Can be overridden with enableOTA("password", port).
    client.enableLastWillMessage("/power/0", "OFF");  // You can activate the retain flag by setting the third parameter to true
    xTaskCreate(blink_task_code, "blink", 1000, 0, 0, &blink_task);
	
}


void onConnectionEstablished()
{
  // Subscribe to "mytopic/test" and display received message to Serial
  client.subscribe("/act/led/0", [](const String & payload) {
    // ledcWrite(0, payload.toInt());
    blink_brightness = payload.toInt();
  });

  client.subscribe("/act/delay/0", [](const String & payload) {
    blink_delay = payload.toInt();
  });

  // Subscribe to "mytopic/wildcardtest/#" and display received message to Serial
//   client.subscribe("mytopic/wildcardtest/#", [](const String & topic, const String & payload) {
//     Serial.println("(From wildcard) topic: " + topic + ", payload: " + payload);
//   });

  // Publish a message to "mytopic/test"
  client.publish("/power/0", "ON"); // You can activate the retain flag by setting the third parameter to true
  // Execute delayed instructions
//   client.executeDelayed(5 * 1000, []() {
//     client.publish("mytopic/wildcardtest/test123", "This is a message sent 5 seconds later");
//   });
}


unsigned long last_publish = 0;

void loop()
{
	client.loop();

    unsigned long m = millis();
    if(m - last_publish > 333){
        last_publish = m;
        int val = analogRead(33);
        client.publish("/sensors/pot/0", String("pot value=") + val);
    }
    
}
