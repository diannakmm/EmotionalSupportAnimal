import spidev
import time

def info():
    '''Prints a basic library description'''
    print("Software library for the EmotionalSupportAnimal project.")

# Establish SPI connection with Bus 0, Device 0
# Make sure HR sensor if connected to SPI 0
def setupHR():
	spi = spidev.SpiDev()
	spi.open(0,0)

# Get data from adc
def get_adc(channel):
	r = spi.xfer([1, (8 + channel) << 4, 0])
	adcout = ((r[1] & 3) << 8) + r[2])
	return adcout

# Should calculate BPM (wired HR sensor)
def getBPM_wired():
        prev = 0                #set prev value = 0, no beat
        num_beats = 0           #val to see how many beats in 10s
        for n in range (100): #loop 100 times, 100 * 0.1s = 10s
                output = get_adc(0) #gets pulse sensor data
                if (output != 0 & prev == 0): #only care when 0 -> 62
                        num_beats += 1
                prev = output   #store curr pulse val before looping
                time.sleep(0.1) #change if frequency isnt fast enough
        #now num_beats should be the number of beats detected in 10s
        #(beats per 10s) * 6 = bpm ... i think?
        bpm = 6 * num_beats
        return(num_bpm)

# Should get BPM from BT sensor
def getBPM_BT():
	# delete existing .txt file with all the data if it exists
	# create new .txt file to store new BT data
	# read from sensor and push to .txt file
	# read from file --> second hexadecimal value = HR

	# might not need to push to txt file and just directly read
	pass

def setuptouch():
    pass

def gettouch():
    pass
