import time, sys, threading, os, glob
from bottle import *
import json, inspect
from board import Board
import pins
import methods as M # All methods stored here
from lcd1602 import LCD1602
from tkinter import *

board = Board().board
lcd = LCD1602(board)

s = [100,100,100]
#enable bottle debug
debug(True)
# WebApp route path
routePath = ''
# get directory of WebApp (bottleJQuery.py's dir)
rootPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

@route(routePath)
def rootHome():
    return redirect(routePath+'/index.html')

@route(routePath + '/<filename:re:.*\.html>')
def html_file(filename):
    return static_file(filename, root=rootPath)

@route('/text', method='POST')
def getText(frame):
    text1 = request.forms.get('texttodisplay1')
    text2 = request.forms.get('texttodisplay2')
    print('------------------------------------------------------------')
    print('DEBGUG: text1 = ' + str(text1) + '\n' + 'DEBGUG: text2 = ' + str(text2))
    print('------------------------------------------------------------')
    lcd.lcd_string(text1, lcd.LCD_LINE_1)
    lcd.lcd_string(text2, lcd.LCD_LINE_2)
    lcd1Label = Label(frame, text=(text1), borderwidth=1, width=17, fg='white', bg='blue', height=1,anchor=W, justify=LEFT)
    lcd1Label.grid(row=13, column=1, padx=5, pady=5)  # Allignment on the grid
    lcd2Label = Label(frame, text=(text2), borderwidth=1, width=17, fg='white', bg='blue', height=1, anchor=W,justify=LEFT)
    lcd2Label.grid(row=14, column=1, padx=5, pady=5)

@route('/setup', method='GET')
def setup(frame):
    print('------------------------------------------------------------')
    notwanted, t = M.getTemp(frame, board, ledBlue, ledGreen, ledRed, highTemp, lowTemp)
    t = str(t)
    ###
    p = M.getPir(pirSensor, board, pirLight, buzzSensor, frame)
    p = str(p)
    ###
    l = M.getLight(lightSensor, board, frame, lsLight)
    l = str(l)
    ###
    d = M.getDist(dtSensor, deSensor, board, frame)
    d = str(d)
    print('------------------------------------------------------------')
    ###
    data = {}
    data['temp'] = t
    data['pir'] = p
    data['lightsensor'] = l
    data['distance'] = d
    json_data = json.dumps(data)
    return json_data

#Pins
tempSensor = 7
tempLed = 23
dtSensor = 29
deSensor = 31
pirSensor = 32
buzzSensor = 35
fadeLed = 11
lightButton = 22
lightSensor = 18
pirLight = 10
ledRed = 36
ledGreen = 38
ledBlue = 40
buzzButton = 16
lsLight = 12

highTemp = 68
lowTemp = 63

root = Tk()
print('')
root.title('Home Automation System by Reece Small')
frame = Frame(root)
frame.grid()

try:
    M.tempSet()
    M.pisetup()
    #screen = threading.Thread(target=M.ButtonSwitch, args=(fadeLed, lightButton, board, lightState, frame, buzzButton, buzzSensor)).start()
    M.createWidgets(frame, root)
    M.mainWidgets(frame)
    print('')
    #threading.Thread(target=run(host='0.0.0.0', port=8080, reloader=False).start()) # BOTTLE
    #threading.Thread(target=root.mainloop().start())
    run(host='0.0.0.0', port=8080, reloader=False)
    root.mainloop()
    print('\n \n### Exiting ###')
    lcd.lcd_clear()
    board.cleanup()
    sys.exit()
except (KeyboardInterrupt):
    print('\n \n \n \n### Exiting ###')
    root.destroy()
    lcd.lcd_clear()
    board.cleanup()
    sys.exit()
