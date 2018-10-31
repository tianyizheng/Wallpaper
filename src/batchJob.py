import os
import sys
import time
import requests
import concurrent.futures
from requests.auth import HTTPBasicAuth
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

import simpleDesktop
destination = '-----your next cloud--------'
suffix = '.png'

sdUrl = 'http://simpledesktops.com/browse/'

ua = UserAgent(fallback='Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36')
sdHeaders = {'User-Agent':str(ua.chrome)}
imgpath = '/assets/'
dir_path = os.path.dirname(os.path.realpath(__file__))


def usage():
    #need a better way to determine what the user wants to download
    print("Usage: python batchJob.py local 1")
    print("       python batchJob.py cloud 1 username password")
    print("       python batchJob.py cloud all username password")
def parseHtml(pageNum):
    sdResponse = requests.get(sdUrl + pageNum, headers=sdHeaders)
    sdHtmlContent = sdResponse.content
    sdSoup = BeautifulSoup(sdHtmlContent, 'html.parser', from_encoding='utf-8')
    sdItems = sdSoup.find_all('img')
    return sdItems

def saveImgToDevice(imgUrl, fileName):
    imgData = requests.get(imgUrl).content
    with open(fileName + suffix, 'wb') as handler:
        handler.write(imgData)

# def downloadLocally(sdImageUrls, rootFolder):
#     indx = 0
#     while indx < len(sdImageUrls):
#         imagePath = rootFolder + '/' + str(indx)
#         print('Downloading image #{imgName}\n'.format(imgName=imagePath))
#         saveImgToDevice(sdImageUrls[indx], imagePath)
#         indx += 1
#         print('Pausing...\n')
#         time.sleep(0.5)

def multithreadLocally(sdImageUrl, title, rootFolder):
    imagePath = rootFolder + '/' + title
    saveImgToDevice(sdImageUrls[indx], imagePath)
    print('Done with image #{imgName}\n'.format(imgName=imagePath))
    time.sleep(0.5)

# def uploadToCloud(sdImageUrls, pageNum, username, password):
#     rFolder = destination+str(pageNum)+'/'
#     indx = 0
#     requests.request('MKCOL', rFolder, auth=HTTPBasicAuth(username, password))
#     while indx < len(sdImageUrls):
#         print('Grabbing image #{imgName}'.format(imgName=indx))
#         imgData = requests.get(sdImageUrls[indx]).content
#         print('Uploading...')
#         r = requests.put(rFolder+str(indx)+suffix, auth=HTTPBasicAuth(username, password), data=imgData)
#         print r.status_code
#         indx += 1
#         print('Pausing...\n')
#         time.sleep(2)

def multithreadToCloud(sdImageUrl, title, rFolder, username, password):
    target = rFolder+title+'.png'
    imgData = requests.get(sdImageUrl).content
    r = requests.put(target, auth=HTTPBasicAuth(username, password), data=imgData)
    if r.status_code == requests.codes.created :
        print('Done with image #{imgName}'.format(imgName=title))
    else:
        print('Error with image #{imgName}'.format(imgName=title))
    time.sleep(0.5)

def helperCloud(pageNum, username, password):
    sdImgs = parseHtml(pageNum)
    sdImageUrls = simpleDesktop.getImgUrlWithTitle(sdImgs)
    rFolder = destination+str(pageNum)+'/'
    requests.request('MKCOL', rFolder, auth=HTTPBasicAuth(username, password))
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
        for title in sdImageUrls.keys():
            executor.submit(multithreadToCloud, sdImageUrls[title], title, rFolder, username, password)
    # uploadToCloud(sdImageUrls, pageNum, sys.argv[3], sys.argv[4])


def helperLocal(pageNum):
    sdImgs = parseHtml(pageNum)
    rootFolder = dir_path+'/assets/'+str(pageNum)
    if not os.path.isdir(rootFolder):
        os.makedirs(rootFolder)
    sdImageUrls = simpleDesktop.getImgUrlWithTitle(sdImgs)
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
            for title in sdImageUrls.keys():
                executor.submit(multithreadLocally, sdImageUrls[title], title, rootFolder)

def main():
    if len(sys.argv) == 3 and sys.argv[1] == 'local':
        try:
            int(sys.argv[2])
            helperLocal(sys.argv[2])
            exit(0)
        except ValueError:
            if sys.argv[2] == 'all':
                for i in range(49):
                    helperLocal(str(i))
                    exit(0)
            else:
                usage()
                exit(0)
        else:
            usage()
            exit(0)
    elif len(sys.argv) == 5 and sys.argv[1] == 'cloud':
        username = sys.argv[3]
        password = sys.argv[4]
        try:
            int(sys.argv[2])
            helperCloud(sys.argv[2], username, password)
            exit(0)
        except ValueError:
            if sys.argv[2] == 'all':
                for i in range(49):
                    helperCloud(str(i), username, password)
                    exit(0)
            else:
                usage()
                exit(0)
        else:
                usage()
                exit(0)

if __name__ == '__main__':
    main()


