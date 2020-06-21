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

microservo0 = 3
microservo1 = 4
microservo2 = 5
microservo3 = 6

print("Test Motor Left")
kit.continuous_servo[motorLeft].throttle = 0
time.sleep(1)
print("- forward (fullspeed)")
kit.continuous_servo[motorLeft].throttle = 1
time.sleep(1)
kit.continuous_servo[motorLeft].throttle = 0
time.sleep(1)

kit.continuous_servo[motorLeft].throttle = 0
time.sleep(1)
print("- backward (fullspeed)")
kit.continuous_servo[motorLeft].throttle = -1
time.sleep(1)
kit.continuous_servo[motorLeft].throttle = 0
time.sleep(1)

print("Test Motor Right")
kit.continuous_servo[motorRight].throttle = 0
time.sleep(1)
print("- forward (fullspeed)")
kit.continuous_servo[motorRight].throttle = 1
time.sleep(1)
kit.continuous_servo[motorRight].throttle = 0
time.sleep(1)

kit.continuous_servo[motorRight].throttle = 0
time.sleep(1)
print("- backward (fullspeed)")
kit.continuous_servo[motorRight].throttle = -1
time.sleep(1)
kit.continuous_servo[motorRight].throttle = 0
time.sleep(1)

# Test servos
print("Test microservos")
print("- microservo0")
kit.servo[microservo0].angle = 0
time.sleep(1)
kit.servo[microservo0].angle = 90
time.sleep(1)
kit.servo[microservo0].angle = 0
time.sleep(1)

print("- microserver1")
kit.servo[microservo1].angle = 0
time.sleep(1)
kit.servo[microservo1].angle = 90
time.sleep(1)
kit.servo[microservo1].angle = 0
time.sleep(1)

print("- microservo2")
kit.servo[microservo2].angle = 0
time.sleep(1)
kit.servo[microservo2].angle = 90
time.sleep(1)
kit.servo[microservo2].angle = 0
time.sleep(1)

print("-microserver3")
kit.servo[microservo3].angle = 0
time.sleep(1)
kit.servo[microservo3].angle = 90
time.sleep(1)
kit.servo[microservo3].angle = 0
time.sleep(1)

print("done!")
