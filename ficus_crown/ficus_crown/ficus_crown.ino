// Double-buffered 8-bit Adafruit_GFX-compatible framebuffer for PicoDVI.
// Animates without redraw flicker. Requires Adafruit_GFX >= 1.11.4

#include <PicoDVI.h>
#include "ficus_colors_rgb565.h"
#include "graphical_shell_dvi.h"
#include "ficus_vine_format.h"

// #define USE_DVI

// Here's how a 320x240 8-bit (color-paletted) framebuffer is declared.
// Second argument ('true' here) enables double-buffering for flicker-free
// animation. Third argument is a hardware configuration -- examples are
// written for Adafruit Feather RP2040 DVI, but that's easily switched out
// for boards like the  Pimoroni Pico DV (use 'pimoroni_demo_hdmi_cfg') or
// Pico DVI Sock ('pico_sock_cfg').
DVIGFX8 f_display(DVI_RES_320x240p60, false, adafruit_feather_dvi_cfg);

// A 400x240 mode is possible but pushes overclocking even higher than
// 320x240 mode. SOME BOARDS MIGHT SIMPLY NOT BE COMPATIBLE WITH THIS.
// May require selecting QSPI div4 clock (Tools menu) to slow down flash
// accesses, may require further over-volting the CPU to 1.25 or 1.3 V.
//DVIGFX8 f_display(DVI_RES_400x240p60, true, adafruit_feather_dvi_cfg);
GraphicalShellDVI f_shell(&f_display);

#define READ_BUFFER_LEN 1024
#define BYTE_BUFFER_LEN 2

char read_buffer[READ_BUFFER_LEN];
char byte_buffer[BYTE_BUFFER_LEN];

void setup() { // Runs once on startup
  Serial1.begin(38400);
  if (!f_display.begin()) { // Blink LED if insufficient RAM
    
    pinMode(LED_BUILTIN, OUTPUT);
    
    for (;;) digitalWrite(LED_BUILTIN, (millis() / 500) & 1);
  }

  //setup colors
  for(uint16_t i = 0; i < sizeof(color_array); i++){
    Serial.print(i);
    f_display.setColor(i, color_array[i]);
  }

  f_display.setColor(255, 0xFFFF); // Last palette entry = white
  f_display.swap(false, true); // Duplicate same palette into front & back buffers
  
  wait_screen();
  wait_screen();
  wait_screen();
  Serial.println("Starting main loop");
  f_shell.setup();
}


void wait_screen(){
  f_display.fillScreen(0);
  f_display.setFont();
  f_display.setTextSize(1);
  const uint16_t cx = f_display.width() / 2;  
  const uint16_t cy = f_display.height() / 2; 
  const uint16_t size_x = (f_display.width() / 8) + 53;
  const uint16_t size_y = (f_display.height() / 8) - 10;
  const uint16_t start_x = cx - size_x/2;
  const uint16_t start_y = cy - size_y/2;

  
  f_display.setCursor(cx-20, cy-4);
  f_display.setTextColor(255, 0);
  f_display.print(F("FicusOS"));
  delay(1000);
  f_display.swap();

  for(int8_t i = 1; i<23; i++){
    int16_t offset = i * 5;
    f_display.drawRoundRect(start_x-offset, start_y-offset, size_x+(offset*2), size_y+(offset*2), 8, i);
    f_display.setCursor(cx-20, cy-4);
    
    f_display.print(F("FicusOS"));

    f_display.setTextColor(i, 0);
    delay(100);
    f_display.swap();
  }
  
}


// received incoming shell command header
void handle_shell_command(){
  uint16_t len = Serial1.readBytesUntil(VINE_END, read_buffer, READ_BUFFER_LEN);
  read_buffer[len] = '\0';
  Serial.println("GOT COMMAND: ");
  Serial.println(read_buffer);
  f_shell.add_command(read_buffer);
}

// received incoming shell response header
void handle_shell_response(){
  uint16_t len = Serial1.readBytesUntil(VINE_END, read_buffer, READ_BUFFER_LEN);
  read_buffer[len] = '\0';
  Serial.println("GOT RESPONSE: ");
  Serial.println(read_buffer);
  f_shell.add_response(read_buffer);
}

// received incoming error header
void handle_error(){
  uint16_t len = Serial1.readBytesUntil(VINE_END, read_buffer, READ_BUFFER_LEN);
  read_buffer[len] = '\0';
  Serial.println("GOT Err: ");
  Serial.println(read_buffer);
  f_shell.add_error(read_buffer);
}

//received incoming keypress header
void handle_keypress(){
  uint16_t len = Serial1.readBytesUntil(VINE_END, byte_buffer, BYTE_BUFFER_LEN);
  byte_buffer[len] = '\0';
  Serial.println("GOT KEYPRESS: ");
  Serial.println(byte_buffer);
  f_shell.add_keypress(byte_buffer);
   
}

void loop() {
  
  if(Serial1.available() > 0){
    uint8_t header_byte = Serial1.read();
    Serial.println("Data available");
    switch (header_byte){
        case VINE_SHELL:
          handle_shell_command();
          break;

        case VINE_SHELL_RESPONSE:
          handle_shell_response();
          break;

        case VINE_SHELL_ERROR:
          handle_error();
          break;

        case VINE_KEYPRESS:
          handle_keypress();
          break;

        case VINE_GFX_START:
          break;

        default:
          Serial.println("Incoming messages started with unknown header: ");
          Serial.println(header_byte); 
    }

    

  }    


  
}














