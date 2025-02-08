#ifndef GRAPHICAL_SHELL_H
#define GRAPHICAL_SHELL_H

#include "ficus_colors_rgb565.h"

#define WIDGET_PADDING_X 0
#define WIDGET_PADDING_Y 5
#define TEXT_PADDING_X 25
#define LINE_SPACING 12
#define TOP_WIDGET_Y 20
#define TOP_WIDGET_HEIGHT 30
#define BOTTOM_WIDGET_Y 60
#define BOTTOM_WIDGET_HEIGHT 150
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
      widget_width = display->width();
      strcpy(command_text, "Welcome to Ficus Shell DVI!");
      strcpy(response_text,"Press enter to execute buffer.\nCommands and responses will show up here.\n\nPress escape to clear.");
    }

    void setup(){
      draw_shell();
    }

    void draw_top_panel(){
      display->fillRect(WIDGET_PADDING_X, TOP_WIDGET_Y, widget_width, TOP_WIDGET_HEIGHT, COLOR_ALMOSTBLACK);
      display->drawRect(WIDGET_PADDING_X, TOP_WIDGET_Y, widget_width, TOP_WIDGET_HEIGHT, COLOR_STEELBLUE);
      display->setTextColor(COLOR_YELLOW);
      draw_text(command_text, TOP_WIDGET_Y+5);
    }

    void draw_bottom_panel(){
      display->fillRect(WIDGET_PADDING_X, BOTTOM_WIDGET_Y, widget_width, BOTTOM_WIDGET_HEIGHT, COLOR_ALMOSTBLACK);
      display->drawRect(WIDGET_PADDING_X, BOTTOM_WIDGET_Y, widget_width, BOTTOM_WIDGET_HEIGHT, COLOR_STEELBLUE);
      display->setTextColor(COLOR_SPRINGGREEN);
      draw_text(response_text, BOTTOM_WIDGET_Y+5);
    }

    void draw_error_panel(){
      display->fillRect(WIDGET_PADDING_X, BOTTOM_WIDGET_Y, widget_width, BOTTOM_WIDGET_HEIGHT, COLOR_ALMOSTBLACK);
      display->drawRect(WIDGET_PADDING_X, BOTTOM_WIDGET_Y, widget_width, BOTTOM_WIDGET_HEIGHT, COLOR_RED);
      display->setTextColor(COLOR_RED);
      draw_text(response_text, BOTTOM_WIDGET_Y+5);
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

    void add_keypress(char* press){
      //todo
    }

    void draw_shell(){
      display->fillScreen(0);
      
      // Setup the app labels
      display->setTextSize(1);
      display->setTextColor(COLOR_DODGERBLUE);
      draw_text("Ficus Shell - 0.4 DVI", 5);
      //draw_text(response_text, 5);

      //draw rest of the pieces
      draw_top_panel();
      draw_bottom_panel();
      display->swap();
    }

    void draw_text(char* text, uint16_t y_start){
      char *end, *r, *tok;
      uint16_t current_y = y_start;
      r = end = strdup(text);
      assert(end != NULL);

      while ((tok = strsep(&end, "\n")) != NULL) {
        display->setCursor(TEXT_PADDING_X, current_y);
        display->print(tok);
        current_y += LINE_SPACING;
      }

      free(r);
     
    }

};
#endif