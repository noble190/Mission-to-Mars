#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[2]:


# Path to chromedriver
#!which chromedriver


# In[111]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

# In[112]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[113]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[114]:


slide_elem.find("div", class_='content_title')


# In[115]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[116]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[117]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[118]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[119]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[120]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[121]:


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[122]:


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

# In[123]:


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# In[124]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[125]:


df.to_html()


# ### Mars Weather

# In[126]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[127]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[128]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[131]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[132]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

#use splinter to find all hemisphere description links
hemi_items = browser.find_by_id('product-section').first.find_by_css('.item')

hemi_links = [hemi_item.find_by_tag('a').first['href'] for hemi_item in hemi_items]

#loop through extracted links
for hemi_link in hemi_links:
    
    #navigate to link page
    browser.visit(hemi_link)
    
    #capture page html
    html = browser.html
    hemi_page_soup = soup(html, 'html.parser')
    
    #find image url (jpg format) and title
    img_url = hemi_page_soup.select_one('div.downloads').select_one('a', href=True, text='Sample')['href']
    title = hemi_page_soup.select_one('h2.title').getText()

    #save to list
    hemisphere_image_urls.append({'img_url': img_url, 'title': title})
    


# In[133]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[134]:


# 5. Quit the browser
browser.quit()


# In[ ]:




