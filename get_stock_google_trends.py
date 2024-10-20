

def GetStockGoogleTrends():
    from tqdm import tqdm
    from pytrends.request import TrendReq
    import time, json

    pytrends = TrendReq(hl='en-US')

    ticker_list = []
    with open('tickerlist.txt') as file:
        ticker_list = json.load(file)['list']

    _dict = {}
    for ticker in tqdm(ticker_list):
        date_list = []
        trend_index_list = []

        try:
            pytrends.build_payload([ticker], cat=0, timeframe='today 5-y', geo='US', gprop='')

            df = pytrends.interest_over_time()

            the_dict = df.to_dict()
            for k,v in the_dict.items():
                if k == ticker:
                    for date, value in v.items():
                        string_date = date.strftime("%Y-%m-%d")
                        date_list.append(string_date)
                        trend_index_list.append(value)
            code200 = True

        except:
            time.sleep(15)

        data = [list(a) for a in zip(date_list,trend_index_list)]
        _dict[ticker] = data

    with open('google_index.txt', 'w') as convert_file:
        convert_file.write(json.dumps(_dict))
