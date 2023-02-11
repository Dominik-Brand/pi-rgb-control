// Published under GPL v3 by Dominik Brand on 2023-02-11
// Version 1.0
// Tested with Raspberry Pi 3b and Arduino Uno + Mega
#include <Adafruit_NeoPixel.h>
#include <SoftwareSerial.h>
#include <string.h>
#include <stdlib.h>
#include <EEPROM.h>
// Which pin on the Arduino is connected to the NeoPixels?
#define PIN 2
enum class MODE
{
  COLOR,
  RAINBOW,
  SOLIDLOOP,
  STARFALL,
  CYCLE
};
// How many NeoPixels are attached to the Arduino?
const int NUMPIXELS = 300;
MODE NEWMODE = MODE::COLOR;
bool modechanged = false;
bool firstboot = true;
bool serialIn = false;
unsigned long currTime;
String rgb = "";
String receivedString = "";
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN);
void setup()
{
  Serial.begin(2400);
  pixels.begin();
}
void writeEEPROM(int address, int number)
{ 
  EEPROM.write(address, number >> 8);
  EEPROM.write(address + 1, number & 0xFF);
}
int readEEPROM(int address)
{
  return (EEPROM.read(address) << 8) + EEPROM.read(address + 1);
}
void wipe (int red,int green,int blue){
  for (int i = 0; i < NUMPIXELS; i++)
  {
    // takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(red, green, blue));
  }
  pixels.show();
}
void color (int red,int green,int blue){
  writeEEPROM(20, red);
  writeEEPROM(30, green);
  writeEEPROM(40, blue);
  while (Serial.available() == 0 & serialIn == false){
    currTime = millis();
    for (int i = 0; i < NUMPIXELS; i++)
    {
      wipe(red, green, blue);
    }
    pixels.show();
    while(currTime + 10000 < millis()) {
      if(Serial.available() > 0){
        serialIn = true;
        break;
      }
    }
  }
}
void solidloop (uint8_t wait) {
  while (Serial.available() == 0 & serialIn == false){
    for (int i = 0; i < NUMPIXELS; i++)
    {
      pixels.setPixelColor(i, Wheel(i * 256 / pixels.numPixels()));
    }
    pixels.show();
    if(Serial.available() > 0){
      serialIn = true;
      break;
    }
    delay(wait);
  }
}
void starfall (uint8_t speed){ //option for setting colors to be implemented
  wipe(0,0,0);
  int i;
  while (Serial.available() == 0 & serialIn == false){
    i = 0;
    while (i < NUMPIXELS/10){
      pixels.setPixelColor(random(NUMPIXELS), pixels.Color(random(255), random(255), random(255)));
      delay(speed);
      for (int j = 0; j < 5; j++){
        pixels.setPixelColor(random(NUMPIXELS), pixels.Color(0, 0, 0));
      }
      pixels.show();
      i++;
    }
  }
}
uint32_t Wheel(byte WheelPos) {
  if(WheelPos < 85) {
   return pixels.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  } else if(WheelPos < 170) {
   WheelPos -= 85;
   return pixels.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else {
   WheelPos -= 170;
   return pixels.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
}
// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle(uint8_t wait) {
  uint16_t i, j;
  while (Serial.available() == 0 & serialIn == false){
    for(j=0; j<256*5; j++) { // 5 cycles of all colors on wheel
      for(i=0; i< pixels.numPixels(); i++) {
        pixels.setPixelColor(i, Wheel((i + j) & 255));
      }
      pixels.show();
      if(Serial.available() > 0){
        serialIn = true;
        break;
      }
    delay(wait);
    }
  }
}
void colorCycle(uint8_t wait) {
  uint16_t x, y;
  while (Serial.available() == 0 & serialIn == false){
    for(y=0; y<256*5; y++) { // 5 cycles of all colors on wheel
      for(x=0; x< pixels.numPixels(); x++) {
        pixels.setPixelColor(x, Wheel(((x * 256)) + y & 255));
      }
      pixels.show();
      if(Serial.available() > 0){
        serialIn = true;
        break;
      }
    delay(wait);
    }
  }
}
void loop()
{
  char *input;
  int red, green, blue, len;
  serialIn = false;
  if(firstboot){
    red = readEEPROM(20);
    green = readEEPROM(30);
    blue = readEEPROM(40);
    firstboot = false;
    color(red,green,blue);
  }
  if (Serial.available() > 0)
  {
    do {
      receivedString = Serial.readStringUntil('\n');
      len = receivedString.length();
    }
    while (len<2);
    input = &receivedString[0];
    char *s = strtok_r(input, ",", &input);


    if (strstr(s,"COLOR"))
    {
      NEWMODE = MODE::COLOR;
      modechanged = true;
      red = atoi(strtok_r(input, ",",&input));
      green = atoi(strtok_r(input, ",",&input));
      blue = atoi(strtok_r(input, ",",&input));
    }
    else if (strstr(s,"RAINBOW"))
    {
      NEWMODE = MODE::RAINBOW;
      modechanged = true;
    }
    else if (strstr(s,"SOLIDLOOP"))
    {
      NEWMODE = MODE::SOLIDLOOP;
      modechanged = true;
    }
    else if (strstr(s,"STARFALL"))
    {
      NEWMODE = MODE::STARFALL;
      modechanged = true;
    }
    else if (strstr(s,"CYCLE"))
    {
      NEWMODE = MODE::CYCLE;
      modechanged = true;
    }
    else
    {
      Serial.println("NAK");
    }

    if (modechanged)
    {
      Serial.println("ACK");
      int timeDelay;
      switch (NEWMODE)
      {
      case MODE::COLOR:
        modechanged = false;
        color(red,green,blue);
        break;
      case MODE::STARFALL:
        modechanged = false;
        starfall(12);
        break;
      case MODE::RAINBOW:
        timeDelay = atoi(strtok_r(input, ",",&input));
        if(timeDelay==0 || timeDelay >=1000){
          timeDelay = 50;
        }
        modechanged = false;
        rainbowCycle(timeDelay);      
        break;
      case MODE::SOLIDLOOP:
        timeDelay = 50;
        modechanged = false;
        solidloop(timeDelay);
        break;
      case MODE::CYCLE:
        timeDelay = atoi(strtok_r(input, ",",&input));
        if(timeDelay==0 || timeDelay >=1000){
          timeDelay = 50;
        }
        modechanged = false;
        colorCycle(timeDelay);
        break;
      default:
        break;
      }
    } 
  }
}