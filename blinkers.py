# Copyright (c) 2021 tapiocode
# https://github.com/tapiocode
# MIT License

import utime
import _thread
from machine import Pin, PWM

LEFT_SWITCH_GPIO = 28
RIGHT_SWITCH_GPIO = 16
LEFT_BLINKER_GPIOS = [0, 2, 4, 6, 8, 27, 12]
RIGHT_BLINKER_GPIOS = [1, 3, 5, 7, 9, 26, 13]

left_switch_depressed = False
right_switch_depressed = False

def run():
    array_left = get_pwm_array(LEFT_BLINKER_GPIOS)
    array_right = get_pwm_array(RIGHT_BLINKER_GPIOS)
    while True:
        if left_switch_depressed:
            blink(array_left)
        if right_switch_depressed:
            blink(array_right)
        utime.sleep(0.1)

def switches_thread():
    global left_switch_depressed, right_switch_depressed
    left_switch = Pin(LEFT_SWITCH_GPIO, Pin.IN, Pin.PULL_UP)
    right_switch = Pin(RIGHT_SWITCH_GPIO, Pin.IN, Pin.PULL_UP)
    while True:
        left_switch_depressed = left_switch.value() == 0
        right_switch_depressed = right_switch.value() == 0
        utime.sleep(0.1)

def get_pwm_array(gpios: list[int]) -> list[PWM]:
    arr = []
    for gpio in gpios:
        pwm = PWM(Pin(gpio))
        pwm.freq(1000)
        arr.append(pwm)
    return arr

def blink(pwm_array: list[PWM]):
    max_duty = 65535
    led_range = range(len(pwm_array))
    # Turn off all LEDs
    for led in pwm_array:
        led.duty_u16(0)
    # While the last LED has not maxed out
    while pwm_array[-1].duty_u16() < max_duty:
        for i in led_range:
            for j in led_range:
                led = pwm_array[j]
                if j <= i and led.duty_u16() < max_duty:
                    led.duty_u16(min(int((2 + led.duty_u16() * 2.3)), max_duty))
            utime.sleep(0.005)
    utime.sleep(0.4)
    # Fade out all LEDs
    for duty in range(max_duty + 1, -1, -512):
        for led in pwm_array:
            led.duty_u16(duty)
        utime.sleep(0.001)

if __name__ == '__main__':
    print('Starting')
    _thread.start_new_thread(switches_thread, ())
    run()
