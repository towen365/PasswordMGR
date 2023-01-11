import machine
import sdcard
import uos
import json

import utime

#from lock import callLock

CS = machine.Pin(9, machine.Pin.OUT) #Sets up pins associated with the SD card and creates an instance of the SD object
spi = machine.SPI(1,baudrate=1000000,polarity=0,phase=0,bits=8,firstbit=machine.SPI.MSB,sck=machine.Pin(10),mosi=machine.Pin(11),miso=machine.Pin(12))
sd = sdcard.SDCard(spi,CS)
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

col_list=[16,17,18,19] #sets pins associated with keypad
row_list=[20,21,22,26]

activescreen = "Lock"
#callLock()
currentPassword = ""
exOutput = ""
password = 0

for x in range(0,4):
    row_list[x]=Pin(row_list[x], Pin.OUT) #sets row pins to output pins
    row_list[x].value(1)

for x in range(0,4):
    col_list[x] = Pin(col_list[x], Pin.IN, Pin.PULL_UP) #sets column pins to input pins

#create a keypad I can later reference as coordinates
key_map=[["1","4","7","*"],\
         ["A","B","C","D"],\
         ["3","6","9","#"],\
         ["2","5","8","0"]]

while True:
    key=Keypad4x4Read(col_list, row_list)
    if key != None:
        if activescreen == "Lock":
            lockInput(key)
        if activescreen == "Hub":
            hubInput(key)
        if activescreen == "NewName"
            newNameInput(key)
            
def newNameInput(key):
    return

def hubInput(key):
    if key == "B":
        activescreen = "NewName"
        callNewName()
    if key == "A":
        activescreen = "SearchPass"
        callSearchPass()
    
def lockInput(key):
    if key not in "ABCD*#": #checks if input is key entry
        currentPassword = currentPassword + key #adds key to string and updates the screen
        callLock(currentPassword)
    elif key == "*":
        currentPassword = currentPassword[:-1] #deletes the last character in the string
    elif key == "A":
        if decrypt(currentPassword) == exOutput: #uses decryption algorithm as a hash, checks password against known hash
            password = int(currentPassword)
            activeScreen = "Hub" #changes screen
            onLogin(password)
            callHub()
        else:
            callLock("wrong")
            utime.sleep(1)
            currentPassword = ""
            callLock(currentPassword)

def onLogin(key):
    with open("/sd/data.txt", "r") as file:
        encryptedRead = file.read() #dumps contents of SD card into a variable
        #do something with json here xx
        dictionary = decrypt(encryptedRead,key) #Decrypts contents of SD card

def Keypad4x4Read(cols,rows):
  for r in rows:
    r.value(0)
    result=[cols[0].value(),cols[1].value(),cols[2].value(),cols[3].value()]
    if min(result)==0:
      key=key_map[int(rows.index(r))][int(result.index(0))]
      r.value(1) # manages key keept pressed
      return(key)
    r.value(1)

currentText = ""
letterMap = {"1":[""],"2":["a","b","c"],"3":["d","e","f"],"4":["g","h","i"],"5":["j","k","l"],"6":["m","n","o"],"7":["p","q","r","s"],"8":["t","u","v"],"9":["w","x","y","z"],"0":" "}
floatingInput = ""
floatingChar = ""
floatingReps = 0

def clearTyping(): #function to reset the value of all variable associated with typing
    global currentText, letterMap, floatingInput, floatingChar, floatingReps
    floatingInput = ""
    floatingChar = ""
    floatingReps = 0
    currentText = ""

def Typing(key):
    global currentText, letterMap, floatingInput, floatingChar, floatingReps
    if key == "*":
        if floatingInput == "":
            currentText = currentText[:-1]
        floatingInput = ""
        floatingChar = ""
        floatingReps = 0
    else:
        if key == floatingChar:
            floatingReps = floatingReps + 1
        else:
            currentText = currentText + floatingInput
            floatingInput = ""
            floatingChar = key
            floatingReps = 0
        try:
            floatingIndex = len(nokia[key])
            floatingInput = nokia[key][floatingReps%floatingIndex]
        except:
            print("NO!")  
    
    
    
# while True:
#     on keypad press:
#         if active screen == ...:
#             command = activescreencall(key, relevant vars)
#             if command == nextscreen:
#                 nextscreen()