import board
import busio
import adafruit_pca9685 # Allows more control over PWM

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

print("Hello blinka!")
 
# Try to create an I2C device
#i2c = busio.I2C(board.SCL, board.SDA)
#hat = adafruit_pca9685.PCA9685(i2c)
#print("I2C ok!")

servo0 = 8
servo1 = 9

kit.servo[servo1].angle = 180
time.sleep(1)
kit.servo[servo1].angle = 0

print("done!")
