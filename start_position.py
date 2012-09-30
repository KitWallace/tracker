#!/usr/bin/env python

from persistant import *
from position import *

position = Position("gps")

position.update("/dev/gps1")
