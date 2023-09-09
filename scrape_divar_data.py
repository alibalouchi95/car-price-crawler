from bs4 import BeautifulSoup
import os
import pandas as pd
from scrape_divar_car_card import get_car_data
from selenium import webdriver

url = "https://divar.ir/s/tehran/car?price=100000000-8000000000"

columns = [
    "mileage",
    "year",
    "color",
    "brand_model",
    "fuel_type",
    "engine_status",
    "chassis_status",
    "back_chassis",
    "front_chassis",
    "body_status",
    "insurance_remain",
    "gear_box_type",
    "price",
]
dataset_path = "./Divar_Dataset.csv"


def get_page(driver):
    driver.get(url)
    response = driver.page_source
    return response


def get_car_card(driver):
    soup = BeautifulSoup(get_page(driver), "lxml")
    return soup.find_all("div", {"class": "post-card-item-af972"})


def get_link_from_card(card):
    href = card.find("a")["href"]
    return href


def get_all_links(driver):
    cards = get_car_card(driver)
    links = []
    for card in cards:
        link = get_link_from_card(card)
        links.append("https://divar.ir" + link)

    return links


def get_data(request_number=200):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    saved_data = 0

    if os.path.exists(dataset_path):
        df = pd.read_csv(dataset_path)
    else:
        df = pd.DataFrame(columns=columns)

    while request_number > 0:
        links = get_all_links(driver)
        for link in links:
            data = get_car_data(driver, link, True)
            df.loc[len(df)] = data
            print("NUMBER OF SAVED DATA IS", saved_data)
            saved_data += 1

        df.to_csv(dataset_path, index=False)
        request_number -= 1

    driver.close()


get_data()
