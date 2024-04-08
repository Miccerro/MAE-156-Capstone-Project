const int stepPin = 5;
const int dirPin = 2;
const int enPin = 8;
const int numstep = 6400;

void setup() {
  // put your setup code here, to run once:
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin,OUTPUT);
  pinMode(enPin,OUTPUT);
  digitalWrite(enPin,LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(dirPin, HIGH);
  for(int x=0; x<numstep*5; x++){
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(50);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(50);
  }
  while(1){
  }
}
