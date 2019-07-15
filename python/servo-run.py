debug = True
hardware = True

from pynput.keyboard import Key, Listener

import time

if hardware:
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


throttle = 0  # Use signed integer -100..100 for integer steps
align    = 0  # Motor drive alignment, used for differential motor
              # driving Range -200..200, twice size of throttle for
              # spinning at full speed.

# Zero Throttle
if hardware:
    kit.continuous_servo[motorLeft].throttle  = 0.0
    kit.continuous_servo[motorRight].throttle = 0.0

def on_press(key):
    global throttle
    global align

    do_quit = False
    
    try:
        if debug:
            print('{0} pressed'.format(key.char))

        if key.char == 'w':
            throttle = throttle + 10
        if key.char == 's':
            throttle = throttle - 10
        if key.char == 'a':
            align = align + 5
        if key.char == 'd':
            align = align - 5
        if key.char == ' ':
            throttle = 0
            align    = 0
        if key.char == 'q':
            throttle = 0
            align    = 0
            do_quit  = True

        # Raw Limits
        if throttle > 100:  throttle = 100
        if throttle < -100: trottle = -100
        if align > 100:     align = 100
        if align < -100:    align = -100

        # Scale integers to range -1.0 to 1.0
        left_throttle  = (throttle - align) / 100
        right_throttle = (throttle + align) / 100
        # Not true steering as turn rate does not increase with throttle
        # Might need to use ratio's instead
   
        # Scaled limits
        if left_throttle > 1.0:
            left_throttle = 1.0
        if left_throttle < -1.0:
            left_throttle = -1.0

        if right_throttle > 1.0:
            right_throttle = 1.0
        if right_throttle < -1.0:
            right_throttle = -1.0

        if debug:
            print('Throttle {0}'.format(throttle))
            print('Align    {0}'.format(align))
        if hardware:
            kit.continuous_servo[motorLeft].throttle  = left_throttle
            kit.continuous_servo[motorRight].throttle = right_throttle

        if do_quit:
            return False
        
    except AttributeError:
        if debug:
            print('Key {0} pressed'.format(key))

        if key == Key.space:
            # Emergency Reset
            throttle = 0
            align    = 0
            if debug:
                print('Throttle {0}'.format(throttle))
                print('Align    {0}'.format(align))
            if hardware:
                kit.continuous_servo[motorLeft].throttle  = 0.0
                kit.continuous_servo[motorRight].throttle = 0.0
            
        #Add Code

def on_release(key):
    if debug:
        print('{0} release'.format(key))

    if key == Key.esc:
        # Shutdown and Stop listener
        if hardware:
            kit.continuous_servo[motorLeft].throttle  = 0.0
            kit.continuous_servo[motorRight].throttle = 0.0
        return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
