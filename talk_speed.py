#!/usr/bin/env python
import time,sys

import speak
import conv
import xmlutils
import control
from persistant import get
import position

control.Control("speed",step=10,initial=60)

while True :
   if get("speed").on :
      position = get("gps")
      speed = int(float(position.speedOverGround))
      course = int(float(position.courseOverGround))
      points = conv.degree_to_compass_point(course)
      text = points + " at " + str(speed) + " knots " 
      speak.say(text)
      print(text)

   time.sleep(get("speed").value)
