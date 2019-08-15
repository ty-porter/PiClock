#!/usr/bin/env python
from appbase import AppBase
import requests
import datetime
from rgbmatrix import graphics
import time

class PiClock(AppBase):
  def __init__(self, *args, **kwargs):
    super(PiClock, self).__init__(*args, **kwargs)
    self.getData()

# Main function
if __name__ == "__main__":
  piClock = PiClock()
  if (not piClock.process()):
      piClock.print_help()

