#include "hid_keys.h"
#include "scan_ascii.h"
#include "shift_scan_ascii.h"
#include "ficus_vine_format.h"
#include "lcd_buffer.h"

#define ACTION_BACKSPACE 8
#define ACTION_ENTER 10
#define ACTION_ESCAPE 27 
#define KEY_MAP_LEN 5

class LineBufferKB{

  private:
    LCDBuffer iobuffer;


  public:

    LineBufferKB(){
       
    }

    void setup(){
      iobuffer.setup();
    }

    void log(const char* msg){
      iobuffer.log(msg);
    }


    void map_report(uint8_t const *report, uint16_t len){
      //a key has been pressed - lets map it to an ascii char

      //is shift pressed?
      bool shift = false;
      if(report[0] == KEY_MOD_LSHIFT || report[0] == KEY_MOD_RSHIFT){
        shift = true;
      }
      bool ctl = false;

      for(uint16_t i=2; i<len; i++){
        int scan = int(report[i]);
        int key_code = 0;
        if(shift){
          key_code = shift_scanmap[scan];
        }
        else{
          key_code = scanmap[scan]; 
        }

        if(key_code!=0){
          //send the keypress event
          Serial.printf("%c", key_code);
          Serial1.write(VINE_KEYPRESS);
          Serial1.write(key_code);
          Serial1.write(VINE_END);
          Serial1.flush();
          if(key_code == ACTION_BACKSPACE){
            //backspace
            iobuffer.backspace();
          }
          else if(key_code == ACTION_ESCAPE){
            //escape is pressed, so clear the buffer
            iobuffer.clear();
          }
          else if(key_code == ACTION_ENTER){
            //enter has been pressed - send the buffer
            Serial.println("Sending buffer:");
            Serial.println(iobuffer.buffer);
            Serial1.write(VINE_SHELL);
            Serial1.print(iobuffer.buffer);
            Serial1.write(VINE_END);
            Serial1.flush();
            iobuffer.clear();
          }
          else{
            iobuffer.add_char(key_code);
          }

        } 
        else{
          
        }
      }

    }

};