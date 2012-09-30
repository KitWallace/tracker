#!/usr/bin/env python
import time,sys

import speak
import conv
import xmlutils
import control
from persistant import get
import position

substitutes = {
     "W":"West","N":"North","S":"South","E":"East",
     "km/h":"kilometers per hour","C":"Celsius","mph":"miles per hours", "kts": "knots",
     "Mon":"Monday","Tue":"Tuesday","Wed":"Wednesday","Thu":"Thursday","Fri":"Friday","Sat":"Saturday","Sun":"Sunday",
     "NNE":"Nor Nor East","NE":"Nor East","ENE":"East Nor East","ESE":"East Sow East",
     "SE":"Sow East" ,"SSE" :"Sow Sow East", "SSW":"Sow Sow West","SW":"Sow West","WSW":"West Sow West",
     "WNW":"West Nor West","NW":"Nor West","NNW":"Nor Nor West",
     "%":"percent"
     }


control.Control("speed",step=10,initial=60)

while True :
   if get("speed").on :
      position = get("gps")
      speed = round(conv.convert(position.speedOverGround,"kt","mph"),1)
      course = int(position.courseOverGround)
      points = conv.degree_to_compass_point(course)
      text = points + " at " + str(speed) + " mph " 
      mtext = speak.expand(text,substitutes)
      speak.say(mtext)
      print(text)

   time.sleep(get("speed").value)
