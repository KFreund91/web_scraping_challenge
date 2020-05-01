#Import Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests


def init_browser():
    executable_path = {"executable_path": "./chromedriver.exe"}
    browser = Browser("chrome", **executable_path)

def scrape():
    # NASA Mars News
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    article = news_soup.find('li', class_ = 'slide')
    news_title = news_soup.find("div",class_="list_text").find("a").text
    print(news_title)
    news_p = news_soup.find("div", class_="article_teaser_body").text
    print(news_p)
    browser.quit()


    #space image
    browser = init_browser()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    image_soup.find("article", class_="carousel_item")
    image_soup.find("a", class_="button fancybox")
    img_url = "https://www.jpl.nasa.gov" + image_soup.find("a", class_="button fancybox")["data-fancybox-href"]
    print (img_url)
    browser.quit()

    #Mars facts
    browser = init_browser()
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    html = browser.html
    fact_soup = BeautifulSoup(html, 'html.parser')
    mars_facts = fact_soup.find("tbody").text
    mars_facts
    mars_df = pd.read_html(url)[0]
    mars_df
    mars_df.columns=["Description", "Value"]
    mars_df.set_index("Description", inplace=True)
    mars_df
    browser.quit()


    # Mars Hemispheres
    browser = init_browser()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    hemi_soup = BeautifulSoup(html, 'html.parser')
    hemisphere_image_urls = []
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[item].click()
        sample_element = browser.links.find_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        hemisphere["title"] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    hemisphere_image_urls
    browser.quit()

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "img_url": img_url,
        "table": mars_df,
        "hemisphere_image_urls" :hemisphere_image_urls
              }
    # Return results
    return mars_data

