# servo-run.py
# Script for using keyboard to control the Junkbot robot

# Author: Paul Schulz <paul@mawsonlakes.org>

hardware = True   # Is i2c PWM controller board present. It is useful to
                  # be able to turn this off during development.
tuning   = True   # Additionsl options for adjusting tuning parameters.
debug    = False
monitor  = False

from pynput.keyboard import Key, Listener

import time

# Command Line Processing
import sys
import argparse

parser = argparse.ArgumentParser(description='Drive the robot with the keyboard.')
parser.add_argument('--debug',
                    action='store_const',
                    const=True,
                    help='Turn on debugging output (default: off)')
parser.add_argument('--monitor',
                    action='store_const',
                    const=True,
                    help='Turn on monitoring output (default: off)')
parser.add_argument('--hardware',
                    action='store_const',
                    const=True,
                    help='Run with hardware (default)')
parser.add_argument('--nohardware',
                    action='store_const',
                    const=True,
                    help='Run without hardware (used for testing)')

# Override defaults
args = parser.parse_args()
if args.debug      != None: debug    = args.debug
if args.monitor    != None: monitor  = True
if args.hardware   != None: hardware = True
if args.nohardware != None: hardware = False

if hardware:
    import board
    import busio
    from adafruit_servokit import ServoKit
    kit = ServoKit(channels=16)

if debug:
    print("This is the name of the script: ", sys.argv[0])
    print("Number of arguments: ", len(sys.argv))
    print("The arguments are: " , str(sys.argv))
    print("  args.debug:    ", args.debug)
    print("  args.monitor:  ", args.monitor)
    print("  args.hardware: ", args.hardware)
    print("  args.nohardware: ", args.nohardware)
    print("Configuration")
    print("debug:    ", debug)
    print("monitor:  ", monitor)
    print("hardware: ", hardware)

# PWM Channels
motorLeft  = 0
motorRight = 1

servoArmB  = 4
servoArmT  = 5
servoWrist = 6
servoClaw1 = 8
servoClaw2 = 9

pwmLight = 12

# Labels
Left                  = 0
Right                 = 1

##############################################################################
# Motor channels
motor                 = [motorLeft,motorRight]

##############################################################################
# Servo channels
servos                = [servoArmB,
                         servoArmT,
                         servoWrist,
                         servoClaw1,
                         servoClaw2,
                         pwmLight
]

servoInit = []

##############################################################################
# Init
# Drive
drive_direction       = [1,1]
drive_throttle_step   = 20
drive_steering_step   = 20
drive_bias            = 0 # Left/Right ratio fix for motor variation

# There are a couple of different driving/stearing modes
# 1 - Direct Drive mode
# 2 - Managed mode
# 4 - Dance mode
# 3 - Autonomous mode (TODO)
drive_mode            = 2
drive_mode_string     = ["Direct","Managed","Dance","Autonomous"]

# Drive dynamic parameters
throttle = 0     # Use signed integer -100..100 for integer steps
steering = 0     # Used for differential motor driving Range -100..100

# Servo values
servo_angle      = [0,0,0,0,
                    0,0,0,0,
                    0,0,0,0,
                    0,0,0,0]
servo_angle_min  = [0,0,0,0,
                    0,0,0,0,
                    0,0,0,0,
                    0,0,0,0]
servo_angle_max  = [180,180,180,180,
                   180,180,180,180,
                   180,180,180,180,
                   180,180,180,180]
servo_angle_init = [90,90,90,90,
                    90,90,90,90,
                    90,90,90,90,
                    90,90,90,90]

do_quit  = False # Exit if true

# Zero Throttle and set arm servos to sensible values.
for servo in servos:
    servo_angle[servo] = servo_angle_init[servo]

if hardware:
    kit.continuous_servo[motorLeft].throttle  = 0.0
    time.sleep(1)
    kit.continuous_servo[motorRight].throttle = 0.0
    time.sleep(1)

    for servo in servos:
        kit.servo[servo].angle  = servo_angle[servo]
        time.sleep(1)

##############################################################################
# Functions
def show_tuning():
    print()
    print('  Throttle:  {0}'.format(throttle))
    print('  Steering:  {0}'.format(steering))
    print('  drive_direction     = [{0},{1}]'.format(drive_direction[Left],
                                                     drive_direction[Right]))
    print('  drive_throttle_step = {0}'.format(drive_throttle_step))
    print('  drive_steering_step = {0}'.format(drive_steering_step))
    print('  drive_bias          = {0}'.format(drive_bias))

def show_keys():
    print("----------")
    print("Librarybot")
    print("----------")
    print("");
    print("To drive the Librarybot from the keyboard use the following keys.")
    print("Drive mode: {0}".format(drive_mode_string[drive_mode - 1]))
    print("  Drive:             Arm:")
    print("                     Bot  Top  Wrist Claw1 Claw2 Light")
    print("            w         y    u    i     o     p     n    - Up")
    print("         a  s  d      h    j    k     l     ;     m    - Down")
    print("")
    print("          space   - Emergency Stop")
    print("            q     - Quit program")
    print("")
    if tuning:
        print("  Tuning:")
        print("    t      - Show tuning numbers")
        print("    r f    - Increase/decrease throttle step size")
        print("    z x    - Decrease/increase steering step size")
        print("    [ ]    - Toggle Motor directions")
        print("    , .    - Adjust Left/Right Bias Ratio")
        show_tuning()

def on_press_servo(key):
    global servo_angle
    global servo_angle_max

    # Servos
    # servo_key_press(key)
    # servoArmB
    if key.char == 'y':
        servo_angle[servoArmB]  += 5
    if key.char == 'h':
        servo_angle[servoArmB]  -= 5
    # servoArmT
    if key.char == 'u':
        servo_angle[servoArmT]  -= 5 # Reversed
    if key.char == 'j':
        servo_angle[servoArmT]  += 5
    # servoWrist
    if key.char == 'i':
        servo_angle[servoWrist] += 5
    if key.char == 'k':
        servo_angle[servoWrist] -= 5
    # servoClaw1
    if key.char == 'o':
        servo_angle[servoClaw1] += 5
    if key.char == 'l':
        servo_angle[servoClaw1] -= 5
    # servoClaw2
    if key.char == 'p':
        servo_angle[servoClaw2] += 5
    if key.char == ';':
        servo_angle[servoClaw2] -= 5
    # pwmLight
    if key.char == 'm':
        servo_angle[pwmLight]   += 5
    if key.char == 'n':
        servo_angle[pwmLight]   -= 5

    # Apply Limits (Servos)
    # servo_limits()
    for servo in servos:
        if servo_angle[servo] < servo_angle_min[servo]:
            servo_angle[servo] = servo_angle_min[servo]
        if servo_angle[servo] > servo_angle_max[servo]:
            servo_angle[servo] = servo_angle_max[servo]

# FIXME Direct Drive
def on_press_direct(key):
    global throttle
    global steering
    global drive_direction
    global drive_bias
    global drive_throttle_step
    global drive_steering_step
    global drive_mode

    global servo_angle
    global servo_angle_max

    do_quit = False

    try:
        if debug:
            print('{0} pressed'.format(key.char))

        # Driving
        if key.char == 'w':
            throttle = throttle + drive_throttle_step
        if key.char == 's':
            throttle = throttle - drive_throttle_step
        if key.char == 'a':
            steering = steering + drive_steering_step
        if key.char == 'd':
            steering = steering - drive_steering_step
        if key.char == ' ':
            throttle = 0
            steering = 0
        if key.char == 'q':
            throttle = 0
            steering = 0
            do_quit  = True

        # Tuning the drive parameters
        # Show
        if key.char == 't':
            show_tuning()

        # Drive throttle step size
        if key.char == 'r':
            drive_throttle_step    = drive_throttle_step + 1
        if key.char == 'f':
            drive_throttle_step    = drive_throttle_step - 1

        # Drive steering  step size
        if key.char == 'x':
            drive_steering_step    = drive_steering_step + 1
        if key.char == 'z':
            drive_steering_step    = drive_steering_step - 1

        # Drive direction
        if key.char == '[':
            drive_direction[Left]  = -1 * drive_direction[Left]
        if key.char == ']':
            drive_direction[Right] = -1 * drive_direction[Right]

        # Bias
        if key.char == ',':
            drive_bias             = drive_bias - 1
        if key.char == '.':
            drive_bias             = drive_bias + 1

        # Apply Limits (Driving)
        # Raw Driving Limits
        if throttle >  100: throttle =  100
        if throttle < -100: throttle = -100
        if steering >  100: steering =  100
        if steering < -100: steering = -100

        # Tuning limits
        if drive_throttle_step < 1: drive_throttle_step = 1
        if drive_steering_step < 1: drive_steering_step = 1
        if drive_bias > 100:  drive_bias =  100
        if drive_bias < -100: drive_bias = -100

        # Scale integers to range -1.0 to 1.0
        left_throttle = drive_direction[Left] \
            * (100 - drive_bias) / 100.0 \
            * ((throttle - steering) / 100.0)

        right_throttle = drive_direction[Right] \
            * (100 + drive_bias) / 100.0 \
            * ((throttle + steering) / 100.0)
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

        on_press_servo(key)

        # Drive motors
        if debug:
            print('Throttle {0}'.format(throttle))
            print('Steering {0}'.format(steering))
        if hardware:
            kit.continuous_servo[motorLeft].throttle  = left_throttle
            kit.continuous_servo[motorRight].throttle = right_throttle

        # Move servos
        # servo_drive()
        if debug:
            print('Servo left  {0}'.format(servo_angle[Left]))
            print('Servo right {0}'.format(servo_angle[Right]))
        if hardware:
            kit.servo[servoLeft].angle  = servo_angle[Left]
            kit.servo[servoRight].angle = servo_angle[Right]

        if do_quit:
            return False

    except AttributeError:
        if debug:
            print('Key {0} pressed'.format(key))

        if key == Key.space:
            # Emergency Reset
            throttle = 0
            steering = 0
            if debug:
                print('Throttle {0}'.format(throttle))
                print('Steering {0}'.format(steering))
            if hardware:
                kit.continuous_servo[motorLeft].throttle  = 0.0
                kit.continuous_servo[motorRight].throttle = 0.0

# Managed keyboard driving
# ------------------------
# Pressing a direction button will trigger motor motion for a fixed amount of time.
# This function will set up the motion, which is then done in the main
# loop, which controls the duration for the movement.
#
# throttle: set to (+/-)drive_trottle_stepsize or zero.
# steering: set to (+/-)drive_steering_stepsize or zero.
#
# Once motion is set, these vales are reset to zero (elsewhere).
def on_press_managed(key):
    global throttle
    global steering
    global drive_direction
    global drive_bias
    global drive_throttle_step
    global drive_steering_step
    global drive_mode
    global do_quit

    global servo_angle
    global servo_angle_max

    do_quit = False

    try:
        if debug:
            print('{0} pressed'.format(key.char))

        # Managed: start from 0
        throttle = 0
        steering = 0
        if key.char == 'w':
            throttle = throttle + drive_throttle_step
        if key.char == 's':
            throttle = throttle - drive_throttle_step
        if key.char == 'a':
            steering = steering + drive_steering_step
        if key.char == 'd':
            steering = steering - drive_steering_step
        # Stop - see extended keycodes

        # Quit
        if key.char == 'q':
            throttle = 0
            steering = 0
            do_quit  = True

        # Tuning
        if key.char == 't':
            show_tuning()

        # Drive throttle step size
        if key.char == 'r':
            drive_throttle_step    = drive_throttle_step + 1
        if key.char == 'f':
            drive_throttle_step    = drive_throttle_step - 1

        # Drive steering step size
        if key.char == 'x':
            drive_steering_step    = drive_steering_step + 1
        if key.char == 'z':
            drive_steering_step    = drive_steering_step - 1

        # Drive direction
        if key.char == '[':
            drive_direction[Left]  = -1 * drive_direction[Left]
        if key.char == ']':
            drive_direction[Right] = -1 * drive_direction[Right]

        # Bias
        if key.char == ',':
            drive_bias             = drive_bias - 1
        if key.char == '.':
            drive_bias             = drive_bias + 1

        # Apply Limits (Driving)
        # Raw Limits
        if throttle > 100:  throttle = 100
        if throttle < -100: throttle = -100
        if steering > 100:  steering = 100
        if steering < -100: steering = -100

        # Tuning limits
        if drive_throttle_step < 1: drive_throttle_step = 1
        if drive_steering_step < 1: drive_steering_step = 1
        if drive_bias > 100:  drive_bias = 100
        if drive_bias < -100: drive_bias = -100

        # Servos
        on_press_servo(key)

        if debug:
            print('Key {0} pressed'.format(key))

    except AttributeError:
        if debug:
            print('Key {0} pressed'.format(key))

        if key == Key.space:
            # Emergency Reset
            throttle = 0
            steering = 0
            if debug:
                print('Emergency Stop')
                print('Throttle {0}'.format(throttle))
                print('Steering {0}'.format(steering))

        if key == Key.esc:
            do_quit = True

def on_release(key):
    if debug:
        print('{0} release'.format(key))

show_keys()
# Collect events until released
if drive_mode == 1:
    # Direct Drive Mode
    listener = Listener(
        on_press=on_press_direct,
        on_release=on_release)
elif drive_mode == 2:
    # Managed Drive Mode
    listener = Listener(
        on_press=on_press_managed,
        on_release=on_release)
    listener.start()
else:
    print("Invalid driving mode set.")
    do_quit = True

# Main control loop
left_throttle  = 0.0
right_throttle = 0.0

millis_last = int(round(time.time() * 1000))
millis_delta = 250

while True:
    millis = int(round(time.time() * 1000))
    if millis_last + millis_delta < millis:
        millis_last = millis

        # Set throttle amounts
        # Scale integers to range -1.0 to 1.0
        left_throttle = drive_direction[Left] \
            * (100 - drive_bias) / 100.0 \
            * ((throttle - steering) / 100.0)

        right_throttle = drive_direction[Right] \
            * (100 + drive_bias) / 100.0 \
            * ((throttle + steering) / 100.0)
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

        if monitor:
            formatstr = "{0} Drive L/R: {1:4.2f} {2:4.2f}   Servos {3} {4} {5} {6} {7} {8}"
            print(formatstr.format(millis,
                                   left_throttle,
                                   right_throttle,
                                   servo_angle[servoArmB],
                                   servo_angle[servoArmT],
                                   servo_angle[servoWrist],
                                   servo_angle[servoClaw1],
                                   servo_angle[servoClaw2],
                                   servo_angle[pwmLight]))

        if hardware:
            # Drive motors
            kit.continuous_servo[motorLeft].throttle  = left_throttle
            kit.continuous_servo[motorRight].throttle = right_throttle

            # Drive servos FIXME
            kit.servo[servoArmB].angle  = servo_angle[servoArmB]
            kit.servo[servoArmT].angle  = servo_angle[servoArmT]
            kit.servo[servoWrist].angle = servo_angle[servoWrist]
            kit.servo[servoClaw1].angle = servo_angle[servoClaw1]
            kit.servo[servoClaw2].angle = servo_angle[servoClaw2]
            kit.servo[pwmLight].angle   = servo_angle[pwmLight]

        # Stop after run
        left_throttle  = 0.0
        right_throttle = 0.0
        throttle       = 0
        steering       = 0

    if do_quit == True:
        if hardware:
            kit.continuous_servo[motorLeft].throttle  = 0.0
            kit.continuous_servo[motorRight].throttle = 0.0
        if debug:
            print("Quitting")
        quit()
