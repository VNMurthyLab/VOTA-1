#include <SPI.h>

const int PIN_SOL_1=5;
const int PIN_SOL_2=7;

byte incomingbytes=B0;
unsigned int wait_time=0;
char mark='a';

void setup() {
  // put your setup code here, to run once:
  Serial.begin(250000);
  Serial.flush();
  pinMode(PIN_SOL_1,OUTPUT);
  digitalWrite(PIN_SOL_1,LOW);
  pinMode(PIN_SOL_2,OUTPUT);
  digitalWrite(PIN_SOL_2,LOW);
}


void loop() {
  // put your main code here, to run repeatedly:


  if( Serial.available() >0){
   Serial.readBytes(&mark,1);
   if (mark==119){
    Serial.readBytes(&incomingbytes,1);
    wait_time=incomingbytes;
    digitalWrite(PIN_SOL_1,HIGH);
    delay(wait_time);
    digitalWrite(PIN_SOL_1,LOW);
    Serial.println(wait_time,DEC);
    Serial.flush();
      }
   else if (mark==111){
    Serial.println("sol on");
    digitalWrite(PIN_SOL_1,HIGH);
    Serial.flush();
      }
    else if (mark==102){
    Serial.println("sol off");
    digitalWrite(PIN_SOL_1,LOW);
    Serial.flush();}
    else if (mark==87){
    Serial.readBytes(&incomingbytes,1);
    wait_time=incomingbytes;
    digitalWrite(PIN_SOL_2,HIGH);
    delay(wait_time);
    digitalWrite(PIN_SOL_2,LOW);
    Serial.println(wait_time,DEC);
    Serial.flush();}
    else if (mark==79){
    Serial.println("sol on");
    digitalWrite(PIN_SOL_2,HIGH);
    Serial.flush();}
    else if (mark==70){
    Serial.println("sol off");
    digitalWrite(PIN_SOL_2,LOW);
    Serial.flush();}
      }
  }

