import requests
import datetime
from logger import log

"""
Модуль currency містить клас для роботи з курсами валют.

Класи:
- CurrencyRates: Клас для отримання та конвертації валютних курсів.
"""

class CurrencyRates:
    """
    Клас для роботи з курсами валют.

    Атрибути:
    - rates: Словник з курсами валют.
    - _last_usage: Час останнього оновлення курсів.

    Методи:
    - __init__: Ініціалізує об'єкт та оновлює курси.
    - update_rates: Оновлює курси валют через API.
    - convert: Конвертує суму з однієї валюти в іншу.
    """

    def __init__(self):
        """
        Ініціалізує об'єкт CurrencyRates та оновлює курси валют.
        """
        self.rates = {}
        self.update_rates()
        self._last_usage = datetime.datetime.now()

    def update_rates(self):
        """
        Оновлює курси валют через API ПриватБанку.

        Оновлює дані кожну годину.
        """
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
        """
        Конвертує суму з однієї валюти в іншу.

        Аргументи:
            amount (float): Сума для конвертації.
            from_currency (str): Валюта, з якої конвертуємо.
            to_currency (str): Валюта, в яку конвертуємо.

        Повертає:
            float: Конвертована сума.

        Винятки:
            Exception: Якщо валюта не підтримується.
        """
        if from_currency not in ["UAH", "USD", "EUR"]:
            e = Exception(f"from_currency : {from_currency} - невідоме значення")
            log.exception("Невідома стартова валюта", e)
            raise e
        if to_currency not in ["UAH", "USD", "EUR"]:
            e = Exception(f"to_currency : {to_currency} - невідоме значення")
            log.exception("Невідома стартова валюта", e)
            raise e

        self.update_rates()
        if from_currency == to_currency:
            return amount
        if from_currency != 'UAH':
            amount = amount * self.rates[from_currency]['sale']
        if to_currency != 'UAH':
            amount = amount / self.rates[to_currency]['buy']
        return amount

currate = CurrencyRates()