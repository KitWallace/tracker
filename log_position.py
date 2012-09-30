#!/usr/bin/env python
import time
from persistant import *
from position import *
import log
import control
import sys

control.Control("logger",initial=60,step=10)
control.Control("marker",initial=1,step=1)
log = log.Log("track")
log.monitor("logger")

