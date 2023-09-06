import requests
import pandas as pd
import os
import numpy as n 
import time

columns = [
  "acceleration",
  "engine",
  "fuel_status",
  "url_price",
  "url_review",
  "volume",
  "authenticated",
  "badge",
  "body_color",
  "body_status",
  "body_type",
  "code",
  "color",
  "description",
  "fuel",
  "image",
  "image_count",
  "inside_color",
  "location",
  "mileage",
  "modified_date",
  "pin",
  "rank",
  "specialcase",
  "subtitle",
  "time",
  "title",
  "transmission",
  "trim",
  "type",
  "url",
  "year",
  "images",
  "keywords",
  "price"
]

url = "https://bama.ir/cad/api/search?mileageFrom=1&priced=1"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def create_page_index(idx=1):
  _url = url + "&pageIndex={0}".format(idx)
  print(_url)
  return _url

def get_price(data):
  return [data["price"]["price"] if data["price"] and data["price"]["price"] else None]

def get_specs(data):
  return [
  data["specs"]["acceleration"] if data["specs"] and data["specs"]["acceleration"] else None,
  data["specs"]["engine"] if data["specs"] and data["specs"]["engine"] else None,
  data["specs"]["fuel"] if data["specs"] and data["specs"]["fuel"] else None,
  data["specs"]["url_price"] if data["specs"] and data["specs"]["url_price"] else None,
  data["specs"]["url_review"] if data["specs"] and data["specs"]["url_review"] else None,
  data["specs"]["volume"] if data["specs"] and data["specs"]["volume"] else None,
  ]
  
def get_details(data):
  return [
    data["detail"]["authenticated"] if data["detail"] and data["detail"]["authenticated"] else None,
    data["detail"]["badge"] if data["detail"] and data["detail"]["badge"] else None,
    data["detail"]["body_color"] if data["detail"] and data["detail"]["body_color"] else None,
    data["detail"]["body_status"] if data["detail"] and data["detail"]["body_status"] else None,
    data["detail"]["body_type"] if data["detail"] and data["detail"]["body_type"] else None,
    data["detail"]["code"] if data["detail"] and data["detail"]["code"] else None,
    data["detail"]["color"] if data["detail"] and data["detail"]["color"] else None,
    data["detail"]["description"] if data["detail"] and data["detail"]["description"] else None,
    data["detail"]["fuel"] if data["detail"] and data["detail"]["fuel"] else None,
    data["detail"]["image"] if data["detail"] and data["detail"]["image"] else None,
    data["detail"]["image_count"] if data["detail"] and data["detail"]["image_count"] else None,
    data["detail"]["inside_color"] if data["detail"] and data["detail"]["inside_color"] else None,
    data["detail"]["location"] if data["detail"] and data["detail"]["location"] else None,
    data["detail"]["mileage"] if data["detail"] and data["detail"]["mileage"] else None,
    data["detail"]["modified_date"] if data["detail"] and data["detail"]["modified_date"] else None,
    data["detail"]["pin"] if data["detail"] and data["detail"]["pin"] else None,
    data["detail"]["rank"] if data["detail"] and data["detail"]["rank"] else None,
    data["detail"]["specialcase"] if data["detail"] and data["detail"]["specialcase"] else None,
    data["detail"]["subtitle"] if data["detail"] and data["detail"]["subtitle"] else None,
    data["detail"]["time"] if data["detail"] and data["detail"]["time"] else None,
    data["detail"]["title"] if data["detail"] and data["detail"]["title"] else None,
    data["detail"]["transmission"] if data["detail"] and data["detail"]["transmission"] else None,
    data["detail"]["trim"] if data["detail"] and data["detail"]["trim"] else None,
    data["detail"]["type"] if data["detail"] and data["detail"]["type"] else None,
    data["detail"]["url"] if data["detail"] and data["detail"]["url"] else None,
    data["detail"]["year"] if data["detail"] and data["detail"]["year"] else None,
  ]
  
def get_images(data):
  return ["".join(list(map(lambda x: x["thumb"], data["images"]))) if data["images"] else None]

def get_keywords(data):
  return [data["metadata"]["keywords"] if data["metadata"] and data["metadata"]["keywords"] else None]


def get_page_data(url=create_page_index(), dataset_path="./Dataset.csv", columns=columns):
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    data = response.json()
    
    if os.path.exists(dataset_path):
      df = pd.read_csv(dataset_path)
    else:
      df = pd.DataFrame(columns=columns)
    
    for car_ad in data["data"]["ads"]:
      specs = get_specs(car_ad)
      detail = get_details(car_ad)
      price = get_price(car_ad)
      images_links = get_images(car_ad)
      keywords = get_keywords(car_ad)
      
      result = n.concatenate([specs, detail, images_links, keywords, price])
      
      df.loc[len(df)] = result
      
    df.to_csv(dataset_path, index=False)

for idx in range(1, 10):
  print(idx)
  get_page_data(url=create_page_index(idx))
  time.sleep(3)
  print(idx)