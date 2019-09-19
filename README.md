# PiClock ![Version](https://img.shields.io/badge/Version-1.2.0-green) ![Python](https://img.shields.io/badge/Python-v2.7-blue) ![RPI](https://img.shields.io/badge/Raspberry-Pi-red) ![Active](https://img.shields.io/badge/Active-Yes-brightgreen)

PiClock is a desk clock firmware built for Raspberry Pi 3-compatible LED displays. It pulls data from the AccuWeather API once per hour and details current weather as well as rain forecast for your area. PiClock comes with a utility tool to look up your current area by zip code to generate a compatible location key to be used by the AccuWeather API.

PiClock is designed to work around a low API call limit imposed by AccuWeather. Currently, the "trial" period for this API limits the amount of calls that can be made to 50 per day. PiClock makes 2 calls per hour (one for current weather details and one for forecast), so it maximizes the refresh rate while making sure you don't get charged for API calls.

PiClock was built with a proximity sensor in order to enable changes in brightness by hand gestures. No worries if your build doesn't use one! It's disabled by default, and can be re-enabled with a simple command line flag.

![PiClock](https://i.imgur.com/WRlIgvr.jpg)

## Required Hardware

I recommend using products from Adafruit as that is where I sourced the hardware. Other sources may not be compatible with PiClock.

* **Raspberry Pi Model 3 B+** -- *Other models may work*
* **LED board**
* **[Adafruit RGB Matrix HAT](https://www.adafruit.com/product/2345)**
* **5V, 2A OR 4A Power cable for LED board** -- *Optional, but recommended to avoid overloading the Pi's power supply*
* **[ADPS9960 sensor](https://www.adafruit.com/product/3595)** -- *Optional, if you want to use it to change brightness levels*


## Current Limitations

The original version of PiClock only gives consideration to LED screens consisting of a single 64x64 panel. Exact specifications of the panel I used can be found on Adafruit [here](https://www.adafruit.com/product/3649).

The Adafruit HAT does require soldering connectors to the board. The LED matrix I used also requires additional soldering of a jumper pad to enable 64x64 display. You can find installation instructions for the HAT [here](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/assembly). You will need to follow instructions to assemble the HAT specifically for your display.

PiClock currently runs on Python 2.7.

## Installation

**Step 1.** -- Assemble Hardware

Assemble the HAT and LED matrix according to manufacturer specifications. You can find HAT assembly instructions [here](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/assembly), and the LED panel I used required little assembly.

If you choose to install the ADPS9960 sensor for gesture detection, you can follow [these instructions](https://github.com/liske/python-apds9960/blob/master/RPi.md) to make sure it is wired up correctly. Please also check the required dependencies section for how to install related libraries.

**Step 2.** -- Download Required Dependencies

PiClock requires an RGB matrix library from [Henner Zeller](https://github.com/hzeller/rpi-rgb-led-matrix) to drive the display. Install it from the terminal on the Pi:

```
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh >rgb-matrix.sh

sudo bash rgb-matrix.sh
```

According to installation instructions for the HAT, you will want to select Option 2 for the interface board type and Option 1 for Quality, following instructions for soldering for that option (this works best for changes in brightness).

At this point you can test samples from 

```
rpi-rgb-led-matrix/bindings/python/samples/
```

using

```
sudo ./{SAMPLE_FILE_NAME}.py --led-rows={MATRIX_WIDTH} --led-rows={MATRIX_HEIGHT}
```

A full list of command line arguments can be found in the sections below. These will also work with the sample files from the RGB matrix library. If you choose, PiClock also has additional arguments that you can utilize if you add an ADPS9960 sensor.

If you have added the ADPS9960 sensor, you can install the matching library with 

```
pip install apds9960
```

**Step 3.** Get an AccuWeather Developer API key

You can navigate to AccuWeather's [package pricing](https://developer.accuweather.com/packages) page to sign up for the limited free tier. 

From there, you will need to create an app to generate an API key. 

**Step 4.** Fork Repo and Run!

Fork the repo, navigate to the project folder, and open the `apikey.py` file. Inside this file, replace the dummy text with your API key you generated from AccuWeather, and save it.

Next, you'll need to generate your location code (this is different than your zip code). There is an included `utility.py` file in the project directory. You can run that with

```
sudo ./utility.py
```

and follow the prompts in order to poll the API and fetch the code. Once it's saved, you won't need to run this again (unless you want to get data from a different location).

Once that's all done, you're ready to go! Simply open up a terminal and navigate to the project directory, then run

```
sudo ./PiClock.py
```

to run PiClock on a 64x64 display.

### Command Line Arguments:
| Argument | Description |
| --- | --- |
| -e, --enable-motion-sensor | Enable motion sensor for brightness adjustment. ***Requires [ADPS9960 sensor](https://www.adafruit.com/product/3595)*** or equivalent. |
| -r, --led-rows |  Display rows. 16 for 16x32, 32 for 32x32. Default: 64 | 
| --led-cols |  Panel columns. Typically 32 or 64. Default: 64 | 
| -c, --led-chain |  Daisy-chained boards. Default: 1 | 
| -P, --led-parallel |  For Plus-models or RPi2: parallel chains. 1..3. Default: 1 | 
| -p, --led-pwm-bits |  Bits used for PWM. Something between 1..11. Default: 11 | 
| -b, --led-brightness |  Sets brightness level. Default: 100. Range: 1..100 | 
| -m, --led-gpio-mapping |  Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm | 
| --led-scan-mode | Progressive or interlaced scan. 0 Progressive, 1 Interlaced (default) | 
| --led-pwm-lsb-nanosecondsBase | time-unit for the on-time in the lowest significant bit in nanoseconds. Default: 130 | 
| --led-show-refresh |  Shows the current refresh rate of the LED panel | 
| --led-slowdown-gpio |  Slow down writing to GPIO. Range: 1..100. Default: 1 | 
| --led-no-hardware-pulse | Don't use hardware pin-pulse generation | 
| --led-rgb-sequence |  Switch if your matrix has led colors swapped. Default: RGB | 
| --led-pixel-mapper |  Apply pixel mappers. e.g \Rotate:90\ | 
| --led-row-addr-type |  0 = default; 1=AB-addressed panels;2=row direct | 
| --led-multiplexing |  Multiplexing type: 0=direct; 1=strip; 2=checker; 3=spiral; 4=ZStripe; 5=ZnMirrorZStripe; 6=coreman; 7=Kaler2Scan; 8=ZStripeUneven (Default: 0) |

## Contributing
### 1.2.0 and onwards

PiClock as of 1.2.0 is a fully functional clock with day / date and weather integration. I would also like to add other features, such as a calendar or event reminder page, with future releases.

I am also currently accepting feedback on whether to adapt this kind of clock to a lower resolution display. This would eliminate the need to pass through panel dimensions as arguments when running the display from the terminal.

PiClock is freely distributed as-is, but if you would like to contribute to the development of PiClock, feel free to open a PR!
