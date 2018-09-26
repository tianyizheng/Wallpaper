import os
import io
import sys
import cv2
import math
import numpy as np
import requests
import concurrent.futures

import batchJob
import simpleDesktop

sdUrl = simpleDesktop.sdUrl

def usage():
    #need a better way to determine what the user wants to download
    print("Usage: python brightness.py 1")
    print("       python brightness.py all")

def analyze(imgUrl):
    imgData = requests.get(imgUrl).content
    bin_data = io.BytesIO(imgData)
    file_bytes = np.asarray(bytearray(bin_data.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    param = [0.114, 0.587, 0.299]
    result = 0
    for i in range(3):
        histr = cv2.calcHist([img],[i],None,[256],[0,256])
        result += np.argmax(histr)**2 * param[i]
    print math.sqrt(result)

def submitAnalyzeJobs(pageNum):
    if pageNum > 49 or pageNum < 1:
      print "Cannot process pageNum = " + pageNum
    sdImgs = batchJob.parseHtml(pageNum)
    sdImageUrls = simpleDesktop.getImgUrl(sdImgs)
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
            for indx in range(len(sdImageUrls)):
                executor.submit(analyze, sdImageUrls[indx])


def main():
    if len(sys.argv) == 2:
        try:
            submitAnalyzeJobs(int(sys.argv[1]))
            exit(0)
        except ValueError:
            if sys.argv[1] == 'all':
                for i in range(49):
                    submitAnalyzeJobs(sys.argv[1])
                    exit(0)
            else:
                usage()
                exit(0)
        else:
            usage()
            exit(0)
    else:
        usage()
        exit(0)

if __name__ == '__main__':
    main()