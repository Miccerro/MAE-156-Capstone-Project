#include <Ethernet.h>

// Define MAC address and IP address
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(192, 168, 1, 100);

// Define port for server
unsigned int port = 80;

// Create a TCP server
EthernetServer server(port);

// Define pins for the stepper motor
const int stepPin = 6;
const int dirPin = 2;
const int enPin = 4;

void setup() {
  //Why deos the order of how the code matter. I can 
    // Initialize Ethernet and serverI 
  Ethernet.begin(mac, ip);
  server.begin();

  









}

void loop() {


    // Initialize pins for the stepper motor
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(enPin, OUTPUT); //IF SET UP HERE, THERE IS NO ETHERNET COMMUNICATION. 

  digitalWrite(enPin, LOW); // Enable the motor
  digitalWrite(stepPin, LOW); //
  digitalWrite(dirPin, LOW); // Direction of motor


  // Check for client connection
  EthernetClient client = server.available();
  if (client) {
    // Wait for data from client
    while (client.connected()) {
      if (client.available()) {
        // Read rotation command from client
        String rotationCommand = client.readStringUntil('\n');
        int rotations = rotationCommand.toInt();
        //int rotations = 3;
        Serial.println(rotations);
        // Rotate the stepper motor
        rotateMotor(rotations);
      }
    }
    // Close client connection
    client.stop();
  }
}

void rotateMotor(int rotations) {
  pinMode(enPin, OUTPUT);
  // Enable the motor
  digitalWrite(enPin, LOW);

  // Set direction (clockwise or counterclockwise based on rotations value)
  if (rotations >= 0) {
    digitalWrite(dirPin, HIGH); // Set direction to clockwise
  } else {
    digitalWrite(dirPin, LOW);  // Set direction to counterclockwise
  }

  // Convert rotations to steps (adjust as needed)
  long steps = abs(rotations) * 6400; // Adjust based on your motor

  // Move the stepper motor
  for (int i = 0; i < steps; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(300);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(300);
  }

  // Disable the motor
  digitalWrite(enPin, HIGH);
}
