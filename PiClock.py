#!/usr/bin/env python
from appbase import AppBase
import requests
import datetime
from rgbmatrix import graphics
import time
from PIL import Image

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
    largeFont = graphics.Font()
    medFont = graphics.Font()
    smallFont = graphics.Font()

    largeFont.LoadFont("./fonts/10x20.bdf")
    medFont.LoadFont("./fonts/6x12.bdf")
    smallFont.LoadFont("./fonts/4x6.bdf")

    # Set colors
    timeColor = graphics.Color(255, 255, 255)
    hiColor = graphics.Color(255, 0, 0)
    loColor = graphics.Color(0, 0, 255)

    # Load images
    # hi_icon = Image.open('hi.png')
    # lo_icon = Image.open('lo.png')

    # Set text positions
    x_pos = 2
    y_pos = 14
    bottom_bar_y = 63

    while True: 
      offscreen_canvas.Clear()

      # Draw time
      graphics.DrawText(offscreen_canvas, largeFont, x_pos, y_pos, timeColor, "12:34")
      graphics.DrawText(offscreen_canvas, smallFont, x_pos + 52, y_pos, timeColor, "PM")

      # Draw date
      graphics.DrawText(offscreen_canvas, smallFont, x_pos, y_pos + 6, timeColor, "Thursday")
      graphics.DrawText(offscreen_canvas, smallFont, x_pos, y_pos + 13, timeColor, "August 15")

      # Draw Hi/Lo temp & rain chance
      # hi_icon.thumbnail((11, 9))
      # offscreen_canvas.SetImage(hi_icon.convert('RGB'), 0, 52)
      # lo_icon.thumbnail((11, 9))
      # offscreen_canvas.SetImage(lo_icon.convert('RGB'), 12, 52)

      graphics.DrawText(offscreen_canvas, smallFont, x_pos - 2, bottom_bar_y, hiColor, "HI")
      graphics.DrawText(offscreen_canvas, smallFont, x_pos + 6, bottom_bar_y, timeColor, "79")
      graphics.DrawText(offscreen_canvas, smallFont, x_pos + 15, bottom_bar_y, loColor, "LO")
      graphics.DrawText(offscreen_canvas, smallFont, x_pos + 23, bottom_bar_y, timeColor, "59")

      time.sleep(0.05)
      offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

# Main function
if __name__ == "__main__":
  piClock = PiClock()
  if (not piClock.process()):
      piClock.print_help()

