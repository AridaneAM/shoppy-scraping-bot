import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def getProductData(product_id):
    url = 'https://shoppy.gg/product/' + product_id
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--no-sandbox')
    chromedriver_path = '/usr/local/bin/chromedriver'
    options.binary_location= '/usr/bin/google-chrome'
    driver = webdriver.Chrome(options=options,  executable_path=chromedriver_path)
    driver.get(url)  
    time.sleep(2)
    html = driver.page_source 
    driver.quit() 
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        stock = int(soup.find('span', {'class' : 'text-muted'}).text)
        title = soup.find('div', {'class' : 'card-header'}).text
        price = soup.find('h5', {'class' : 'user-product__about__price'}).text
        return dict(stock = stock, 
                    title = title, 
                    price = price)
    except:
        return dict(stock= 0, 
                    title = '0', 
                    price= '0')     
