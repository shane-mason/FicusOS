#ifndef GRAPHICAL_SHELL_H
#define GRAPHICAL_SHELL_H

#include "ficus_colors_rgb565.h"

#define WIDGET_PADDING 5
#define TOP_WIDGET_Y 20
#define TOP_WIDGET_HEIGHT 30
#define BOTTOM_WIDGET_Y 60
#define BOTTOM_WIDGET_HEIGHT 170
#define WAITING_MESSAGE "Hang tight, getting a response to that..."

class GraphicalShellDVI{

  private:
    DVIGFX8* display;
    uint16_t cx;
    uint16_t cy;
    uint16_t widget_width;
    char command_text[255];
    char response_text[1024];

  public:

    GraphicalShellDVI(DVIGFX8* disp){
      display = disp;
      cx = display->width() / 2;
      cy = display->height() / 2;
      widget_width = display->width() + (WIDGET_PADDING*2);
      strcpy(command_text, "Welcome to Ficus Shell DVI!");
      strcpy(response_text,"Use input buffer to enter command and press enter.\nCommands and responses will show up here.\n\nPress escape to clear.");
    }

    void setup(){
      draw_shell();
    }

    void draw_top_panel(){
      display->fillRect(-WIDGET_PADDING, TOP_WIDGET_Y, widget_width, TOP_WIDGET_HEIGHT, COLOR_ALMOSTBLACK);
      display->drawRect(-WIDGET_PADDING, TOP_WIDGET_Y, widget_width, TOP_WIDGET_HEIGHT, COLOR_STEELBLUE);
      display->setTextColor(COLOR_YELLOW);
      display->setCursor(1, TOP_WIDGET_Y+5);
      display->print(command_text);
    }

    void draw_bottom_panel(){
      display->fillRect(-WIDGET_PADDING, BOTTOM_WIDGET_Y, widget_width, BOTTOM_WIDGET_HEIGHT, COLOR_ALMOSTBLACK);
      display->drawRect(-WIDGET_PADDING, BOTTOM_WIDGET_Y, widget_width, BOTTOM_WIDGET_HEIGHT, COLOR_STEELBLUE);
      display->setTextColor(COLOR_SPRINGGREEN);
      display->setCursor(1, BOTTOM_WIDGET_Y+5);
      display->print(response_text);
    }

    void draw_error_panel(){
      display->fillRect(-WIDGET_PADDING, BOTTOM_WIDGET_Y, widget_width, BOTTOM_WIDGET_HEIGHT, COLOR_ALMOSTBLACK);
      display->drawRect(-WIDGET_PADDING, BOTTOM_WIDGET_Y, widget_width, BOTTOM_WIDGET_HEIGHT, COLOR_RED);
      display->setTextColor(COLOR_RED);
      display->setCursor(1, BOTTOM_WIDGET_Y+5);
      display->print(response_text);
    }

    void add_command(char* text){
      strcpy(command_text, text);
      strcpy(response_text, WAITING_MESSAGE);
      draw_top_panel();
      draw_bottom_panel();
      display->swap();
    }

    void add_response(char* text){
      strcpy(response_text, text);
      draw_bottom_panel();
      display->swap();
    }

    void add_error(char* err){
      strcpy(response_text, err);
      draw_error_panel();
      display->swap();
    }

    void draw_shell(){
      display->fillScreen(0);
      
      // Setup the app labels
      display->setTextSize(1);
      display->setTextColor(COLOR_DODGERBLUE);
      display->setCursor(1, WIDGET_PADDING);
      display->print(F("Ficus Shell - 0.3 DVI"));
      
      //draw rest of the pieces
      draw_top_panel();
      draw_bottom_panel();
      display->swap();
    }

};
#endif