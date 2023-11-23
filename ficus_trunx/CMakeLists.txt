cmake_minimum_required(VERSION 3.13)

# initialize the SDK based on PICO_SDK_PATH
# note: this must happen before project()
include(pico_sdk_import.cmake)

project(ficus_trunx C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)


# initialize the Raspberry Pi Pico SDK
pico_sdk_init()

add_executable(ficus_trunx
  ficus_trunx.c
)

# rest of your project
pico_enable_stdio_usb(ficus_trunx 1)
pico_enable_stdio_uart(ficus_trunx 0)


pico_add_extra_outputs(ficus_trunx)
# Pull in basic dependencies
target_link_libraries(ficus_trunx pico_stdlib hardware_spi hardware_uart)
