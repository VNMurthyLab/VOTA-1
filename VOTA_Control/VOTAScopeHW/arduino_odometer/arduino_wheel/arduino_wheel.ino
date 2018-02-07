const int PIN_CS = 3;
const int PIN_CLOCK = 7;
const int PIN_OUTPUT = 5;
byte s[10]={0,0,0,0,0,0,0,0,0,0};
int incomingbytes=0;

void setup() {
 Serial.begin(250000);
 pinMode(PIN_CS, OUTPUT);
 pinMode(PIN_CLOCK, OUTPUT);
 pinMode(PIN_OUTPUT, INPUT);
 
 digitalWrite(PIN_CLOCK, HIGH);
 digitalWrite(PIN_CS, LOW);
}

void loop() {
 
 digitalWrite(PIN_CS, HIGH);
 delayMicroseconds(1);
 digitalWrite(PIN_CS, LOW);
 delayMicroseconds(1);
 

 for (int i=0; i<16; i++) {
   digitalWrite(PIN_CLOCK, LOW);
   digitalWrite(PIN_CLOCK, HIGH);
   if (i<10) s[i]=digitalRead(PIN_OUTPUT);
 }
 digitalWrite(PIN_CLOCK, LOW);
 digitalWrite(PIN_CLOCK, HIGH);

 Serial.flush();
 
 if (Serial.available() > 0) {
 incomingbytes=Serial.read();
 Serial.write(s,10);
 }
}
