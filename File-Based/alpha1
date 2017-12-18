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
import sys, time, random, os, subprocess

try:    # Try to import other stuffs (eg. easygui)
    import timer
    import easygui
except:
    print("There is a critical problem: Required modules are not installed.")
    print("Attempting to install required modules...")
    subprocess.check_output("pip install pypiwin32",stderr=subprocess.STDOUT,shell=True)
    subprocess.check_output("pip install easygui",stderr=subprocess.STDOUT,shell=True)
    sysExit()

# ===== Set constants =====
IRC_FILEPATH = 'T:/_classDragNDrop/MATH/nos.log'
TIMER_DELAY = 1000
SYMBOLS = chr(30)+chr(31)+""" !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""
ADMIN = 0
# This line scrambles the checksum of this file, making checksum-specific blocks useless
CHECKSUM_SCRAMBLER = '''
rendomnez
'''

# Definitions
def readFile(filePath): # Get the file readout and close it
    fObj = open(filePath, 'r')  # Open a file at filePath
    fRead = fObj.readlines()    # Read the file
    fObj.close()    # Close the file to prevent memory locking
    return fRead

def sendMsg(msg, filePath):
    if msg == 1:
        fMsg = "A user has joined @ "+time.asctime(time.gmtime())+':'+user
    elif msg == 0:
        fMsg = "A user has left @ "+time.asctime(time.gmtime())+':'+user
    else:
        if ADMIN == 0:
            fMsg = '['+user+'] '+msg
        else:
            fMsg = '[(ADMIN) '+user+'@'+time.asctime(time.gmtime())+'] '+msg
    encMsg = enc(fMsg)
    fObj = open(filePath, 'a')
    fObj.write(encMsg+"\n")
    fObj.close()

def main(a, b):
    ''' This function reads out an IRC file '''
    # Compare last line in the file to the last line sent
    global lastLine
    lastIrcLine = readFile(IRC_FILEPATH)[-1:][0] # Get the last IRC chat sent
    if lastLine != lastIrcLine:
        print(dec(lastIrcLine.strip()))
    lastLine = lastIrcLine
    #print("Timer executed")#TEMP

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

def createAuthKey(usr, pwd, adm=False):
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

def sysExit(exitCode=1):
    try:
        raw_input("Press enter to continue_")
    except:
        input("Press enter to continue_")
    sys.exit(exitCode)

def readMsg():
    pass

if __name__ == "__main__":
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
    timerID = timer.set_timer(TIMER_DELAY, main)
    #print("Timer ID: "+str(timerID))
    x = ''
    while x != '!quit' and x != None:
        x = easygui.enterbox('Enter a message. Send !quit (or press Cancel) to exit.','NOS_FILE')
        if x != '!quit' and x != None:
            sendMsg(x, IRC_FILEPATH)
        else:
            sendMsg(0, IRC_FILEPATH)
    timer.kill_timer(timerID)
