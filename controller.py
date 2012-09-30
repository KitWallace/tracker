#!/usr/bin/env python

import sys
import speak
import time
import termios

from menu import *
from persistant import *

# the following are application specific so should be in the menu
import control
import position
import log

# assumes gps already started 
# assumes logging already started

def visit(item) :
   action = item.getAttribute('action')
   if action == "" :
      text = item.getAttribute('title')
   else : 
      text = eval(action)
   speak.say(text)
   print (text)
   


name = sys.argv[1]
menu = Menu(name)
menu.run(visit) 

