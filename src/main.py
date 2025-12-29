# *** MODULE IMPORTS ***

import plasma
import time

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
  BELL_TO_LED = [[],[],[],[],[],[],[],[],[]]
  i = NUM_LEDS // 8
  n = i * 8
  for l in range(NUM_LEDS):
    b = l % 8
    BELL_TO_LED[b+1].append(l)

else:
  print("Config file found!")
  PLASMA_BOARD = config.PLASMA_BOARD
  NUM_LEDS = config.NUM_LEDS
  BRIGHTNESS = config.BRIGHTNESS
  BELL_INTERVAL_MS = config.BELL_INTERVAL_MS
  LED_COLOR_ORDER = config.LED_COLOR_ORDER
  if config.BELL_PATTERN == 0:
    BELL_TO_LED = [[],[],[],[],[],[],[],[],[]]
    i = NUM_LEDS // 8
    n = i * 8
    for b in range(1,9):
      for l in range((b-1)*i,b*i):
        BELL_TO_LED[b].append(l)
    for l in range(n,NUM_LEDS):
      BELL_TO_LED[0].append(l)
  elif config.BELL_PATTERN == 1:
    BELL_TO_LED = [[],[],[],[],[],[],[],[],[]]
    i = NUM_LEDS // 8
    n = i * 8
    for l in range(NUM_LEDS):
      b = l % 8
      BELL_TO_LED[b+1].append(l)
  elif config.BELL_PATTERN == 2:
    BELL_TO_LED = config.BELL_TO_LED

try:
  touch = open("touch.txt","rt")
  ROUNDS = False
except:
  print("Couldn't open touch.txt! Ringing Rounds.")
  ROUNDS = True

led_strip = plasma.WS2812(NUM_LEDS, color_order=LED_COLOR_ORDER)

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

bells = [Bell(0,"NONE",0,1),
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
    t = touch.read(1)
    while t not in ['0','1','2','3','4','5','6','7','8']:
      if t == '':
        touch.seek(0)
      t = touch.read(1)
      
    return int(t)

# *** LED MANAGEMENT ***

def update_leds():
  for bell in bells:
    h = bell.hue
    v = bell.amplitude()
    
    for led in BELL_TO_LED[bell.n]:
      led_strip.set_hsv(led, h, 1.0, v)


# *** MAIN ROUTINE ***    

last_ring = None
led_strip.start()

while True:
  if time.ticks_diff(time.ticks_ms(), last_ring) > BELL_INTERVAL_MS:
    b = next_bell()
    if b > 0:
      bells[b].ring()
    last_ring = time.ticks_ms()
    last_bell = b

  update_leds()
  time.sleep_ms(25)