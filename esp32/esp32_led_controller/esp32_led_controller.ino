#include <WiFi.h>
#include <PubSubClient.h>
#include <ctype.h>

// WiFi credentials
const char* ssid = "ssid";
const char* password = "password";

// MQTT Broker details
const char* mqtt_broker = "10.56.74.139"; // Change to your broker IP
const int mqtt_port = 1883;
const char* mqtt_client_id = "ESP32_LED_Controller";

// MQTT Topics
const char* GESTURE_TOPIC = "handAI2/gesture";
const char* ESP32_STATUS_TOPIC = "handAI2/esp32/status";
const char* SERIAL_TOPIC = "handAI2/serial";

// LED Pins
const int GREEN_LED_PIN = 17;
const int RED_LED_PIN = 16;
const int WHITE_LED_PIN = 18;

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi();
void reconnect_mqtt();
void callback(char* topic, byte* payload, unsigned int length);
void publish_status();
void control_leds(char gesture_char);
void send_serial_log(const String& message);

void setup() {
  Serial.begin(115200);

  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(WHITE_LED_PIN, OUTPUT);

  digitalWrite(GREEN_LED_PIN, LOW);
  digitalWrite(RED_LED_PIN, LOW);
  digitalWrite(WHITE_LED_PIN, LOW);

  setup_wifi();

  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect_mqtt();
  }
  client.loop();

  static unsigned long last_status_publish_time = 0;
  if (millis() - last_status_publish_time > 5000) {
    publish_status();
    last_status_publish_time = millis();
  }
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  send_serial_log("Connecting to WiFi: " + String(ssid));

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  send_serial_log("WiFi connected, IP: " + WiFi.localIP().toString());
}

void reconnect_mqtt() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    send_serial_log("Attempting MQTT connection...");

    if (client.connect(mqtt_client_id)) {
      Serial.println("connected");
      send_serial_log("MQTT connected");

      client.publish(ESP32_STATUS_TOPIC, "ESP32 Connected", true);
      client.subscribe(GESTURE_TOPIC);

      Serial.print("Subscribed to topic: ");
      Serial.println(GESTURE_TOPIC);
      send_serial_log("Subscribed to: " + String(GESTURE_TOPIC));
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      send_serial_log("MQTT connection failed, rc=" + String(client.state()));

      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  char message_buff[length + 1];

  for (unsigned int i = 0; i < length; i++) {
    message_buff[i] = (char)payload[i];
  }
  message_buff[length] = '\0';

  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  Serial.println(message_buff);

  if (strcmp(topic, GESTURE_TOPIC) == 0 && length > 0) {
    char received_char = toupper((unsigned char)message_buff[0]);
    Serial.print("Parsed gesture: ");
    Serial.println(received_char);

    control_leds(received_char);
  }
}

void control_leds(char gesture_char) {
  digitalWrite(GREEN_LED_PIN, LOW);
  digitalWrite(RED_LED_PIN, LOW);
  digitalWrite(WHITE_LED_PIN, LOW);

  String log_message = "LEDs controlled: ";

  switch (gesture_char) {
    case 'G':
      digitalWrite(GREEN_LED_PIN, HIGH);
      log_message += "Green ON";
      break;

    case 'R':
      digitalWrite(RED_LED_PIN, HIGH);
      log_message += "Red ON";
      break;

    case 'W':
      digitalWrite(WHITE_LED_PIN, HIGH);
      log_message += "White ON";
      break;

    default:
      log_message += "Unknown gesture: ";
      log_message += gesture_char;
      break;
  }

  Serial.println(log_message);
  send_serial_log(log_message);
  publish_status();
}

void publish_status() {
  char status_message[32];
  snprintf(
    status_message,
    sizeof(status_message),
    "G:%d,R:%d,W:%d",
    digitalRead(GREEN_LED_PIN),
    digitalRead(RED_LED_PIN),
    digitalRead(WHITE_LED_PIN)
  );

  client.publish(ESP32_STATUS_TOPIC, status_message, true);
  Serial.print("Published ESP32 status: ");
  Serial.println(status_message);
}

void send_serial_log(const String& message) {
  Serial.println(message);

  if (client.connected()) {
    client.publish(SERIAL_TOPIC, message.c_str(), false);
  }
}



//Done by A.M.A   ^_^