from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

def callHub():
    oled.fill(0)
    oled.text("Password Manager",0,0)
    oled.text("A to Search",20,10)
    oled.text("B to Create",20,20)
    oled.show()
    
def callLock(text):
    oled.fill(0)
    oled.text("Enter Password:",0,0)
    oled.text(text,0,20)
    oled.text("A to Enter",20,50)
    oled.show()
    
def callNewName(currName):
    oled.fill(0)
    oled.text("Enter Name:",0,0)
    oled.text(currName,0,15)
    oled.text("A to Accept",20,30)
    oled.text("B to go Back",20,40)
    oled.show()
    
def callNewPass(accName,genPass):
    oled.fill(0)
    oled.text("Do you want",20,0)
    oled.text(accName,((128-(len(accName)*8))//2),10)
    oled.text("to have password",0,20)
    oled.text(genPass,20,30)
    oled.text("A-Accept B-Back",0,40)
    oled.text("C-Regenerate",0,50)
    oled.show()
    
def callSearchPass(search,results):
    oled.fill(0)
    oled.text("Enter Search:",0,0)
    oled.text(search,0,10)
    oled.text("A-"+results[0],0,20)
    oled.text("B-"+results[1],0,30)
    oled.text("C-"+results[2],0,40)
    oled.text("#-Back",0,50)
    oled.show()
    
def callSelectPass(selected,password):
    oled.fill(0)
    oled.text(selected,0,0)
    oled.text(password,0,15)
    oled.text("A to Type",0,30)
    oled.text("B to Delete",0,40)
    oled.text("C to go Back",0,50)
    oled.show()

def callFavourites(favDict):
    oled.fill(0)
    oled.text("Favourites",0,0)
    oled.text("1-"+favDict["1"],0,10)
    oled.text("2-"+favDict["2"],0,20)
    oled.text("3-"+favDict["3"],0,30)
    oled.text("4-"+favDict["4"],0,40)
    oled.text("5-"+favDict["5"],0,40)
    oled.show()
    
    