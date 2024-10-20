"""
Ett objekt i json filen ser typisk slik ut:
{
    'symbol': 'AAPL',
    'name': 'Apple Inc. Common Stock',
    'lastsale': '$134.76',
    'netchange': '1.35',
    'pctchange': '1.012%',
    'volume': '57809719',
    'marketCap': '2336379938400.00',
    'country': 'United States',
    'ipoyear': '1980',
    'industry': 'Computer Manufacturing',
    'sector': 'Technology',
    'url': '/market-activity/stocks/aapl'
}
"""

def getTickerSymbols():
    import requests

    LIMIT = 8000
    URL = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit="+str(LIMIT)+"&offset=0&download=true"
    HEADER = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

    response_json = requests.get(URL, headers=HEADER).json()["data"]["rows"]

    list_of_tickers = []
    for stock in response_json:

        if stock["ipoyear"] == "": continue
        elif stock["marketCap"] == "": continue
        elif float(stock["marketCap"]) == 0: continue
        elif stock["country"] != "United States": continue
        elif int(stock["volume"]) < 50: continue
        else:
            list_of_tickers.append(stock["symbol"])

    return list_of_tickers
