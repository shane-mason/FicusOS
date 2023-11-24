#define PANEL_WIDTH 480
#define PANEL_HEIGHT 320

class GraphicsManager{

  private:
    GFXcanvas1 topPanel = GFXcanvas1(PANEL_WIDTH, PANEL_HEIGHT);
  public:

    void thanks(){
      int count = 0;
      int top = 0;
      while(count < 10){
        top += 20;
        tft.fillScreen(DARK_BROWN);  
        delay( 250 );
        tft.setCursor(70, top);
        tft.setTextColor(ORANGE);  
        tft.setTextSize(5);
        tft.println("Happy");
        delay( 250 );
        tft.setTextColor(BRIGHT_ORANGE);  
        tft.setCursor(70, top+60);
        tft.println("Thanksgiving!");
        delay( 2000 );
        count++;
      }
      tft.fillScreen(ORANGE);
    }  


};
