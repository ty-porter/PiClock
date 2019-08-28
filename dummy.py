#!/usr/bin/env python
import json
import requests
from apikey import apikey
from location import locationCode

## Utility Description

# This utility dumps the contents of a GET request to AccuWeather for your location 
# in order to prevent using up valuable API calls. The free tier for AccuWeather dev
# tools limits you to 50 calls per day, and PiClock requires 48 of those to update
# current conditions throughout the day (24 hours * 2 calls per hour).
#
# You can use this tool to generate real data for testing purposes. Simply run
# sudo ./dummy.py to generate new data to the dummydata.txt file.

class Dummy:
	
	def __init__(self):
		self.jsonData = {}
		self.getData()
		self.parseData()
	
	def getData(self):
		url = 'http://dataservice.accuweather.com/currentconditions/v1/' + locationCode + '?apikey=' + apikey + "&details=true"
		data = requests.get(url).json()

		if 'Message' not in data:
			print('Generating new AccuWeather dummy data...')
			with open('dummydata.json', 'w') as f:
				json.dump(data, f)
		else:
			print('Maxed out API calls to AccuWeather. Attempting to use cached data...')	

	def parseData(self):
		with open('dummydata.json', 'r') as f:
			jsonData = json.load(f)
		self.jsonData = jsonData
