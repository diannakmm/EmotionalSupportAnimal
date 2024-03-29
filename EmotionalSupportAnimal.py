import spidev
import time
import pexpect
import RPi.GPIO as GPIO
from gpiozero import LED
from digitalio import DigitalInOut, Direction
import board

def info():
    '''Prints a basic library description'''
    print("Software library for the EmotionalSupportAnimal project.")

# Establish SPI Bus
spi = spidev.SpiDev()
spi.open(0,0)

# Set motor pin
GPIO.setmode(GPIO.BCM)
motorPin = 3
motorLED = LED(26)
GPIO.setup(motorPin, GPIO.OUT)
GPIO.output(motorPin, GPIO.LOW)
Motspeed = 0

# Establish SPI connection with Bus 0, Device 0
# Make sure HR sensor if connected to SPI 0
def setupHR_Wired():
	spi = spidev.SpiDev()
	spi.open(0,0)

BT_data = [2]
ch = [2]
"""
def setupHR_BT():
        # Probably will need a seperate function to find BT device ip address
        Device = "E5:74:B0:F1:CE:9B"
        # Establish connection to bluetooth device
        child = pexpect.spawn("sudo gatttool -t random -b {0} -I".format(Device))
        child.sendline("Connect")
        child.expect("Connection successful", timeout = 5)
        # If got here, then connection to BT device was successful
        # Can just directly read from sensor
        ch[0] = child
#child.sendline("char-write-req 0x0011 0100")
 #       child.expect("Notification handle = 0x0010 value: ", timeout = 10)
  #      child.expect("\r\n", timeout = 10)
   #     BT_data[0] = child

"""
# Setup GPIO to BCM
# Might not need this function and just set up in global
def setupMotor():
	GPIO.setmode(GPIO.BCM)

# Get data from adc
def get_adc(channel):
	r = spi.xfer([1, (8 + channel) << 4, 0])
	adcout = ((r[1] & 3) << 8) + r[2]
	return adcout

# Should calculate BPM (wired HR sensor)
def getBPM_wired():
        prev = 0                # set prev value = 0, no beat
        num_beats = 0           # val to see how many beats in 10s
        peak = 500
        bottom = 500
        new_beat = True
        for n in range (1000): # loop 1000 times, 1000 * 0.01s = 10s
                output = get_adc(0) # gets pulse sensor data
                if (output > peak): # find the peak value
                        peak = output
                if (output < bottom): # find the bottom value
                        bottom = output

                # pulse data always hovers at the peak
                if (output != peak & output <= peak - 10 & new_beat == True): # when moves away from the peak increase beats
                        num_beats += 1
                        new_beat = False
                if (output <= peak & output >= peak - 10 & new_beat == False): # when gets back to peak, new beat
                        new_beat = True
                prev = output   # store curr pulse val before looping
                time.sleep(0.01) # change if frequency isnt fast enough
        #now num_beats should be the number of beats detected in 10s
        #(beats per 10s) * 6 = bpm ... i think?
        bpm = 6 * num_beats
        print("peak = ", peak)
        print("bottom = ", bottom)
        print("num beats = ", num_beats)
        return(bpm)

# Should get BPM from BT sensor
def getBPM_BT():
	Device = "E5:74:B0:F1:CE:9B"
	child = pexpect.spawn("sudo gatttool -t random -b {0} -I".format(Device))
	child.sendline("Connect")
	child.expect("Connection successful", timeout = 5)
	child.sendline("char-write-req 0x0011 0100")
	child.expect("Notification handle = 0x0010 value: ", timeout = 10)
	child.expect("\r\n", timeout = 10)
        #BT_data[0] = child

	return(hexToInt(child.before[3:5]))

# Function to convert hexa-decimal values to integer values
def hexToInt(hex):
        val = int(hex[0:2], 16)
        return val

# Function to set motor speed
# Will be used to start and stop motor
# Speed = 0 means stop, will send this in main with threshold code
# Speed ~ bpm
def motorSpeed(speed):
        Motspeed = speed
        GPIO.setup(motorPin, GPIO.OUT)
        # check if speed is 0
        if speed == 0:
                motorStop()
        GPIO.output(motorPin, GPIO.HIGH)
        motorLED.on()
        time.sleep(speed)
        GPIO.output(motorPin, GPIO.LOW)
        motorLED.off()
        time.sleep(speed)


def motorStop():
        GPIO.setup(motorPin, GPIO.OUT)
#        while True:
 #               GPIO.output(motorPin, GPIO.LOW)
  #              motorLED.off()
        GPIO.output(motorPin, GPIO.LOW)
        motorLED.off()
        return

def decreaseSpeed(speed):
        Motspeed = Motspeed - speed
        motorSpeed(Motspeed)

def setuptouch():
    pad_pin = board.D23
    # connect each pin with the digital in out of the 5 pad
    pad = DigitalInOut(pad_pin)
    pad.direction = Direction.INPUT
    # when works, prints petting
    while True:
        if pad.value:
            print("Petting")
            time.sleep(0.1)

def getFlex():
    pass
