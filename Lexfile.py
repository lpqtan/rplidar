# Set up libraries and overall settings
import re
import subprocess
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
GPIO.setmode(GPIO.BOARD) # Sets the pin numbering system to use the physical layout
import os


def processdata(resultstring,servoangle):
    new = re.split('theta:|Dist:|Q:|\n', resultstring)
    new.pop(0)
    final = ""
    count = 1
    for somestring in new:
        somestring = somestring.strip()
        try:
            testvar = float(somestring)
            if count % 3 != 0:
                final += somestring + ","
            else:
                final += somestring + "," + servoangle + "\n"
        except:
            continue
        count += 1
    return final

    

# Set up pin 11 for PWM
GPIO.setup(11,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
p = GPIO.PWM(11, 50)     # Sets up pin 11 as a PWM pin
p.start(0)               # Starts running PWM on the pin and sets it to 0

# Move the servo back and forth
p.ChangeDutyCycle(3)     # Changes the pulse width to 3 (so moves the servo)
command = ["./output/Linux/Release/ultra_simple", "--channel", "--serial", "/dev/ttyUSB0", "115200"]

if os.path.exists("lidardatafile.csv"):
  os.remove("lidardatafile.csv")
else:
  print("file has not been created before")

outputfile = open("lidardatafile.csv", "a")

for i in range(20,120,2):
    i /= 10
    p.ChangeDutyCycle(i)
    sleep(0.7)
    result = subprocess.run(command, capture_output=True, text=True)
    sleep(0.2)
    # convert to degrees, i from 2-12 to 0-180
    i = (i-2)*18
    cleanstring = processdata(result.stdout,str(i))
    outputfile.write(cleanstring)
    
    
outputfile.close()


sleep(1)

# Clean up everything
p.stop()                 # At the end of the program, stop the PWM
GPIO.cleanup()           # Resets the GPIO pins back to defaults
