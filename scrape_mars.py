# Used jupyter nbconvert --to script mission_to_mars.ipynb to convert to 
# python script
# coding: utf-8

# In[2]:


# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd


# In[3]:


# Create BeautifulSoup object; parse with 'html.parser'
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')


# In[3]:


soup.body


# In[4]:


news_title = soup.body.find('div', class_ = 'content_title').text
print(news_title)


# In[5]:


news_p = soup.body.find(class_ = 'rollover_description_inner').text
print(news_p)


# In[6]:


soup.body.find('div', class_ = 'content_title' ).find('a')['href']


# In[7]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(image_url)


# In[8]:


# HTML object
html = browser.html
# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

#browser.click_link_by_partial_text('FULL IMAGE')

# Retrieve all elements that contain book information
featured_image_url = soup.body.find('footer').find('a')['data-fancybox-href']


# In[9]:


featured_image_url = featured_image_url.replace('medium', 'large').replace('ip','hires')
base_nasa_url = 'https://www.jpl.nasa.gov'
print(base_nasa_url + featured_image_url)


# In[10]:


twt_l = []


# In[20]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
twitter_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(twitter_url)

for x in range(5):
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    #browser.click_link_by_partial_text('FULL IMAGE')
    # Retrieve all elements that contain book information
    mars_tweets = soup.body.find('p', class_ = 'TweetTextSize')
    
    for mars_tweets_items in mars_tweets:
        twt_l.append(mars_tweets_items)


# In[23]:





# In[24]:


for tweets in range(len(twt_l)):
    if 'InSight' in twt_l[tweets]:
        mars_weather = twt_l[tweets]
        break



# In[25]:


print(mars_weather)


# In[26]:


mars_table_df = pd.read_html('https://space-facts.com/mars/')[0]


# In[30]:


mars_table_dict = mars_table_df.to_dict()


# In[32]:


mars_table_html = mars_table_df.to_html(justify = 'left')


# In[39]:


hemi_ls = ['Cerberus Hemisphere Enhanced', 'Schiaparelli Hemisphere Enhanced', 'Syrtis Major Hemisphere Enhanced', 'Valles Marineris Hemisphere Enhanced']
hemi_dict = {}
hemi_all_ls = []


# In[40]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(mars_hemi_url)

for hemisphere in hemi_ls:
    hemi_dict = {}
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    
    browser.click_link_by_partial_text(hemisphere)
    current_url = browser.url
    
    response = requests.get(current_url)
    soups = BeautifulSoup(response.text, 'lxml')
    # Retrieve all elements that contain book information
    
    hemi_dict['title'] = soups.body.find('h2', class_ = 'title').text.replace(' Enhanced',"")
    hemi_dict['img_url'] = soups.body.find('div', class_ = 'downloads').find('li').find('a')['href']
    
    
    hemi_all_ls.append(hemi_dict)
    print(current_url)
    browser.click_link_by_partial_text('Back')


# In[41]:


print(hemi_dict)
print(hemi_all_ls)


# In[42]:


hemi_dict
hemi_all_ls


# In[217]:


soup.body.find('div', class_ = 'downloads').find('li').find('a')['href']
soup.body.find('h2', class_ = 'title').text

