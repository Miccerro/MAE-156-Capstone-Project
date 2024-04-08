#include <Ethernet.h>

// Define pins for the stepper motor
const int stepPin = 5;
const int dirPin = 2;
const int enPin = 8;

// Ethernet Configuration
byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};  // MAC address for the PLC
IPAddress ip(192, 168, 1, 100);                      // Static IP address for the PLC
EthernetServer server(80);                           // TCP server instance on port 80

void setup() {
  // Setup pins for the stepper motor
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);  // Ensure the motor is enabled during setup

  // Initialize serial communication
  Serial.begin(9600);

  // Initialize Ethernet with static IP address
  Ethernet.begin(mac, ip);

  // Start TCP server
  server.begin();

  // Print debug message to serial monitor
  Serial.println("Arduino PLC initialized and waiting for rotation commands...");
}

void loop() {
  // Check for incoming client connections
  EthernetClient client = server.available();
  if (client) {
    // If a client is connected, handle the rotation command
    while (client.connected()) {
      if (client.available()) {
        // Read the rotation command from the client
        String rotationCommand = client.readStringUntil('\n');
        // Print received command to serial monitor
        Serial.print("Received rotation command: ");
        Serial.println(rotationCommand);

        // Parse the rotation command and rotate the motor accordingly
        int rotations = rotationCommand.toInt();
        rotateMotor(rotations);

        // Respond to the client with an acknowledgment message
        client.println("Rotation completed!");

        // Close the connection
        client.stop();
      }
    }
  }
}

void rotateMotor(int rotations) {
  // Enable the motor
  digitalWrite(enPin, LOW);
  Serial.println("Motor enabled.");

  // Set direction to counterclockwise
  digitalWrite(dirPin, LOW);
  Serial.println("Direction set to counterclockwise.");

  // Convert rotations to steps
  long steps = rotations * 200;  // Adjust steps per rotation based on your motor's specification

  // Move the stepper motor
  for (int i = 0; i < steps; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
  }

  // Disable the motor
  digitalWrite(enPin, HIGH);
  Serial.println("Motor disabled.");
}
