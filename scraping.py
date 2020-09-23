
#Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd



# set executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)

# define Mars News function
def mars_news(browser):

    # Visit the mars site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #delay for loading
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)



    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        ## (removed for no apparent reason????? slide_elem.find("div", class_='content_title')

        # Use parent element to find the first 'a' tag and save it
        news_title = slide_elem.find("div", class_='content_title').get_text()
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_p

#### Featured Images

def featured_image(browser):
    
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click it
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None

    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
   

    return img_url

def mars_facts():
    
    try:
    df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    
    return df.to_html()

    browser.quit()



