from pulsesensor import Pulsesensor
import time

p = PulseSensor()
p.startAsyncBPM()

try:
  while True:
    bpm = p.BPM
    if bpm > 0:
      print("BPM: %d" % bpm)
    else:
      print("No Heartbeat")
    time.sleep(1)
except:
  p.stopAsyncBPM()
