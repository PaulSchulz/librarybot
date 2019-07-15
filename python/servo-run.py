from pynput.keyboard import Key, Listener

import time
import board
import busio
# import adafruit_pca9685 # Allows more control over PWM

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

print("Hello blinka!")
 
# Try to create an I2C device
#i2c = busio.I2C(board.SCL, board.SDA)
#hat = adafruit_pca9685.PCA9685(i2c)
#print("I2C ok!")

motorLeft  = 0
motorRight = 1

microservo0 = 2
microservo1 = 3

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

print("Test done!")

def on_press(key):
    print('{0} pressed'.format(
        key))

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
