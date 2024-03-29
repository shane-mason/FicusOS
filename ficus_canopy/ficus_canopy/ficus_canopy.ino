
#include <SPI.h>
#include "Adafruit_GFX.h"
#include "Adafruit_HX8357.h"
#include "ficus_vine_format.h"
#include <Adafruit_NeoPixel.h>

// These are 'flexible' lines that can be changed
#define TFT_CS 1
#define TFT_DC 9
#define TFT_RST 10

/*

Pico wiring:

Display->Pico

GND   ->  GND       =>pin 23
3-5V  ->  3V3(OUT)  =>pin 36
CLK   ->  SPI SCK   => GP18 
MISO  ->  SPI RX    => GP16
MOSI  ->  SPI TX    => GP19
CS    ->  SPI CSn   => GP17
D/C   ->            => GP20
Reset ->            => GP21


Waveshare zero:

Display->Waveshare Zero
GND   ->  GND
3-5   ->  3v
CLK   ->  SPI SCK   => GP2 
MISO  ->  SPI RX    => GP0
MOSI  ->  SPI TX    => GP3
CS    ->  SPI CSn   => GP1
D/C   ->            => GP9
Reset ->            => GP10   

*/

// Use hardware SPI (on Uno, #13, #12, #11) and the above for CS/DC
Adafruit_HX8357 tft = Adafruit_HX8357(TFT_CS, TFT_DC, TFT_RST);

#include "shell_colors.h"
#include "start_screen.h"
#include "graphical_shell.h"
#include "graphics_manager.h"

#define LINE_BUFFER_LEN 255
#define BYTE_BUFFER_LEN 2
#define NEO_PIN 16
#define NEO_COUNT 1

char line_buffer[LINE_BUFFER_LEN];
char byte_buffer[BYTE_BUFFER_LEN];
uint8_t startByte = 0;

GraphicalShell gshell;
unsigned long last_time;
bool led_state = false;

GraphicsManager gman;

Adafruit_NeoPixel strip(NEO_COUNT, NEO_PIN, NEO_GRB + NEO_KHZ800);
unsigned long pixel_time;
uint8_t pixel_bright;

void setup() {
  Serial.begin(9600);
  Serial.println("Ficus TFT Starting Up");

  Serial1.setRX(13);
  Serial1.begin(38400);
  
  tft.begin();
  tft.setRotation(1);
  start_screen(); 
  gshell.setup();
  pinMode(16, OUTPUT);
  last_time = millis();
  strip.begin();
  strip.setBrightness(25);
  strip.show(); // Initialize all pixels to 'off'
  pixel_time = last_time;
  pixel_bright = 0;
  Serial.println("Setup completed...");
}

uint32_t Wheel(byte WheelPos) {
  if(WheelPos < 85) {
   return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  } else if(WheelPos < 170) {
   WheelPos -= 85;
   return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else {
   WheelPos -= 170;
   return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial1.available() > 0) {
    Serial.println("Got start bytes");
    // read the incoming byte:
    startByte = Serial1.read();
    Serial.println(startByte);

    if(startByte == VINE_SHELL){
      uint16_t len = Serial1.readBytesUntil(VINE_END, line_buffer, LINE_BUFFER_LEN); 
      line_buffer[len] = '\0';
      Serial.println("Display got shell command:");
      Serial.println(line_buffer);
      if(strcmp(line_buffer,"thanks") == 0){
          Serial.println("IN COMMAND: thanks");
          gman.thanks();
      } 
      else{
        gshell.add_command(line_buffer);
      }

    }
    else if(startByte == VINE_SHELL_RESPONSE){
      uint16_t len = Serial1.readBytesUntil(VINE_END, line_buffer, LINE_BUFFER_LEN); 
      line_buffer[len] = '\0';
      Serial.println("Display Got Shell response:");
      Serial.println(line_buffer);
      gshell.add_response(line_buffer);
    }
    else if(startByte == VINE_SHELL_ERROR){
      uint16_t len = Serial1.readBytesUntil(VINE_END, line_buffer, LINE_BUFFER_LEN); 
      line_buffer[len] = '\0';
      Serial.println("Display Got Shell error:");
      Serial.println(line_buffer);
      gshell.add_error(line_buffer);

    }
    else if(startByte == VINE_KEYPRESS){
      uint16_t len = Serial1.readBytesUntil(VINE_END, byte_buffer, BYTE_BUFFER_LEN); 
      uint8_t pressed = byte_buffer[0];
      //who cares that it was pressed
    }
    else if(startByte == VINE_GFX_START){
      uint16_t len = Serial1.readBytesUntil(VINE_END, line_buffer, LINE_BUFFER_LEN); 
      line_buffer[len] = '\0';
      Serial.println("Display Got GFX Request");
      Serial.println(line_buffer);
      gshell.add_command(line_buffer);
      tft.fillScreen(PURPLE);
    }
  }
  if((millis()-pixel_time)>80){
    pixel_bright++;
    strip.setPixelColor(0, Wheel((pixel_bright & 255)));
    strip.show();
    pixel_time = millis();
    
  }
  if((millis()-last_time)>1000){
    Serial.println("Looping");
    Serial.printf("%d %d\n", last_time, millis());
  /*
    if( led_state == true ){
      led_state = false;
      digitalWrite(13, LOW);
    }
    else{
      led_state = true;
      digitalWrite(13, HIGH);

    }
    */
    last_time = millis();
  }
}

