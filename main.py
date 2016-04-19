import time, os, sys, glob, threading
# FILES IMPORT BELOW
from board import Board
import pins
import methods as M
#from lightClass import Light as L
#from LedClass import Led as l
#from tempClass import Temp as t
#from distClass import Dist as d
#from pirClass import Pir as p
#from buzzerClass import Buzz as b
from lcd1602 import LCD1602

#Pins
tempSensor = 7
tempLed = 23
dtSensor = 31
deSensor = 29
pirSensor = 32
buzzSensor = 35
fadeLed = 11
lightButton = 22
nextButton = 12
backButton = 16
lightSensor = 18
pirLight = 31
ledRed = 36
ledGreen = 38
ledBlue = 40

board = Board().board
lcd = LCD1602(board)

def tempSet():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

def setup():
    board.setmode(board.BOARD)    #set GPIO up
    board.setwarnings(False)
    inputs = [tempSensor, pirSensor, deSensor]   # Set there categories in arrays
    outputs = [pirLight, tempLed, dtSensor, buzzSensor, fadeLed, lightSensor, ledBlue, ledGreen, ledRed]
    buttons = [lightButton, nextButton, backButton]
    print('### ATTEMPTING TO IMPORT AND SETUP PINS ###')
    pins.Pins(inputs, outputs, buttons, board, time)    #Set up pins from a class
    print('### ALL PINS ARE IMPORTED AND SETUP SUCCESSFULLY ###')
    board.output(fadeLed, board.HIGH)

def getTemp():
    c, f = t.read_temp() # Get temp values
    ct = str(int(c))     # converts degrees c to string
    ft = str(int(f))     # converts degrees f to string
    temp = (ct + ' Celsius & ' + ft + ' Fahrenheit') # creates compiled string of temperature values
    print ('Temperature: ' + temp)
    tempFin = (ct + ' ' + ft)
    return tempFin
    
def getDist(dtSensor, deSensor, board):
    dval = d(dtSensor, deSensor, board)
    value = (str(dval.distValue))
    return value

def getPir(pirSensor, board, counter, pirLight, buzzSensor):
    if counter >= 5:
        l(pirLight, board).LedOff()
        counter = 0
    pval = p(pirSensor, board)
    value = pval.pirState
    print ('PIR Value = ' + str(value) + ' // 1 = on // 0 = off')
    if value == 1:
        finValue = 'ON '
        l(pirLight, board).LedOn()
        counter = (counter + 1)
        b(buzzSensor, board).buzzOn()
        time.sleep(0.4)
        b(buzzSensor, board).buzzOff()
    else:
        finValue = 'OFF'
    return finValue, counter

def getLight(lightSensor, board):
    LSV = 0
    lval = L(lightSensor, board, LSV)
    value = lval.LSV
    print ('Light Sensor Value = ' + str(value))
    return value

def lightSwitch(fadeLed, lightButton, board, lightState):
    while True:
        time.sleep(0.8)
        if board.input(lightButton) == False:
            if lightState == 'on':
                l(fadeLed, board).LedOff()
                lightState = 'off'
            elif lightState == 'off':
                l(fadeLed, board).LedOn()
                lightState = 'on'

try:
    M.tempSet()
    setup()
    lightState = 'on'
    counter = 0
    lcd.lcd_string('C  F  Pir Dis Cm', lcd.LCD_LINE_1)
    loopVal = 1
    threading.Thread(target=M.lightSwitch, args=(fadeLed, lightButton, board, lightState)).start()
    while True:
        print('### Loop ' + str(loopVal) + ' ###')
        loopVal = loopVal + 1
        pir, counter = M.getPir(pirSensor, board, counter, pirLight, buzzSensor)
        temp = M.getTemp()
        light = M.getLight(lightSensor, board)
        #dist = getDist(dtSensor, deSensor, board)
        lcd.lcd_string('C  F  Pir Dis Cm', lcd.LCD_LINE_1)
        lcd.lcd_string(temp + ' ' + pir + ' ' + str(light), lcd.LCD_LINE_2)
except KeyboardInterrupt:
    print('### Ctrl-C Pressed: Exiting ###')
    time.sleep(0.1)
    lcd.lcd_clear()
    lcd.cleanup()
    sys.exit()
