import time, os, sys, glob, threading
# FILES IMPORT BELOW

from board import Board
from lightClass import Light as L
from LedClass import Led as l
from tempClass import Temp as t
from distClass import Dist as d
from pirClass import Pir as p
from buzzerClass import Buzz as b
from lcd1602 import LCD1602
from tkinter import *
from tkinter import messagebox

board = Board().board
lcd = LCD1602(board)

def tempSet():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

def getTemp(frame, board, ledRed, ledGreen, ledBlue, highTemp, lowTemp):
    c, f = t.read_temp() # Get temp values
    f = round(f, 2)
    c = round(c, 2)
    ct = str(int(c))     # converts degrees c to string
    ft = str(int(f))     # converts degrees f to string
    temp = (ct + ' Celsius & ' + ft + ' Fahrenheit') # creates compiled string of temperature values
    sys.stdout.write("\033[K")
    print ('### Temperature: ' + temp)
    tempFin = (ct + ' ' + ft)
    gui = (str(c) + ' C ' + str(f) + ' F')
    TempValue = Label(frame, text=('              '), borderwidth=1).grid(row=4,column=2,padx=5,pady=5)
    if f <= lowTemp:
        TempValue = Label(frame, text=(gui), fg='blue', borderwidth=1).grid(row=4, column=2, padx=5, pady=5)
    elif f >= highTemp:
        TempValue = Label(frame, text=(gui), fg='red', borderwidth=1).grid(row=4, column=2, padx=5, pady=5)
    else:
        TempValue = Label(frame, text=(gui), fg='green', borderwidth=1).grid(row=4, column=2, padx=5, pady=5)
    tempLight(board, f, ledRed, ledGreen, ledBlue, highTemp, lowTemp)
    c = round(c)
    return tempFin, c

def getDist(dtSensor, deSensor, board, frame):
    dval = d(dtSensor, deSensor, board)
    value = (dval.distValue)
    value = round(value)
    value = str(value)
    sys.stdout.write("\033[K")
    print('### Distance: ' + value)
    DistValue = Label(frame, text=(str(value) + 'cm'), borderwidth=1)
    DistValue.grid(row=6, column=2, padx=5, pady=5)
    return value

def getPir(pirSensor, board, pirLight, buzzSensor, frame):
    '''
    if counter >= 5:
        l(pirLight, board).LedOff()
        counter = 0
    '''
    pval = p(pirSensor, board, frame)
    value = pval.pirState
    sys.stdout.write("\033[K")
    print ('### PIR Value = ' + str(value) + ' // 1 = on // 0 = off')
    if value == 1:
        finValue = 'ON '
        PirValue = Label(frame, text=(finValue), fg='green', borderwidth=1).grid(row=3, column=2, padx=5, pady=5)
        l(pirLight, board).LedOn()
        #counter = 0
        BuzzValue = Label(frame, text=(' ON '), fg='green', borderwidth=1).grid(row=7,column=2,padx=5,pady=5)
        b(buzzSensor, board).buzzOn()
        time.sleep(0.4)
        BuzzValue = Label(frame, text=(''), borderwidth=1).grid(row=7, column=2, padx=5, pady=5)
        BuzzValue = Label(frame, text=('OFF'), fg='red', borderwidth=1).grid(row=7, column=2, padx=5, pady=5)
        b(buzzSensor, board).buzzOff()
    else:
        finValue = 'OFF'
        PirValue = Label(frame, text=(finValue), fg='red', borderwidth=1).grid(row=3, column=2, padx=5, pady=5)
        #counter = (counter + 1)
    BuzzValue = Label(frame, text=('OFF'), fg='red', borderwidth=1).grid(row=7, column=2, padx=5, pady=5)
    return finValue

def getLight(lightSensor, board, frame, lsLight):
    LSV = 0
    lval = L(lightSensor, board, LSV)
    value = lval.LSV
    sys.stdout.write("\033[K")
    if value > 1500:
        lsLightLabel = Label(frame, text=(' ON '), fg='green', borderwidth=1).grid(row=19,column=3,padx=5,pady=5)
        l(lsLight, board).LedOn()
    else:
        lsLightLabel = Label(frame, text=('OFF'), fg='red', borderwidth=1).grid(row=19, column=3, padx=5, pady=5)
        l(lsLight, board).LedOff()
    print ('### Light Sensor Value = ' + str(value))
    LightValue = Label(frame, text=(value), borderwidth=1)
    LightValue.grid(row=5, column=2, padx=5, pady=5)
    return value

def ButtonSwitch(fadeLed, lightButton, board, lightState,frame, buzzSensor, buzzButton):
    while True:
        time.sleep(0.05)
        if board.input(lightButton) == False:
            if lightState == 'on':
                lsta = Label(frame, text=('OFF'), borderwidth=1, fg=('red')).grid(row=14,column=3,padx=5,pady=5)
                l(fadeLed, board).LedOff()
                lightState = 'off'
            elif lightState == 'off':
                lsta = Label(frame, text=(' ON '), borderwidth=1, fg=('green')).grid(row=14, column=3, padx=5, pady=5)
                l(fadeLed, board).LedOn()
                lightState = 'on'
        if board.input(buzzButton) == False:
            doorbell = Label(frame, text=(' ON '), borderwidth=1, fg=('green'))
            doorbell.grid(row=16, column=2, padx=5, pady=5)
            for i in range(1,6):
                b(buzzSensor, board).buzzOn()
                time.slee(0.1)
                b(buzzSensor, board).buzzOff()
            doorbell = Label(frame, text=('OFF'), borderwidth=1, fg=('red'))
            doorbell.grid(row=16, column=2, padx=5, pady=5)


'''
def lsLightMethod(board, frame):

'''
def tempLight(board, f, ledRed, ledGreen, ledBlue, highTemp, lowTemp):
    if f <= lowTemp:
        l(ledBlue, board).LedOn()
        l(ledGreen, board).LedOff()
        l(ledRed, board).LedOff()
    elif f >= highTemp:
        l(ledRed, board).LedOn()
        l(ledGreen, board).LedOff()
        l(ledBlue, board).LedOff()
    else:
        l(ledGreen, board).LedOn()
        l(ledRed, board).LedOff()
        l(ledBlue, board).LedOff()

def Closeness(board, buzzSensor, dist):
    if dist <= 5:
        b(buzzSensor, board).buzzOn()
        time.sleep(0.6)
        b(buzzSensor, board).buzzOff()
    elif dist <= 10:
        b(buzzSensor, board).buzzOn()
        time.sleep(0.45)
        b(buzzSensor, board).buzzOff()
    elif dist <= 15:
        b(buzzSensor, board).buzzOn()
        time.sleep(0.35)
        b(buzzSensor, board).buzzOff()
    elif dist <= 20:
        b(buzzSensor, board).buzzOn()
        time.sleep(0.2)
        b(buzzSensor, board).buzzOff()
    elif dist <= 25:
        b(buzzSensor, board).buzzOn()
        time.sleep(0.1)
        b(buzzSensor, board).buzzOff()
    else:
        b(buzzSensor, board).buzzOn()
        time.sleep(0.03)
        b(buzzSensor, board).buzzOff()

def setLcd(line1, line2, frame):
    lcd.lcd_string(str(line1.get()), lcd.LCD_LINE_1)
    lcd.lcd_string(str(line2.get()), lcd.LCD_LINE_2)
    lcd1Label = Label(frame, text=(' ' + line1.get()), borderwidth=1, width=17, fg='white', bg='blue', height=1, anchor=W, justify=LEFT).grid(row=13,column=1,padx=5,pady=5)
    lcd2Label = Label(frame, text=(' ' + line2.get()), borderwidth=1, width=17, fg='white', bg='blue', height=1, anchor=W, justify=LEFT).grid(row=14,column=1,padx=5,pady=5)

def testBuzz(board, buzzSensor, frame):
    BuzzValue = Label(frame, text=(' ON '), fg='green', borderwidth=1).grid(row=7, column=2, padx=5, pady=5)
    b(buzzSensor, board).buzzTest()
    BuzzValue = Label(frame, text=('OFF'), fg='red', borderwidth=1).grid(row=7, column=2, padx=5, pady=5)

def clearLcd(line1, line2, frame):
    lcd1Label = Label(frame, text=(' '), borderwidth=1, width=17, fg='white', bg='blue', height=1, anchor=W, justify=LEFT).grid(row=13,column=1,padx=5,pady=5)
    lcd2Label = Label(frame, text=(' '), borderwidth=1, width=17, fg='white', bg='blue', height=1, anchor=W, justify=LEFT).grid(row=14,column=1,padx=5,pady=5)
    lcd.lcd_clear()

def createWidgets(frame, root):
    ##################################################
    #titleLabel = Label(frame, text=('Home\nAutomation\nSystem'), borderwidth=1).grid(row=1, column=1, padx=5, pady=5)
    ##################################################
    for i in range(1,4):
        sepLabel = Label(frame, text=('###########'), borderwidth=1).grid(row=2, column=i, padx=5, pady=5)
    ##################################################
    PirLabel = Label(frame, text=('Pir Value: '), borderwidth=1).grid(row=3, column=1, padx=5, pady=5)
    TempLabel = Label(frame, text=('Temperature: '), borderwidth=1).grid(row=4, column=1, padx=5, pady=5)
    LightLabel = Label(frame, text=('Light Sensor Value: '), borderwidth=1).grid(row=5, column=1, padx=5, pady=5)
    DistLabel = Label(frame, text=('Distance: '), borderwidth=1).grid(row=6, column=1, padx=5, pady=5)
    BuzzerLabel = Label(frame, text=('Buzzer: '), borderwidth=1).grid(row=7, column=1, padx=5, pady=5)
    ##################################################
    line1lab = Label(frame, text=('LCD Line 1: '), fg='blue', borderwidth=1).grid(row=8,column=1,padx=5,pady=2)
    line2lab = Label(frame, text=('LCD Line 2: '), fg='blue', borderwidth=1).grid(row=9, column=1, padx=5, pady=2)
    ##################################
    line1 = StringVar(frame, value='')
    lcdLine1 = Entry(frame, bd =2, width=16, textvariable=line1).grid(row=8,column=2,padx=5,pady=2)
    ##################################
    line2 = StringVar(frame, value='')
    lcdLine2 = Entry(frame, bd=2, width=16, textvariable=line2).grid(row=9, column=2, padx=5, pady=2)
    ##################################
    lcdBut = Button(frame, text=('Set Text'), borderwidth=1, width=11, command=lambda: setLcd(line1, line2, frame)).grid(row=8, column=3, padx=5, pady=2)
    lcdClearBut = Button(frame, text=('Clear LCD'), borderwidth=1, width=11, command=lambda: clearLcd(line1, line2, frame)).grid(row=9, column=3, padx=5, pady=2)
    ##################################################
    BuzzButton = Button(frame, text=('Use Buzzer'), borderwidth=1, width=11, command=lambda: testBuzz(board, 35, frame)).grid(row=7,column=3,padx=5,pady=2)
    CloseButton = Button(frame, text=('Quit'), fg=('red'), borderwidth=1, command=lambda: root.quit()).grid(row=1, column=2, padx=5, pady=5)
    HelpButton = Button(frame, text=('Help'), fg=('black'), bg=('yellow'), borderwidth=1, command=lambda: helpscreen).grid(row=1,column=1,padx=5,pady=5)
    ##################################################
    for i in range(1,4):
        sepLabel = Label(frame, text=('###########'), borderwidth=1).grid(row=11, column=i, padx=5, pady=5)
    ##################################################
    lcdLabel = Label(frame, text=('LCD State'),borderwidth=1).grid(row=12,column=1,padx=5,pady=5)
    lcd1Label = Label(frame, text=(line1.get()), borderwidth=1, width=17, fg='white', bg='blue', height=1, anchor=W, justify=LEFT).grid(row=13,column=1,padx=5,pady=5)
    lcd2Label = Label(frame, text=(line2.get()), borderwidth=1, width=17, fg='white', bg='blue', height=1, anchor=W, justify=LEFT).grid(row=14,column=1,padx=5,pady=5)
    ##################################################


def helpscreen():
    messagebox.showinfo("Help", "Welcome to the the Home Automation help screen.\n \nClick the buttons on the same row as the modules to recieve the sensor value manually.\n \nUsing the text box's, enter what you want to be displayed on the LCD Screen and press 'Set Text' to display it on screen.\n \n")
