from bs4 import BeautifulSoup

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


def fa_to_en_int(number_str):
    if number_str == "":
        return 0

    number_mapper = {
        "۰": "0",
        "۱": "1",
        "۲": "2",
        "۳": "3",
        "۴": "4",
        "۵": "5",
        "۶": "6",
        "۷": "7",
        "۸": "8",
        "۹": "9",
    }
    numbers = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    ]

    res = []

    for char in number_str:
        if char in dict.keys(number_mapper):
            res.append(number_mapper[char])
        elif char in numbers:
            res.append(char)

    if len(res) == 0:
        return 0

    return int("".join(res))


def get_card_data(driver, url):
    driver.get(url)
    response = driver.page_source
    return response


def get_mileage_year_color(soup):
    elements = soup.find_all("div", {"class": "kt-group-row-item"})
    result = {"mileage": 0, "year": 0, "color": ""}
    for elem in elements:
        title = elem.find("span", {"class": "kt-group-row-item__title"}).text
        value = elem.find("span", {"class": "kt-group-row-item__value"}).text

        if title == "کارکرد":
            result["mileage"] = fa_to_en_int(value)
        elif title == "مدل (سال تولید)":
            result["year"] = fa_to_en_int(value)
        elif title == "رنگ":
            result["color"] = value

    return result


def get_table_data(soup):
    table_rows = soup.find_all("div", {"class": "kt-unexpandable-row"})
    result = {
        "brand_model": "",
        "fuel_type": "",
        "engine_status": "",
        "chassis_status": "",
        "back_chassis": "",
        "front_chassis": "",
        "body_status": "",
        "insurance_remain": "",
        "gear_box_type": "",
        "price": 0,
    }

    for row in table_rows:
        title = row.find("div", {"class": "kt-base-row__start"}).text
        value = row.find("div", {"class": "kt-base-row__end"}).text

        if title == "برند و تیپ":
            result["brand_model"] = value
        elif title == "نوع سوخت":
            result["fuel_type"] = value
        elif title == "وضعیت موتور":
            result["engine_status"] = value
        elif title == "وضعیت شاسی‌ها":
            result["chassis_status"] = value
        elif title == "وضعیت بدنه":
            result["body_status"] = value
        elif title == "مهلت بیمهٔ شخص ثالث":
            result["insurance_remain"] = value
        elif title == "گیربکس":
            result["gear_box_type"] = value
        elif title == "قیمت پایه":
            result["price"] = fa_to_en_int(value)
        elif title == "شاسی عقب":
            result["back_chassis"] = value
        elif title == "شاسی جلو":
            result["front_chassis"] = value

    return result


def get_car_data(driver, url, write_data=False, dataset_path=dataset_path):
    response = get_card_data(driver, url)
    soup = BeautifulSoup(response, "lxml")

    mileage_year_color = get_mileage_year_color(soup)
    table_data = get_table_data(soup)

    result = [
        mileage_year_color["mileage"],
        mileage_year_color["year"],
        mileage_year_color["color"],
        table_data["brand_model"],
        table_data["fuel_type"],
        table_data["engine_status"],
        table_data["chassis_status"],
        table_data["back_chassis"],
        table_data["front_chassis"],
        table_data["body_status"],
        table_data["insurance_remain"],
        table_data["gear_box_type"],
        table_data["price"],
    ]

    return result
