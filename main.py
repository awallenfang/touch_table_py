from machine import Pin, Timer

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

minute_timer = Timer(period=60000, mode=Timer.PERIODIC, callback=lambda t: minutes_left -= 1)  # type: ignore
minute_timer.init(period=60000, mode=Timer.PERIODIC, callback=lambda t: minutes_left -= 1)  # type: ignore

button_pin = Pin(21, Pin.IN)
led_pin = Pin(20, Pin.OUT)
piezo_pin = Pin(22, PIN.OUT)

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

while True:
    # If button is pressed, reset minutes left and start new timers
    if button_pin.value() == 0:
        minutes_left = 15
        minute_timer.init(period=60000, mode=Timer.PERIODIC, callback=lambda t: global minutes_left -= 1)  # type: ignore


    # If the minute timer is done, restart it and decrease minutes_left until minutes_left is at 0 at that point disable the beamer
    if minutes_left <= 0:
        led_pin.value(0)
        minute_timer.deinit()
        # ! TODO: Send IR Code to Beamer here

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

    
    
        