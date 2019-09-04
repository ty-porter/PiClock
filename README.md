# PiClock ![Version](https://img.shields.io/badge/Version-1.0.0-green) ![Python](https://img.shields.io/badge/Python-v2.7-blue) ![RPI](https://img.shields.io/badge/Raspberry-Pi-red) ![Active](https://img.shields.io/badge/Active-Yes-brightgreen)

PiClock is a desk clock firmware built for Raspberry Pi 3-compatible LED displays. It pulls data from the AccuWeather API once per hour and details current weather as well as rain forecast for your area. PiClock comes with a utility tool to look up your current area by zip code to generate a compatible location key to be used by the AccuWeather API.

PiClock is designed to work around a low API call limit imposed by AccuWeather. Currently, the "trial" period for this API limits the amount of calls that can be made to 50 per day. PiClock makes 2 calls per hour (one for current weather details and one for forecast), so it maximizes the refresh rate while making sure you don't get charged for API calls.

![PiClock](https://i.imgur.com/Z5RS6eY.jpg)

## Required Hardware

I recommend using products from Adafruit as that is where I sourced the hardware. Other sources may not be compatible with PiClock.

* **Raspberry Pi Model 3** -- *2 will most likely work but is untested*
* **LED board**
* **[Adafruit RGB Matrix HAT](https://www.adafruit.com/product/2345)**
* **5V, 2A OR 4A Power cable for LED board** -- *Optional, but recommended to avoid overloading the Pi's power supply*


## Current Limitations

The original version of PiClock only gives consideration to LED screens consisting of a single 64x64 panel. Exact specifications of the panel I used can be found on Adafruit [here](https://www.adafruit.com/product/3649).

The Adafruit HAT does require soldering connectors to the board. The LED matrix I used also requires additional soldering of a jumper pad to enable 64x64 display. You can find installation instructions for the HAT [here](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/assembly). You will need to follow instructions to assemble the HAT specifically for your display.

PiClock currently runs on Python 2.7.

## Installation

**Step 1.** -- Assemble Hardware

Assemble the HAT and LED matrix according to manufacturer specifications. You can find HAT assembly instructions [here](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/assembly), and the LED panel I used required little assembly.

**Step 2.** -- Download Required Dependencies

PiClock requires an RGB matrix library from [Henner Zeller](https://github.com/hzeller/rpi-rgb-led-matrix) to drive the display. Install it from the terminal on the Pi:

```
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh >rgb-matrix.sh

sudo bash rgb-matrix.sh
```

According to installation instructions for the HAT, you will want to select Option 2 for the interface board type and Option 1 for Quality, following instructions for soldering for that option.

At this point you can test samples from 

```
rpi-rgb-led-matrix/bindings/python/samples/
```

using

```
sudo ./{SAMPLE_FILE_NAME}.py --led-rows={MATRIX_WIDTH} --led-rows={MATRIX_HEIGHT}
```

A full list of commannd line arguments can be found [here](https://github.com/hzeller/rpi-rgb-led-matrix#changing-parameters-via-command-line-flags)

**Step 3.** Get an AccuWeather Developer API key

You can navigate to AccuWeather's [package pricing](https://developer.accuweather.com/packages) page to sign up for the limited free tier. 

From there, you will need to create an app to generate an API key. 

**Step 4.** Fork Repo and Run!

Fork the repo, navigate to the project folder, and open the `apikey.py` file. Inside this file, replace the dummy text with your API key you generated from AccuWeather, and save it.

Once that's all done, you're ready to go! Simply open up a terminal and navigate to the project directory, then run

```
sudo ./PiClock.py --led-rows=64 --led-cols=64
```

to run PiClock on a 64x64 display.

## Contributing
### 1.0.0 and onwards

PiClock as of 1.0.0 is a fully functional clock with day / date and weather integration. I would also like to add hourly temperature graphing as well as other features, such as a calendar or event reminder page, with future releases.

PiClock currently runs at 100% brightness, which for a large LED panel can be too bright for some users. I plan on implementing a motion-controlled dimmer switch with version 1.1.0. It would not be a bad idea to integrate a software-only (i.e. command-line) toggles for brightness to alleviate this concern for some users.

I am also currently accepting feedback on whether to adapt this kind of clock to a lower resolution display. This would eliminate the need to pass through panel dimensions as arguments when running the display from the terminal.

PiClock is freely distributed as-is, but if you would like to contribute to the development of PiClock, feel free to open a PR!
