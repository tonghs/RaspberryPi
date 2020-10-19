from time import sleep
import datetime
from rpi_ws281x import PixelStrip, Color
from libs.ws281.utils import base_bmp, bmplist2matrix, show, render_char
import math


COLUMN = 32
ROW = 8

# LED strip configuration:
LED_COUNT = ROW * COLUMN  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 4  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Create NeoPixel object with appropriate configuration.
strip = PixelStrip(
    LED_COUNT,
    LED_PIN,
    LED_FREQ_HZ,
    LED_DMA,
    LED_INVERT,
    LED_BRIGHTNESS,
    LED_CHANNEL,
)

strip.begin()


def show_str(color):
    _base_bmp = base_bmp * LED_COUNT
    base_matrix = bmplist2matrix(_base_bmp, COLUMN, ROW)

    x = 2
    y = 1
    char_list = []

    for i, char in enumerate('01:23:45'):
        char_list.append((x, y, char))
        if i % 3:
            x += 3
        else:
            x += 4

    render_char(base_matrix, char_list)
    show(strip, base_matrix, color)


def main():
    show_str(Color(238, 154, 73))
    while True:
        p = 55  # 频率
        a = 10  # 振幅
        min_brightness = 1
        # 周期计算
        for i in range(int(p * 3.14 * 2)):
            b = math.floor(a / 2 * math.sin(i / p) + a / 2 + min_brightness)
            strip.setBrightness(b)
            strip.show()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
