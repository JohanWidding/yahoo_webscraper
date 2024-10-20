import time
import undetected_chromedriver as uc
from selenium import webdriver
from yahoo_historic_prices import proxy_list as px

def seleniumGoogleTrend():
    chromedriver = "chromedriver.exe"
    proxy_dict = px()
    proxy = proxy_dict[0]["proxie"]
    user_agent = proxy_dict[0]["header"]

    browser = webdriver.Chrome(chromedriver)
    url = "https://trends.google.com/trends/explore?date=2018-01-01%202023-03-07&geo=US&q=TSLA"

    browser.get(url)

    time.sleep(500)

def seleniumUndetectedGoogleTrend():
    options = uc.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(use_subprocess=True, options=options)
    url = "https://trends.google.com/trends/explore?date=2018-01-01%202023-03-07&geo=US&q=TSLA"
    driver.get(url)
    time.sleep(20)
    driver.close()