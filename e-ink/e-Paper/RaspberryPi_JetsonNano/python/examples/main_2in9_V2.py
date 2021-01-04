#!/usr/bin/python
import requests
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in9_V2
import time
import datetime
from PIL import Image,ImageDraw,ImageFont
import traceback
import subprocess

logging.basicConfig(level=logging.WARN)

def get_temp():
    logging.info('get temp')
    url = "https://api.qweather.com/v7/weather/now?location=101010100&key=cd148b001c4a439fa0f9cfa210a5d16a"
    try:
        r = requests.get(url)
        set_msg('get temp success')

    except Exception as e:
        set_msg('network error')
        logging.error(e)

        return 'Error'
    logging.info('get temp done')

    if r.status_code != 200:
        return

    return r.json().get('now', {}).get('temp')

def set_msg(msg):
    with open('msg.txt', 'w') as f:
        f.write(msg)

def get_msg():
    with open('msg.txt', 'r') as f:
        return f.read().strip()

try:
    epd = epd2in9_V2.EPD()
    epd.init()
    epd.Clear(0xFF)
    
    # font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    # font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    ff = 'Technology.ttf'
    big_size = 56
    medium_size = 24
    font_b = ImageFont.truetype(os.path.join(picdir, ff), big_size)
    font_m = ImageFont.truetype(os.path.join(picdir, ff), medium_size)
    
    # partial update
    logging.info("show time")
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    epd.display_Base(epd.getbuffer(time_image))
    temp = get_temp()
    temp_update_interval = 15

    start_x = 10
    start_y = 10
    gap = 5
    width = 296
    height = 128
    while (True):
        now = datetime.datetime.now()
        if now.minute % temp_update_interval == 0 and now.second == 0:
            temp = get_temp()

        time_draw.rectangle((start_x, start_y, width, height), fill = 255)
        time_draw.text((start_x, start_y), now.strftime('%H:%M'), font=font_b, fill = 0)
        # 获取 IP
        cmd = "hostname -I"
        ip = subprocess.check_output(cmd, shell=True).decode('utf-8').split(' ')[0]
        time_draw.text((start_x, start_y + big_size + gap), f"{now.strftime('%Y-%m-%d')} - {now.strftime('%A')} ", font=font_m, fill = 0)
        time_draw.text((start_x, start_y + big_size + medium_size + gap * 2), f"TEMP:{temp}  IP:{ip} ", font=font_m, fill = 0)
        # 计算 msg 位置
        msg = get_msg()
        length = len(msg) * 10 
        _start_x = max(110, width - 10 - length)
        time_draw.text((_start_x, start_y + 2), msg, font=font_m, fill = 0)

        newimage = time_image.crop([10, 10, 296, 128])
        time_image.paste(newimage, (10,10))  
        epd.display_Partial(epd.getbuffer(time_image))
        
    logging.info("Clear...")
    epd.init()
    epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()
    time.sleep(2)
        
    epd.Dev_exit()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    # epd.init()
    # epd.Clear(0xFF)
    
    # logging.info("Goto Sleep...")
    # epd.sleep()
    # time.sleep(1)

    epd2in9_V2.epdconfig.module_exit()
    exit()
