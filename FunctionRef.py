import random

def encrypt(plaintext,cipher):
    if len(plaintext) > 16:
        plaintext = plaintext + " "*(16-len(plaintext)%16)
    if len(plaintext) < 16:
        plaintext = plaintext + " "*(16-len(plaintext))
    charlist = []
    for char in plaintext:
        charlist.append(char)
    pointer = 0
    grid = []
    tmpgrid = []
    tmprow = []
    while pointer < len(charlist):
        for i in range(0,4):
            for j in range(0,4):
                tmp = ord(charlist[pointer])
                tmprow.append(tmp^cipher)
                pointer = pointer + 1
            tmpgrid.append(tmprow)
            tmprow = []
        grid.append(tmpgrid)
        tmpgrid = []
    return grid

def decrypt(decgrid,cipher):
    outstring = ""
    for decsubgrid in decgrid:
        for decline in decsubgrid:
            for decitem in decline:
                outstring = outstring + chr(decitem ^ cipher)
    return outstring.strip()

def genPass():
    # List of characters to choose from for the password
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%&()_+-=;:?/\\"
    password_length = 10
    password = ""
    while len(password) < password_length:
      password += random.choice(characters)
    return password

def returnSearched(query,accList):
    results = []
    if len(query) > 0:
        for item in accList.keys():
            if item.startswith(query) == True:
                results.append(item)
        if len(results) == 0:
            for item in accList.keys():
                if len(query) > 1:
                    if item.startswith(query[:-1]) == True:
                        results.append(item)
        if len(results) == 0 and len(query) > 2:
            for item in accList.keys():
                if query in item:
                    results.append(item)
    sortedRes = sorted(results, key=len)
    if len(sortedRes) < 3:
        for i in range(0,3-len(sortedRes)):
            sortedRes.append("")
    print(sortedRes)
    return sortedRes
    
def serialSend(text):
    return
