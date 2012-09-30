#!/usr/bin/env python
import time
from persistant import *
import position
import control

class Log(Persistant) :
   def __init__(self,name) :
      self.name = name
      self.put()

   def log(self,message) :
      position = get("gps")
      file = open("log/"+self.name+".txt","a")
      file.write(str(position) + "," + str(message)+"\n")
      file.close()
      return message

   def monitor(self, control_name) :
      while True :
        control = get(control_name)
        if control.on :
           position = get("gps")
           file = open("log/"+self.name+".txt","a")
           file.write(str(position)+"\n")
           file.close()
        time.sleep(control.value)

   def kml(self) :
      file = open("log/"+self.name+".txt","r")
      kml=  "<kml xmlns='http://www.opengis.net/kml/2.2'><Folder><name>"+self.name+"</name>\n"
      for line in file.readlines():
         if line == "":
           continue
         data = line.strip().split(",")
         ts = data[0]
         (date,time) = ts.split("T")
         latitude = data[1]
         longitude = data[2]
         altitude = data[3]
         message = ""
         try :
            message = data[4]
         except :
            pass
         kml+= "<Placemark>"

         kml+= "<description>" + time[0:5] + " " + str(round(float(latitude),4)) + "," + str(round(float(longitude),4)) + "<br/>" + message  + "</description>\n"

         kml+= "<TimeStamp><when>"+ts+"</when></TimeStamp>\n"
         kml+= "<Point><coordinates>" + longitude + "," + latitude + "," + altitude+"</coordinates></Point>\n"
         kml+= "</Placemark>\n"
      kml+="</Folder></kml>\n"
      return kml
