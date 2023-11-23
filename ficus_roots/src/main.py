#
# MIT License (MIT)
# Copyright (c) 2023 Shane C Mason
# FicusOS
#
import uasyncio as asyncio
from ficus.ficus_server import FicusServer
import _thread
from ficus.ficus_piezo import FicusPiezo
from time import sleep
import random

def set_global_exception():
    def handle_exception(loop, context):
        import sys
        sys.print_exception(context["exception"])
        sys.exit()
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)


def os_core0(outq, outq_lock):
    async def main():
        set_global_exception()  # Debug aid
        ficus = FicusServer(outq, outq_lock)  # Constructor might create tasks
        await ficus.run_forever()  # Non-terminating method
    try:
        asyncio.run(main())
    finally:
        asyncio.new_event_loop()  # Clear retained state


def sample_core1(outq, outq_lock):
    FicusPiezo.play_start_seq()
    while(True):
        FicusPiezo.play_blinkin()
        sleep(random.random()*5)

# hello world
outq_lock = _thread.allocate_lock()
outq = {
        "ux": []
        }
shell_thread = _thread.start_new_thread(sample_core1, (outq, outq_lock))
os_core0(outq, outq_lock)

