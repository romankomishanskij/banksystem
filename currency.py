import requests
import datetime

class CurrencyRates:

    def __init__(self):
        self.rates = {}
        self.update_rates()
        self._last_usage = datetime.datetime.now()

    def update_rates(self):
        now = datetime.datetime.now()
        if now - self._last_usage > datetime.timedelta(hours=1):
            url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
            response = requests.get(url)
            data = response.json()
            for item in data:
                self.rates[item['ccy']] = {
                    'buy': float(item['buy']),
                    'sale': float(item['sale'])
                }

    def convert(self, amount, from_currency, to_currency):
        self.update_rates()
        if from_currency == to_currency:
            return amount
        if from_currency != 'UAH':
            amount = amount * self.rates[from_currency]['sale']
        if to_currency != 'UAH':
            amount = amount / self.rates[to_currency]['buy']
        return amount

currate = CurrencyRates()
