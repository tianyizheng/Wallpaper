import os
import random
import subprocess
import requests


SCRIPT = """/usr/bin/osascript<<END
tell application "System Events"
tell every desktop
set picture to POSIX file "%s"
end tell
end tell
END"""

imgpath = '/assets/imgbuffer.png'
dir_path = os.path.dirname(os.path.realpath(__file__))

def saveImgToDevice(imgUrl):
    imgData = requests.get(imgUrl).content
    with open(dir_path + imgpath, 'wb') as handler:
        handler.write(imgData)

def set_desktop_background(filename):
    subprocess.Popen(SCRIPT%filename, shell=True)
    subprocess.check_call("killall Dock", shell=True)

def saveAndSetBackground(imgUrl):
    saveImgToDevice(imgUrl)
    set_desktop_background(dir_path + imgpath)