import time
from machine import Pin, PWM
from ir_tx.nec import NEC
import math

# digits to 7 segment display
lookup = [
    [1,1,1,1,1,1,0], # 0
    [0,1,1,0,0,0,0], # 1
    [1,1,0,1,1,0,1], # 2
    [1,1,1,1,0,0,1], # 3
    [0,1,1,0,0,1,1], # 4
    [1,0,1,1,0,1,1], # 5
    [1,0,1,1,1,1,1], # 6
    [1,1,1,0,0,0,0], # 7
    [1,1,1,1,1,1,1], # 8
    [1,1,1,1,0,1,1], # 9
]


minutes_left = 0

# CRUDE TIMER VARIANT
#start = time.ticks_ms() # get millisecond counter
#delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference

# ORIGNIAL TIMER
#minute_timer = Timer(period=60000, mode=Timer.PERIODIC, callback=lambda t: minutes_left -= 1)  # type: ignore
#minute_timer.init(period=60000, mode=Timer.PERIODIC, callback=lambda t: minutes_left -= 1)  # type: ignore

button_pin = Pin(21, Pin.IN, Pin.PULL_UP)
piezo_pin = PWM(Pin(22))

tens_a = Pin(13, Pin.OUT)
tens_b = Pin(12, Pin.OUT)
tens_c = Pin(2, Pin.OUT)
tens_d = Pin(1, Pin.OUT)
tens_e = Pin(0, Pin.OUT)
tens_f = Pin(14, Pin.OUT)
tens_g = Pin(15, Pin.OUT)
_tens_dot = Pin(3, Pin.OUT)

ones_a = Pin(9, Pin.OUT)
ones_b = Pin(8, Pin.OUT)
ones_c = Pin(6, Pin.OUT)
ones_d = Pin(5, Pin.OUT)
ones_e = Pin(4, Pin.OUT)
ones_f = Pin(10, Pin.OUT)
ones_g = Pin(11, Pin.OUT)
_ones_dot = Pin(7, Pin.OUT)

tens_digit = 0
ones_digit = 0


nec = NEC(Pin(22, Pin.OUT)) # Add NEC Transmitter
delta = 0
start_time = time.ticks_ms()
print("started")

def piezo_sound_turn_on(piezo_pin):
    piezo_pin.freq(400) # frequency in Hz [Range 10Hz to 12000Hz]
    piezo_pin.duty_u16(1000) # Dutycyle (Volume) [Range 0 (Silent/Off) to 1000 (Full blast)]
    time.sleep(1) # Delay in seconds

    piezo_pin.duty_u16(0)

def piezo_sound_turn_off(piezo_pin):
    return

def piezo_sound_remider(piezo_pin):
    return

while True:
    # If button is pressed, reset minutes left and start new timers
    if button_pin.value() == 0:
        if delta == 0: # If beamer was off, it will turn on.
            nec.transmit(0xCA8B, 0x12) # turn beamer on
            time.sleep(1)
            print("Turnon")
            piezo_sound_turn_on(piezo_pin)
            
        start_time = time.ticks_ms() # get millisecond counter
        delta = 1


    if delta != 0:
        time.sleep(0.05)
        delta = time.ticks_diff(time.ticks_ms(), start_time)
        minutes_left = 15 - math.floor(delta/10/60)
        
    # drunk coding lmao yeet
    #delta = time.ticks_diff(time.ticks_ms(), start_time)
    if delta >= 9000: #900.000 ms = 15mins
        delta = 0 # gotta make sure, computers are fucky wucky sometimes uwu
        nec.transmit(0xCA8B, 0x12)  # address == 0xCA8B, data == 0x12
        time.sleep(3)
        nec.transmit(0xCA8B, 0x12) # Shutting the beamer off requires two (2) button presses
        time.sleep(1)
        minutes_left = 0
    

    if minutes_left == 0 :
        tens_digit = 0
        ones_digit = 0
    else:
        tens_digit = (minutes_left - (minutes_left % 10)) // 10
        ones_digit = minutes_left % 10

    # Set the pins according to the digits
    tens_a.value(lookup[tens_digit][0])
    tens_b.value(lookup[tens_digit][1])
    tens_c.value(lookup[tens_digit][2])
    tens_d.value(lookup[tens_digit][3])
    tens_e.value(lookup[tens_digit][4])
    tens_f.value(lookup[tens_digit][5])
    tens_g.value(lookup[tens_digit][6])

    ones_a.value(lookup[ones_digit][0])
    ones_b.value(lookup[ones_digit][1])
    ones_c.value(lookup[ones_digit][2])
    ones_d.value(lookup[ones_digit][3])
    ones_e.value(lookup[ones_digit][4])
    ones_f.value(lookup[ones_digit][5])
    ones_g.value(lookup[ones_digit][6])






