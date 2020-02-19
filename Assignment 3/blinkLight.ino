#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi/MQTT parameters
#define WLAN_SSID       "dan_2"
#define WLAN_PASS       "supersecretpassword"
#define BROKER_IP       "192.168.1.22"

//pins
#define LED 5 //define 
#define BUTTON 4
bool lightstate;
bool buttonstate;
bool clickedflag = false;

WiFiClient client;
PubSubClient mqttclient(client);

void callback (char* topic, byte* payload, unsigned int length) {
  Serial.println(topic);
  Serial.write(payload, length); //print incoming messages
  Serial.println("");

  payload[length] = '\0'; // add null terminator to byte payload so we can treat it as a string

  if (strcmp(topic, "/led") == 0){
     if (strcmp((char *)payload, "toggle") == 0){
        lightstate = digitalRead(LED);
        if(lightstate){
          digitalWrite(LED, LOW);
        }
        else{
          digitalWrite(LED, HIGH);
        }
     } 
  }
}


void setup() {
  Serial.begin(115200);
  
  // connect to wifi
  WiFi.mode(WIFI_STA);
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(F("."));
  }

  Serial.println(F("WiFi connected"));
  Serial.println(F("IP address: "));
  Serial.println(WiFi.localIP());

  // connect to mqtt server
  mqttclient.setServer(BROKER_IP, 1883);
  mqttclient.setCallback(callback);
  connect();
  
  //setup pins
  pinMode(LED, OUTPUT); // setup pin for input
}

void loop() {
  buttonstate = digitalRead(BUTTON);
  if (!mqttclient.connected()) {
    connect();
  }

  // if the button is clicked and it was not clicked previously
  if (buttonstate and not clickedflag){
      
      // set the clicked flag
      clickedflag = true;
  }

  // if the button is not clicked now and it was clicked previously (a commplete click has now happened)
  if (not buttonstate and clickedflag){

    // set the clicked flag
    clickedflag = false;

    // print
    Serial.println("clicked");
    mqttclient.publish("/test","toggle",false);
  }
  mqttclient.loop();
}


void connect() {
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println(F("Wifi issue"));
    delay(3000);
  }
  Serial.print(F("Connecting to MQTT server... "));
  while(!mqttclient.connected()) {
    if (mqttclient.connect(WiFi.macAddress().c_str())) {
      Serial.println(F("MQTT server Connected!"));

       mqttclient.subscribe("/led");
      
    } else {
      Serial.print(F("MQTT server connection failed! rc="));
      Serial.print(mqttclient.state());
      Serial.println("try again in 10 seconds");
      // Wait 5 seconds before retrying
      delay(20000);
    }
  }
}
