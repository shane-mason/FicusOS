#ifndef _SPI_TRUNK_COMMS
#define _SPI_TRUNK_COMMS

#include <stdio.h>
#include <string.h>
#include "hardware/spi.h"
#include "ficus_vine_format.h"

#define SPI_BUF_LEN 256 
uint8_t spi_out_buf [SPI_BUF_LEN], spi_in_buf [SPI_BUF_LEN];
const uint8_t vine_end_spi = VINE_END;

void spi_init_trunk(){

  //init SPI  
  spi_init(spi0, 1000*1000);
  gpio_set_function(16, GPIO_FUNC_SPI);
  gpio_set_function(17, GPIO_FUNC_SPI);
  gpio_set_function(18, GPIO_FUNC_SPI);
  gpio_set_function(19, GPIO_FUNC_SPI);
}


void spi_send_vine(uint8_t vstart, char * in_str){
  if(spi_is_writable(spi0)){
    spi_write_read_blocking (spi0, &vstart, spi_in_buf, 1);
    for(uint8_t i=0; i<strlen(in_str); i++){
      spi_write_read_blocking (spi0, &in_str[i], spi_in_buf, 1);
    }
    spi_write_read_blocking (spi0, &vine_end_spi, spi_in_buf, 1);
  }
}

#endif