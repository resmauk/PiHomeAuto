import RPi.GPIO as gpio
import time, os, sys

class Pir:
    def __init__(self, pirSensor):
        self.pirSensor = pirSensor
        self.pirState = 0
        self.pirMethod()
    
    def pirMethod(self):
        self.pirState = gpio.input(self.pirSensor)
        if self.pirState == 1:
            self.pirState = 'on'
        elif self.pirState == 0:
            self.pirState = 'off'
        else:
            print('Error PIR not functioning, aborting...')
            gpio.cleanup()
            sys.exit()

if __name__ == "__main__":
    pirSensor = 32
    #p = Pir()
    for i in range(5):
        pirState = gpio.input(pirSensor)
        print (pirState)
        time.sleep(0.7)
