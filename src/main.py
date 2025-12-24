# *** MODULE IMPORTS ***

from machine import Pin
from pimoroni import Button
import plasma
import time
import random

# *** INITIAL CONFIG ***

# If config.py exists, import starting values from there, otherwise use sensible defaults
try:
  import config

except:
  print("No config file found! Using default values.")
  PLASMA_BOARD = 1
  NUM_LEDS = 50
  BRIGHTNESS = 0.7
  BELL_INTERVAL_MS = 250
  LED_COLOR_ORDER = 2 # Possible values are: RGB = 0; RBG = 1; GRB = 2; GBR = 3; BRG = 4; BGR = 5

else:
  print("Config file found!")
  PLASMA_BOARD = config.PLASMA_BOARD
  NUM_LEDS = config.NUM_LEDS
  BRIGHTNESS = config.BRIGHTNESS
  BELL_INTERVAL_MS = config.BELL_INTERVAL_MS
  LED_COLOR_ORDER = config.LED_COLOR_ORDER
  BELL_TO_LED = config.bell_to_led

ROUNDS = True

# Board-specific setup

if PLASMA_BOARD == 1: # Plasma 2040
  print("Board is Plasma 2040")
  led_strip = plasma.WS2812(NUM_LEDS)
  print("Board setup complete")

class Bell:
  def __init__(self, n, name, hue, decay):
    self.n = n
    self.name = name
    self.hue = hue
    self.decay = decay
    self.value = 0.0
    self.last_ring = None

  def ring(self):
    self.last_ring = time.ticks_ms()

  def amplitude(self):
    time_since_last_ring = time.ticks_diff(time.ticks_ms(), self.last_ring)
    if time_since_last_ring > self.decay:
      return 0.0
    else:
      return 1-(time_since_last_ring / self.decay) * BRIGHTNESS

# The bells (names from The Nine Tailors by Dorothy L Sayers)

GAUDE = 1
SABAOTH = 2
JOHN = 3
JERICHO = 4
JUBILEE = 5
DIMITY = 6
BATTY_THOMAS = 7
TAILOR_PAUL = 8

bells = [Bell(0,"NONE",0,0),
         Bell(GAUDE,"Gaude",280/360,1000),
         Bell(SABAOTH,"Sabaoth",240/360,1100),
         Bell(JOHN,"John",200/360,1200),
         Bell(JERICHO,"Jericho",160/360,1300),
         Bell(JUBILEE,"Jubilee",120/360,1400),
         Bell(DIMITY,"Dimity",80/360,1500),
         Bell(BATTY_THOMAS,"Batty Thomas",40/360,1600),
         Bell(TAILOR_PAUL,"Tailor Paul",0,2000)]

last_bell = 0

# *** HELPER FUNCTIONS ***

def next_bell():

  if ROUNDS:
    return (last_bell % 8) + 1
  else:
    return 8

# *** LED MANAGEMENT ***

led_strip.start()

def update_leds():
  for bell in bells:
    h = bell.hue
    v = bell.amplitude()
    for led in BELL_TO_LED[bell.n]:
      led_strip.set_hsv(led, h, 1.0, v)


# *** MAIN ROUTINE ***    

print("Starting main routine")

last_ring = None

while True:
  if time.ticks_diff(time.ticks_ms(), last_ring) > BELL_INTERVAL_MS:
    b = next_bell()
    bells[b].ring()
    last_ring = time.ticks_ms()
    last_bell = b
  update_leds()
  time.sleep_ms(10)