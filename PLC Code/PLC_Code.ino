#include <SPI.h>
#include <Ethernet.h>
#include <Math.h>
#include <TimerOne.h>

// MAC address and IP address for the Ethernet shield
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
//IPAddress ip(192, 168, 1, 177);
IPAddress ip(155,211,111,10);
unsigned int port = 8888;
EthernetServer server(port);

// States for the state machine
enum State {
  Idle,
  Calibrate,
  AtSpoke,
  AtSafe
};

State currentState = Idle;
int n_spokes = 0;
bool clientActive = true;
bool calibrationComplete = false;
int currentSpoke = 0; // Track the current spoke

//Motor and Conversion Setup
// Motor 1 - SMALL MOTOR
const int stepPin1 = 24; 
const int dirPin1 = 26; 
const int enPin1 = 28;
// Motor 2 - BIG MOTOR
const int stepPin2 = 34; 
const int dirPin2 = 36; 
const int enPin2 = 38;
// Motor 3 - x-axis motor
const int stepPin3 = 11; 
const int dirPin3 = 12; 
const int enPin3 = 13;
int xCoordinate = 0; // Track position of motor 3

const int currentSensorPin = A1;  // Analog pin for current sensor
const int overcurrentThreshold = 620; // Set a reasonable threshold for overcurrent detection


const float y_conversion_factor = 0.003048 / 1;  // Conversion factor for Y coordinate in mm/steps (NEMA 8)
const float z_conversion_factor = 10.0 / 200.0;  // Conversion factor for Z coordinate in mm/steps (NEMA 17)
const int safeAreaYSteps = -45 / y_conversion_factor;  // Convert 8mm to steps
const int safeAreaZSteps = -45 / z_conversion_factor;  // Convert 8mm to steps


const int safeAreaYSteps8 = -50 / y_conversion_factor;  // Convert 8mm to steps for 8 spokes
const int safeAreaZSteps8 = -45 / z_conversion_factor;  // Convert 8mm to steps for 8 spokes



const int safeAreaYSteps16 = 10 / y_conversion_factor;  // Convert 8mm to steps for 16 spokes
const int safeAreaZSteps16 = -35 / z_conversion_factor;  // Convert 8mm to steps for 16 spokes

float x1 = 0, y1 = 0, x_opposite = 0, y_opposite = 0;  // Coordinate storage

// Thresholds for button presses
int threshold1 = 195; // Below Button1
int threshold2 = 245; // Above Button1, Below Button2
int threshold3 = 330; // Above Button 2, Below Button3
int threshold4 = 505; // Above Button 3, Below Button4 
int threshold5 = 1020; // Above Button 4, Below Button5
int threshold6 = 1030; // Above Button 5 

// Global variables to track coordinates
int yCoordinate = 0; // Track position of motor 1
int zCoordinate = 0; // Track position of motor 2
int yStepResolution = 100; // Play around with this value, try 35 steps
int zStepResolution = 10;  // Play around with this value, try 2 steps

// Stall detecting parameters
const int sensorPin = A1; // define the Arduino pin A1 as voltage input (V in)
const float VCC = 4.72; // supply voltage
const float sensitivity = 0.185; // ACS712-30A sensitivity (66mV/A)
const float zeroCurrentVoltage = VCC / 2; // Voltage at 0A, typically VCC/2 for ACS712
int xStepResolution = 200 * 10;  // Play around with this value, try a suitable number of steps
const float CurrThreshold = 1.5; // Set this to an appropriate current threshold value in amps
const float noiseThreshold = 0.3; // Current below this value is considered zero
volatile float current = 0.0; // Global variable to store current value
volatile bool motorStalled = false; // Flag to indicate motor stall
volatile bool motorEnabled = true; // Flag to control motor state
unsigned long lastStepTime = 0;
const unsigned long stepInterval = 1500; // Interval in microseconds
int stepsRemaining = 0; // Track steps remaining for non-blocking motor control

float spokes_coords[16][2] = {0};  // Initialize all elements to zero, max 16 spokes

// Button press state
int button5PressCount = 0;
unsigned long previousMillis = 0; // will store last time LED was updated
bool ledState = false;
int LEDPin1 = 46;
int LEDPin2 = 44;
int interval = 700;

bool movingToSafeArea = false;
String pendingResponse = "";
EthernetClient currentClient;


void setup() {
  // Initialize Ethernet
  Ethernet.begin(mac, ip);
  server.begin();
  Serial.begin(9600);
  Serial.println("Server started");

  // Motor1
  pinMode(stepPin1, OUTPUT); 
  pinMode(dirPin1, OUTPUT);
  pinMode(enPin1, OUTPUT);
  // Motor2
  pinMode(stepPin2, OUTPUT); 
  pinMode(dirPin2, OUTPUT);
  pinMode(enPin2, OUTPUT);
  // Motor3
  pinMode(stepPin3, OUTPUT); 
  pinMode(dirPin3, OUTPUT);
  pinMode(enPin3, OUTPUT);

  // LED Pins
  pinMode(LEDPin1, OUTPUT);
  pinMode(LEDPin2, OUTPUT);

  digitalWrite(enPin1, LOW);
  digitalWrite(enPin2, LOW);
  digitalWrite(enPin3, LOW);
}

void loop() {
  EthernetClient client = server.available();
  if (client) {
    Serial.println("Client connected");
    clientActive = true;
    currentClient = client;  // Assign current client

    while (client.connected() && clientActive) {
      String incomingMessage = "";
      unsigned int messageLength = 0;

      // Read the length of the incoming message (4 bytes)
      if (client.available() >= 4) {
        byte lengthBytes[4];
        client.readBytes(lengthBytes, 4);
        messageLength = lengthBytes[0] | (lengthBytes[1] << 8) | (lengthBytes[2] << 16) | (lengthBytes[3] << 24);
      }

      // Read the actual message
      while (client.connected() && incomingMessage.length() < messageLength) {
        if (client.available()) {
          char c = client.read();
          incomingMessage += c;
        }
      }

      if (incomingMessage.length() > 0) {
        handleIncomingMessage(incomingMessage, client);
        incomingMessage = "";  // Reset the incoming message string
      }

      // Non-blocking motor control
      if (stepsRemaining > 0 && (micros() - lastStepTime >= stepInterval)) {
        lastStepTime = micros(); // Update the last step time
        int sensorValue = analogRead(currentSensorPin);  // Read the value from the current sensor

        // Reduce the frequency of Serial prints
        if (stepsRemaining % 100 == 0) {
          Serial.print("Sensor value: ");
          Serial.println(sensorValue);
        }

        if (sensorValue > overcurrentThreshold) {
          // Overcurrent detected
          Serial.println("Overcurrent detected! Stopping motor.");
          stepsRemaining = 0; // Stop the motor
        } else {
          digitalWrite(stepPin3, HIGH);
          delayMicroseconds(1300); // Minimum pulse width
          digitalWrite(stepPin3, LOW);
          delayMicroseconds(1300);

          stepsRemaining--; // Decrement steps remaining

          // Update X coordinate based on direction
          if (digitalRead(dirPin3) == HIGH) {
            xCoordinate++; // Increase X coordinate if moving clockwise
          } else {
            xCoordinate--; // Decrease X coordinate if moving counterclockwise
          }
        }
      }

      // Print the current X position once the motor movement is complete
      if (stepsRemaining == 0 && lastStepTime != 0) {
        lastStepTime = 0; // Reset last step time to avoid multiple prints
        Serial.print("Current X Position: ");
        Serial.println(xCoordinate);
        sendResponse("MotorMovementFinished", currentClient); // Send response when motor movement is finished

        // Send the pending response if moving to a safe area
        // if (movingToSafeArea) {
        //   sendResponse(pendingResponse, currentClient);
        //   movingToSafeArea = false;
        //   pendingResponse = "";
        // }
      }

      // Handle button presses to move out of the Calibrate state
      handleButtonPresses();

      // Transition out of Calibrate state if calibration is complete
      if (currentState == Calibrate && calibrationComplete) {
        Serial.println("Calibration complete. Transitioning to AtSpoke state.");
        currentState = AtSpoke;
        calibrationComplete = false; // Reset the flag
        sendResponse("CalibrationComplete", currentClient); // Send response when calibration is complete
      }
    }

    client.stop();
    Serial.println("Client disconnected");
  }
}

void handleIncomingMessage(String message, EthernetClient& client) {
  String response;
  Serial.print("Received message: ");
  Serial.println(message);

  if (currentState == Idle) {
      digitalWrite(LEDPin1, LOW);
      digitalWrite(LEDPin2, LOW);
    if (message.startsWith("Spokes")) {
      n_spokes = message.substring(6).toInt();
      Serial.print("Number of spokes set to: ");
      Serial.println(n_spokes);
      response = "SpokesSetTo" + String(n_spokes);
      sendResponse(response, client);
    } else if (message == "CalibrationOn") {
      currentState = Calibrate;
      response = "EnteringCalibrationMode";
      // Turn on LEDs
      digitalWrite(LEDPin1, HIGH);
      digitalWrite(LEDPin2, HIGH);
      sendResponse(response, client);
    } else if (message == "connect plc") {
      response = "PLC Received Connection Request --> Establishing Connection...";
      sendResponse(response, client);
    } else {
      response = "UnrecognizedCommand";
      sendResponse(response, client);
    }
  } else if (currentState == Calibrate) {
    if (message == "CalibrationOff") {
      currentState = Idle;
      response = "ExitingCalibrationMode";
      // Turn off LEDs
      digitalWrite(LEDPin1, LOW);
      digitalWrite(LEDPin2, LOW);
      sendResponse(response, client);
    }
  } else if (currentState == AtSpoke) {
    if (message == "MoveToSafe8") {
    moveToSafeAreaFromSpoke(8);
    currentState = AtSafe;
    response = "MovedToSafeArea";
    Serial.println(response);  // Debug print
    sendResponse(response, client);
  } else if (message == "MoveToSafe16") {
    moveToSafeAreaFromSpoke(16);
    currentState = AtSafe;
    response = "MovedToSafeArea";
    Serial.println(response);  // Debug print
    sendResponse(response, client);
  } else if (message.startsWith("MoveToSpoke")) {
    int spokeIndex = message.substring(11).toInt() - 1;
    moveToSpoke(spokeIndex);
    response = "MovedToSpoke" + String(spokeIndex + 1);
    Serial.println(response);  // Debug print
    sendResponse(response, client);
  } else if (message == "PushSample") {
      Serial.print("PLC: Received Message to Push");
      moveMotor3Steps(dirPin3, stepPin3, true, 69); // Move motor 3 CW xStepResolution
      response = "SamplePushed";
      Serial.print("Sending to API: SamplePushed");
      sendResponse(response, client);
      Serial.println(response);  // Debug print
    } else if (message == "PullSample") {
      Serial.print("PLC: Received Message to Pull");
      moveMotor3Steps(dirPin3, stepPin3, false, 69); // Move motor 3 CCW xStepResolution
      response = "SamplePulled";
      Serial.print("Sending to API: SamplePulled");
      sendResponse(response, client);
      Serial.println(response);  // Debug print
    } else if (message == "CalibrationOn") {
      Serial.print("Shouldnt get this, but force enter spoke state");
      int calspoke = 0;
      moveToSpokeFromSafeArea(calspoke);
      response = "MovedToSpoke" + String(calspoke + 1);
      sendResponse(response, client);
      Serial.println(response);  // Debug print
      currentState = AtSpoke;
    } else if (message == "Vacuum Error: Aborting Process") {
      Serial.print("Vacuum Error: Returning to IDLE");
      response = "Returning back to IDLE";
      currentState = Idle;
      sendResponse(response, client);
    } 



  } else if (currentState == AtSafe) {
    if (message.startsWith("MoveToSpoke")) {
      digitalWrite(LEDPin1, LOW);
      digitalWrite(LEDPin2, LOW);
      int spokeIndex = message.substring(11).toInt() - 1;
      moveToSpokeFromSafeArea(spokeIndex);
      currentState = AtSpoke;
      response = "MovedToSpoke" + String(spokeIndex + 1);
      sendResponse(response, client);
      Serial.println(response);  // Debug print
    } else if (message == "Wagon Wheel Analysis Completed") {
      response = "Returning back to IDLE";
      currentState = Idle;
      sendResponse(response, client);
    }
  }

  if (message == "exit") {
    response = "Acknowledge: Connection closing";
    clientActive = false;
    sendResponse(response, client);
  }
}


void sendInitialMessage(EthernetClient& client) {
  String initialMessage = "PLC Recieved Connection Request --> Establishing Connection...";
  sendResponse(initialMessage, client);
}

void sendResponse(String response, EthernetClient& client) {
  unsigned int responseLength = response.length();
  Serial.print("Sending response: ");
  Serial.println(response);

  // Send 4 bytes of response length
  byte responseLengthBytes[4];
  responseLengthBytes[0] = (responseLength >> 0) & 0xFF;
  responseLengthBytes[1] = (responseLength >> 8) & 0xFF;
  responseLengthBytes[2] = (responseLength >> 16) & 0xFF;
  responseLengthBytes[3] = (responseLength >> 24) & 0xFF;
  client.write(responseLengthBytes, 4);

  // Send the actual response message
  client.write(response.c_str(), responseLength);

  Serial.println("Response sent: " + response);
}

void handleButtonPresses() {
  if (currentState == Calibrate) {
    int threshold = analogRead(A0); // Assume the buttons are connected to analog pin A0
    //Serial.println(threshold);
    if (threshold < 50) { // If below this limit, no button is pressed
        digitalWrite(stepPin1, LOW);
    } else if (threshold > threshold1 && threshold < threshold2) { // Button 1 pressed (SMALL RIGHT)
        moveMotor1Steps(dirPin1, stepPin1, HIGH, yStepResolution); // Move motor 1 CW, adjust the steps as needed
    } else if (threshold > threshold2 && threshold < threshold3) { // Button 2 pressed (SMALL LEFT)
        moveMotor1Steps(dirPin1, stepPin1, LOW, yStepResolution); // Move motor 1 CCW, adjust the steps as needed
    } else if (threshold > threshold3 && threshold < threshold4) { // Button 3 pressed
        moveMotor2Steps(dirPin2, stepPin2, HIGH, zStepResolution); // Move motor 2 CW, adjust the steps as needed
    } else if (threshold > threshold4 && threshold < threshold5) { // Button 4 pressed
        moveMotor2Steps(dirPin2, stepPin2, LOW, zStepResolution); // Move motor 2 CCW, adjust the steps as needed
    }
    
    // Check if Button 5 is pressed
    if (threshold > threshold5 && threshold < threshold6) {
      if (button5PressCount == 0) {
        // First button press
        Serial.println("Button 5 pressed for the first time.");
        x1 = 0; y1 = 0;  // Assuming this is the origin
        yCoordinate = 0;
        zCoordinate = 0;

        button5PressCount++;
      } else if (button5PressCount == 1) {
        // Second button press
        Serial.println("Button 5 pressed for the second time.");
        // Calculate coordinates for the opposite spoke (Spoke 5 for 8 spokes, Spoke 9 for 16 spokes)
        x_opposite = yCoordinate; 
        y_opposite = zCoordinate;
        button5PressCount++;

        // Debug prints before calling calculate_spokes
        Serial.print("x1: "); Serial.print(x1);
        Serial.print(", y1: "); Serial.print(y1);
        Serial.print(", x_opposite: "); Serial.print(x_opposite);
        Serial.print(", y_opposite: "); Serial.print(y_opposite);
        Serial.print(", n_spokes: "); Serial.println(n_spokes);

        // Call function to calculate and output all spoke coordinates
        calculate_spokes(x1, y1, x_opposite, y_opposite, n_spokes);
        delay(2000);
        // Move to origin or spoke 1:
        // if (n_spokes == 8) {
        //   moveToSpoke1FromSpoke(4); // Move from Spoke 5 to Spoke 1
        // } else if (n_spokes == 16) {
        //   moveToSpoke1FromSpoke(8); // Move from Spoke 9 to Spoke 1
        // }
        calibrationComplete = true; // Set the flag to indicate calibration is complete
      }
      delay(400); // Debounce Delay
    }
  }
}


void moveMotor1Steps(int dirPin, int stepPin, bool clockwise, int steps) {
    digitalWrite(dirPin, clockwise ? HIGH : LOW); // Set direction
    for (int i = 0; i < steps; i++) {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(300);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(300);
    }
    // Update Y coordinate based on direction
    if (clockwise) {
        yCoordinate += steps; // Increase Y coordinate if moving clockwise
    } else {
        yCoordinate -= steps; // Decrease Y coordinate if moving counterclockwise
    }
    // Serial.println("Current Y Position(Steps): "+ String(yCoordinate));
    // Serial.println("Current Y Position: "+ String(yCoordinate*y_conversion_factor)+"mm");
    //Aim for 38mm difference
}

void moveMotor2Steps(int dirPin, int stepPin, bool clockwise, int steps) {
  digitalWrite(dirPin, clockwise ? HIGH : LOW); // Set direction
  for (int i = 0; i < steps; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(920);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(920);
  }
  // Update Z coordinate based on direction
  if (clockwise) {
    zCoordinate += steps; // Increase Z coordinate if moving clockwise
  } else {
    zCoordinate -= steps; // Decrease Z coordinate if moving counterclockwise
  }
  //Serial.println("Current Z Position: " + String(zCoordinate));
}

void moveMotor3Steps(int dirPin, int stepPin, bool clockwise, int steps) {
  digitalWrite(dirPin, clockwise ? HIGH : LOW); // Set direction
  stepsRemaining = steps; // Initialize steps remaining
  lastStepTime = micros(); // Initialize the last step time
  Serial.print("Moving motor ");
  Serial.print(clockwise ? "clockwise" : "counterclockwise");
  Serial.print(" for ");
  Serial.print(steps);
  Serial.println(" steps.");
}

// Function to calculate spokes
void calculate_spokes(int x1_steps, int y1_steps, int x_opposite_steps, int y_opposite_steps, int n_spokes) {
    Serial.println("Calculating spokes...");
    // Convert step inputs to millimeters
    float x1_mm = x1_steps * y_conversion_factor;
    float y1_mm = y1_steps * z_conversion_factor;
    //float x_opposite_mm = x_opposite_steps * y_conversion_factor;
    float x_opposite_mm = 38;
    float y_opposite_mm = y_opposite_steps * z_conversion_factor;

    // Calculate the center and radius in millimeters
    float center_x_mm = (x1_mm + x_opposite_mm) / 2;
    float center_y_mm = (y1_mm + y_opposite_mm) / 2;
    float radius_mm = sqrt(pow(x_opposite_mm - x1_mm, 2) + pow(y_opposite_mm - y1_mm, 2)) / 2;
    
    // Calculate the initial angle in radians (adjusted for counterclockwise direction)
    float initial_angle = atan2(y1_mm - y_opposite_mm, x1_mm - x_opposite_mm);
    
    // Angle between spokes (positive for counterclockwise)
    float angle_increment = 2 * PI / n_spokes;
    
    for (int i = 0; i < n_spokes; i++) {
        float angle = initial_angle + i * angle_increment;
        float x = center_x_mm + radius_mm * cos(angle);
        float y = center_y_mm + radius_mm * sin(angle);
        spokes_coords[i][0] = x / y_conversion_factor;  // Convert mm back to Y steps
        spokes_coords[i][1] = y / z_conversion_factor;  // Convert mm back to Z steps
    }
    
    // Print distances from Spoke 1 to each other spoke
    for (int i = 1; i < n_spokes; i++) {
        float diff_x_mm = (spokes_coords[i][0] - spokes_coords[0][0]) * y_conversion_factor;
        float diff_y_mm = (spokes_coords[i][1] - spokes_coords[0][1]) * z_conversion_factor;
        float diff_x_steps = spokes_coords[i][0] - spokes_coords[0][0];
        float diff_y_steps = spokes_coords[i][1] - spokes_coords[0][1];

        Serial.print("Distance from Spoke 1 to Spoke ");
        Serial.print(i + 1);
        Serial.print(": Steps (");
        Serial.print(diff_x_steps, 0); // Difference in steps for Y
        Serial.print(", ");
        Serial.print(diff_y_steps, 0); // Difference in steps for Z
        Serial.print(") | mm (");
        Serial.print(diff_x_mm, 2); // Difference in mm for Y
        Serial.print(", ");
        Serial.print(diff_y_mm, 2); // Difference in mm for Z
        Serial.println(")");
    }
}

void moveToSpoke1FromSpoke(int spokeIndex) {
    // Calculate steps to move from given spoke to Spoke 1
    int yStepsToMove = -spokes_coords[spokeIndex][0];  // Calculate Y steps from given spoke to Spoke 1
    int zStepsToMove = -spokes_coords[spokeIndex][1];  // Calculate Z steps from given spoke to Spoke 1
    bool yDirection = yStepsToMove > 0;  // Fix direction logic
    bool zDirection = zStepsToMove > 0;  // Fix direction logic

    yStepsToMove = abs(yStepsToMove);  // Absolute number of steps to move in Y
    zStepsToMove = abs(zStepsToMove);  // Absolute number of steps to move in Z

    Serial.print("Steps to move from Spoke ");
    Serial.print(spokeIndex + 1);
    Serial.print(" to Spoke 1: Y Steps: ");
    Serial.print(yStepsToMove);
    Serial.print(", Z Steps: ");
    Serial.println(zStepsToMove);

    Serial.print("Y Direction: ");
    Serial.println(yDirection ? "Clockwise" : "Counter-Clockwise");
    Serial.print("Z Direction: ");
    Serial.println(zDirection ? "Clockwise" : "Counter-Clockwise");

    // Move motors to Spoke 1 from given spoke
    moveMotor1Steps(dirPin1, stepPin1, yDirection, yStepsToMove);
    moveMotor2Steps(dirPin2, stepPin2, zDirection, zStepsToMove);

    // Update the current coordinates to Spoke 1
    yCoordinate = 0;
    zCoordinate = 0;

    Serial.println("Moved to Spoke 1, reset as origin.");
    Serial.print("Updated Current Y Position: ");
    Serial.println(yCoordinate);
    Serial.print("Updated Current Z Position: ");
    Serial.println(zCoordinate);
}

void moveToSafeAreaFromSpoke(int spokeCount) {
  int safeAreaYSteps = (spokeCount == 8) ? safeAreaYSteps8 : safeAreaYSteps16;
  int safeAreaZSteps = (spokeCount == 8) ? safeAreaZSteps8 : safeAreaZSteps16;

  // Calculate steps to move to the safe area from the current position
  int yStepsToSafe = safeAreaYSteps - yCoordinate;
  int zStepsToSafe = safeAreaZSteps - zCoordinate;
  bool yDirectionSafe = yStepsToSafe > 0;
  bool zDirectionSafe = zStepsToSafe > 0;

  yStepsToSafe = abs(yStepsToSafe);
  zStepsToSafe = abs(zStepsToSafe);

  moveMotor2Steps(dirPin2, stepPin2, zDirectionSafe, zStepsToSafe);
  moveMotor1Steps(dirPin1, stepPin1, yDirectionSafe, yStepsToSafe);
  

  yCoordinate = safeAreaYSteps;  // Update Y coordinate to safe area
  zCoordinate = safeAreaZSteps;  // Update Z coordinate to safe area

  // Serial.print("Current Y Position: ");
  // Serial.println(yCoordinate);
  // Serial.print("Current Z Position: ");
  // Serial.println(zCoordinate);
  // Serial.println("Moved to Safe Area");
}

void moveToSpokeFromSafeArea(int spokeIndex) {
  int safeAreaYSteps = (n_spokes == 8) ? safeAreaYSteps8 : safeAreaYSteps16;
  int safeAreaZSteps = (n_spokes == 8) ? safeAreaZSteps8 : safeAreaZSteps16;

  // Calculate steps to move from the safe area to the target spoke
  int yStepsToMove = spokes_coords[spokeIndex][0] - yCoordinate;
  int zStepsToMove = spokes_coords[spokeIndex][1] - zCoordinate;
  bool yDirection = yStepsToMove > 0;
  bool zDirection = zStepsToMove > 0;

  yStepsToMove = abs(yStepsToMove);
  zStepsToMove = abs(zStepsToMove);

  moveMotor1Steps(dirPin1, stepPin1, yDirection, yStepsToMove);
  moveMotor2Steps(dirPin2, stepPin2, zDirection, zStepsToMove);

  yCoordinate = spokes_coords[spokeIndex][0];
  zCoordinate = spokes_coords[spokeIndex][1];

  // Serial.print("Current Y Position: ");
  // Serial.println(yCoordinate);
  // Serial.print("Current Z Position: ");
  // Serial.println(zCoordinate);
  // Serial.print("Moved from Safe Area to Spoke ");
  // Serial.println(spokeIndex + 1);
}

void moveToSpoke(int spokeIndex) {
  int yStepsToMove = spokes_coords[spokeIndex][0] - yCoordinate;
  int zStepsToMove = spokes_coords[spokeIndex][1] - zCoordinate;
  bool yDirection = yStepsToMove > 0;  // Fix direction logic
  bool zDirection = zStepsToMove > 0;  // Fix direction logic

  yStepsToMove = abs(yStepsToMove);
  zStepsToMove = abs(zStepsToMove);

  moveMotor1Steps(dirPin1, stepPin1, yDirection, yStepsToMove);
  moveMotor2Steps(dirPin2, stepPin2, zDirection, zStepsToMove);

  // Update global position to new position after movement
  yCoordinate = spokes_coords[spokeIndex][0];
  zCoordinate = spokes_coords[spokeIndex][1];

  // Serial.print("Moved to Spoke ");
  // Serial.println(spokeIndex + 1);
  // Serial.print("Current Y Position: ");
  // Serial.println(yCoordinate);
  // Serial.print("Current Z Position: ");
  // Serial.println(zCoordinate);
}
