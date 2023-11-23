#include <LiquidCrystal_I2C.h>


#define BUFFER_LEN 80
#define LCD_ROWS 4
#define LCD_COLS 20

class LCDBuffer{

  private:
    int8_t cursor = 0;
    LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, LCD_COLS, LCD_ROWS);
    bool dirty = false;

  public:
    char buffer[BUFFER_LEN];

    LCDBuffer(){
      dirty = false;
    }

    void setup(){
      clear();
      lcd.init(); //initialize the lcd
      lcd.backlight(); //open the backlight 
      
      lcd.setCursor(0, 0);
      lcd.cursor();
      lcd.blink();
      lcd.print("Starting up!");
      dirty = true;
    }

    void log(const char* msg){
      clear();
      lcd.print(msg);
      dirty = true;
    }

    void full_print(){
      lcd.clear();
      bool ended = false;
      uint8_t r = 0;
      uint8_t c = 0; 
      uint8_t i = 0;
      while(!ended){
        if(buffer[i] != '\0'){
          lcd.setCursor(c,r);
          lcd.print(buffer[i]);
          c++;
          if(c>=LCD_COLS){
            c=0;
            r++;
          }
        }
        else{
          ended = true;
        }
        i++;
      }  
    }

    void incremental_print(){

      uint8_t r = (uint8_t)(cursor/LCD_COLS);
      int8_t c = (uint8_t)(cursor%LCD_COLS); 

      lcd.setCursor(c,r);
      lcd.print(buffer[cursor]);
    }

    void increment_cursor(){
      if(cursor < BUFFER_LEN-1){
        cursor++;
      } 
    }

    void decrement_cursor(){
      if(cursor>0){
        cursor--;
      }
      buffer[cursor] = '\0';
    }

    void add_char(uint8_t c){
    
      if(dirty){
        clear();
      }
      buffer[cursor] = c;
      incremental_print();
      increment_cursor();
    }

    void backspace(){
        decrement_cursor();    
        full_print();
    }

    void clear(){
      cursor = 0;
      for(uint8_t i=0; i<BUFFER_LEN; i++){
        buffer[i] = '\0';
      }
      lcd.clear();
      lcd.setCursor(0,0);
      dirty = false;
    }
};
