import time
from machine import Pin, PWM
from ir_tx.nec import NEC
import math

# Digits to 7 segment display
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

# Initialise Piezo
piezo = machine.Pin(22)
piezo_pin = machine.PWM(piezo)

# Initialise Button
button_pin = Pin(21, Pin.IN, Pin.PULL_UP)

# Initialise NEC Transmitter
nec = NEC(Pin(16, Pin.OUT)) 

# Initialise 7 Segment Displays
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

# Flag for reminder tone
flag_reminder_2min_triggered = False
flag_standby = False


# Initialise Timer
delta = 0 # Delta between Now and Timer starttime
start_time = time.ticks_ms() # Moment Button was pressed


delta_blinker = 0
standby_blinker = time.ticks_ms() 

delta_blinker_active = 0
active_blinker = time.ticks_ms() 

# Piezo Helper Subroutines
def piezo_sound_turn_on(pin):
    pin.freq(530) # frequency in Hz [Range 10Hz to 12000Hz]
    pin.duty_u16(512) # Dutycyle (Volume) [Range 0 (Silent/Off) to 1000 (Full blast)]
    time.sleep(0.25) # Delay in seconds
    pin.freq(590)
    time.sleep(0.2)
    pin.freq(800)
    time.sleep(0.3)
    pin.duty_u16(128)
    pin.freq(590)
    time.sleep(0.2)
    pin.freq(800)
    time.sleep(0.3)
    pin.duty_u16(64)
    pin.freq(590)
    time.sleep(0.2)
    pin.freq(800)
    time.sleep(0.3)
    pin.duty_u16(0)
    
def piezo_sound_turn_off(pin):
    pin.freq(840) # frequency in Hz [Range 10Hz to 12000Hz]
    pin.duty_u16(512) # Dutycyle (Volume) [Range 0 (Silent/Off) to 1000 (Full blast)]
    time.sleep(0.4) # Delay in seconds
    pin.freq(630)
    time.sleep(0.25)
    pin.freq(420)
    time.sleep(0.2)
    pin.duty_u16(0)

def piezo_sound_reminder(pin):
    pin.freq(840)
    pin.duty_u16(512)
    time.sleep(0.4)
    pin.duty_u16(0)
    time.sleep(0.2)
    pin.duty_u16(512)
    time.sleep(0.4)
    pin.duty_u16(0)
    time.sleep(0.2)
    pin.duty_u16(512)
    time.sleep(0.4)
    pin.duty_u16(0)  
    
def piezo_sound_button_press(pin):
    pin.freq(261) # frequency in Hz [Range 10Hz to 12000Hz]
    pin.duty_u16(512) # Dutycyle (Volume) [Range 0 (Silent/Off) to 1000 (Full blast)]
    time.sleep(0.1) # Delay in seconds
    pin.freq(330)
    time.sleep(0.1) # Delay in seconds
    pin.freq(392)
    time.sleep(0.05)
    pin.duty_u16(0)

#Loop-de-Loop
while True:
    
    # If button is pressed, reset minutes left and start new timers
    if button_pin.value() == 0:
        if delta == 0: # If beamer was off, it will turn on.
            piezo_sound_turn_on(piezo_pin)
            time.sleep(0.25)
            nec.transmit(0xCA8B, 0x12) # turn beamer on
            time.sleep(0.25)
        start_time = time.ticks_ms() # get millisecond counter
        delta = 1
        flag_standby = False
        flag_reminder_2min_triggered = False
        if minutes_left <= 14:
            piezo_sound_button_press(piezo_pin)
        
        
    if delta != 0:
        time.sleep(0.05)
        delta = time.ticks_diff(time.ticks_ms(), start_time)
        minutes_left = 15 - math.floor(delta/1000/60)
            
    if delta >= 780000: #780.000 ms = 13mins passed; 2 mins left
        if flag_reminder_2min_triggered == False:
            flag_reminder_2min_triggered = True
            piezo_sound_reminder(piezo_pin)
    
    
    # drunk coding lmao yeet
    # delta = time.ticks_diff(time.ticks_ms(), start_time)
    if delta >= 900000: #900.000 ms = 15mins
        delta = 0 # gotta make sure, computers are fucky wucky sometimes uwu
        nec.transmit(0xCA8B, 0x12)  # address == 0xCA8B, data == 0x12
        time.sleep(3)
        nec.transmit(0xCA8B, 0x12) # Shutting the beamer off requires two (2) consecutive button presses
        time.sleep(1)
        minutes_left = 0
        piezo_sound_turn_off(piezo_pin)
        
        #Timer Coundown 60s cooldown with no input + Enter standby mode
        
        for i in range(60;0;i = i - 1):
            tens_digit = (i - (i % 10)) // 10
            ones_digit = i % 10
            
            tens_a.value(lookup[tens_digit][0])  # type: ignore
            tens_b.value(lookup[tens_digit][1])  # type: ignore
            tens_c.value(lookup[tens_digit][2])  # type: ignore
            tens_d.value(lookup[tens_digit][3])  # type: ignore
            tens_e.value(lookup[tens_digit][4])  # type: ignore
            tens_f.value(lookup[tens_digit][5])  # type: ignore
            tens_g.value(lookup[tens_digit][6])  # type: ignore
            
            ones_a.value(lookup[ones_digit][0])  # type: ignore
            ones_b.value(lookup[ones_digit][1])  # type: ignore
            ones_c.value(lookup[ones_digit][2])  # type: ignore
            ones_d.value(lookup[ones_digit][3])  # type: ignore
            ones_e.value(lookup[ones_digit][4])  # type: ignore
            ones_f.value(lookup[ones_digit][5])  # type: ignore
            ones_g.value(lookup[ones_digit][6])  # type: ignore
            
            time.sleep(1)
        flag_standby = True
        standby_blinker = time.ticks_ms() 
        time.sleep(0.1)
        _ones_dot.value(0)
        _tens_dot.value(0)
        
        
    if minutes_left == 0 :
        tens_digit = 0
        ones_digit = 0
    else:
        tens_digit = (minutes_left - (minutes_left % 10)) // 10
        ones_digit = minutes_left % 10
    
    
    
    # Last but not Least:
    # Set the pins according to the digits and depending on standby mode
    if flag_standby == False:
        tens_a.value(lookup[tens_digit][0])  # type: ignore
        tens_b.value(lookup[tens_digit][1])  # type: ignore
        tens_c.value(lookup[tens_digit][2])  # type: ignore
        tens_d.value(lookup[tens_digit][3])  # type: ignore
        tens_e.value(lookup[tens_digit][4])  # type: ignore
        tens_f.value(lookup[tens_digit][5])  # type: ignore
        tens_g.value(lookup[tens_digit][6])  # type: ignore
        
        ones_a.value(lookup[ones_digit][0])  # type: ignore
        ones_b.value(lookup[ones_digit][1])  # type: ignore
        ones_c.value(lookup[ones_digit][2])  # type: ignore
        ones_d.value(lookup[ones_digit][3])  # type: ignore
        ones_e.value(lookup[ones_digit][4])  # type: ignore
        ones_f.value(lookup[ones_digit][5])  # type: ignore
        ones_g.value(lookup[ones_digit][6])  # type: ignore
        
        #_ones_dot.value(0)
        _tens_dot.value(0)
        delta_blinker = 0
        
        # put normal blinker 'ere
        active_blinker = time.ticks_ms()
        delta_blinker_active = time.ticks_diff(time.ticks_ms(), standby_blinker)
        if delta_blinker_active >= 1000:
            #Do blinky blinky
            _ones_dot.value( not _ones_dot.value() )
            active_blinker = time.ticks_ms() 
            delta_blinker_active = 1
        
    else:
        tens_a.value(0)
        tens_b.value(0)
        tens_c.value(0)
        tens_d.value(0)
        tens_e.value(0)
        tens_f.value(0)
        tens_g.value(0)
        
        ones_a.value(0)
        ones_b.value(0)
        ones_c.value(0)
        ones_d.value(0)
        ones_e.value(0)
        ones_f.value(0)
        ones_g.value(0)
        
        delta_blinker = time.ticks_diff(time.ticks_ms(), standby_blinker)
        if delta_blinker >= 1000:
            #Do blinky blinky
            _ones_dot.value( not _ones_dot.value() )
            _tens_dot.value( not _ones_dot.value() )
            standby_blinker = time.ticks_ms() 
            delta_blinker = 1
        
        
        
        