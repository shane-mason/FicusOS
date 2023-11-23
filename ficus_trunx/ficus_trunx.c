#include <stdio.h>
#include <string.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "pico/binary_info.h"
#include "vine_router.h"
#include <time.h>

const uint LED_PIN = 25;

void loop_forever()
{
  clock_t last_tick = time_us_64();
  bool led_state = false;
  while (1)
  {
    
    if (uart_is_readable(uart0))
    {
      puts("UART0 Readable");
      gpio_put(LED_PIN, 1);
      poll_vine(uart0);
      gpio_put(LED_PIN, 0);
    }
    if (uart_is_readable(uart1))
    {
      puts("UART1 Readable");
      gpio_put(LED_PIN, 1);
      poll_vine(uart1);
      gpio_put(LED_PIN, 0);
    }
    clock_t current = time_us_64();
    if((current-last_tick) > 333333){
      printf("%d %d\n", current, last_tick);
      if( led_state == true ){
        led_state = false;
      }
      else{
        led_state = true;
      }
      gpio_put(LED_PIN, led_state);
      last_tick = time_us_64();
    }
    /*  
    gpio_put(LED_PIN, 1);
    sleep_ms(250);
    gpio_put(LED_PIN, 0);
    sleep_ms(250);
    puts("Looping");
    */    
  
  }

}

void test_loop(){
  int count = 0;
  while(1){
    count+=1;
    printf("Count: %d\n", count);
    sleep_ms(250);
    while (uart_is_readable(uart0))
    {
      char c = uart_getc(uart0);
      printf("UART0: %c\n", c);
      
    }
    while (uart_is_readable(uart1))
    {
      char c = uart_getc(uart1);
      printf("UART1: %c\n", c);  
    }
    uart_puts(uart0,"FIG Statement on 0");
    uart_puts(uart1,"FIG Statement on 1");
    

  }
}




int main()
{
  bi_decl(bi_program_description("FicusOS Trunx"));
  bi_decl(bi_1pin_with_name(LED_PIN, "TrunkModule"));

  stdio_init_all();

  gpio_init(LED_PIN);
  gpio_set_dir(LED_PIN, GPIO_OUT);

  spi_init_trunk();
  uart_init_trunk();
  //test_loop();
  loop_forever();
}