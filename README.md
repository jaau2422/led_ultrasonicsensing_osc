# led_ultrasonicsensing_osc

This is a collaborative project using Raspberry Pi and Python to send OSC messages into the Unreal Engine
Based on the distance of an object to the distance sensor, it changes the brightness and color of an LED pixel ring.

To run this on your raspberry pi you need to do these steps:
first in order to use the LED pixel you need to disable your audio on the pi
in your project folder you need to install the following libraries running these commands:

sudo pip3 install rpi_ws281x
sudo pip3 install python-osc

run the python code as a root
sudo python Led_ultrasonic.py
