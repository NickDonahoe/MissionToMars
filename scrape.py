# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    
    browser = init_browser()

    python_dict = {}

    #1

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    news_title = soup.body.find('div', class_ = 'content_title').text
    news_p = soup.body.find(class_ = 'rollover_description_inner').text
    
    python_dict['news_title'] = news_title
    python_dict['news_description'] = news_p

    #2

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve all elements that contain book information
    featured_image_url = soup.body.find('footer').find('a')['data-fancybox-href']

    featured_image_url = featured_image_url.replace('medium', 'large').replace('ip','hires')
    base_nasa_url = 'https://www.jpl.nasa.gov'
    
    python_dict['featured_image_url'] = base_nasa_url + featured_image_url
    
    #3

    twt_l = []

    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)

    for x in range(5):
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')
        #browser.click_link_by_partial_text('FULL IMAGE')
        # Retrieve all elements that contain book information
        mars_tweets = soup.body.find('p', class_ = 'TweetTextSize')
        x += 1
    
    for mars_tweets_items in mars_tweets:
        twt_l.append(mars_tweets_items)
    
    for tweets in range(len(twt_l)):
        if 'InSight' in twt_l[tweets]:
            mars_weather = twt_l[tweets]
            break
    
    python_dict['weather'] = mars_weather

    #4

    mars_table_df = pd.read_html('https://space-facts.com/mars/')[0]
    mars_table_one = mars_table_df[0].values.tolist()
    mars_table_two = mars_table_df[1].values.tolist()

#    python_dict['info'] = mars_table_one    
#    python_dict['data'] = mars_table_two

    python_dict['wow'] = "wow"

    return python_dict