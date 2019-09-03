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
from apicaller import ApiCaller

class PiClock(AppBase):
  def __init__(self, *args, **kwargs):
    super(PiClock, self).__init__(*args, **kwargs)
    
    # Instantiate an API caller object, then use it to seed initial data
    self.caller = ApiCaller()
    self.clockVars = {}
    self.getData()    
    self.updateClockVars = True

  def getData(self):
    # Set an initial API call datetime object to prevent multiple API calls
    self.callTimer = datetime.datetime.now()
    
    # Calls API, or reverts to using cached data if too many calls have been made
    self.caller.getAndParse()
    self.weather = self.caller.currentWeather
    self.forecast = self.caller.forecast  

    self.selectCurrentWeatherIcon()
    self.defineClockVars()

  def selectCurrentWeatherIcon(self):
    # Sets the weather icon based on weather data
    weatherIconNum = int( self.weather[0]['WeatherIcon'] )
    
    def weatherIconFile(num):
      if num < 3 or num == 33 or num == 34:
        return 'sunny'
      elif (num > 2 and num < 6) or ( num > 34 and num < 38 ):
        return 'partsunny'
      elif (num > 5 and num < 12) or ( num > 37 and num < 39 ):
        return 'cloudy'
      elif (num > 11 and num < 15) or ( num > 38 and num < 40 ) or num == 18:
        return 'rain'
      elif (num > 14 and num < 18) or ( num > 40 and num < 43 ):
        return 'tstorm'
      elif (num > 18 and num < 24) or ( num > 42 and num < 45 ):
        return 'snow'
      elif num > 23 and num < 30:
        return "mix"
      elif num == 32:
        return "windy"
      else:
        return "unknown"

    self.weather_icon = Image.open('./images/' + weatherIconFile(weatherIconNum) +'.png')
    
  def defineClockVars(self):
  
    # Set current temp & weather data from API call
    currentTemp = str( int(self.weather[0]['Temperature']['Imperial']['Value']) )
    currentWeather = self.weather[0]['WeatherText']
    
    isDayTime = self.weather[0]['IsDayTime']
    dayOrNight = 'Day' if isDayTime else 'Night'
        
    rainChance = self.forecast['DailyForecasts'][0][dayOrNight]['PrecipitationProbability']
    rainChance = str(rainChance)
    
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

    # Set text positions
    x_pos = 2
    y_pos = 14
    bottom_bar_y = 63
    time_x_pos = 2
    current_weather_pos = x_pos + 16
    degree_pos = 23
    rain_pos = 48
    percent_pos = 54
    large_num_offset = 0

    # Perform some checks to prevent text overflow
    if len(currentTemp) == 2:
      degree_pos += 6
    elif len(currentTemp) > 2:
      degree_pos += 12

    if len(rainChance) == 2:
      rain_pos -= 6
    elif len(rainChance) > 2:
      rain_pos -= 12

    if len(rainChance + currentTemp) > 5:
      midRowFont = smallFont
      rain_pos += 6
      degree_pos -= 6
      large_num_offset += 1
    else: 
      midRowFont = medFont

    # Load rain chance icon
    rain_icon = Image.open('./images/drop.png')
    
    self.clockVars = {
        'currentWeather': currentWeather,
        'currentTemp': currentTemp,
        'rainChance': rainChance,
        'largeFont': largeFont,
        'medFont': medFont,
        'smallFont': smallFont,
        'timeColor': timeColor,
        'hiColor': hiColor,
        'loColor': loColor,
        'x_pos': x_pos,
        'y_pos': y_pos,
        'bottom_bar_y': bottom_bar_y,
        'current_weather_pos': current_weather_pos,
        'degree_pos': degree_pos,
        'rain_pos': rain_pos,
        'percent_pos': percent_pos,
        'large_num_offset': large_num_offset,
        'midRowFont': midRowFont,
        'rain_icon': rain_icon,
        'time_x_pos': time_x_pos
    }
    
    # Set the flag to have clock update the clockVars within run() function
    self.updateClockVars = True
    
  def run(self):
    offscreen_canvas = self.matrix.CreateFrameCanvas()

    ### Begin running clock functions
    while True: 
      
      # Check flag to determine whether to update clockVars
      # Prevents this from happening on every clock cycle.
      if self.updateClockVars:
        
        # Reset the flag
        self.updateClockVars = False
        
        currentWeather = self.clockVars['currentWeather']
        currentTemp = self.clockVars['currentTemp']
        rainChance = self.clockVars['rainChance']
        largeFont = self.clockVars['largeFont']
        medFont = self.clockVars['medFont']
        smallFont = self.clockVars['smallFont']
        timeColor = self.clockVars['timeColor']
        hiColor = self.clockVars['hiColor']
        loColor = self.clockVars['loColor']
        x_pos = self.clockVars['x_pos']
        y_pos = self.clockVars['y_pos']
        bottom_bar_y = self.clockVars['bottom_bar_y']
        current_weather_pos = self.clockVars['current_weather_pos']
        degree_pos = self.clockVars['degree_pos']
        rain_pos = self.clockVars['rain_pos']
        percent_pos = self.clockVars['percent_pos']
        large_num_offset = self.clockVars['large_num_offset']
        midRowFont = self.clockVars['midRowFont']
        rain_icon = self.clockVars['rain_icon']
        time_x_pos = self.clockVars['time_x_pos']

      ### Clock functions

      # Create datetime object and localize it
      d_naive = datetime.datetime.now()
      timezone = pytz.timezone("America/Chicago")
      d_aware = timezone.localize(d_naive)

      # Make a new API call if the call timer is greater than 1 hour
      if (d_naive - self.callTimer).total_seconds() >= 3600:
        self.getData()

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
      elif len(currentHour) == 2:
        time_x_pos = 2

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

      # Draw current weather text & icon as well as current temperature
      self.weather_icon.thumbnail((15, 18))
      offscreen_canvas.SetImage(self.weather_icon.convert('RGB'), 1, 29)
      graphics.DrawText(offscreen_canvas, smallFont, current_weather_pos, y_pos + 28, timeColor, currentWeather)
      graphics.DrawText(offscreen_canvas, midRowFont, current_weather_pos, y_pos + 22, timeColor, currentTemp)
      
      # Draw degree symbol
      for pixel_x in range(1,4):
        for pixel_y in range(1,4):
          if (pixel_x == 2 or pixel_y == 2) and pixel_x != pixel_y:
            offscreen_canvas.SetPixel(pixel_x + degree_pos, pixel_y + 28 + (large_num_offset * 2), 255, 255, 255)
            
      # Draw rain chance icon & percentage
      offscreen_canvas.SetImage(rain_icon.convert('RGB'), 58, 29)
      graphics.DrawText(offscreen_canvas, midRowFont, rain_pos, y_pos + 22, timeColor, rainChance)
      graphics.DrawText(offscreen_canvas, smallFont, percent_pos, y_pos + 21 + large_num_offset, timeColor, "%")

      # Draw bottom info bar 
      
      # CURRENTLY NOT IMPLEMENTED!
      
      # graphics.DrawText(offscreen_canvas, smallFont, x_pos - 2, bottom_bar_y, hiColor, "HI")
      # graphics.DrawText(offscreen_canvas, smallFont, x_pos + 6, bottom_bar_y, timeColor, "79")
      # DrawText(offscreen_canvas, smallFont, x_pos + 15, bottom_bar_y, loColor, "LO")
      # graphics.DrawText(offscreen_canvas, smallFont, x_pos + 23, bottom_bar_y, timeColor, "59")

      time.sleep(0.05)
      offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

# Main function
if __name__ == "__main__":
  piClock = PiClock()
  if (not piClock.process()):
      piClock.print_help()

