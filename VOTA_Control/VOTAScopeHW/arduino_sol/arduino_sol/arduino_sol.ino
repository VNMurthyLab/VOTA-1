#include <SPI.h>

const int PIN_CS[4]={10,9,8,7};

byte incomingbytes[8]={B0,B0,B0,B0,B0,B0,B0,B0};
unsigned int v[4]={0,0,0,0};
char mark='a';

void setup() {
  // put your setup code here, to run once:
  Serial.begin(250000);
  Serial.flush();
  for (int i=0;i<4;i++){
    pinMode(PIN_CS[i],OUTPUT);
    }
   SPI.begin();  
   SPI.setClockDivider(SPI_CLOCK_DIV2);
}

void setOutput(int addr, unsigned int val)
{
  byte lowByte = val & 0xff;
  byte highByte = ((val >> 8) & 0xff) | 0x10;
   
  digitalWrite(addr,LOW);
  SPI.transfer(highByte);
  SPI.transfer(lowByte);
  digitalWrite(addr,HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  char mark='b';
//setOutput(PIN_CS[4],3500);
  if( Serial.available() >0){
   Serial.readBytes(&mark,1);
   if (mark=115){
    
    Serial.readBytes(&incomingbytes[0],8);
    for (int i=0;i<4;i++){
    v[i]=(incomingbytes[i*2] << 8) + incomingbytes[i*2+1];
    setOutput(PIN_CS[i],v[i]);
   }
   Serial.flush();
 }
   }
}
