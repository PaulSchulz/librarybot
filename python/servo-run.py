from pynput.keyboard import Key, Listener

import time
import board
import busio
# import adafruit_pca9685 # Allows more control over PWM

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

print("--------------")
print("Hello junkbot!")
print("--------------")

motorLeft  = 0
motorRight = 1

microservo0 = 2
microservo1 = 3

throttle = 0.0
 # Motor drive alignment, used for differential motor driving
align    = 0.0

# Zero Throttle
kit.continuous_servo[motorLeft].throttle  = throttle
kit.continuous_servo[motorRight].throttle = throttle

def on_press(key):
    global throttle
    global align
    print('{0} pressed'.format(
        key))
    if key == "w":
        throttle = throttle + 0.1
    if key == "s":
        throttle = throttle - 0.1
    if key == "a":
        align = align + 0.05
    if key == "d":
        align = align - 0.05
    if key == "q":
        quit()

    # Not true steering as turn rate does not increase with throttle
    # Might need to use ratio's instead
    left_throttle  = throttle - align
    right_throttle = throttle + align
    
    # limits
    if left_throttle > 1.0:
        left_throttle = 1.0
    if left_throttle < -1.0:
        left_throttle = -1.0

    if right_throttle > 1.0:
       right_throttle = 1.0
    if right_throttle < -1.0:
        right_throttle = -1.0
    
    kit.continuous_servo[motorLeft].throttle  = left_throttle
    kit.continuous_servo[motorRight].throttle = right_throttle
    print('Throttle {0}'.format(throttle))
    print('Align    {0}'.format(align))

def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
