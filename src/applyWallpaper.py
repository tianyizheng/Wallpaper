import os
import datetime
import random
from utils import saveAndSetBackground, create_connection

dir_path = os.path.dirname(os.path.realpath(__file__))
database = dir_path + "/store.db"
set_score = 4500

def selectImage(imgList):
  length = len(imgList)
  index = random.randint(0, length-1)
  return imgList[index][0]


def getImageForNow(pageNum, night):
    sql_night = '''SELECT url FROM page{0} WHERE score <= {1} ORDER BY score ASC'''.format(pageNum,set_score)
    sql_day = '''SELECT url FROM page{0} WHERE score > {1} ORDER BY score DESC'''.format(pageNum,set_score)
    try:
        conn = create_connection(database)
        with conn:
            cur = conn.cursor()
            if night:
              cur.execute(sql_night)
            else:
              cur.execute(sql_day)
            data = cur.fetchall()
            return selectImage(data)
    except Exception as e:
        print(e)

def getImageFromDb():
  now = datetime.datetime.now()
  pageNum = random.randint(1, 49)
  imgUrl = ''
  if (now.hour > 20):
    imgUrl = getImageForNow(pageNum, True)
  else:
    imgUrl = getImageForNow(pageNum, False)
  return imgUrl

def main():
    imgUrl = getImageFromDb()
    saveAndSetBackground(imgUrl)



if __name__ == '__main__':
    main()