#!/usr/bin/env python
from apicaller import ApiCaller
import re

# A simple command line tool to generate new location codes or cache weather data.

class Utility:
    
    def __init__(self):
        self.startTool()
        
    def startTool(self):
        caller = ApiCaller()
        
        gui = [ 
            '****************************************',
            '  Welcome to the PiClock Utility Tool!  ',
            '****************************************\n',
            'This tool is used to generate a new location code from AccuWeather or',
            'to cache weather data (to prevent too many API calls for AccuWeather\'s',
            'free tier developer access.\n\n'
            'Here are the following options:\n'
            'GET DATA -- (G)',
            'SET LOCATION -- (L)\n',
            'BOTH FUNCTIONS -- (B)',
            '(Set location first) \n\n'
        ]
            
        for line in gui:
            print(line)
            
        selection = raw_input('Please input your choice (G/L/B): ')
        s = selection.lower()
        
        if selection == 'b' or selection == 'l':
            zipcode = raw_input('Please enter your zip code: ')
            if re.search('[^0-9]', zipcode):
                print('Invalid zip. Restarting. Press Ctrl + C to exit')
                self.startTool()
            else:
                z = int(zipcode)
                caller.getLocation(z)
            
        if s == 'b' or selection == 'g':
            caller.getData()
        
            
        if re.search('glb', s):
            print('Selection invalid. Will attempt restarting. Press Ctrl + C to exit.')
            self.startTool()
            
            
Utility()
