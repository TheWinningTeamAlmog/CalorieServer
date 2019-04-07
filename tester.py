from selenium import webdriver
from bs4 import BeautifulSoup

googleURL = "https://www.instagram.com/or.a.94/p/BuL2h1aHbKq"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)

browser.get(googleURL)
content = browser.page_source

soup = BeautifulSoup(content)
with open("./out", "w") as out:
    out.write(soup)