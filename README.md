# twinklebells
_Ringing in the New Year with LEDs_

## Introduction

Last year I celebrated the 12 Days of Christmas by programming my Christmas lights to demonstrate [a different sort method each day](https://github.com/scripsi/xmasort). This year I'm inspired to explore the world of bell ringing in lights, after reading Dorothy L. Sayers' _The Nine Tailors_.

**The aim of this project is to visualise bell ringing methods and ring peals of changes using strings of RGB LEDs**!

## Background

### About _The Nine Tailors_

_The Nine Tailors_ is a detective novel and a love-letter to country life in the English Fens where the author Dorothy L. Sayers grew up. At the beginning of the book, her hero, Lord Peter Wimsey arrives in the small village of Fenchurch St Paul on a snowy New Year's Eve and is instantly recruited to help ring in the New Year with a full peal on the church bells. The ensuing story is threaded through with the strange and beautiful language of bells and bell-ringing as Wimsey slowly unravels the tangle of circumstances around a gruesome discovery in the churchyard. To ensure authenticity for the story, Sayers evidently spent a long time researching the peculiarly English art of change-ringing. Puzzles and ciphers are expressed in the mathematical methods of the changes, while the bells mark out the beats of the story from that joyful New Year peal, through solemn tolling for the dead, to alarms warning of a final, dramatic and deadly flood.

### About bell ringing

The [Central Council of Church Bell Ringers](https://cccbr.org.uk/) is the fount of knowledge about the history of bell ringing in England. What began as a simple and largely secular use of church bells to announce community events grew into a complex musical art form through the 17th to 19th centuries as technological advancements in bell founding allowed ever larger and better [tuned scales of bells](https://www.hibberts.co.uk/). In Europe, this eventually resulted in carillons of bells spanning several octaves of a chromatic scale and able to [play full pieces of music](https://www.youtube.com/watch?v=8WVbmDewfnQ) either by hand or mechanically-driven. In England, things took a different tack, with ringers exploring all of the possible combinations of a diatonic scale of bells in mathematical sequences. These changes or [methods](https://ringing.org/) became ever more numerous and elaborate as bell ringing teams from neighbouring parishes competed with each other to produce the longest peals with the most harmonious sound. 

Change ringing is a team effort which requires intense concentration, physical stamina and long experience to do well. A complex terminology and tradition has built up around English bell ringing, which Sayers celebrates in her book. I have never done any bell ringing and so I've clearly got a very steep learning curve ahead of me, but it looks like it will be a fun rabbit-hole to fall down...

### A brief explanation of terms

A **Stage** indicates the number of bells being rung. A stage of 7 bells is called **Trebles**, while 8 bells are called **Major**. The bells are numbered: The highest pitch bell, the **Treble**, is number 1, and the remaining bells are numbered in order of decreasing pitch. The lowest pitch bell is the **Tenor**.

The bells are rung in a sequence indicated by their numbers. A complete sequence where every bell rings exactly once is a **Row**. A row which is rung in order from highest to lowest pitch is called **Rounds**. A bell's position within a row is called its **Place**. One or more pairs of adjacent bells in a row can swap places in the following row, which is called a **Change**. The complete set of unique rows possible with a set of bells is its **Extent** (the extent of _n_ bells = _n_!).

```text
# A row of Major rounds followed by a row with changes at places 1&2 and 7&8
12345678
21345687
```

A sequence of changes is a **Method**. Methods can be combined into longer **Compositions**, with **Calls** used to change the method (or places of bells within the method) at strategic points. The complete sequence of changes is a **Touch** and it is **True** if each possible order of bells is rung exactly once (excluding any rows of rounds at the beginning and end). A touch of at least 5000 changes is a **Peal**. 

### About the bells

So, er, I won't actually be using bells in my project. I will be using coloured lights to represent the bells and the patterns of changes as they are "rung". Nevertheless, I want to be as faithful to the ideas and principles of change-ringing as I can, by incorporating the language and notation into my programming. I also want to model the project on the story of _The Nine Tailors_, so let me introduce the bells:

| Number | Position | Name           | Colour | Hex     | Hue  |
| ------ | -------- | -------------- | ------ | ------- | ---- |
| 1      | Treble   | _Gaude_        | Purple | #AA00FF | 280° |
| 2      | Second   | _Sabaoth_      | Blue   | #0000FF | 240° |
| 3      | Third    | _John_         | Cyan   | #00AAFF | 200° |
| 4      | Fourth   | _Jericho_      | Teal   | #00FFAA | 160° |
| 5      | Fifth    | _Jubilee_      | Green  | #00FF00 | 120° |
| 6      | Sixth    | _Dimity_       | Yellow | #AAFF00 | 80°  |
| 7      | Seventh  | _Batty Thomas_ | Orange | #FFAA00 | 40°  |
| 8      | Tenor    | _Tailor Paul_  | Red    | #FF0000 | 0°   |

The eight bells form a musical octave, and are named as in the book. Each bell is represented by a different light colour, and these are chosen at simple intervals around the colour-wheel to form a rainbow gradient.

## Hardware

The hardware is the same as last year's project and consists of [Pimoroni Plasma 2040](https://shop.pimoroni.com/products/plasma-2040) boards connected to a variety of programmable RGB LED strings and powered using USB-C. I have three types of LED string:

- [10-metre LED star wire](https://shop.pimoroni.com/products/10m-addressable-rgb-led-star-wire) with 66 star-shaped leds
- [5-metre flexible LED wire](https://shop.pimoroni.com/products/5m-flexible-rgb-led-wire-50-rgb-leds-aka-neopixel-ws2812-sk6812) with 50 diffused LEDs
- A 1-metre strip of ws2812 60-LEDs/m, which I use for prototyping and testing

The Plasma 2040 boards are encased in [these 3D-printed enclosures](https://www.printables.com/model/261123-plasma-2040-case), which keeps them protected while potentially allowing the use of the additional buttons for control of the lights.

## Software

The Plasma 2040s are all flashed with Pimoroni's [Pirate-brand MicroPython](https://github.com/pimoroni/pimoroni-pico/releases) version 1.25.0. [Microsoft Visual Studio Code](https://code.visualstudio.com/) is used to program them, with the help of the recently-released official [Raspberry Pi Pico Extension](https://marketplace.visualstudio.com/items?itemName=raspberry-pi.raspberry-pi-pico). The `main.py` program installed on each Plasma 2040 will run automatically whenever it is powered on, taking its configuration from `config.py`.

To install, copy `main.py` and `config.py` from the `src/` directory of this repository to the Plasma 2040. If using the Raspberry Pi Pico extension in VSCode, you can do this by opening the command palette with CTRL-SHIFT-P and choosing the `MicroPico: Upload file to pico` command for each file. If necessary, edit `config.py` to match your LED string before uploading.

The basic `main.py` is derived from last year's version. It imports necessary libraries, reads the config file for constants like the number of LEDs and default brightness, and has functions for managing and updating the LED colours. It then enters an infinite loop, repeatedly showing the chosen touch.
