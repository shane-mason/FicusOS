#define TOP_PANEL_WIDTH 420
#define TOP_PANEL_HEIGHT 40
#define BOTTOM_PANEL_WIDTH 420
#define BOTTOM_PANEL_HEIGHT 210
#define PADDING_LEFT 30
#define TOP_PANEL_Y 30
#define BOTTOM_PANEL_Y 95

//GFXcanvas1 topPanel(TOP_PANEL_WIDTH, TOP_PANEL_HEIGHT);
//GFXcanvas1 bottomPanel(BOTTOM_PANEL_WIDTH, BOTTOM_PANEL_HEIGHT);

class GraphicalShell{

  private:
    GFXcanvas1 topPanel = GFXcanvas1(TOP_PANEL_WIDTH, TOP_PANEL_HEIGHT);
    GFXcanvas1 bottomPanel = GFXcanvas1(BOTTOM_PANEL_WIDTH, BOTTOM_PANEL_HEIGHT);

  public:
    GraphicalShell(){

    }

    void setup(){
      topPanel = GFXcanvas1(TOP_PANEL_WIDTH, TOP_PANEL_HEIGHT);
      bottomPanel = GFXcanvas1(BOTTOM_PANEL_WIDTH, BOTTOM_PANEL_HEIGHT);
      draw_shell();
      tft.setCursor(30, 35); 
      tft.setTextSize(2);
      tft.println("Use line buffer to enter command.");
      topPanel.setTextSize(2);
      bottomPanel.setTextSize(2);
    }

    void add_command(char* command){
      //draw_shell();

      int clen = strlen(command);
      if(clen<25){
        topPanel.setTextSize(3);
      }
      else if(clen < 60){
        topPanel.setTextSize(2);
      }
      else{
        topPanel.setTextSize(1);
      }

      topPanel.fillScreen(0);
      bottomPanel.fillScreen(0);

      topPanel.setCursor(0, 5);
      topPanel.print(">");
      topPanel.println(command);

      tft.drawBitmap(PADDING_LEFT, TOP_PANEL_Y, topPanel.getBuffer(),
      topPanel.width(), topPanel.height(), GREEN0, COBALT);

      //bottomPanel.setCursor(12, 5);
      //bottomPanel.print("Hang tight, getting that for you!");

      tft.drawBitmap(PADDING_LEFT, BOTTOM_PANEL_Y, bottomPanel.getBuffer(),
      bottomPanel.width(), bottomPanel.height(), ORANGE, COBALT);
      
    }

    void add_response(char* response){

      bottomPanel.fillScreen(0);

      bottomPanel.setCursor(0, 5);
      bottomPanel.print(response);

      tft.drawBitmap(PADDING_LEFT, BOTTOM_PANEL_Y, bottomPanel.getBuffer(),
      bottomPanel.width(), bottomPanel.height(), BRIGHT_BLUE, COBALT);
      
    }
    
    void add_error(char* err){

      bottomPanel.fillScreen(0);

      bottomPanel.setCursor(0, 5);
      bottomPanel.print(err);

      tft.drawBitmap(PADDING_LEFT, BOTTOM_PANEL_Y, bottomPanel.getBuffer(),
      bottomPanel.width(), bottomPanel.height(), RED, COBALT);
      
    }

    void draw_shell(){
      tft.setRotation(1);
      tft.fillScreen(COBALT);
      tft.setCursor(20, 5);
      tft.setTextColor(YELLOW);  
      tft.setTextSize(2);
      tft.println("FICUS SHELL 0.4");
      tft.drawRoundRect(20, 25, TOP_PANEL_WIDTH+20, TOP_PANEL_HEIGHT+10, 5, DARK_GRAY);
      tft.drawRoundRect(20, 90, BOTTOM_PANEL_WIDTH+20, BOTTOM_PANEL_HEIGHT+10, 5, DARK_GRAY);
    }
};