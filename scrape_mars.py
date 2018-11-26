from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    #NASA news title and paragraph text
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser') 
    news_title = soup.find('div', class_='content_title').text.strip()
    news_p = soup.find('div', class_='rollover_description_inner').text.strip()

    #JPL Mars featured image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    rel_path = soup.find('a', class_='button fancybox')['data-fancybox-href']
    featured_img = 'https://www.jpl.nasa.gov' + rel_path

    #Mars weather (twitter)
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup.find('p', class_='TweetTextSize').text

    #Mars facts
    url = 'https://space-facts.com/mars/'
    table = pd.read_html(url)
    mars_df = table[0]
    mars_df.columns = ['description','value']
    mars_df.set_index('description', inplace=True)
    html_table = mars_df.to_html()
    mars_html_table = html_table.replace('\n', '')

    #Mars Hemispheres
    hemi_list = []

    def get_image():
        html = browser.html
        soup = bs(html, 'html.parser')
        dl = soup.find('div', class_='downloads')
        link = dl.find('a')
        img_url = link['href']
        title = soup.find('h2', class_='title').text
        d = {'title': title, 'img_url': img_url}
        hemi_list.append(d)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)
    browser.click_link_by_partial_text('Cerberus')
    get_image()

    browser.visit(url)
    browser.click_link_by_partial_text('Schiaparelli')
    get_image()

    browser.visit(url)
    browser.click_link_by_partial_text('Syrtis')
    get_image()

    browser.visit(url)
    browser.click_link_by_partial_text('Valles')
    get_image()

    
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_img": featured_img,
        "mars_weather": mars_weather,
        "mars_html_table": mars_html_table,
        "hemi_list": hemi_list
    }
    
    browser.quit()

    return mars_data

