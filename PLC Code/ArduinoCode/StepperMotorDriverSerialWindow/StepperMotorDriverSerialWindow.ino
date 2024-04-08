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
  digitalWrite(enPin, HIGH);  // Disable the motor

  // Initialize serial communication
  Serial.begin(9600);

  // Print debug message to serial monitor
  Serial.println("Arduino PLC initialized and waiting for rotation commands...");
}

void loop() {
  // Check if data is available to read from the serial port
  if (Serial.available() > 0) {
    // Read the rotation command from the serial port
    String rotationCommand = Serial.readStringUntil('\n');
    // Print received command to serial monitor
    Serial.print("Received rotation command: ");
    Serial.println(rotationCommand);

    // Parse the rotation command and rotate the motor accordingly
    int rotations = rotationCommand.toInt();
    rotateMotor(rotations);
  }
}

void rotateMotor(int rotations) {
  // Enable the motor
  digitalWrite(enPin, LOW);

  // Set direction (clockwise or counterclockwise based on rotations value)
  if (rotations >= 0) {
    digitalWrite(dirPin, HIGH);  // Set direction to clockwise
  } else {
    digitalWrite(dirPin, LOW);   // Set direction to counterclockwise
  }

  // Convert rotations to steps (adjust as needed)
  long steps = abs(rotations) * 800;  // Adjust based on your motor and gear ratio

  // Move the stepper motor
  for (int i = 0; i < steps; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
  }

  // Disable the motor
  digitalWrite(enPin, HIGH);

  // Print debug message to serial monitor
  Serial.println("Motor rotation completed.");
}
