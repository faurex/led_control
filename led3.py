import os                       # to read a local directory
import re                       # for regular expressions
import random                   # to generate random numbers
from gpiozero import LED        # to turn led on, off or get the state
from gpiozero import LEDBoard   # to use led objects in a array
from time import sleep          # need wait time in the loop

# Start the code with python3 led3.py or put the line
# sudo python3 /opt/cron/led3.py &
# above the exit 0 in /etc/rc.local for execute the script at reboot or startup.
# With the command
# ps -A | grep python
# you can find the running script in the background and stop it with kill <number>
#
# Maybe you have to install the GPIO Zero package with
# apt install python3-gpiozero
#
# Max LEDs you can control are 4, but you can change it by modify the code
# You can get the led number by execute the command pinout on command line (cli), python3-gpiozero must be installed

#globals
leds = LEDBoard(22, 23)                     # Max 4 entries, like LEDBoard(22, 23, 24, 25)
ident = [0, 1]                              # Max 4 entries, like [0, 1, 2, 3]
max = len(ident)                            # do not change
dircontrol = "/var/www/html/ledcontrol/"    # you have to change to the directory of the website with the
                                            # subdir /ledcontrol/. /html/ is where the index.php is stored.
                                            # /ledcontrol/ must be writeable for the user/group www-data
methods = ["alt", "rnd"]                    # do not change
fileprefix = ".rex"                         # do not change
looptime = 1                                # = 0.1 seconds - do not change
alttime = 30                                # = 3.0 seconds
rndtimeposmin = 5                           # = 0.5 seconds
rndtimeposmax = 35                          # = 3.5 seconds
rndtimenegmin = 5                           # = 0.5 seconds
rndtimenegmax = 15                          # = 1.5 seconds

def active(number):
    "Return 0 in case of active and 1 when not"
    return leds[number].value

def on(number):
    "Switch LED on if it's off"
    if active(number) == 1:
        leds[number].off()

def off(number):
    "Switch LED off if it's on"
    if active(number) == 0:
        leds[number].on()

def switch(number):
    "Reverse status of LED"
    if active(number) == 0:
        leds[number].on()
    elif active(number) == 1:
        leds[number].off()

def command():
    "Returns the execute commands as array"
    commands = []
    files = os.listdir(dircontrol) # Get files from directory
    for filename in files:
        filename = re.sub(f"\{fileprefix}$", "", filename)
        if filename.isdigit() and int(filename) > 0 and int(filename) <= max:
            commands.append(int(filename)-1) # If filename is a integer and in range
        elif filename == "alt" or filename == "rnd":
            commands.append(filename)
    return commands

for index in ident:
    off(index) # set all leds off

#initialize
ledcounter = 0
loopcounter = 0
ledtime = [-rndtimenegmin, -rndtimenegmin, -rndtimenegmin, -rndtimenegmin] # for 4 leds

#never stop
while True:

    commands = command() # get commands

    if "rnd" in commands:
        for led in ident:
            if ledtime[led] >= -rndtimenegmin and ledtime[led] < 0: # if time is negative and passed set new positive time
                ledtime[led] = random.randint(rndtimeposmin, rndtimeposmax) # let led on for a random time
            elif ledtime[led] <= rndtimeposmin and ledtime[led] >= 0: # if time is positive and passed set new negative time
                ledtime[led] = -random.randint(rndtimenegmin, rndtimenegmax) # let led off for a random time
            if ledtime[led] > 0:  # if positive time
                on(led)           # turn led on
                ledtime[led] -= 1 # decrease time
            else:
                off(led)
                ledtime[led] += 1
        #reset for alt mode
        ledcounter = 0
        loopcounter = 0
    elif "alt" in commands:
        if loopcounter > (looptime * alttime) - 1: # if time has passed switch led
            loopcounter = 0
            ledcounter += 1
        if(ledcounter == max): # if the last led was active start with the first led again
            ledcounter = 0
        for led in ident:
            if led == ledcounter: # turn on active led
                on(led)
            else:
                off(led)
        #reset for rnd mode
        loopcounter += 1
        ledtime = [-rndtimenegmin, -rndtimenegmin, -rndtimenegmin, -rndtimenegmin] # for 4 leds
    else:
        for led in ident:
            if led not in commands:
                off(led)
            else:
                on(led) # if integer is in commands array turn led of
        #reset special mods
        ledcounter = 0
        loopcounter = 0
        ledtime = [-rndtimenegmin, -rndtimenegmin, -rndtimenegmin, -rndtimenegmin] # for 4 leds

    sleep(looptime / 10) # Wait for a short time
