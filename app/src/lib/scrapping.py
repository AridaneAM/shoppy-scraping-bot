import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

def getProductData(product_id):
    url = 'https://shoppy.gg/product/' + product_id
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path='./lib/geckodriver')
    driver.get(url)  
    time.sleep(3)
    html = driver.page_source 
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
# def checkID(product_id):
#     url = 'https://shoppy.gg/product/' + product_id

#     options = Options()
#     options.headless = True
#     driver = webdriver.Firefox(options=options, executable_path='./lib/geckodriver')
#     driver.get(url)  
#     html = driver.page_source 
#     soup = BeautifulSoup(html, 'html.parser')

#     if soup.find('div', {'id' : 'user-product'}):
#         return 0
#     else:
#         return -1


#pip3 install bs4 selenium
#https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25
#https://chromedriver.storage.googleapis.com/index.html?path=88.0.4324.96/
#https://www.geeksforgeeks.org/scrape-content-from-dynamic-websites/
#https://shoppy.gg/product/nXQ5JMN

#1560578141:AAHxpwm7uK0bwaicch4y-HNUD7ddWGtHzRE


# URL = 'https://shoppy.gg/product/nXQ5JMN'
# URL = 'https://shoppy.gg/product/8kWGc1V'
