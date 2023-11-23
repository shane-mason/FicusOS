unsigned long showTriangles() {
  unsigned long start;
  int           n, i, cx = tft.width()  / 2 - 1,
                      cy = tft.height() / 2 - 1;

  
  n     = min(cx, cy);
  start = micros();
  for(i=0; i<n; i+=5) {
    tft.drawTriangle(
      cx    , cy - i, // peak
      cx - i, cy + i, // bottom left
      cx + i, cy + i, // bottom right
      tft.color565(i, 200, 20));
    delay(20);
  }

  return micros() - start;
}

void start_screen(){
  tft.fillScreen(HX8357_BLACK);
  tft.setRotation(0);
  showTriangles();
  tft.setRotation(1);
  showTriangles();
  tft.setRotation(2);
  showTriangles();
  tft.setRotation(3);
  showTriangles();

}

