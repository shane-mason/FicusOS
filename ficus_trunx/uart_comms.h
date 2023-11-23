#ifndef _UART_TRUNK_COMMS
#define _UART_TRUNK_COMMS

#include <stdio.h>
#include <string.h>
#include "hardware/uart.h"
#include "ficus_vine_format.h"

//UART Speeds 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600
#define UART_SPEED 38400 

void uart_init_trunk(){
  //init uart
  //HCI (keyboard, display etc) on trunk
  gpio_set_function(12, GPIO_FUNC_UART);
  gpio_set_function(13, GPIO_FUNC_UART);  
  //Event stream on trunk
  gpio_set_function(8, GPIO_FUNC_UART);
  gpio_set_function(9, GPIO_FUNC_UART); 
  //uart zero == input stream (keyboard in, display out) 
  uart_init(uart0, UART_SPEED);
  uart_init(uart1, UART_SPEED);
}

void uart_init_fig(){
  //init uart
  //shell reponses/actions on fig
  gpio_set_function(0, GPIO_FUNC_UART);
  gpio_set_function(1, GPIO_FUNC_UART);  
  gpio_set_function(4, GPIO_FUNC_UART);
  gpio_set_function(5, GPIO_FUNC_UART); 
  //uart zero == input stream (keyboard in, display out) 
  uart_init(uart0, UART_SPEED);
  uart_init(uart1, UART_SPEED);
}

void uart_send_vine(uart_inst_t* the_uart, uint8_t vstart,  char* wbuff){
    uart_putc(the_uart, vstart);
    uart_puts(the_uart, wbuff);
    uart_putc(the_uart, VINE_END);
}

bool uart_read_until_end(uart_inst_t* the_uart, uint8_t* rbuff, uint16_t buff_len){
    bool end_found = false;
    uint8_t rbyte = 0;
    for(uint16_t i = 0; i < buff_len-1; i++){
        rbyte = uart_getc(the_uart);
        if(rbyte==VINE_END){
            end_found = true;
            break;
        }
        else{
            rbuff[i] = rbyte;
            rbuff[i+1] = '\0';
        }
    }
    

}

#endif