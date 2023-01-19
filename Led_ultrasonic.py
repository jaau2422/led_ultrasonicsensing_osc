import RPi.GPIO as GPIO
import time
from pythonosc import udp_client
from rpi_ws281x import *
client= udp_client.SimpleUDPClient("10.106.50.54",8003)

trigPin = 16
echoPin = 18
MAX_DISTANCE = 220 #define the maximum measured distance(cm)
timeOut = MAX_DISTANCE*60 #calculate timeout(μs) according to the maximum measured distance

# LED strip configuration:
LED_COUNT = 8 # Number of LED pixels.
LED_PIN = 18 # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000 # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10 # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255 # Set to 0 for darkest and 255 for brightest
LED_INVERT = False # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0 # set to '1' for GPIOs 13, 19, 41, 45 or 53
# Define functions which animate LEDs in various ways.
def pulseIn(pin,level,timeOut): # function pulseIn: obtain pulse time of a pin
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime
def getSonar(): #get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin,GPIO.HIGH) #make trigPin send 10us high level
    time.sleep(0.00001) #10us
    GPIO.output(trigPin,GPIO.LOW)
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut) #read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0 # the sound speed is 340m/s, and calculate
    return distance
    
def setup():
    print ('Program is starting...')
    GPIO.setmode(GPIO.BOARD) #numbers GPIOs by physical location
    GPIO.setup(trigPin, GPIO.OUT) # set trigPin to output mode
    GPIO.setup(echoPin, GPIO.IN) # set echoPin to input mode
    
class Led:
    def __init__(self):
        #Control the sending order of color data
        self.ORDER = "RGB"
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
        self.strip.begin()
#self.strip.setPixelColor(i, color)
led=Led()



# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    setup()
    try:
        while True:
            time.sleep(0.05)
            for i in range(8):
                distance= getSonar()
                newdistance = int(distance)
                newdistance2= 1/(newdistance+1)*600
                print(int(1.5*newdistance2))
                client.send_message("/color",newdistance2)
                led.strip.setPixelColor(i, Color(int(newdistance2*1.5),int(40),int(1/(newdistance2+1)*1000)))
                led.strip.show()
                time.sleep(0.05)
    except KeyboardInterrupt: # When 'Ctrl+C' is pressed, the child program destroy() will be

        for i in range(8):
            led.strip.setPixelColor(i, Color(0,0,0))
        led.strip.show()
        GPIO.cleanup()