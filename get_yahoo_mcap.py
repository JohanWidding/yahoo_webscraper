import random
import time, json
from tqdm import tqdm
import undetected_chromedriver as uc
from bs4 import BeautifulSoup as bs

def get_content():
    FILENAME_TICKERS = 'tickerlist.txt'
    with open(FILENAME_TICKERS) as file:
        stock_tickers = json.load(file)["dict"]
    urlLilst = {}
    for ticker, stockName in stock_tickers.items():
        url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}"
        urlLilst[ticker] = url

    options = uc.ChromeOptions()
    driver = uc.Chrome(use_subprocess=True, options=options)
    driver.get(urlLilst["JOBY"])
    time.sleep(15)

    companies = {}
    for name, url in tqdm(urlLilst.items()):
        try:
            driver.get(url)
            time.sleep(3)
            req = driver.page_source
            soup = bs(req, 'html.parser').find_all("tbody")[1]
            marketCap = soup.find('td', {"data-test":"MARKET_CAP-value"}).text
            beta = soup.find('td', {"data-test":"BETA_5Y-value"}).text
            PE_2023 = soup.find('td', {"data-test":"PE_RATIO-value"}).text
            stock_info = {
                "market_cap": marketCap,
                "yahoo_beta": beta,
                "PE_2023": PE_2023,
            }
            companies[name] = stock_info
            time.sleep(random.randint(2,7))
            break
        except:
            time.sleep(random.randint(2,7))

    driver.close()


    print('Found', len(companies), 'investment funds')

    with open('mcaps.txt', 'w') as convert_file:
        convert_file.write(json.dumps(companies))
