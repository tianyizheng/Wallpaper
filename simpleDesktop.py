import os
import random
import subprocess
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from utils import saveAndSetBackground

# This script gets a random image from SimpleDesktop
# saves it locally under the assets folder
# and changes your background to that

SCRIPT = """/usr/bin/osascript<<END
tell application "System Events"
tell every desktop
set picture to POSIX file "%s"
end tell
end tell
END"""

sdUrl = 'http://simpledesktops.com/browse/'
sdRandomPage = str(random.randint(1, 49))

ua = UserAgent(fallback='Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36')
sdHeaders = {'User-Agent':str(ua.chrome)}
imgpath = '/assets/imgbuffer.png'
dir_path = os.path.dirname(os.path.realpath(__file__))

def parseHtml():
    sdResponse = requests.get(sdUrl + sdRandomPage, headers=sdHeaders)
    sdHtmlContent = sdResponse.content
    sdSoup = BeautifulSoup(sdHtmlContent, 'html.parser', from_encoding='utf-8')
    sdItems = sdSoup.find_all('img')
    return sdItems


def getImgUrl(allImgs):
    imgUrl = []
    for eachImg in allImgs:
        sdLinks = eachImg.get('src')
        sdUserUploadLinks = sdLinks.split('.295x184_q100')[0]
        if sdUserUploadLinks.rfind('uploads') != -1:
            imgUrl.append(sdUserUploadLinks)
    return imgUrl

def getImgUrlWithTitle(allImgs):
    imgUrl = {}
    for eachImg in allImgs:
        sdLinks = eachImg.get('src')
        sdTitle = eachImg.get('title')
        sdUserUploadLinks = sdLinks.split('.295x184_q100')[0]
        if sdUserUploadLinks.rfind('uploads') != -1:
            imgUrl[sdTitle] = sdUserUploadLinks
    return imgUrl

def getImage():
    sdImgs = parseHtml()
    sdImageUrls = getImgUrl(sdImgs)
    randomImage = random.randint(0, len(sdImageUrls) - 1)
    return sdImageUrls[randomImage]


def main():
    sdUrl = getImage()
    saveAndSetBackground(sdUrl)


if __name__ == '__main__':
    main()
