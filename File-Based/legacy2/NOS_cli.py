'''
Novus Ordo Seclorum - Hacker IRC

Please note that this requires the following modules:
timer    (pip install pypiwin32)
easygui  (pip install easygui)

auth.key is stored in this format:
key
enc(usr, key)
enc(pwd, key)
'''
# Import yer stuffs
import sys, time, random, os, threading, base64, webbrowser
from datetime import datetime
sys.path.insert(0, 'E:/misc/coding/scripts/easy')

try:    # Try to import other stuffs (eg. easygui)
    import easygui
except:
    print("There is a critical problem: Required modules are not installed.")

# ===== Set constants =====
IRC_FILEPATH = 'T:/_classDragNDrop/MATH/nos.log'
TIMER_DELAY = 1000
SYMBOLS = chr(30)+chr(31)+""" !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""
ADMIN = 0
CHECKSUM_SCRAMBLER = '''
lol lol lol
'''

# Definitions
def readFile(filePath): # Get the file readout and close it
    fObj = open(filePath, 'r')  # Open a file at filePath
    fRead = fObj.readlines()    # Read the file
    fObj.close()    # Close the file to prevent memory locking
    return fRead

def sendMsg(msg, filePath):
    if msg == 1:
        fMsg = "A user has joined: "+user
    elif msg == 0:
        fMsg = "A user has left: "+user
    else:
        if ADMIN == 0:
            fMsg = '['+user+'] '+msg
        else:
            fMsg = '[(ADMIN) '+user+' '+str(datetime.now())+'] '+msg
    encMsg = enc(fMsg)
    fObj = open(filePath, 'a')
    fObj.write(encMsg+"\n")
    fObj.close()

def sendImg(loc):
    if os.path.isfile(loc):
        pass
    else:
        print('specify image file location (if local, just type "{file}.jpg"')
        return
    global IRC_FILEPATH
#    msg = 'sent image file; open in browser with !open_image'
#    sendMsg(msg, IRC_FILEPATH)
    with open(loc, "rb") as img:
        sti = base64.b64encode(img.read())
        sti = str('img: '+sti)
        encSti = enc(sti)
        fObj = open(IRC_FILEPATH, 'a')
        fObj.write(encSti+'\n')
        fObj.close()
        
def readImg(data):
    data = base64.b64decode(data)
    with open('img.jpg', 'wb') as f:
        f.write(data)
    f.close()
    webbrowser.open('img.jpg')

def main():
    ''' This function reads out an IRC file '''
    # Compare last line in the file to the last line sent
    global lastLine
    lastIrcLine = readFile(IRC_FILEPATH)[-1:][0] # Get the last IRC chat sent
    if lastLine != lastIrcLine:
        print(dec(lastIrcLine.strip()))
    lastLine = lastIrcLine
    #print("Timer executed")#TEMP
    
def l_lines(lines):
    ''' Prints out (lines)# of lines in file '''
    lns = []
    file = readFile(IRC_FILEPATH)
    for x in range(int(lines)+1):
        lns.append(dec(file[-x].strip()))
    lns.reverse()
    for i in lns:
        print(i)
        
# LOGIN SCRIPT
def login():
    global ADMIN
    x = easygui.multpasswordbox("Please enter your usr/pwd:",
                                'NOS_FILE', ("Username", "Password"))
    if x == None:
        sys.exit(401)
    if os.path.isfile('auth.key'):
        xObj = open('auth.key', 'r')
        xComp = xObj.readlines()
        usr = dec(xComp[1].strip(), int(xComp[0].strip()))
        pwd = dec(xComp[2].strip(), int(xComp[0].strip()))
        if x[0] == usr and x[1] == pwd:
            print("Auth complete!")
        else:
            print("Incorrect credentials.")
            sysExit(401)
        try:
            if dec(xComp[3].strip(),int(xComp[0].strip())) == 'admin':
                ADMIN = 1
                print("Admin enabled!")
            else:
                ADMIN = 0
        except:
            ADMIN = 0
        return x[0]
    else:
        easygui.msgbox("No auth.key detected!")
        sys.exit(401)

def enc(code, encryption_num=14815):
    ''' Encrypts code to be used with the dePolymorph/dePolymorph_run functions '''
    final = ''
    if encryption_num == None:
        encryption_num = getRandomNum()
        print("Encryption num = "+str(encryption_num))

    # For each symbol in the code provided
    for symbol in code:
        if symbol in SYMBOLS:   # If the symbol can be encrypted
            symbol_num = ord(symbol)
            symbol_num += encryption_num
            final += str(symbol_num)
    return final

def dec(code, encryption_num=14815, digits=5):
    ''' DePolymorphs Polymorphed code '''
    final = ''

    for i in range(0, len(code), digits):
        symbol = ''
        for j in range(digits):
            symbol += code[i+j]

        symbol = int(symbol)
        symbol_num = symbol - encryption_num
        if (symbol_num != 31) and (symbol_num != 30):
            symbol = chr(symbol_num)
            final += symbol
        elif symbol_num == 30:
            final += '\t'
        else:
            final += '\n'
    return final

def getRandomNum(digits=5):
    ''' Gets a random polymorphic-compatible number with the specified amount of digits '''
    final = 0
    randGen = random.SystemRandom()
    while True:
        final = ''
        for i in range(digits):
            j = randGen.randint(1, 9)
            final += str(j)

        final = int(final)
        finaltemp1 = str(final + 31)
        finaltemp2 = str(final + 126)
        if (len(finaltemp1) == digits) and (len(finaltemp2) == digits):
            break
    return final

def createAuthKey(usr, pwd, adm=True):
    key = getRandomNum()
    encUsr = enc(usr, key)
    encPwd = enc(pwd, key)
    encAdm = ''
    if adm:
        encAdm = enc('admin', key)
    print(key)
    print(encUsr)
    print(encPwd)
    print(encAdm)

def tmr(tmr_stop):
    main()
    if not tmr_stop.is_set():
        threading.Timer(1, tmr, [tmr_stop]).start()

def sysExit(exitCode=1):
    try:
        raw_input("Press enter to continue_")
    except:
        input("Press enter to continue_")
    sys.exit(exitCode)

print("Modules loaded!")

if os.path.isfile(IRC_FILEPATH):
    print("Connecting to IRC file...")
else:
    print("No IRC file found!")
    sysExit(404)

user = login() #Login

# Print the irc log upon startup
for line in readFile(IRC_FILEPATH)[-2:]:
    print(dec(line.strip())) # Prints the last 2 lines sent thru irc
lastLine = readFile(IRC_FILEPATH)[-1:][0]

sendMsg(1, IRC_FILEPATH) # Announce user's login

# === PAST HERE IS (mostly) A TEST ===
# Set a scheduler to update the IRC, messages sent thru easygui.enterbox
x = ''
while True:
    #x = easygui.enterbox('Enter a message. Send !quit to exit.','NOS_FILE')
    tmr_stop = threading.Event()
    tmr(tmr_stop)
    x = input(str('>> '))
    if x != '!quit' and x != None:
        if '!list' in x:
            if x == '':
                print("specify line amount as argument (ex: !list 10)")
            else:
                l_lines(x[6:])
        elif '!open_image' in x:
            lastIrcLine = readFile(IRC_FILEPATH)[-1:][0] # grabbed from main(), finds image sent (only last msg)
            if 'img: ' in lastIrcLine:
                readImg(lastIrcLine[5:-2]) # removes "img: " and "\n" from b64 img
        elif '!image' in x:
            sendImg(x[7:])
        else:
            sendMsg(x, IRC_FILEPATH)
            tmr_stop.set()
    else:
        sendMsg(0, IRC_FILEPATH)
        sys.exit()
#except KeyboardInterrupt:
#    sendMsg(0, IRC_FILEPATH)
#    sys.exit()
