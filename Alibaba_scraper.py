from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import os.path
import json
import time
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_exist_of_element(driver, value, flag=0):
    if flag == 0:
            # print('error')
            return False
    if flag ==2:
        try:
            print("im in third try")
            print(value)
            driver.find_element(By.TAG_NAME, value)
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
   'https://www.alibaba.com/Agriculture_p1?spm=a27aq.cp_1.scGlobalHomeHeader.750.63ef34341ww1sG')

driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(5)
element_agricultures = driver.find_element(By.CSS_SELECTOR,"div.tab-inner-wrapper").find_elements(By.CSS_SELECTOR,"div.hugo-dotelement")
print(element_agricultures,"element_agricultures")
print(len(element_agricultures),"len")
# li_name_agri = []
li_link_agri =[]
for category in element_agricultures:
    time.sleep(2)
    # time.sleep(12)
    # action = ActionChains(driver)
    # action.move_to_element(category).perform()
    # time.sleep(20)
    # try:
    #     action.move_to_element(category).click().perform()
    # except:
    #     print("not find the div")

    # name = category.find_element(By.CSS_SELECTOR, "div.item-title-container").find_element(By.CLASS_NAME,"item-title").text
    # print("name", name)
    link = category.find_element(By.TAG_NAME,"a").get_attribute("href")
    # print("link",link)
    li_link_agri.append(link)
    # li_name_agri.append(name)

if os.path.exists("log.txt"):
    with open("log.txt",'r') as f:
        datas = f.read()
        dic_info = json.loads(datas)
        print(dic_info)
else:
    dic_info = dict()

if dic_info != {}:
    if "category_main" in dic_info.keys():
        index =li_link_agri.index(dic_info['category_main'])
        # li_name_agri = li_name_agri[index+1]
        li_link_agri = li_link_agri[index+1]

for category_link in li_link_agri:
    driver.get(category_link)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)
    link_kind_category=[]
    if check_exist_of_element(driver, "cv-you-are-in__option-childs", flag=1):
        div_kinds_of_category = driver.find_elements(By.CLASS_NAME,"cv-you-are-in__option-childs")[-1]
        if check_exist_of_element(driver, "cv-you-are-in__viewmore", flag=1):
            # span_show_more = div_kinds_of_category.find_element(By.CLASS_NAME,"cv-you-are-in__viewmore")
            # time.sleep(4)
            span_element = WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.CLASS_NAME,"cv-you-are-in__viewmore")))
            span_element.click()
            # span_show_more.click()


        div_kinds_of_category_div = div_kinds_of_category.find_elements(By.TAG_NAME,"div")
        # print(len(div_kinds_of_category_div))
        for div in div_kinds_of_category_div:
            if check_exist_of_element(div, "a", flag=2):
                link = div.find_element(By.TAG_NAME,"a").get_attribute("href")
                link_kind_category.append(link)
            else:
                link_kind_category.append(driver.current_url)
                # print(link,"link")
        else:
           link_kind_category.append(category_link)

        for l in link_kind_category:
            # driver_kind_category = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
            # driver_kind_category.get(l)
            # driver_kind_category.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            driver.get(l)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            if check_exist_of_element(driver, "cv-you-are-in__option-childs", flag=1):
                div_kinds_of_category = driver.find_elements(By.CLASS_NAME, "cv-you-are-in__option-childs")[-1]
                if check_exist_of_element(driver, "cv-you-are-in__viewmore", flag=1):
                    span_show_more = div_kinds_of_category.find_element(By.CLASS_NAME, "cv-you-are-in__viewmore")
                    time.sleep(3)
                    span_show_more.click()
                div_kinds_of_category_div = div_kinds_of_category.find_elements(By.TAG_NAME, "div")
                if len(div_kinds_of_category_div) > 1:
                    # print(len(div_kinds_of_category_div))
                    for div in div_kinds_of_category_div:
                        if check_exist_of_element(div, "a", flag=2):
                            link = div.find_element(By.TAG_NAME, "a").get_attribute("href")
                            link_kind_category.append(link)
                        else:
                            break
                    link_kind_category.pop()
                    continue


        organic_list = driver.find_element(By.CLASS_NAME,"organic-list").find_elements(By.CLASS_NAME,"J-offer-wrapper")
        print(len(organic_list))
        for organic in organic_list:
            try:
                link_organic = organic.find_element(By.CSS_SELECTOR,"h2.elements-title-normal__outter > a").get_attribute('href')
                driver_organic = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
                driver_organic.get(link_organic)
                driver_organic.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                #code romina
                try:
                    product_info = {}
                    product_name = driver_organic.find_element(By.CLASS_NAME, "product-title").text
                    product_info['name'] = product_name
                    print(product_name)

                    price = driver_organic.find_element(By.CLASS_NAME, "price").text
                    # if check_exist_of_element(driver_organic, '//*[@id="container"]/div[1]/div/div[2]/div/div[1]/div[3]/div[5]/div/div/span[2]'):
                    #     unit = driver_organic.find_element(By.XPATH,
                    #                                '//*[@id="container"]/div[1]/div/div[2]/div/div[1]/div[3]/div[5]/div/div/span[2]').text
                    #
                    #     price = price + "/" + unit.split()[1]
                    #     print(unit)
                    # product_info['price'] = price
                    if check_exist_of_element(driver_organic, "unit", 1):
                        unit = driver_organic.find_element(By.CLASS_NAME, "unit").text
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
                    product_info['link'] = driver_organic.current_url

                    essential_details = driver_organic.find_element(By.CLASS_NAME, "do-entry-separate").find_elements(By.TAG_NAME,
                                                                                                              'dl')
                    for item in essential_details:
                        detail_name = item.find_element(By.TAG_NAME, 'dt').text
                        detail_value = item.find_element(By.TAG_NAME, 'dd').text
                        print(detail_name, " ", detail_value)
                        product_info[detail_name] = detail_value

                    Specification = False
                    FAQ = False
                    if check_exist_of_element(driver_organic, "nav-wrapper", 1):
                        bar = driver_organic.find_element(By.CLASS_NAME, "nav-wrapper").find_elements(By.TAG_NAME, 'li')
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
                            table = driver_organic.find_element(By.CLASS_NAME, 'ife-detail-decorate-table').find_elements(
                                By.TAG_NAME, 'tr')
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

                    time.sleep(5)
                    driver_organic.close()
                except:
                    print("every page in product")
            except:
                print("i don't have link")

