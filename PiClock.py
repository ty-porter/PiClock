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

    # Load Fonts
    timeFont = graphics.Font()
    smallFont = graphics.Font()
    timeFont.LoadFont("./fonts/10x20.bdf")
    smallFont.LoadFont("./fonts/4x6.bdf")
    textColor = graphics.Color(255, 255, 255)

    # Set text positions
    x_pos = 2
    y_pos = 14

    while True: 
      offscreen_canvas.Clear()

      # Draw time
      graphics.DrawText(offscreen_canvas, timeFont, x_pos, y_pos, textColor, "12:34")
      graphics.DrawText(offscreen_canvas, smallFont, x_pos + 52, y_pos, textColor, "PM")

      # Draw date
      graphics.DrawText(offscreen_canvas, smallFont, x_pos, y_pos + 6, textColor, "Thursday")
      graphics.DrawText(offscreen_canvas, smallFont, x_pos, y_pos + 13, textColor, "August 15")

      # Draw Hi/Lo temp & rain chance
      # IMPLEMENT THIS!!

      time.sleep(0.05)
      offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

# Main function
if __name__ == "__main__":
  piClock = PiClock()
  if (not piClock.process()):
      piClock.print_help()

