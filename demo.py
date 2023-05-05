import EmotionalSupportAnimal as esa
import time
from threading import Thread, Event
from queue import Queue
import sys

e = Event()
q = Queue()

threshold = [2]
threshold[0] = 100

# Setup all sensors
esa.setupHR_BT()
esa.setupMotor()

# Check when heart rate >= set threshold
# Turn motor func on when threshold exceeded
# Turn motor func off when heart rate is below threshold
def HR():
	while True:
		curr_HR = esa.getBPM_BT()
		print("Heart Rate = ", curr_HR)
		if curr_HR >= int(threshold[0]):
			esa.motorSpeed(int(threshold[0]) / curr_HR)
		elif curr_HR < int(threshold[0]):
			esa.motorStop()

"""

# Check when being petted
# Is motor on?
# Decrease motor speed if motor is on AND being petted
def petted():
	petted = esa.setuptouch()
	if petted == True:
		esa.decreaseSpeed(0.1)
                time.sleep(1)

# Check when being hugged
# Is motor on?
# Decrease motor speed if motor is on AND being hugged
def hugged():
	hugged = esa.getPressure()
	if hugged == True:
		esa.decreaseSpeed(0.1)
		time.sleep(1)

"""

# Change threshold of heart rate
def change_HR(thresh):
	threshold[0] = thresh
	print("changed threshold to ", threshold[0])

def get_thresh():
	return threshold[0]

def dummy():
	time.sleep(1)
	return

t1 = Thread(target = HR)
t2 = Thread(target = dummy)
t1.start()
t2.start()
t1.join()
t2.join()

#t2 = Thread(target = petted)
#t2.start()
#t3 = Thread(target = hugged)
#t3.start()

#t1.join()
#t2.join()
#t3.join()
