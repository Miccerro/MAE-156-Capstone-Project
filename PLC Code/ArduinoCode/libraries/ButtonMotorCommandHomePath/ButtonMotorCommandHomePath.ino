 //Define pin numbers:
const int stepPin = 7;
const int dirPin = 4;
const int enPin = 2;
int buttonPin = A0;

const int del = 250; //miliseconds

//Constants to travel to and from HOME and ANALYSIS
  int homePosition = 0;
  int analysisPosition = 0;
  int currentPosition = 0;
  bool positionsSet = false;



void setup() {
  pinMode(stepPin,OUTPUT);
  pinMode(dirPin,OUTPUT);
  pinMode(enPin,OUTPUT);

  digitalWrite(enPin,LOW);

  Serial.begin(9600);
  


}

void loop() {

  int threshold = analogRead(buttonPin);
  //Serial.println(threshold);
  digitalWrite(dirPin,HIGH); //CW

  if (threshold < 100){ //If below this limit, no button is pressed
    //Serial.println("Nothing Pressed");
    digitalWrite(stepPin, LOW);
  }

  else if (threshold < 200){ //If below 200, Button 1 is pressed
    //Serial.println("BUTTON1");

    digitalWrite(dirPin, HIGH); // Set direction as clockwise
    // Step the motor
    for(int i = 0; i < 200; i++) { // 200 steps for one revolution
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(del); // Adjust speed by changing delay
      digitalWrite(stepPin, LOW);
      delayMicroseconds(del); // Adjust speed by changing delay
    }
  }

  else if(threshold > 200 && threshold < 300){ //If below 300, but above 200 , Button 2 is pressed
    //Serial.println("BUTTON2");

    digitalWrite(dirPin, LOW); // Set direction as clockwise
    // Step the motor
    for(int i = 0; i < 200; i++) { // 200 steps for one revolution
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(del); // Adjust speed by changing delay
      digitalWrite(stepPin, LOW);
      delayMicroseconds(del); // Adjust speed by changing delay
    }
  }

  else if(threshold > 400 && threshold < 500){ //If below 300, but above 200 , Button 2 is pressed
    //Serial.println("BUTTON3");

    //positionsSet = true;
    }


    else {
      digitalWrite(stepPin, LOW);
    }

if (positionSet){

  currentPosition++;


}


  }


