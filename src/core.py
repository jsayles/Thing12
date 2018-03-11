import time
import network
import socket


THING1 = 1
THING2 = 2
LOW = 0
HIGH = 1
PRESS = 0
RELEASE = 1


class LED:

    def __init__(self, pin, on_value=LOW, start_on=False):
        self.pin = pin
        self.on_value = on_value
        if start_on:
            self.on()
        else:
            self.off()

    def on(self, seconds=0):
        if self.on == HIGH:
            self.pin.on()
        else:
            self.pin.off()
        if seconds > 0:
            time.sleep(seconds)
            self.off()

    def off(self):
        if self.on == HIGH:
            self.pin.off()
        else:
            self.pin.on()
        self.is_off = False


class RGB_LED:

    def __init__(self, red_led, green_led, blue_led):
        self.red_led = red_led
        self.green_led = green_led
        self.blue_led = blue_led

    def off(self):
        self.red_led.off()
        self.blue_led.off()
        self.green_led.off()

    def on(self):
        self.red_on()
        self.green_on()
        self.blue_on()

    def red_on(self):
        self.red_led.on()

    def red_off(self):
        self.red_led.off()

    def red(self):
        self.off()
        self.red_on()

    def green_on(self):
        self.green_led.on()

    def green_off(self):
        self.green_led.off()

    def green(self):
        self.off()
        self.green_on()

    def blue_on(self):
        self.blue_led.on()

    def blue_off(self):
        self.blue_led.off()

    def blue(self):
        self.off()
        self.blue_on()

    def white(self):
        self.on()

    def yellow(self):
        self.off()
        self.green_on()
        self.blue_on()

    def orange(self):
        self.off()
        self.red_on()
        self.green_on()

    def purple(self):
        self.off()
        self.red_on()
        self.blue_on()

    def cycle(self, seconds=1, full=False):
        self.off()
        self.red()
        time.sleep(seconds)
        if full:
            self.orange()
            time.sleep(seconds)
        self.green()
        time.sleep(seconds)
        if full:
            self.yellow()
            time.sleep(seconds)
        self.blue()
        time.sleep(seconds)
        if full:
            self.purple()
            time.sleep(seconds)
            self.white()
            time.sleep(seconds)
        self.off()


class Vibe:
    # PWM Settings for adjustable vibe strength
    # pwm = machine.PWM(machine.Pin(PIN_VIBE))
    # How fast the PWM signal is turned on and off
    # 60 = 60 times per second
    # pwm.freq(60)
    # Percent of time that the signal is on vs. off,
    # Range of 0 to 1023
    # pwm.duty(1023)
    # Turn off the pin
    # pwm.duty(0)

    def __init__(self, pin, led=None):
        self.pin = pin
        self.led = led

    def set_led(self, led):
        self.led = led

    def on(self):
        if self.led:
            self.led.on()
        self.pin.on()

    def off(self):
        if self.led:
            self.led.off()
        self.pin.off()

    def pulse(self, seconds=.5):
        self.on()
        time.sleep(seconds)
        self.off()


class Thingnet:

    def __init__(self, thing_id, ssid, passwd, ip_range):
        self.thing_id = thing_id
        self.ssid = ssid
        self.passwd = passwd

        # Calculate the address for Thing1
        split_ip = ip_range.split('.')
        split_ip[3] = str(THING1)
        self.thing1_ip = ".".join(split_ip)
        self.thing1_port = 8080 + THING1
        self.thing1_addr = (self.thing1_ip, self.thing1_port)

        # Calculate the ip for Thing2
        split_ip[3] = str(THING2)
        self.thing2_ip = ".".join(split_ip)
        self.thing2_port = 8080 + THING2
        self.thing2_addr = (self.thing2_ip, self.thing2_port)

    def create_thingnet(self):
        print("Turning on THINGNET (SSID:  %s)" % self.ssid)

        # Turn off the other interface
        network.WLAN(network.STA_IF).active(False)

        # Create an access point for THINGNET
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid=self.ssid, password=self.passwd, authmode=3, channel=11, hidden=1)
        ap.ifconfig((self.thing1_ip, '255.255.255.0', self.thing1_ip, '8.8.8.8'))
        return ap

    def join_thingnet(self):
        print("Connecting to THINGNET (SSID: %s)" % self.ssid)

        # Turn off the other interface
        network.WLAN(network.AP_IF).active(False)

        # Join the THINGNET network
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.ssid, self.passwd)
        wlan.ifconfig((self.thing2_ip, '255.255.255.0', self.thing1_ip, '8.8.8.8'))
        return wlan
