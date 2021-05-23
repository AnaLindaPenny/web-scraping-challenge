#Imports
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import os
import pandas as pd
import pymongo
import warnings
warnings.filterwarnings('ignore)
from webdriver_manager.chrome import ChromeDriverManager


#Chromedriver Setup
def init_browser():
    #Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/Users/AnaLindaPenny/.wdm/drivers/chromedriver/mac64/90.0.4430.24/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)

def scrape():

    browser = init_browser()
    

    #define urls
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    table_url = "https://space-facts.com/mars/"
    images_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(news_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    #recent = None

    

    recent = soup.find('li', class_='slide')

    mars_info = {}

    if recent is None:
        mars_info = {
            'n_Title': "Cannot find anything",
            'n_Summary': "Uh oh."
        }
    else:
        news_title = recent.h3.text

        news_p = recent.find('div', class_='rollover_description_inner').text

        mars_info = {
            "n_Title": news_title,
            'n_Summary': news_p
        }

#Images
    browser.visit(images_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    pic_titles = []
    photo_info = {}
    results = soup.find_all('div', class_='item')

    for result in results:
        title = result.find("h3").text
        pic_titles.append(title)


    mars_info["images"] = {}
    for title in pic_titles:

        browser.links.find_by_partial_text(title).click()
        next_html = browser.html
        next_soup = bs(next_html, 'html.parser')
        pic = next_soup.find_all('div', class_='downloads')[0].li.a['href']
        half = next_soup.find('h2', class_='title').text
        photo_info.update({half: pic})
        browser.visit(images_url)

        mars_info["images"].update({
            title:photo_info[title]
        })

    # browser.quit()

#Fact Table

    tables = pd.read_html(table_url)
    df = tables[0]
    df=df.rename(columns={0:'',1:'Mars'})
    table = df.to_html(index=False,classes='table table-striped', justify='left')  
    
    mars_info.update({
       "mars_table":table
        })

    return mars_info