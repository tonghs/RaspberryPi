from time import sleep
import datetime
from rpi_ws281x import PixelStrip, Color
from libs.ws281.utils import base_bmp, bmplist2matrix, show, render_char


COLUMN = 32
ROW = 8

# LED strip configuration:
LED_COUNT = ROW * COLUMN  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 16  # Set to 0 for darkest and 255 for brightest
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


def show_time(color=None):
    # 生成 8 行 32 列的 matrix，对应
    _base_bmp = base_bmp * LED_COUNT
    base_matrix = bmplist2matrix(_base_bmp, COLUMN, ROW)
    now = datetime.datetime.now()

    x = 2
    y = 1
    char_list = []

    for i, char in enumerate(now.strftime('%H:%M:%S')):
        char_list.append((x, y, char))
        if i % 3:
            x += 3
        else:
            x += 4

    x = 2
    y = 7
    for i in range(7):
        char = '_'
        if now.weekday() == i:
            char = '__'
        char_list.append((x, y, char))
        x += 4

    render_char(base_matrix, char_list)
    show(strip, base_matrix, color)


def main():
    while True:
        # show_time(Color(205, 102, 29))
        show_time()
        sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
