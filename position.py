#!/usr/bin/env python

import math 
import serial
from persistant import *

R =  3437.74677   #nautical miles
# but wikipedia has the mean radius  3440.06479

class Position(Persistant) :

  def __init__(self,name,latitude=0.0,longitude=0.0,altitude=0.0) :
    self.name=name
    self.latitude = latitude
    self.longitude = longitude
    self.altitude = altitude
    self.courseOverGround = 0.0
    self.speedOverGround = 0.0
    self.HDOP = 0.0
    self.satellites = 0
    self.dateTime= ""
    self.put()

  def update_with_RMC(self, sent) :
    data= sent.split(",")
    try :
      lat=data[3]
      latd=lat[0:2]
      latm=lat[2:]
      lat_dir = 1
      if data[4] == "S" :
        lat_dir = -1
      latitude = (int(latd) + float(latm) / 60) * lat_dir

      long=data[5]
      longd=long[0:3]
      longm=long[3:]
      long_dir = 1
      if data[6] == "W" :
        long_dir = -1
      longitude = (int(longd) + float(longm) / 60) * long_dir

      time =data[1]
      h = time[0:2]
      m = time[2:4]
      s = time[4:len(time)]
    
      date= data[9]
      day = date[0:2]
      month = date[2:4]
      year = date[4:6]
      dateTime = "-".join(("20"+year,month,day)) + "T" + ":".join((h,m,s))

      sog = float(data[7])
      cog = float(data[8])
      # all conversion done with no error

      self.latitude = latitude
      self.longitude = longitude
      self.dateTime = dateTime
      self.speedOverGround = sog
      self.courseOverGround = cog 
    except :
       pass
    return self

  def update_with_GGA(self, sent) :
    data = sent.split(",")
    self.altitude = data[9]
    self.satellites = data[7]
    self.HDOP = data[8]
    return self

  def update(self,port) :   
    s = serial.Serial(port,4800)
    while True:
       nmea = s.readline()
       if nmea.startswith("$GPRMC") :
         self.update_with_RMC(nmea)
         self.put()
       elif nmea.startswith("$GPGGA") :
         self.update_with_GGA(nmea)

  def __str__(self) :
    return ",".join((self.dateTime,str(round(self.latitude,5)),str(round(self.longitude,5)),str(self.altitude)))

  def psdistance(self,p):
    # but wikipedia has the mean radius  3440.06479
    lat1,lon1,lat2,lon2 = map(math.radians,[self.latitude,self.longitude,p.latitude,p.longitude])
    dlat = lat1 - lat2
    dlon = lon1 - lon2
    x = dlon * math.cos((lat1+lat2)/2)
    y = dlat
    d = math.sqrt(x*x + y*y) * R
    return d

  def gcdistance(self,p):
    """
    Calculate the great circle distance in nautical miles between this position and another
    using the haversine formula and the initial bearing in degrees

    see http://en.wikipedia.org/wiki/Haversine_formula
    and http://www.movable-type.co.uk/scripts/latlong.html
    """
    lat1,lon1,lat2,lon2 = map(math.radians,[self.latitude,self.longitude,p.latitude,p.longitude])
    dlat = lat1 - lat2
    dlon = lon1 - lon2
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    nm = c * R
    return nm

  def gcbearing(self,p):
    """
    Calculate the great circle initial bearing in degrees
    """
    lat1,lon1,lat2,lon2 = map(math.radians,[self.latitude,self.longitude,p.latitude,p.longitude])
    dlat = lat1 - lat2
    dlon = lon1 - lon2
    y = math.sin(dlon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    bearing = math.degrees(math.atan2(y, x))
    bearing = (bearing + 360) % 360
    return bearing

if __name__ == "__main__" :
    p1 = Position(0,0)
    print p1.gcdistance(Position(0,1))
    print p1.psdistance(Position(0,1))
    print p1.gcdistance(Position(1,0))
    print p1.psdistance(Position(1,0))

    p2 = Position(0,-0.5)
    print p2.gcdistance(Position(0,0.5))
    print p2.psdistance(Position(0,0.5))

    p1 = Position(51,-2)
    print p1.gcdistance(Position(51,-3))
    print p1.psdistance(Position(51,-3))
    print p1.gcdistance(Position(52,-2))
    print p1.psdistance(Position(52,-2))

