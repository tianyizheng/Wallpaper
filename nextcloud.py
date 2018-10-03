import os
import urllib
import random
import subprocess
import sqlite3
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

SCRIPT = """/usr/bin/osascript<<END
tell application "System Events"
tell current desktop
set picture to POSIX file "%s"
end tell
END"""

destination = '---------your next cloud folder url--------------'
suffix = '.png'

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
    try:
        conn = create_connection(database)
        with conn:
            sql = '''SELECT imgID FROM page1 ORDER BY RANDOM() LIMIT 1;'''
            cur = conn.cursor()
            filename = str(cur.execute(sql).fetchall()[0][0])
            filename = urllib.quote(filename)
            return destination + filename + ".png"
    except Exception as e:
        print(e)

def saveImgToDevice(imgUrl):
    imgData = requests.get(imgUrl, auth=HTTPBasicAuth("username", "password")).content
    with open(dir_path + "/test.png", 'wb') as handler:
        handler.write(imgData)

def set_desktop_background(filename):
    subprocess.Popen(SCRIPT%filename, shell=True)
    subprocess.check_call("killall Dock", shell=True)


def main():
    urlString = getImgUrl()
    print urlString
    saveImgToDevice(urlString)
    set_desktop_background(dir_path + "/test.png")


if __name__ == '__main__':
    main()
