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
from utils import create_connection

sdUrl = simpleDesktop.sdUrl
dir_path = os.path.dirname(os.path.realpath(__file__))
database = dir_path + "/store.db"
def usage():
    #need a better way to determine what the user wants to download
    print("Usage: python brightness.py 1")
    print("       python brightness.py all")

def create_table(pageNum):
    sql = """CREATE TABLE IF NOT EXISTS page{0}(
                imgId text PRIMARY KEY,
                score integer NOT NULL);""".format(pageNum)
    try:
        conn = create_connection(database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql)
    except Exception as e:
        print(e)

def create_score(conn, pageNum, data):
    sql = ''' INSERT INTO page{0}(imgId,score,url)
              VALUES(?,?,?) '''.format(pageNum)
    try:
        cur = conn.cursor()
        cur.execute(sql, data)
    except Exception as e:
        print(e)

def clean_table(conn, pageNum):
    sql = '''DELETE FROM page{0} WHERE url is NULL'''.format(pageNum)
    try:
        cur = conn.cursor()
        cur.execute(sql)
    except Exception as e:
        print(e)

def create_or_update_score(conn, pageNum, url, title, score):
    sql_find = '''SELECT url FROM page{0} WHERE imgId = ?'''.format(pageNum)
    sql_update = ''' UPDATE page{0} SET url = '{1}' WHERE
              imgId = '{2}' '''.format(pageNum, url, title)
    sql_insert = ''' INSERT INTO page{0}(imgId,score,url)
              VALUES(?,?,?) '''.format(pageNum)
    try:
        cur = conn.cursor()
        cur.execute(sql_find, (title,))
        data = cur.fetchall()
        if len(data) == 0:
            cur.execute(sql_insert, (title,score,url))
        elif data[0] and data[0][0] is None:
            print((title,url))
            cur.execute(sql_update)
    except Exception as e:
        print(e)

def analyze(imgUrl, title, pageNum):
    imgData = requests.get(imgUrl).content
    bin_data = io.BytesIO(imgData)
    file_bytes = np.asarray(bytearray(bin_data.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    param = [0.114, 0.587, 0.299]
    result = 0
    for i in range(3):
        histr = cv2.calcHist([img],[i],None,[256],[0,256])
        result += np.argmax(histr)**2 * param[i]
    try:
        conn = create_connection(database)
        with conn:
            # create_score(conn, pageNum, (title,result,imgUrl))
            create_or_update_score(conn, pageNum, imgUrl, title, result)
            clean_table(conn, pageNum)
    except Exception as e:
        print(e)

def submitAnalyzeJobs(pageNum):
    if int(pageNum) > 49 or int(pageNum) < 1:
      print "Cannot process pageNum = " + pageNum
      exit(1)
    sdImgs = batchJob.parseHtml(pageNum)
    sdImageUrls = simpleDesktop.getImgUrlWithTitle(sdImgs)
    # create_table(pageNum)
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
            for title in sdImageUrls.keys():
                executor.submit(analyze, sdImageUrls[title], title, pageNum)


def main():
    if len(sys.argv) == 2:
        try:
            int(sys.argv[1])
            submitAnalyzeJobs(sys.argv[1])
            exit(0)
        except ValueError:
            if sys.argv[1] == 'all':
                for i in range(1,49):
                    submitAnalyzeJobs(str(i))
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