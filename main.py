import machine
from machine import Pin
import sdcard
import uos

import json

import utime

import hashlib

from FunctionRef import encrypt,decrypt,genPass,returnSearched, serialSend
from ScreenRef import callHub,callLock,callNewName,callNewPass,callSearchPass,callSelectPass,callFavourites

def searchPassInput(key):
    global floatingText, selectedPass, activescreen
    if key not in "ABC#":
        Typing(key)
        callSearchPass(floatingText,returnSearched(floatingText,passDict))
    if key in "ABC":
        returned = returnSearched(floatingText,passDict)
        if key == "A":
            if returned[0] != "":
                selectedPass = returned[0]
        if key == "B":
            if returned[1] != "":
                selectedPass = returned[1]
        if key == "C":
            if returned[2] != "":
                selectedPass = returned[2]
        activescreen = "SelectPass"
        callSelectPass(selectedPass,passDict[selectedPass])
    if key == "#":
        activescreen = "Hub"
        callHub()
        clearTyping()

def selectPassInput(key):
    global selectedPass, activescreen
    if key in "ABC":
        if key == "A":
            serialSend(passDict[selectedPass])
            callSelectPass(selectedPass,"completed")
            utime.sleep(1)
        if key == "B":
            delAccount(selectedPass)
            callSelectPass(selectedPass,"completed")
            utime.sleep(1)
        activescreen = "Hub"
        callHub()
            
def addNewAccount(username,givenPass):
    global passDict,password
    passDict[username] = givenPass
    with open("/sd/data.txt", "w") as file:
        file.write(hashOut+"\r\n")
        file.write(str(encrypt(json.dumps(passDict),password)))
        
def delAccount(username):
    global passDict
    del passDict[username]
    with open("/sd/data.txt", "w") as file:
        file.write(hashOut+"\r\n")
        file.write(str(encrypt(json.dumps(passDict),password)))

def newPassInput(key):
    global activescreen,newName,newPass
    if key == "A":
        addNewAccount(newName,newPass)
        callNewPass(newName,"Completed")
        utime.sleep(1)
        activescreen = "Hub"
        callHub()
    elif key == "B":
        activescreen = "NewName"
        callNewName("")
    elif key == "C":
        newPass = genPass()
        callNewPass(newName,newPass)

def newNameInput(key):
    global activescreen,floatingText,newName,newPass
    if key not in "AB":
        Typing(key)
        callNewName(floatingText)
    elif key == "A":
        newName = floatingText
        clearTyping()
        activescreen = "NewPass"
        newPass = genPass()
        callNewPass(newName,newPass)
    elif key == "B":
        clearTyping()
        activescreen = "Hub"
        callHub()
        
def hubInput(key):
    global activescreen
    if key == "B":
        activescreen = "NewName"
        callNewName("")
    if key == "A":
        activescreen = "SearchPass"
        clearTyping()
        callSearchPass("",["","",""])
    if key == "C":
        callFavourites(favourites)
    
def lockInput(key):
    global currentPassword, activescreen,dictDump, passDict, password
    if key not in "ABCD*#": #checks if input is key entry
        currentPassword = currentPassword + key #adds key to string and updates the screen
        callLock(currentPassword)
    elif key == "*":
        currentPassword = currentPassword[:-1] #deletes the last character in the string
        callLock(currentPassword)
    elif key == "A":
        if str(hashlib.sha256(currentPassword).digest()) == hashOut: #uses decryption algorithm as a hash, checks password against known hash
            password = int(currentPassword)
            print(dictDump)
            print(password)
            print(decrypt(dictDump,password))
            print(type(decrypt(dictDump,password)))
            passDict = json.loads(decrypt(dictDump,password)) #Decrypts contents of SD card
            activescreen = "Hub" #changes screen
            callHub()
        else:
            callLock("wrong")
            utime.sleep(1)
            currentPassword = ""
            callLock(currentPassword)

def Keypad4x4Read(cols,rows):
  for r in rows:
    r.value(0)
    result=[cols[0].value(),cols[1].value(),cols[2].value(),cols[3].value()]
    if min(result)==0:
      key=key_map[int(rows.index(r))][int(result.index(0))]
      r.value(1) # manages key keept pressed
      return(key)
    r.value(1)

floatingText = ""
fixedText = ""
letterMap = {"1":[""],"2":["a","b","c"],"3":["d","e","f"],"4":["g","h","i"],"5":["j","k","l"],"6":["m","n","o"],"7":["p","q","r","s"],"8":["t","u","v"],"9":["w","x","y","z"],"0":" "}
floatingInput = ""
floatingChar = ""
floatingReps = 0

def clearTyping(): #function to reset the value of all variable associated with typing
    global fixedText, floatingText, letterMap, floatingInput, floatingChar, floatingReps
    floatingInput = ""
    floatingChar = ""
    floatingReps = 0
    fixedText = ""
    floatingText = ""

def Typing(key):
    global fixedText, floatingText, letterMap, floatingInput, floatingChar, floatingReps
    if key == "*":
        if floatingInput == "":
            fixedText = fixedText[:-1]
        floatingInput = ""
        floatingChar = ""
        floatingReps = 0
        floatingText = fixedText
    else:
        if key == floatingChar:
            floatingReps = floatingReps + 1
        else:
            fixedText = fixedText + floatingInput
            floatingInput = ""
            floatingChar = key
            floatingReps = 0
        try:
            floatingIndex = len(letterMap[key])
            floatingInput = letterMap[key][floatingReps%floatingIndex]
            floatingText = fixedText + floatingInput
        except:
            print("Out of range, probably, something else could've gone wrong, but this is an except statement so it clearly isn't that bad so like just firm it and keep going.")

CS = machine.Pin(9, machine.Pin.OUT) #Sets up pins associated with the SD card and creates an instance of the SD object
spi = machine.SPI(1,baudrate=1000000,polarity=0,phase=0,bits=8,firstbit=machine.SPI.MSB,sck=machine.Pin(10),mosi=machine.Pin(11),miso=machine.Pin(12))
sd = sdcard.SDCard(spi,CS)
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

col_list=[16,17,18,19] #sets pins associated with keypad
row_list=[20,21,22,26]

currentPassword = ""
exOutput = ""
password = 0

newName = ""
newPass = ""

selectedPass = ""

activescreen = "Lock"
callLock(currentPassword)

passDict = []

favourites = {"1":"amazon","2":"paypal","3":"google","4":"microsoft","5":"lloyds"}

with open("/sd/data.txt", "r") as file:
    hashOut = file.readline().strip('\r\n') #dumps contents of SD card into a variable
    dictDump = json.loads(file.readline()) #do something with json here xx

for x in range(0,4):
    row_list[x]=Pin(row_list[x], Pin.OUT) #sets row pins to output pins
    row_list[x].value(1)

for x in range(0,4):
    col_list[x] = Pin(col_list[x], Pin.IN, Pin.PULL_UP) #sets column pins to input pins

#password = 4568
# newDict = {"paypal": "test1", "amazon": "test", "tmp": "!WgBsDX-V3"}
# with open("/sd/data.txt", "w") as file:
#     file.write(hashOut+"\r\n")
#     file.write(str(encrypt(json.dumps(newDict),password)))


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
        elif activescreen == "Hub":
            hubInput(key)
        elif activescreen == "NewName":
            newNameInput(key)
        elif activescreen == "NewPass":
            newPassInput(key)
        elif activescreen == "SearchPass":
            searchPassInput(key)
        elif activescreen == "SelectPass":
            selectPassInput(key)
    utime.sleep(0.2)
    
    
    
# while True:
#     on keypad press:
#         if active screen == ...:
#             command = activescreencall(key, relevant vars)
#             if command == nextscreen:
#                 nextscreen()