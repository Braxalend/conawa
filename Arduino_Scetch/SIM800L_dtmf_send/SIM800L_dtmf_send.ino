#include <SoftwareSerial.h>                     
SoftwareSerial SIM800(8, 9);                    

String numCall_1 = "11111111111";
String numCall_2 = "22222222222";

#define pin_1 4 
#define pin_2 5 
#define pin_3 6 
#define pin_4 7 

uint8_t flag_1 = 0;
uint8_t flag_2 = 0;
uint8_t flag_3 = 0;
uint8_t flag_4 = 0;
 
void initGSM(void) {
  delay (2000);
  SIM800.begin(9600);
  Serial.println("AT+CLIP=1");
  SIM800.println("AT+CLIP=1");
  delay(300);
  Serial.println("AT+CMGF=1");
  SIM800.println("AT+CMGF=1");
  delay(300);
  Serial.println("AT+CSCS=\"GSM\"");
  SIM800.println("AT+CSCS=\"GSM\"");
  delay(300);
  Serial.println("AT+CNMI=2,2,0,0,0");
  SIM800.println("AT+CNMI=2,2,0,0,0");
  delay(300);
}

void  setup() {
  Serial.begin(9600);
  initGSM();
  pinMode (pin_1, INPUT);
  pinMode (pin_2, INPUT);
  pinMode (pin_3, INPUT);
  pinMode (pin_4, INPUT);
  if(digitalRead(pin_1) == 1){
    flag_1 = 1;
  }
  else {
    flag_1 = 0;
  }
  if(digitalRead(pin_2) == 1){
    flag_2 = 1;
  }
  else {
    flag_2 = 0;
  }
  if(digitalRead(pin_3) == 1){
    flag_3 = 1;
  }
  else {
    flag_3 = 0;
  }
  if(digitalRead(pin_4) == 1){
    flag_4 = 1;
  }
  else {
    flag_4 = 0;
  }

}

void loop() {
  if (flag_1 == 0 && digitalRead(pin_1) == 1) {
    outgoingcall(numCall_1, "1");
    flag_1 = 1;
  }
  if (flag_1 == 1 && digitalRead(pin_1) == 0) {
    outgoingcall(numCall_1, "7");
    flag_1 = 0;
  }
  if (flag_2 == 0 && digitalRead(pin_2) == 1) {
    outgoingcall(numCall_1, "2");
    flag_2 = 1;
  }
  if (flag_2 == 1 && digitalRead(pin_2) == 0) {
    outgoingcall(numCall_1, "8");
    flag_2 = 0;
  }
  if (flag_3 == 0 && digitalRead(pin_3) == 1) {
    outgoingcall(numCall_2, "1");
    flag_3 = 1;
  }
  if (flag_3 == 1 && digitalRead(pin_3) == 0) {
    outgoingcall(numCall_2, "7");
    flag_3 = 0;
  }
  if (flag_4 == 0 && digitalRead(pin_4) == 1) {
    outgoingcall(numCall_2, "2");
    flag_4 = 1;
  }
  if (flag_4 == 1 && digitalRead(pin_4) == 0) {
    outgoingcall(numCall_2, "8");
    flag_4 = 0;
  }

}

void outgoingcall(String callnumber, String dtmfcommand) {  
    String command;
    command = "ATD+" + callnumber + ";";
    Serial.println(command);
    SIM800.println(command);
    delay (10000);
    Serial.println("AT+VTD=2");
    SIM800.println("AT+VTD=2");
    delay (1000);
    Serial.println("AT+VTS=\"" + dtmfcommand + "\"");
    SIM800.println("AT+VTS=\"8\"");
    delay (5000);
    Serial.println("ATH");
    SIM800.println("ATH");
    delay (1000);
}
