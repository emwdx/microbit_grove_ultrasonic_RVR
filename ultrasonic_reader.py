
import sys
from microbit import *
from sphero_EMW import RVRDrive, RVRLed, RVRPower
import time


#The code below was adapted from the code posted here on the Grove wiki: http://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/

_TIMEOUT1 = 1000
_TIMEOUT2 = 10000

class GroveUltrasonicRanger(object):
    def __init__(self, pin):
        self.dio = pin

    def _get_distance(self):

        self.dio.write_digital(0)
        time.sleep_us(2)
        self.dio.write_digital(1)
        time.sleep_us(10)
        self.dio.write_digital(0)



        t0 = time.ticks_us()
        count = 0
        while count < _TIMEOUT1:
            if self.dio.read_digital():
                break
            count += 1
        if count >= _TIMEOUT1:
            return None

        t1 = time.ticks_us()
        count = 0
        while count < _TIMEOUT2:
            if not self.dio.read_digital():
                break
            count += 1
        if count >= _TIMEOUT2:
            return None


        t2 = time.ticks_us()

        #dt = int((t1 - t0) )
        #if dt > 530:
        #    return None

        distance = ((t2 - t1)  / 29.0 / 2.0)    # cm

        return distance

    def get_distance(self):
        while True:
            dist = self._get_distance()

            if dist:
                return dist

#This sets up the ultrasonic sensor attached to pin0 of the microbit.
sonar = GroveUltrasonicRanger(pin0)

#Proportional control constants
setPoint = 100.0
kP = 1
maxSpeed = 128

#Control loop
while True:

    #get the distance of the RVR from the wall
    distanceValue = sonar.get_distance()

    #calculate proportional distance
    error = setPoint - distanceValue

    #Based on the direction of the ultrasonic sensor on my RVR, the outputSpeed needs a negative sign.
    outputSpeed = -error*kP

    #This constrains the outputs to be no more than the max speed.

    if(outputSpeed > maxSpeed):
        outputSpeed = maxSpeed
    elif(outputSpeed < -maxSpeed):
        outputSpeed = -maxSpeed
    outputSpeed = int(outputSpeed)

    #Tell the RVR to drive at heading zero at the outputSpeed calculated above
    RVRDrive.drive(int(outputSpeed), 0)

    #Print out debug information to make sure the system is doing the right thing.
    print("distance: {} outputSpeed: {}  error: {} ".format(distanceValue, outputSpeed, error))
    time.sleep(0.5)
