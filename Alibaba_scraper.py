import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.common.exceptions import NoSuchElementException


def check_exist_of_element(driver, value, flag=0):
    if flag == 0:
        try:
            print("im in try")
            driver.find_element(By.XPATH, value)
            # print('test')
        except NoSuchElementException:
            print("im in except")
            # print('error')
            return False
        return True
    if flag == 1:
        try:
            print("im in second try")
            print(value)
            driver.find_element(By.CLASS_NAME, value)
            # print('test')
        except NoSuchElementException:
            print("im in except")
            # print('error')
            return False
        return True


option = Options()
option.add_argument('--incognito')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
driver.get(
    "https://www.alibaba.com/product-detail/Fresh-Cut-Durian-Fruits-for-from_1600199291844.html?spm=a2700"
    ".galleryofferlist.normal_offer.d_image.4bed77741z5WJ4")
# driver.get("https://www.alibaba.com/product-detail/Wholesale-Chicken-Table-Eggs-Price-Animal_11000005112612.html?spm"
#            "=a2700.galleryofferlist.normal_offer.d_image.ec3f5c3bVlEGCv")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

product_info = {}
product_name = driver.find_element(By.CLASS_NAME, "product-title").text
product_info['name'] = product_name
print(product_name)

price = driver.find_element(By.CLASS_NAME, "price").text
# if check_exist_of_element(driver, '//*[@id="container"]/div[1]/div/div[2]/div/div[1]/div[3]/div[5]/div/div/span[2]'):
#     unit = driver.find_element(By.XPATH,
#                                '//*[@id="container"]/div[1]/div/div[2]/div/div[1]/div[3]/div[5]/div/div/span[2]').text
#
#     price = price + "/" + unit.split()[1]
#     print(unit)
# product_info['price'] = price
if check_exist_of_element(driver, "unit", 1):
    unit = driver.find_element(By.CLASS_NAME, "unit").text
    unit1 = unit.split()
    print(unit1)
    if unit1[-1] == '|':
        unit = ' '.join(unit1[:-1])
        print(unit)
    else:
        unit = unit.split()[-1]
        print(unit)
    price = price + "/" + unit


print(price)
product_info['link'] = driver.current_url

essential_details = driver.find_element(By.CLASS_NAME, "do-entry-separate").find_elements(By.TAG_NAME, 'dl')
for item in essential_details:
    detail_name = item.find_element(By.TAG_NAME, 'dt').text
    detail_value = item.find_element(By.TAG_NAME, 'dd').text
    print(detail_name, " ", detail_value)
    product_info[detail_name] = detail_value

Specification = False
FAQ = False
if check_exist_of_element(driver, "nav-wrapper", 1):
    bar = driver.find_element(By.CLASS_NAME, "nav-wrapper").find_elements(By.TAG_NAME, 'li')
    print("bar item:")
    for item in bar:
        print(item.text)
        if item.text == 'Specification':
            Specification = True
        if item.text == 'FAQ':
            FAQ = True
    print("-" * 10)
    previous_item = ''
    if Specification:
        print("im in specification")
        table = driver.find_element(By.CLASS_NAME, 'ife-detail-decorate-table').find_elements(By.TAG_NAME, 'tr')
        for i in range(1, len(table)):
            item, value = table[i].find_elements(By.TAG_NAME, 'td')
            item = item.text
            value = value.text
            print(item, " ", value)
            if item == "" and value != "":
                product_info[previous_item] = product_info[previous_item] + "," + value
            else:
                product_info[item] = value
            if item == "" and value == "":
                continue
            previous_item = item

    if FAQ:
        print("im in faq")
        if check_exist_of_element(driver, "detail-decorate-json-renderer-container", 1):
            faqs = driver.find_elements(By.CLASS_NAME, "detail-decorate-json-renderer-container")
            faqs = faqs[-1].text
            product_info['FAQs'] = faqs
            print(faqs)

data = pd.DataFrame([product_info])
print("i make dataframe")
data.to_excel(f'{product_name}.xlsx', index=False)