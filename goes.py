#!/usr/bin/env python3
# -*- coding=utf-8 -*-


import os
import random
import json
import time
import subprocess
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup

SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""

sdUrl = 'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/5424x5424.jpg'

ua = UserAgent(fallback='Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36')
sdHeaders = {'User-Agent':str(ua.chrome)}
imgpath = '/assets/satellite.png'
dir_path = os.path.dirname(os.path.realpath(__file__))

def saveImgToDevice(imgUrl):
    imgData = requests.get(imgUrl).content
    with open(dir_path + imgpath, 'wb') as handler:
        handler.write(imgData)

def set_desktop_background(filename):
    subprocess.Popen(SCRIPT%filename, shell=True)
    subprocess.check_call("killall Dock", shell=True)


def main():
    saveImgToDevice(sdUrl)
    set_desktop_background(dir_path + imgpath)


if __name__ == '__main__':
    main()
