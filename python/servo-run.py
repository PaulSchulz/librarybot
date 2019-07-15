from pynput.keyboard import Key, Listener

import time
import board
import busio
# import adafruit_pca9685 # Allows more control over PWM

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

print("Hello junkbot!")

motorLeft  = 0
motorRight = 1

microservo0 = 2
microservo1 = 3

test = False

if test == True:
    # Test servos
    print("Test microservo0")
    kit.servo[microservo0].angle = 90
    time.sleep(1)
    kit.servo[microservo0].angle = 0
    time.sleep(1)

    print("Test microserver1")
    kit.servo[microservo1].angle = 90
    time.sleep(1)
    kit.servo[microservo1].angle = 0
    time.sleep(1)

    print("Test Motor Left")
    print(" - forward")
    kit.continuous_servo[motorLeft].throttle = 1.0
    time.sleep(1)
    print(" - stop")
    kit.continuous_servo[motorLeft].throttle = 0.0
    time.sleep(1)
    print(" - backwards")
    kit.continuous_servo[motorLeft].throttle = -1.0
    time.sleep(1)
    print(" - stop")
    kit.continuous_servo[motorLeft].throttle = 0.0
    time.sleep(1)

    print("Test Motor Right")
    print(" - forward")
    kit.continuous_servo[motorRight].throttle = 1.0
    time.sleep(1)
    print(" - stop")
    kit.continuous_servo[motorRight].throttle = 0.0
    time.sleep(1)
    print(" - backwards")
    kit.continuous_servo[motorRight].throttle = -1.0
    time.sleep(1)
    print(" - stop")
    kit.continuous_servo[motorRight].throttle = 0.0
    time.sleep(1)
    
    print("Testing done!")

throttle = 0.0
 # Motor drive alignment, used for differential motor driving
align    = 0.0

# Zero Throttle
kit.continuous_servo[motorLeft].throttle  = throttle
kit.continuous_servo[motorRight].throttle = throttle

def on_press(key):
    global throttle
    global align
    do_quit = False
    
    # print('{0} pressed'.format(key))

    # Throttle and Steering
    if key == 'w':
        throttle = throttle + 0.1
    if key == 's':
        throttle = throttle - 0.1
    if key == 'a':
        align = align + 0.05
    if key == 'd':
        align = align - 0.05

    # Stop motion
    if key == Key.space:
        throttle = 0.0
        align    = 0.0

    # Quit (but stop first)
    if key == 'q':
        do_quit  = True
        throttle = 0.0
        align    = 0.0

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
    print('Throttle '.throttle)
    print('Align    '.align)

    if on_quit == True:
        return False

def on_release(key):
    # print('{0} release'.format(key))
    if key == Key.esc:
        # Stop listener, but stop motors first
        kit.continuous_servo[motorLeft].throttle  = 0.0
        kit.continuous_servo[motorRight].throttle = 0.0
        return False
    
# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
