import cv2
import numpy
import gpiozero
import time
from gpiozero import LED

RED = LED(18)
GREEN = LED(23)
GREEN.off()
RED.off()

first_check = 0.0

cam = cv2.VideoCapture(0)
kernel = numpy.ones((5 ,5), numpy.uint8)
while (True):
    ret, frame = cam.read()
    rangomax = numpy.array([255, 50, 50]) # B, G, R
    rangomin = numpy.array([51, 0, 0])
    mask = cv2.inRange(frame, rangomin, rangomax)
    # reduce the noise
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    x, y, w, h = cv2.boundingRect(opening)
#    print(x,y,w,h)
    cv2.rectangle(frame, (x, y), (x+w, y + h), (0, 255, 0), 3)
    cv2.circle(frame, (x+w, y+h), 5, (0, 0, 255), -1)
    cv2.imshow('camera', frame)
    k = cv2.waitKey(1) & 0xFF

    move= cv2.rectangle(frame, (x, y), (x+w, y + h), (0, 255, 0), 3)
#    Backward = gpiozero.OutputDevice(18) # On/Off output
#    Forward = gpiozero.OutputDevice(23) #On/Off output
#    SpeedPWM = gpiozero.PWMOutputDevice(24) # set up PWM pin
    last_check = time.process_time()
    if x > 0 or y > 0 or w>0 or h>0:
        if last_check - first_check > 5.0:
            RED.on()
            time.sleep(1)
            RED.off()
            GREEN.on()
            time.sleep(1)
            GREEN.off()
            first_check = time.process_time()
#        Backward.on() # Sets Backward Direction pin on
#            Forward.off() # Sets Backward Direction pin on
#            speedFlag = float(input("100")) # Gets a number from the from the user
#            SpeedPWM.value = speedFlag/1000 # Sets the duty cycle of the PWM between 0-
#            if x<0 or y<0 or w<0 or h<0:
#                Backward.off() # Sets Backward Direction off
#                Forward.on()   # Sets Backward Direction pin on\
#                speedFlag = float(input("100")) # Gets a number from the from the user
#                SpeedPWM.value = speedFlag/1000 # Sets the duty cycle of the PWM between 0-
    RED.off()
    GREEN.off()

    if k == 27:
        break