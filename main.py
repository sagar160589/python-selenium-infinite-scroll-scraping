import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

# Define Selenium-Chrome driver configurations
chrome_driver_path = 'E:\Python course\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(service=Service(chrome_driver_path))

# Define URLS for selenium to interact
spreadsheet_url = 'https://docs.google.com/forms/d/e/1FAIpQLScIx6rMy8NewS_s_utg2OuUhIC13yq3IUpZYqQqcuFz2yGIGH/viewform?usp=sf_link'
tnt_market_url = 'https://www.tntsupermarket.com/eng/product-categories/snacks.html'

# Create lists
product_list = []
price_list = []
weight_list = []
product_desc_list = []
cat_list = []
image_list = []


# function to scroll the URL to determine the height
def infinite_scroll(name):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        if name == 'ind':
            time.sleep(4)
        else:
            time.sleep(8)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# Get TNT market url to open through driver
driver.get(tnt_market_url)
time.sleep(1)
infinite_scroll("")
time.sleep(0.2)

# Get the items from the TNT URL
item_list = driver.find_elements('class name', 'item-root-ADb')
for item in item_list:
    product_list.append(item.find_element('css selector', '.item-name--yq').text)
    hrefs = item.find_element('css selector', '.item-name--yq')
    image_list.append(hrefs.get_attribute('href'))
driver.close()
print(len(image_list))
prod_dict = {}
driver = webdriver.Chrome(service=Service(chrome_driver_path))

#Loop through the image urls and get details like the size, title, brand, price of the product
for image in image_list:
    print(image)
    driver.get(image)
    time.sleep(1)
    infinite_scroll('ind')
    try:
        title = driver.find_element('class name', 'productFullDetail-productName-6ZL')
        weight = driver.find_element('css selector', ".productFullDetail-optionsSize--RL button")
        brand = driver.find_element('xpath', '//*[@id="details"]/div[2]/div[1]/span[2]')
        price_list = driver.find_element('class name', 'productFullDetail-productPrice-Aod').find_elements('tag name',
                                                                                                           'span')
    except NoSuchElementException:
        print('Key not found')
        continue

    prod_dict[image_list.index(image)] = {
        'title': title.text,
        'price': f"{price_list[0].text}{price_list[1].text}{price_list[2].text}{price_list[3].text}",
        'weight': weight.text,
        'brand': brand.text,
        'image_url': image,
    }

# Fill up google spreadsheet with the data collected above
for i in prod_dict:
    driver.get(spreadsheet_url)
    prod_title = driver.find_element('xpath',
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    prod_price = driver.find_element('xpath',
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    prod_weight = driver.find_element('xpath',
                                      '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    prod_brand = driver.find_element('xpath',
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
    prod_image = driver.find_element('xpath',
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input')
    prod_submit = driver.find_element('xpath',
                                      '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    prod_title.send_keys(prod_dict[i]['title'])
    prod_price.send_keys(prod_dict[i]['price'])
    prod_weight.send_keys(prod_dict[i]['weight'])
    prod_brand.send_keys(prod_dict[i]['brand'])
    prod_image.send_keys(prod_dict[i]['image_url'])
    prod_submit.click()
