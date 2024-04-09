//Define pin numbers:
const int stepPin = 7;
const int dirPin = 4;
const int enPin = 2;
int buttonPin = A0;

const int del = 250; //milliseconds

//Constants to travel to and from HOME and ANALYSIS
int homePosition = 0;
//int analysisPosition = 0;
int currentPosition = 0;
bool positionsSet = false;

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(enPin, OUTPUT);

  digitalWrite(enPin, LOW);

  Serial.begin(9600);
}

void loop() {
  //Serial.println(homePosition);
  int threshold = analogRead(buttonPin);
  //Serial.println(threshold);
  if (threshold < 100) { //If below this limit, no button is pressed
    digitalWrite(stepPin, LOW);
  } 
  else if (threshold < 200) { //If below 200, Button 1 is pressed (CW)
    moveMotorCW();
  } 
  else if (threshold > 200 && threshold < 300) { //If between 200 and 300, Button 2 is pressed (CCW)
    moveMotorCCW();
  } 
  else if (threshold > 400 && threshold < 500) { //If between 400 and 500, Button 3 is pressed (Set Positions)
    // Move the motor back to the original position (homePosition)
    while (currentPosition != homePosition) {
      if (currentPosition < homePosition) {
        moveMotorCW(); // Move clockwise
      } else {
        moveMotorCCW(); // Move counterclockwise
      }
    }
  }
    else if (threshold > 800 && threshold < 1100) { //If between 400 and 500, Button 3 is pressed (Set Positions)
    // Move the motor back to the original position (homePosition)
    homePosition = currentPosition;


  }





  //Serial.print(digitalRead(dirPin));
  //Serial.println(currentPosition);
  //Serial.println()
  // Your other code continues here
}

void moveMotorCW() {
  digitalWrite(dirPin, HIGH); // Set direction as clockwise
  stepMotor();
}

void moveMotorCCW() {
  digitalWrite(dirPin, LOW); // Set direction as counterclockwise
  stepMotor();
}

void stepMotor() {
  // Step the motor
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(del); // Adjust speed by changing delay
  digitalWrite(stepPin, LOW);
  delayMicroseconds(del); // Adjust speed by changing delay
  
  // Update currentPosition
  if (digitalRead(dirPin) == HIGH) {
    currentPosition++;
  } else {
    currentPosition--;
  }
}
