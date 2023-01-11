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
    
def callNewName():
    oled.fill(0)
    oled.text("Enter Name:",0,0)
    oled.text("A to Accept",20,30)
    oled.text("B to go Back",20,40)
    oled.show()
    
def callNewPass(passwordName,genPass):
    oled.fill(0)
    oled.text("Do you want",20,0)
    oled.text(passwordName,((128-(len(passwordName)*8))//2),10)
    oled.text("to have password",0,20)
    oled.text(genPass,20,30)
    oled.text("A-Accept B-Back",0,40)
    oled.text("C-Regenerate",0,50)
    oled.show()
    
def callSearchPass(search):
    oled.fill(0)
    oled.text("Enter Search:",0,0)
    oled.text(search,0,10)
    oled.text("A-Search1 ",0,20)
    oled.text("B-Search2",0,30)
    oled.text("C-Search3",0,40)
    oled.text("#-Back",0,50)
    oled.show()
    
def callSelectPass(selected,password):
    oled.fill(0)
    oled.text(selected,0,0)
    oled.text(password,0,15)
    oled.text("A to Type",0,30)
    oled.text("B to Delete",0,40)
    oled.text("C to Quit",0,50)
    oled.show()