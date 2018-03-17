/****************************************************************************** 
SparkFun Big Easy Driver Basic Demo
Toni Klopfenstein @ SparkFun Electronics
February 2015
https://github.com/sparkfun/Big_Easy_Driver

Simple demo sketch to demonstrate how 5 digital pins can drive a bipolar stepper motor,
using the Big Easy Driver (https://www.sparkfun.com/products/12859). Also shows the ability to change
microstep size, and direction of motor movement.

Development environment specifics:
Written in Arduino 1.6.0

This code is beerware; if you see me (or any other SparkFun employee) at the local, and you've found our code helpful, please buy us a round!
Distributed as-is; no warranty is given.

Example based off of demos by Brian Schmalz (designer of the Big Easy Driver).
http://www.schmalzhaus.com/EasyDriver/Examples/EasyDriverExamples.html
******************************************************************************/
//Declare pin functions on Arduino
#define stp 2
#define dir 3
#define MS1 4
#define MS2 5
#define MS3 6
#define EN  7

//Declare variables for functions
char user_input;
int x;
int y;
int state = 0;

void setup() {
  pinMode(stp, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(MS1, OUTPUT);
  pinMode(MS2, OUTPUT);
  pinMode(MS3, OUTPUT);
  pinMode(EN, OUTPUT);
  resetBEDPins(); //Set step, direction, microstep and enable pins to default states
  Serial.begin(250000); //Open Serial connection for debugging
}

//Main loop
void loop() {
  while(Serial.available()){
      user_input = Serial.read(); //Read user input and trigger appropriate function
      digitalWrite(EN, LOW); //Pull enable pin low to set FETs active and allow motor control
      if (user_input =='f')
      {
         StepForwardDefault();
      }
      else if(user_input =='b')
      {
        ReverseStepDefault();
      }
      else
      {
        Serial.flush();
        }
      resetBEDPins();
  }
}

//Reset Big Easy Driver pins to default states
void resetBEDPins()
{
  digitalWrite(stp, LOW);
  digitalWrite(dir, LOW);
  digitalWrite(MS1, LOW);
  digitalWrite(MS2, LOW);
  digitalWrite(MS3, LOW);
  digitalWrite(EN, HIGH);
}

//Default microstep mode function
void StepForwardDefault()
{
  digitalWrite(dir, HIGH); //Pull direction pin low to move "forward"
  delay(10);
  for(x= 1; x<100; x++)  //Loop the forward stepping enough times for motion to be visible
  {
    digitalWrite(stp,HIGH); //Trigger one step forward
    delayMicroseconds(1400);
    digitalWrite(stp,LOW); //Pull step pin low so it can be triggered again
    delayMicroseconds(1000);
  }
}

//Reverse default microstep mode function
void ReverseStepDefault()
{
  digitalWrite(dir, LOW); //Pull direction pin high to move in "reverse"
  delay(10);
  for(x= 1; x<100; x++)  //Loop the stepping enough times for motion to be visible
  {
    digitalWrite(stp,HIGH); //Trigger one step
    delayMicroseconds(1400);
    digitalWrite(stp,LOW); //Pull step pin low so it can be triggered again
    delayMicroseconds(1000);
  }
}

