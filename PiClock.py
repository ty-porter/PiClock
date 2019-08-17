#!/usr/bin/env python
from appbase import AppBase
import requests
import datetime
from rgbmatrix import graphics
import time
from PIL import Image
from apikey import apikey
from location import locationCode
import pytz

class PiClock(AppBase):
  def __init__(self, *args, **kwargs):
    super(PiClock, self).__init__(*args, **kwargs)
    self.getData()

  def getData(self):
    URL = 'http://dataservice.accuweather.com/currentconditions/v1/' + locationCode + '?apikey=' + apikey + "&details=true"
    #weatherRequest = requests.get(URL)
    #self.weather = weatherRequest.json()

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
    time_x_pos = 2

    # Set current temp from API call
    #currentTemp = str( int(self.weather[0]['Temperature']['Imperial']['Value']) )

    while True: 

      # Clock functions

      # Create datetime object and localize it
      d_naive = datetime.datetime.now()
      timezone = pytz.timezone("America/Chicago")
      d_aware = timezone.localize(d_naive)

      # Set current time & ante/post meridiem (AM/PM)
      currentHour = str( int( d_aware.strftime('%I') ) )
      currentMinute = d_aware.strftime('%M')

      # Blink function for colon
      if int( d_aware.strftime('%f') ) > 499999:
        blink = ":"
      else:
        blink = ' '

      # If single digit hour, adjust time position
      if len(currentHour) == 1:
        time_x_pos = 12

      # Build the clock value
      currentTime = currentHour + blink + currentMinute

      meridiem = d_aware.strftime('%p')

      # Set day of the week
      currentDay = d_aware.strftime('%A')
      currentDate = d_aware.strftime('%B %d')

      offscreen_canvas.Clear()

      # Draw time
      graphics.DrawText(offscreen_canvas, largeFont, time_x_pos, y_pos, timeColor, currentTime)
      graphics.DrawText(offscreen_canvas, smallFont, x_pos + 52, y_pos, timeColor, meridiem)

      # Draw date
      graphics.DrawText(offscreen_canvas, smallFont, x_pos, y_pos + 6, timeColor, currentDay)
      graphics.DrawText(offscreen_canvas, smallFont, x_pos, y_pos + 13, timeColor, currentDate)

      # Draw Hi/Lo temp & rain chance
      # hi_icon.thumbnail((11, 9))
      # offscreen_canvas.SetImage(hi_icon.convert('RGB'), 0, 52)
      # lo_icon.thumbnail((11, 9))
      # offscreen_canvas.SetImage(lo_icon.convert('RGB'), 12, 52)

      graphics.DrawText(offscreen_canvas, smallFont, x_pos - 2, bottom_bar_y, hiColor, "HI")
      graphics.DrawText(offscreen_canvas, smallFont, x_pos + 6, bottom_bar_y, timeColor, "79")
      graphics.DrawText(offscreen_canvas, smallFont, x_pos + 15, bottom_bar_y, loColor, "LO")
      graphics.DrawText(offscreen_canvas, smallFont, x_pos + 23, bottom_bar_y, timeColor, "59")

      # Display weather data
      #graphics.DrawText(offscreen_canvas, medFont, x_pos, y_pos + 35, timeColor, currentTime)

      time.sleep(0.05)
      offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

# Main function
if __name__ == "__main__":
  piClock = PiClock()
  if (not piClock.process()):
      piClock.print_help()

