// Pin where your servo is connected
int servoPin = 9; // You can use any digital pin

// Variables for controlling servo speed and direction
int servoSpeed = 2; // Speed of rotation, adjust as needed
int servoPosition = 90; // Initial position of the servo
int sensorValue3;
int sensorPin = A0;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
}

void loop() {
  // Measure the voltage on input A0
  int sensorValue = analogRead(A0);
  
  // Map the sensor value to voltage (0-5V range)
  float voltage = sensorValue * (5.0 / 1023.0);
  
  // Print the voltage to the Serial Monitor
  //Serial.print("Voltage on A0: ");
  //Serial.print(voltage);
  //Serial.println(" V");

  sensorValue = analogRead(sensorPin);
  Serial.println(sensorValue);
  
  // Gradually change servo position to rotate continuously
  servoPosition += servoSpeed;
  
  // Check if servo reaches the limits (0 and 180)
  if (servoPosition <= 0 || servoPosition >= 180) {
    // Change direction when reaching the limits
    servoSpeed = -servoSpeed;
    delay(1000); // Delay for smoother direction change
  }
  
  // Set the servo position
  analogWrite(servoPin, servoPosition);
  
  // Delay to control the speed of rotation
  delay(15); // Adjust delay for desired speed
}
