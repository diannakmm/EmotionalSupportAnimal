import spidev
import time
import pexpect

def info():
    '''Prints a basic library description'''
    print("Software library for the EmotionalSupportAnimal project.")

# Establish SPI Bus
spi = spidev.SpiDev()
spi.open(0,0)


# Establish SPI connection with Bus 0, Device 0
# Make sure HR sensor if connected to SPI 0
def setupHR():
	spi = spidev.SpiDev()
	spi.open(0,0)

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
        # Probably will need a seperate function to find BT device ip address
        Device = "E5:74:B0:F1:CE:9B"
        # Establish connection to bluetooth device
        child = pexpect.spawn("sudo gatttool -t random -b {0} -I".format(Device))
        child.sendline("Connect")
        child.expect("Connection successful", timeout = 5)
        # If got here, then connection to BT device was successful
        # Can just directly read from sensor
        child.sendline("char-write-req 0x0011 0100")
        child.expect("Notification handle = 0x0010 value: ", timeout = 10)
        child.expect("\r\n", timeout = 10)
        return(hexToInt(child.before[3:5]))

# Function to convert hexa-decimal values to integer values
def hexToInt(hex):
        val = int(hex[0:2], 16)
        return val

def setuptouch():
    pass

def gettouch():
    pass
