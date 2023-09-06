import requests
from bs4 import BeautifulSoup

url = "https://divar.ir/s/tehran/car"

response = requests.get(url)

car_links = []

soup = BeautifulSoup(response.text, "html.parser")
car_boxes = soup.find_all("div", {"class": "post-card-item-af972"})
for idx in range(len(car_boxes)):
    print(idx, car_boxes[idx])
    new_soup = BeautifulSoup(car_boxes[idx], "html.parser")
    link = new_soup.find("a", href=True)
    print(idx, link)
    # if link and link.text:
        # car_links.append(link['href'])
        
print('Status code: ', response.status_code)
print(len(car_links), len(car_boxes))