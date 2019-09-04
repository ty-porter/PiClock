#!/usr/bin/env python
import json
import requests
from apikey import apikey
from location import locationCode
import datetime
import pytz

class ApiCaller:
	
	def __init__(self):
		self.currentWeather = {}
		self.forecast = {}
		
	def getAndParse(self):
		self.getData()
		self.parseData()
	
	def getData(self):
		# Create datetime object and localize it 
		d_naive = datetime.datetime.now()
		timezone = pytz.timezone("America/Chicago")
		d_aware = timezone.localize(d_naive)
		
		# Create a localized timestamp from datetime object
		timestamp = d_aware.strftime('%m/%d/%y %H:%M:%S : ')
    
		url = 'http://dataservice.accuweather.com/currentconditions/v1/' + locationCode + '?apikey=' + apikey + "&details=true"
		currentWeatherRequest = requests.get(url).json()

		if 'Message' not in currentWeatherRequest:
			print(timestamp + 'Generating current weather data from AccuWeather...')
			with open('currentweather.json', 'w') as f:
				try:
					json.dump(currentWeatherRequest, f)
				finally:
					f.close()
		else:
			print(timestamp + 'Maxed out API calls to AccuWeather. Attempting to use cached current weather data...')
			
		url = 'http://dataservice.accuweather.com/forecasts/v1/daily/1day/' + locationCode + '?apikey=' + apikey + "&details=true"
		forecastRequest = requests.get(url).json()

		if 'Message' not in forecastRequest:
			print(timestamp + 'Generating forecast data from AccuWeather...')
			with open('forecast.json', 'w') as f:
				try:
					json.dump(forecastRequest, f)
				finally:
					f.close()
		else:
			print(timestamp + 'Maxed out API calls to AccuWeather. Attempting to use cached forecast data...')		

	def parseData(self):
		with open('currentweather.json', 'r') as f:
			try:
				currentWeather = json.load(f)
			finally:
				f.close()
			
		with open('forecast.json', 'r') as f:
			try:
				forecast = json.load(f)
			finally:
				f.close()
				
		self.currentWeather = currentWeather
		self.forecast = forecast
		
	
	def getLocation(self, zipcode):
		url = 'http://dataservice.accuweather.com/locations/v1/postalcodes/search?apikey=' + apikey + '&q=' + str(zipcode)
		locationRequest = requests.get(url).json()
		
		if 'Message' not in locationRequest:
			newLocationCode = locationRequest[0]['Key']
			print(timestamp + 'Generating new AccuWeather location code...')
			with open('location.py', 'w') as f:
				try:
					f.write('locationCode = "' + newLocationCode + '"')
				finally:
					f.close()
		else:
			print(timestamp + 'Maxed out API calls to AccuWeather. Please try again later...')
			
