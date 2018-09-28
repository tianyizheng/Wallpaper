import os
import random
import subprocess
import sqlite3
import requests
from bs4 import BeautifulSoup

SCRIPT = """/usr/bin/osascript<<END
tell application "System Events"
tell current desktop
set picture to POSIX file "%s"
end tell
END"""

destination = '-----your next cloud--------'
suffix = '.png'

sdUrl = 'http://simpledesktops.com/browse/'

ua = UserAgent(fallback='Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36')
sdHeaders = {'User-Agent':str(ua.chrome)}
imgpath = '/assets/'
dir_path = os.path.dirname(os.path.realpath(__file__))
database = dir_path + "/store.db"

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
        exit(1)

def getImgUrl():
    imgUrl = []
    for eachImg in allImgs:
        sdLinks = eachImg.get('src')
        sdUserUploadLinks = sdLinks.split('.295x184_q100')[0]
        if sdUserUploadLinks.rfind('uploads') != -1:
            imgUrl.append(sdUserUploadLinks)
    return imgUrl

def getImage():
    conn = create_connection()

    sdImgs = parseHtml()
    sdImageUrls = getImgUrl(sdImgs)
    randomImage = random.randint(0, len(sdImageUrls) - 1)
    return sdImageUrls[randomImage]

def saveImgToDevice(imgUrl):
    imgData = requests.get(imgUrl).content
    with open(dir_path + imgpath, 'wb') as handler:
        handler.write(imgData)

def set_desktop_background(filename):
    subprocess.Popen(SCRIPT%filename, shell=True)
    subprocess.check_call("killall Dock", shell=True)


def main():
    sdUrl = getImage()
    saveImgToDevice(sdUrl)
    set_desktop_background(dir_path + imgpath)


if __name__ == '__main__':
    main()
