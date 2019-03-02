/*
  RD10 - Чтение DI pin 10
  RA3  - Чтение AI pin 3
  WD10:1  - Запись 1 (HIGH) в DO pin 10
  WA4:255 - Запись 255 в AO pin 4 (ШИМ)
 */

#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT21
DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27,16,2);
byte symb_grad[8] =
{
B00111,
B00101,
B00111,
B00000,
B00000,
B00000,
B00000,
};

char operation;
char mode;
int pin_number;
int digital_value;
int analog_value;
int value_to_write;
int wait_for_transmission = 5;
unsigned long timing;
float h;
float t;


void set_pin_mode(int pin_number, char mode){
    /*
     mode:
     I: INPUT
     O: OUTPUT
     P: INPUT_PULLUP
     */
    switch (mode){
        case 'I':
            pinMode(pin_number, INPUT);
            break;
        case 'O':
            pinMode(pin_number, OUTPUT);
            break;
        case 'P':
            pinMode(pin_number, INPUT_PULLUP);
            break;
    }
}
void digital_read(int pin_number){
    digital_value = digitalRead(pin_number);
    Serial.print('D');
    Serial.print(pin_number);
    Serial.print(':');
    Serial.println(digital_value);
}
void analog_read(int pin_number){
    analog_value = analogRead(pin_number);
    Serial.print('A');
    Serial.print(pin_number);
    Serial.print(':');
    Serial.println(analog_value);
}
void digital_write(int pin_number, int digital_value){
  digitalWrite(pin_number, digital_value);
}
void analog_write(int pin_number, int analog_value){
  analogWrite(pin_number, analog_value);
}
void dht_read(){
        Serial.print('S');
        Serial.print(":");
        Serial.print(dht.readHumidity());
        Serial.print(":");
        Serial.print(dht.readTemperature());
}
void setup() {
    Serial.begin(9600); 
    Serial.setTimeout(100); 
  	lcd.init();
  	lcd.createChar(1, symb_grad);
	  dht.begin();
}
void loop() {

float h = dht.readHumidity();
float t = dht.readTemperature();

if (millis() - timing > 5000) {
  timing = millis();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Vlaga:         %");
  lcd.setCursor(10, 0);
  lcd.print(h, 1);
  lcd.setCursor(0, 1);
  lcd.print("Temper:        C");
  lcd.setCursor(14, 1);
  lcd.print("\1");
  lcd.setCursor(10, 1);
  lcd.print(t,1);
}
  
	if (Serial.available() > 0) {
        operation = Serial.read();
        delay(wait_for_transmission);
        mode = Serial.read();
        pin_number = Serial.parseInt();
        if (Serial.read()==':'){
            value_to_write = Serial.parseInt();
        }
        switch (operation){
            case 'R':
                if (mode == 'D'){
                    digital_read(pin_number);
                } else if (mode == 'A'){
                    analog_read(pin_number);
                } else {
                break;
                }
                break;
            case 'W':
                if (mode == 'D'){
                    digital_write(pin_number, value_to_write);
                } else if (mode == 'A'){
                    analog_write(pin_number, value_to_write);
                } else {
                    break;
                }
                break;
            case 'M':
                set_pin_mode(pin_number, mode);
                break;
			      case 'S':
                dht_read();
				        break;
            default:
                
              break;
        }
    }
}
