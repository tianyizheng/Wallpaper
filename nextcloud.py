import os
import urllib
import random
import datetime
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

destination = '--------your next cloud url ------------'
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

def randomTable(conn):
    with conn:
        sql = '''SELECT name FROM sqlite_master WHERE type='table';'''
        cur = conn.cursor()
        tables = cur.execute(sql).fetchall()
        num = random.randint(0,len(tables))
        return num

def getImgUrl(sign):
    try:
        conn = create_connection(database)
        pageNum = randomTable(conn)
        with conn:
            sql = '''SELECT imgID FROM page{0} WHERE SCORE {1} 10000 ORDER BY RANDOM() LIMIT 1;'''.format(pageNum, sign)
            cur = conn.cursor()
            filename = str(cur.execute(sql).fetchall()[0][0])
            filename = urllib.quote(filename)
            return destination + filename + ".png"
    except Exception as e:
        print(e)

def saveImgToDeviceWithAuth(imgUrl):
    imgData = requests.get(imgUrl, auth=HTTPBasicAuth("username", "password")).content
    with open(dir_path + "/test.png", 'wb') as handler:
        handler.write(imgData)

def set_desktop_background(filename):
    subprocess.Popen(SCRIPT%filename, shell=True)
    subprocess.check_call("killall Dock", shell=True)


def main():
    currentHour = datetime.datetime.now().hour
    if currentHour > 19 or currentHour < 9:
        urlString = getImgUrl('<')
    else:
        urlString = getImgUrl('>')
    saveImgToDeviceWithAuth(urlString)
    set_desktop_background(dir_path + imgpath)


if __name__ == '__main__':
    main()
