import EmotionalSupportAnimal as esa
import time
from threading import Thread, Event
from queue import Queue
import sys

e = Event()
q = Queue()

threshold = [2]
threshold[0] = 110

# Setup all sensors
esa.setupHR()
esa.setupMotor()

# Check when heart rate >= set threshold
# Turn motor func on when threshold exceeded
# Turn motor func off when heart rate is below threshold
def HR():
	curr_HR = esa.getBPM_BT()
	if curr_HR >= threshold:
		esa.motorSpeed(threshold / curr_HR)
	elif curr_HR < threshold:
		esa.motorStop()

"""

# Check when being petted
# Is motor on?
# Decrease motor speed if motor is on AND being petted
def petted():
	petted = esa.setuptouch()
	if petted == True:
		esa.decreaseSpeed(0.1)
                time.wait(1)

# Check when being hugged
# Is motor on?
# Decrease motor speed if motor is on AND being hugged
def hugged():
	hugged = esa.getPressure()
	if hugged == True:
		esa.decreaseSpeed(0.1)
		time.wait(1)

"""

# Change threshold of heart rate
def change_HR(thresh):
	threshold[0] = thresh
	print("changed threshold to ", threshold[0])

def get_thresh():
	return threshold[0]

#t1 = Thread(target = HR)
#t1.start()
#t2 = Thread(target = petted)
#t2.start()
#t3 = Thread(target = hugged)
#t3.start()

#t1.join()
#t2.join()
#t3.join()
