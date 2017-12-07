/*
A simple DAC code for MAX528/529

Hao Wu
Oct, 2017
*/

#include<SPI.h> // necessary library
const int csPin = 10;

byte incomingbytes[] = {0x00, 0x00};
char mark = 'a';

void initDAC() {
  digitalWrite(csPin, LOW);  
  // Address byte: set buffer mode.
  SPI.transfer(0x00);  
  // Data byte: all outs fully buffered.
  SPI.transfer(0xFF);
  digitalWrite(csPin, HIGH); 

  digitalWrite(csPin, LOW); 
  SPI.transfer(0xFF);
  SPI.transfer(0x00); 
  digitalWrite(csPin, HIGH); 
}


void writeDAC (byte channel, byte x) {
  // channel is output 0 - 7, or a combination of them
  // x is between 0x00(0) to 0xFF(255)
  digitalWrite(csPin, LOW);  
  SPI.transfer(channel);
  SPI.transfer(x);
  digitalWrite(csPin, HIGH);
}

void setup() {
  //setup serial communication
  Serial.begin(500000);
  Serial.flush();
  //set CS pin to output
  pinMode(csPin, OUTPUT);
  SPI.begin(); // wake up the SPI bus.
  SPI.setBitOrder(MSBFIRST);
  SPI.setClockDivider(SPI_CLOCK_DIV4); // Set SPI data rate to 16mhz/4. IE: 4mhz.
  initDAC();  

}



void loop() {
  // wait for serial command
  if (Serial.available()>0){
    //read first available byte to see if is a writing operation
  }
    Serial.readBytes(&mark,1);
    if (mark=='w'){
      mark = 'a';
      Serial.readBytes(&incomingbytes[0],2);
      writeDAC(incomingbytes[0],incomingbytes[1]);
    }
    Serial.flush();
}



