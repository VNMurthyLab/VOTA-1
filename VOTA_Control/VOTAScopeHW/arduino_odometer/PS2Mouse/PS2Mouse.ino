/*
USB Pinout (Left to Right, USB symbol up)
4: GND
3: Clk
2: Data
1: Vcc
*/

#include "PS2Mouse.h"
int incomingbytes=0;
byte s[8] = {0,0,0,0,0,0,0,0};

PS2Mouse mouse(5,6);

void setup(){
  Serial.begin(250000);
  mouse.begin();
}

void loop(){

if (Serial.available()>0) {
  incomingbytes = Serial.read();
  uint8_t stat;
  int x,y;
  mouse.getPosition(stat,x,y);
  if (incomingbytes == 114){
    for (int i = 0; i<8; i++){
      s[i] = bitRead(x,i);
    }
    Serial.write(s,8);

    for (int i = 0; i<8; i++){
      s[i] = bitRead(y,i);
    }
    Serial.write(s,8);

    
    }
  }
}



