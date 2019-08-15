#!/usr/bin/env python
from appbase import AppBase
import requests
import datetime
from rgbmatrix import graphics
import time

class PiClock(AppBase):
  def __init__(self, *args, **kwargs):
    super(PiClock, self).__init__(*args, **kwargs)
    self.getDate()

  def getDate(self):
    global date
    date = str(datetime.datetime.now())
    
  def run(self):
    offscreen_canvas = self.matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("./fonts/4x6.bdf")
    textColor = graphics.Color(255, 255, 255)
    x_pos = 1
    y_pos = 5

    while True: 
      offscreen_canvas.Clear()
      graphics.DrawText(offscreen_canvas, font, x_pos, y_pos, textColor, "Hello World")
  
      time.sleep(0.05)
      offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

# Main function
if __name__ == "__main__":
  piClock = PiClock()
  if (not piClock.process()):
      piClock.print_help()

