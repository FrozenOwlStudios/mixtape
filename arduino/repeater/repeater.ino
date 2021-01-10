#include<LiquidCrystal.h>

LiquidCrystal lcd(8,9,4,5,6,7);
int buf[30];
int buf_ptr=0;

void setup(){
	Serial.begin(9600);
	lcd.begin(16,2);
}


void loop(){
	buf_ptr=0;
	while(Serial.available()==0){
	}
	lcd.clear();
	while(Serial.available()){
		int ser_in = Serial.read();
		lcd.print(ser_in);
		buf[buf_ptr] = ser_in;
		buf_ptr++;
	}
	for(int i=0;i<buf_ptr;i++){
		Serial.write(buf[i]);
	}
	Serial.println();
}

