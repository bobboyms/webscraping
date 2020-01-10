import requests
from datetime import datetime

def str_to_float(value):
    if value == None or value == "null":
        return 0

    return float(value)

def str_to_int(value):
    if value == None or value == "null":
        return 0

    return int(value)

class FinancesYahoo(object):

    headers = {
        'authority': 'query1.finance.yahoo.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'sec-fetch-user': '?1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'navigate',
        # 'referer': 'https://br.financas.yahoo.com/quote/ABEV3.SA/history?period1=1547000984&period2=1578536984&interval=1d&filter=history&frequency=1d',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'PRF=t%3DAAPL; A1=d=AQABBDzzEV4CENOlXKn-eHLc1Pq_7sTrV68FEgEBAQE5E179Xh4Ab2UB_SMAAAYsQVFFQkFRRmVFemxlX1VJWi1BUEYmcz1BUUFBQUFoc3c2YnYmZz1YaEh6ZUEHCAFgRF03pNyB&S=AQAAAt5E_ycSSXIHvjPrZ0PNz8o; A3=d=AQABBDzzEV4CENOlXKn-eHLc1Pq_7sTrV68FEgEBAQE5E179Xh4Ab2UB_SMAAAYsQVFFQkFRRmVFemxlX1VJWi1BUEYmcz1BUUFBQUFoc3c2YnYmZz1YaEh6ZUEHCAFgRF03pNyB&S=AQAAAt5E_ycSSXIHvjPrZ0PNz8o; A1S=d=AQABBDzzEV4CENOlXKn-eHLc1Pq_7sTrV68FEgEBAQE5E179Xh4Ab2UB_SMAAAYsQVFFQkFRRmVFemxlX1VJWi1BUEYmcz1BUUFBQUFoc3c2YnYmZz1YaEh6ZUEHCAFgRF03pNyB&S=AQAAAt5E_ycSSXIHvjPrZ0PNz8o; GUC=AQEBAQFeEzle_UIZ-APF; APID=UPa8d179aa-b542-11e9-ab25-02e6399becda; APIDTS=1578536984; B=83n546tek8o01&b=3&s=o7',
    }

    def __init__(self,code, local='BR'):
        self.code = code
        self.local = local

    def __get_params(self, period1, period2):

        p1 = str(datetime.strptime(period1, "%m/%d/%Y").timestamp()).replace(".0","")
        p2 = str(datetime.strptime(period2, "%m/%d/%Y").timestamp()).replace(".0","")

        return (
                    ('period1', p1),
                    ('period2', p2),
                    ('interval', '1d'),
                    ('events', 'history'),
                    ('crumb', 'ggRTCuiqC1f'),
                )

    def get_data(self, period1, period2):

        params = self.__get_params(period1,period2)

        url = ('https://query1.finance.yahoo.com/v7/finance/download/%s.SA' % self.code)

        response = requests.get(url, headers=self.headers, params=params)

        lista = str(response.content).split("\\n")
        tempList = []

        for forex in lista[1:]:

            papel = forex.split(",")

            if len(papel) == 1:
                continue

            data = {
                'dateobj':datetime.strptime(papel[0], "%Y-%m-%d"),
                'date': papel[0],
                'open': str_to_float(papel[1]),
                'high': str_to_float(papel[2]),
                'low': str_to_float(papel[3]),
                'close': str_to_float(papel[4]),
                'adjclose': str_to_float(papel[5]),
                'volume': str_to_int(papel[6])
            }

            tempList.append(data)

        return tempList
