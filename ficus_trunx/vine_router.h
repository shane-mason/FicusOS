#ifndef _VINE_ROUTER
#define _VINE_ROUTER

#include <stdio.h>
#include <string.h>
#include "uart_comms.h"
#include "spi_trunk_comms.h"
#include "ficus_vine_format.h"

uint8_t input_vine_buffer[VINE_PAYLOAD_LEN];

void route_message(uint8_t vstart, u_int8_t* data, uint16_t data_len){
    printf("Routing message %d %s\n", vstart, data);
    if(vstart == VINE_KEYPRESS || vstart == VINE_SHELL || vstart == VINE_SHELL_RESPONSE || vstart == VINE_SHELL_ERROR){
        uart_send_vine(uart0, vstart, data);
    }
    if(vstart == VINE_SHELL){
        //spi_send_vine(vstart, data);
        uart_send_vine(uart1, vstart, data);
    }
}

void poll_vine(uart_inst_t* the_uart){
    puts("Polling vine");
    uint8_t vstart;
    vstart = uart_getc(the_uart);
    printf("vstart=%d\n", vstart);
    if(vstart > VINE_BASE && vstart <= VINE_SHELL){
        bool message_found = uart_read_until_end(the_uart, input_vine_buffer, VINE_PAYLOAD_LEN);
        if(message_found){
            route_message(vstart, input_vine_buffer, VINE_PAYLOAD_LEN);
        }

        //then we don't know what state we are in...
    }

    //then we don't know what state we are in...
}


#endif