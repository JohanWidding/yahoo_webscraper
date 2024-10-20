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
        url = f"https://finance.yahoo.com/quote/{ticker}/profile?p={ticker}"
        urlLilst[ticker] = url

    options = uc.ChromeOptions()
    driver = uc.Chrome(use_subprocess=True, options=options)
    driver.get(urlLilst["JOBY"])
    time.sleep(25)


    companies = {}
    for name, url in tqdm(urlLilst.items()):
        try:
            driver.get(url)
            time.sleep(random.randint(3,7))
            req = driver.page_source
            soup = bs(req, 'html.parser')
            profile = [span.text for span in soup.find('div', {"data-test": "asset-profile"}).find_all('span')]
            sector = profile[1]
            industry = profile[3]
            workers = profile[5]
            stock_info = {
                "sector": sector,
                "industry": industry,
                "full_time_employees": workers
            }
            companies[name] = stock_info

        except:
            pass

    driver.close()


    print('Found', len(companies), 'investment funds')

    with open('sectors.txt', 'w') as convert_file:
        convert_file.write(json.dumps(companies))
