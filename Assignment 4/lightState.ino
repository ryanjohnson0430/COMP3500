#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi/MQTT parameters
#define WLAN_SSID       "dan_2"
#define WLAN_PASS       "supersecretpassword"
#define BROKER_IP       "192.168.1.32"

// wifi client and mqqt client
WiFiClient client;
PubSubClient mqttclient(client);
int lightstate;
String lightString;
char lightChar[50];


void setup() {
  Serial.begin(115200); 
  
  // connect to wifi
  WiFi.mode(WIFI_STA);
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(F("."));
  }

  // print wifi info
  Serial.println(F("WiFi connected"));
  Serial.println(F("IP address: "));
  Serial.println(WiFi.localIP());

  // connect to mqtt server
  mqttclient.setServer(BROKER_IP, 1883);
  connect();
  
}

void loop() {
  if (!mqttclient.connected()) { //make sure mqqt is connected
    connect();
  }

  static const unsigned long REFRESH_INTERVAL = 1000; // ms
  static unsigned long lastRefreshTime = 0;
  if(millis() - lastRefreshTime >= REFRESH_INTERVAL)
  {
    lastRefreshTime += REFRESH_INTERVAL;
    lightstate = analogRead(A0);
    lightString = String(lightstate);
    lightString.toCharArray(lightChar, lightString.length()+1);
    mqttclient.publish("/light", lightChar);
    Serial.println(lightstate);
  }

  Serial.println("tick");

  mqttclient.loop(); // run client
}

// connect to mqtt
void connect() {
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println(F("Wifi issue"));
    delay(3000);
  }
  Serial.print(F("Connecting to MQTT server... "));
  while(!mqttclient.connected()) {
    if (mqttclient.connect(WiFi.macAddress().c_str())) {
      Serial.println(F("MQTT server Connected!"));   
    } else {
      Serial.print(F("MQTT server connection failed! rc="));
      Serial.print(mqttclient.state());
      Serial.println("try again in 10 seconds");
      // Wait 5 seconds before retrying
      delay(20000);
    }
  }
}
