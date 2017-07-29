#include <ESP8266WiFi.h>

/*
 *  FanServer is an http service which allows
 *  control of fan over gpio. The fan has 
 *  three speeds and an off mode. This sketch
 *  was designed to be run on an ESP8266
 *  board. 
 *  
 *  Three 5v relays should be wired to the
 *  GPIO pins listed below. The relays I 
 *  used would not operate reliably with
 *  3v and so I could not the use board
 *  directly to provide a voltage. Instead
 *  I spliced the USB power supply to obtain
 *  the voltage needed.
 *  
 *  The fan has four wires leading to the motor.
 *  One for each speed and one for ground. Completing
 *  the ground to one of the speed wires in a circuit
 *  would run that speeds. This service ensures that 
 *  only one relay is enabled at a time.
 *  
 *  created by:  Michael Baumgarten
 *  date:  7/29/17
 *  
 */

const char* ssid = "";
const char* password = "";

// GPIO pins
const int lowSpeedPin = 14;
const int medSpeedPin = 12;
const int highSpeedPin = 13;

WiFiServer server(80);

void setup() {
  // gpio initialization
  pinMode(lowSpeedPin, OUTPUT);
  pinMode(medSpeedPin, OUTPUT);
  pinMode(highSpeedPin, OUTPUT);

  digitalWrite(lowSpeedPin, HIGH);
  digitalWrite(medSpeedPin, HIGH);
  digitalWrite(highSpeedPin, HIGH);

  delay(1000);
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  // wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println(".");
  }

  // print information
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  Serial.print("MAC: ");
  Serial.println(WiFi.macAddress());

  server.begin();
  Serial.println("server running");


}

void loop(void) {
  WiFiClient client = server.available();
  if (!client) {
    return;
  }

  Serial.println("new client");
  while (!client.available()) {
    delay(1);
  }

  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();

  String html = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE HTML>\r\n<html>\r\nFan has been set to ";

  if (request.indexOf("/fan/speed/0") != -1) {
    digitalWrite(lowSpeedPin, HIGH);
    digitalWrite(medSpeedPin, HIGH);
    digitalWrite(highSpeedPin, HIGH);
      html += "off";
  }
  else if (request.indexOf("/fan/speed/3") != -1) {
    digitalWrite(medSpeedPin, HIGH);
    digitalWrite(highSpeedPin, HIGH);
    digitalWrite(lowSpeedPin, LOW);
    html += "low";
  }
  else if (request.indexOf("/fan/speed/2") != -1) {
    digitalWrite(lowSpeedPin, HIGH);
    digitalWrite(highSpeedPin, HIGH);
    digitalWrite(medSpeedPin, LOW);
    html += "med";
  }
  else if (request.indexOf("/fan/speed/1") != -1) {
    digitalWrite(lowSpeedPin, HIGH);
    digitalWrite(medSpeedPin, HIGH);
    digitalWrite(highSpeedPin, LOW);
    html += "high";
  }
  else {
    Serial.println("invalid request");
    client.stop();
    return;
  }

  client.flush();

  html += "</html>\n";

  client.print(html);

}





