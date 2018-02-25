#####################################################################
# Main program run after Boot
#####################################################################

import time
import machine
import settings
import vibe
import led

# Hardware Test
led.cycle()
vibe.pulse()

# Hook up our button to vibe when pressed
def button_handler(pin):
    if pin.value() == 0:
        vibe.on()
    else:
        vibe.off()
trigger = machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING
settings.button.irq(trigger=trigger, handler=button_handler)
