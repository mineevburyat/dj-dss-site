import requests
import json
url = 'https://admin.dss-sport.ru/wp-json/wp/v2/pages/'
def printjson(id, url=url):
    body = requests.get(url+str(id))
    print(body.json())



if __name__ == "__main__":
    printjson(983)