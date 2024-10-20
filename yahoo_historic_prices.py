import random
import requests, csv, json
import pandas as pd
from tqdm import tqdm
import time
from bs4 import BeautifulSoup as bs

def proxy_list():
    url = "https://github.com/clarketm/proxy-list/blob/master/proxy-list.txt"
    user_agents = "https://gist.github.com/pzb/b4b6f57144aea7827ae4"
    list = []
    list2 = []

    response = requests.get(url)
    soup = bs(response.text, 'html.parser').find("table").find_all("tr")
    for line in soup:
        text = line.find_all("td")[1].text
        if text[0].isnumeric():
            list.append(text.split(":")[0])

    response = requests.get(user_agents)
    soup = bs(response.text, 'html.parser').find("table").find_all("tr")
    for line in soup:
        text = line.find_all("td")[1].text
        list2.append(text)

    _list = []
    for proxy in list:
        for user in list2:
            _dict = {"header": {"User-Agent": user}, "proxie": {'http': f"http://{proxy}"}}
            _list.append(_dict)
    random.shuffle(_list)

    print("We have", len(_list), "unique combinations")

    return _list



def downloadHistoricStockPrices():
    proxyList = proxy_list()


    FILENAME_TICKERS = 'timeout.txt'
    with open(FILENAME_TICKERS) as file:
        ticker_list = json.load(file)["list"]

    CSV_URL = ["https://query1.finance.yahoo.com/v7/finance/download/","?period1=345427200&period2=1673943183&interval=1d&events=history&includeAdjustedClose=true"]

    _dict = {}
    _dict_timeout = {"list": []}

    with requests.Session() as s:
        for ticker in tqdm(ticker_list):
            try:
                computer = random.choice(proxyList)
                user_agent = computer["header"]
                proxy = computer["proxie"]
                download = s.get(CSV_URL[0]+ticker+CSV_URL[1], headers=user_agent, proxies=proxy, timeout=60)

                decoded_content = download.content.decode('utf-8')

                cr = csv.reader(decoded_content.splitlines(), delimiter=',')
                csv_list = list(cr)
                header = csv_list[0]
                data = [csv_list[i] for i in range(1, len(csv_list))]
                df = pd.DataFrame(data, columns=header)

                stock_dict = df.to_dict()

                _dict[ticker] = stock_dict



            except:
                _dict_timeout["list"].append(ticker)
                print("Kunne ikke finne data for "+ticker)


    with open('stocks_timeout.txt', 'w') as convert_file:
        convert_file.write(json.dumps(_dict))
    with open('timeout.txt', 'w') as convert_file:
        convert_file.write(json.dumps(_dict_timeout))