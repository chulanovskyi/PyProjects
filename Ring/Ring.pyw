# -*- coding: utf-8 -*-
try:
    from tkinter import *
except:
    from Tkinter import *
try:
    import tkinter.ttk as ttk
except:
    import ttk
from itertools import count
import os
import ast
import time
import winsound
try:
    import ConfigParser
except:
    import configparser


class alarmClock():
    
    alarms = {}
    alarmTime = {}
    soundBox = os.listdir("soundBox")
    soundBox.insert(0, '')
    
        
    def makeFrame(self, windowToPlaceIn, row_position, col_position):
        next(_ids)


        def doOn(event):
            caller = event.widget.winfo_parent()
            if indicator["background"] != "lawngreen":
                for key, val in self.alarms.items():
                    for item in self.alarms[key]:
                        if caller in item.winfo_parent() and item.winfo_class() == "Entry":
                            self.alarmTime[val[3]] = val[0].get()+":"+val[1].get()+":00"
                        break
            indicator["background"] = "lawngreen"


        def doOff(event):
            caller = event.widget.winfo_parent()
            tempDict = self.alarmTime.copy()
            if indicator["background"] != "red":
                for key, val in tempDict.items():
                    if caller in key.winfo_parent():
                        del self.alarmTime[key]
            indicator["background"] = "red"

        
        alarmFrame = Frame(windowToPlaceIn,\
                           width=20,\
                           highlightthickness=1,\
                           highlightbackground="black")

        planLabel = Label(alarmFrame, text=""+str(_ids)[6], font=13)
        planLabel.grid(column=0, columnspan=4, row=0)

        onOff = StringVar()
        
        onRbutton = Radiobutton(alarmFrame,\
                                text="Вкл",\
                                variable=onOff,\
                                value="lawngreen",\
                                indicatoron=False)
        onRbutton.grid(column=4, row=0, sticky="E", padx=42)
        onRbutton.bind("<Button-1>", doOn)
        
        offRbutton = Radiobutton(alarmFrame,\
                                 text="Выкл",\
                                 variable=onOff,\
                                 value="red",\
                                 indicatoron=False)
        offRbutton.grid(column=4, row=0, sticky="E")
        offRbutton.bind("<Button-1>", doOff)
        
        indicator = Label(alarmFrame, background="red", width=2)
        indicator.grid(column=4, row=0, sticky="W")
        
        self.addAlarm(alarmFrame)
        self.addAlarm(alarmFrame)
        self.addAlarm(alarmFrame)
        self.addAlarm(alarmFrame)

        alarmFrame.grid(column=col_position, row=row_position, padx=2, pady=4)


    def addAlarm(self,frame):
        
        hourInput = Entry(frame, width=2)
        hourInput.insert(0, "00")
        hourInput.bind("<Any-KeyRelease>", self.scanEntry)
        hourInput.bind("<FocusOut>", self.checkH)
        hourInput.grid(column=0, row=len(self.alarms)+1, pady=2)

        doubleDot = Label(frame, text=":")
        doubleDot.grid(column=1, row=len(self.alarms)+1)

        minuteInput = Entry(frame, width=2)
        minuteInput.insert(0, "00")
        minuteInput.bind("<Any-Key>", self.scanEntry)
        minuteInput.bind("<FocusOut>", self.checkM)
        minuteInput.grid(column=2, row=len(self.alarms)+1, pady=2)

        soundIcon = PhotoImage(file="images\\speaker.gif")
        testSound = Button(frame, image=soundIcon)
        testSound.image = soundIcon
        testSound.grid(column=3, row=len(self.alarms)+1, padx=5, pady=5)
        testSound.bind("<Button-1>", self.playSound)

        sound = ttk.Combobox(frame, values=self.soundBox, state="readonly", width=10)
        sound.grid(column=4, row=len(self.alarms)+1)

        self.alarms[len(self.alarms)+1] = [hourInput, minuteInput, testSound, sound]


    def checkH(self, event):
        caller = event.widget
        if not caller.get():
            caller.insert(0, "00")
        elif int(caller.get()) > 23:
            self.clean(event)
            caller.insert(0, "23")
        if len(caller.get()) < 2:
            caller.insert(0,"0")


    def checkM(self, event):
        caller = event.widget
        if not caller.get():
            caller.insert(0, "00")
        if int(caller.get()) > 59:
            self.clean(event)
            caller.insert(0, "59")
        if len(caller.get()) < 2:
            caller.insert(0,"0")


    def scanEntry(self, event):
        caller = event.widget
        count = len(caller.get())
        if not caller.get().isdigit():
            caller.delete(caller.index(END)-1)
        if count > 2:
            caller.delete(caller.index(END)-1)


    def clean(self, event):
        caller = event.widget
        caller.delete("0", "end")


    def playSound(self, event):
        caller = event.widget
        for key, val in self.alarms.items():
            if caller in val:
                sound = "soundBox\\" + self.alarms[key][3].get()
                winsound.PlaySound(sound, winsound.SND_FILENAME)
        
    
def alarmInfo():
    logo = PhotoImage(file="images\\logo.gif")
    showMessage = Toplevel(root, takefocus=True)
    showMessage.title("!")
    screenSizeX = str(int(showMessage.winfo_screenwidth()/2)-50)
    screenSizeY = str(int(showMessage.winfo_screenheight()/2)-60)
    message = Label(\
        showMessage,\
        compound = LEFT,\
        text=_message.get(),\
        background="white",\
        image=logo,\
        font=18)
    message.image = logo
    message.pack()
    widgetSizeX = str(len(_message.get())+70+logo.width())
    widgetSizeY = str(logo.height()+40)
    okButton = Button(showMessage, text="OK", command=showMessage.destroy)
    okButton.pack(pady=5)
    okButton.focus_set()
    showMessage.geometry(widgetSizeX+"x"+widgetSizeY+"+"+str(screenSizeX)[:-2]+"+"+str(screenSizeY)[:-2])
    showMessage.lift()
    showMessage.wm_attributes('-topmost',1)

def infoOn(event):
    messageIndicator['background'] = 'lawngreen'

def infoOff(event):
    messageIndicator['background'] = 'red'

    
def updateTime():
    clock.after(1000, updateTime)
    clock['text'] = time.strftime('%H:%M:%S')
    if _clockWindow:
        _clockWindow.wm_attributes('-topmost',1)
    if alarmObject.alarmTime:
        for k, v in alarmObject.alarmTime.items():
            if v == clock['text']:
                getSound = "soundBox\\" + k.get()
                winsound.PlaySound(getSound, winsound.SND_FILENAME)
                if messageIndicator['background'] == 'lawngreen':
                    alarmInfo()

def addClockWindow():
    global _clockWindow

    def updateTimeWidget():
        clockWidget.after(1000, updateTimeWidget)
        clockWidget['text'] = time.strftime('%H:%M')


    def closeClock(event):
        global _clockWindow
        _clockOnOff.set(0)
        _clockWindow.destroy()
        _clockWindow = None

    def startMove(event):
        _clockWindow.x = event.x
        _clockWindow.y = event.y

    def stopMove(event):
        _clockWindow.x = None
        _clockWindow.y = None

    def onMotion(event):
        deltaX = event.x - _clockWindow.x
        deltaY = event.y - _clockWindow.y
        x = _clockWindow.winfo_x() + deltaX
        y = _clockWindow.winfo_y() + deltaY
        _clockWindow.geometry("+"+str(x)+"+"+str(y))
            
    if not _clockWindow:
        _clockWindow = Toplevel(root,background='white')
        _clockWindow.wm_attributes('-topmost',1)
        _clockWindow.overrideredirect(True)
        _clockWindow.bind("<Double-Button-1>", closeClock)
        _clockWindow.bind("<ButtonPress-1>", startMove)
        _clockWindow.bind("<B1-Motion>", onMotion)
        screenWidth = (_clockWindow.winfo_screenwidth()/2) -80
        screenHeight = _clockWindow.winfo_screenheight() -30
        _clockWindow.geometry("160x30"+"+"+str(screenWidth)[:-2]+"+"+str(screenHeight))
        
        clockWidget = Label(_clockWindow, text=time.strftime('%H:%M'), font=('Arial',18), background='white')
        clockWidget.pack(side=RIGHT)
        clockWidget.after_idle(updateTimeWidget)

        clockDate = Label(_clockWindow, text=time.strftime('%d.%m.%Y'), font=('Arial',13), background='white')
        clockDate.pack(side=RIGHT)


def clockOn(event):
    addClockWindow()
    
def clockOff(event):
    global _clockWindow
    if _clockWindow:
        _clockWindow.destroy()
        _clockWindow = None
    

def addMessage(event):
    global _editMessage

    
    def sendText(event):
        global _editMessage
        _message = message.get()
        _editMessage.destroy()
        _editMessage = None

    def closeCross():
        global _editMessage
        _message = message.get()
        _editMessage.destroy()
        _editMessage = None

    if not _editMessage:
        _editMessage = Toplevel(root)
        _editMessage.resizable(width=FALSE, height=FALSE)
        _editMessage.bind("<Alt-F4>", sendText)
        _editMessage.protocol("WM_DELETE_WINDOW", closeCross)
        askEnter = Label(_editMessage, text="Введите текст")
        askEnter.pack()
        message = Entry(_editMessage, textvariable=_message)
        message.bind("<Return>", sendText)
        message.pack()
        message.focus_set()
        okButton = Button(_editMessage, text="Ok")
        okButton.bind("<Button-1>", sendText)
        okButton.pack()
        
        frameWidth = 124
        frameHeight = 66
        _editMessage.geometry(str(frameWidth)+'x'+str(frameHeight)+'+'+\
                              str((root.winfo_screenwidth()/2)-frameWidth/2)[:-2]+"+"+\
                              str((root.winfo_screenheight()/2)-frameHeight/2)[:-2])
        

def readCfg():
    try:
        config = ConfigParser.ConfigParser()
    except(NameError):
        config = configparser.ConfigParser()
    config.readfp(open('config.cfg'))
    for alarm in config.items('AlarmsCfg'):
            hourMinuteSound = ast.literal_eval(alarm[1])
            alarmObject.alarms[int(alarm[0])][0].delete(0, END)
            alarmObject.alarms[int(alarm[0])][0].insert(0, hourMinuteSound[0])
            alarmObject.alarms[int(alarm[0])][1].delete(0, END)
            alarmObject.alarms[int(alarm[0])][1].insert(0, hourMinuteSound[1])
            alarmObject.alarms[int(alarm[0])][3].current(\
                alarmObject.alarms[int(alarm[0])][3]['values'].index(hourMinuteSound[2]))

def writeCfg():
    try:
        config = ConfigParser.ConfigParser()
    except(NameError):
        config = configparser.ConfigParser()
    config.add_section('AlarmsCfg')
    for alarmNum in range(1,len(alarmObject.alarms)+1):
        config.set('AlarmsCfg',str(alarmNum),\
                   str([alarmObject.alarms[alarmNum][0].get(),\
                    alarmObject.alarms[alarmNum][1].get(),\
                    alarmObject.alarms[alarmNum][3].get()]))
    with open('config.cfg', 'w') as cfgFile:
        config.write(cfgFile)


def close():
    writeCfg()
    root.destroy()


root = Tk()
rootWidth = 385
rootHeight = 515
root.geometry(str(rootWidth)+'x'+str(rootHeight)+'+'+\
              str((root.winfo_screenwidth()/2)-rootWidth/2)[:-2]+"+"+\
              str((root.winfo_screenheight()/2)-rootHeight/2)[:-2])
root.resizable(width=FALSE, height=FALSE)
root.iconbitmap(r'images\\icon.ico')
root.title('Time')

_editMessage = None
_clockWindow = None

_ids = count(0)

_onOffMessage = StringVar()

_message = StringVar()
_message.set("Перерыв")

_clockOnOff = IntVar()

alarmObject = alarmClock()
alarmObject.makeFrame(root,0,0)
alarmObject.makeFrame(root,0,1)
alarmObject.makeFrame(root,1,0)
alarmObject.makeFrame(root,1,1)
alarmObject.makeFrame(root,2,0)
alarmObject.makeFrame(root,2,1)

#_________________________________________
message_frame = Frame(root)
message_frame.grid(column=0, row=3)

offMRbutton = Radiobutton(message_frame, text="Выкл", variable=_onOffMessage, value='red', indicatoron=False)
offMRbutton.bind("<Button-1>", infoOff)
offMRbutton.pack(side=RIGHT)

onMRbutton = Radiobutton(message_frame, text="Вкл", variable=_onOffMessage, value='lawngreen', indicatoron=False)
onMRbutton.bind("<Button-1>", infoOn)
onMRbutton.pack(side=RIGHT)

messageIndicator = Label(message_frame, background = "red", width=2)
messageIndicator.pack(side=RIGHT, padx=10, pady=10)

messageButton = Button(message_frame, text="Текст")
messageButton.bind("<Button-1>", addMessage)
messageButton.pack(side=RIGHT)

clock_frame = Frame(root)
clock_frame.grid(column=1, row=3)

offClockButton = Radiobutton(clock_frame, text="Выкл", variable=_clockOnOff, value=1, indicatoron=False)
offClockButton.bind("<Button-1>", clockOff)
offClockButton.pack(side=RIGHT)

onClockButton = Radiobutton(clock_frame, text="Вкл", variable=_clockOnOff, value=2, indicatoron=False)
onClockButton.bind("<Button-1>", clockOn)
onClockButton.pack(side=RIGHT)

clock = Label(clock_frame, text="time")
clock.after_idle(updateTime)
clock.pack(side=RIGHT)

#DEBUGBUTTON = Button(clock_frame, text="DEBUG", command=alarmInfo)
#DEBUGBUTTON.grid(column=0, row=2)
#_____________________________________________

readCfg()

root.protocol("<Alt-F4>", close)
root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()
