import json
from src.applyWallpaper import getImageFromDb

def handle(event, context):
  url = getImageFromDb()
  body = {
    "url" : url
  }
  response = {
    "statusCode": 200,
    "body": json.dumps(body)
  }
  return response

# if __name__ == '__main__':
#     handle("event", "context")