import datetime
from user import User
from logger import log
from currency import currate


class Cheking_account:
    __id = 1
    _suported_currency = ["UAH", "USD", "EUR"]

    def __init__(self, user : User, currency : str= "UAH") -> None:
        if currency not in self._suported_currency:
            e = ValueError(f"Значення {currency}, для валют не припустиме")
            log.exception("Некоректна валюта для рахунку", e)
            raise e

        if not isinstance(user, User):
            log.exception(f"Неіснуючий користувач : {user}", TypeError())
            raise TypeError("Неіснуючий користувач")

        self._account_id = Cheking_account.change_id()
        self._currency = currency
        self._balance = 0
        self._owner = user
        self._blocked = False
        log.info(f"Рахунок з id = {self._account_id}, користувача {user}, було успішно створено!")

    @classmethod
    def change_id(cls):
        cls.__id += 1
        return cls.__id - 1

    def deposit(self, suma : (int, float), currency : str = "UAH"):
        if currency not in self._suported_currency:
            e = ValueError(f"Значення {currency}, для валют не припустиме")
            log.exception("Некоректна валюта для рахунку", e)
            raise e

        if not isinstance(suma, (float, int)) or suma <= 0.05:
            e = Exception(f"Сума дезиту не може приймати знчення: {suma}, мінімальне значення депозиту: {suma} {currency}")
            log.exception("Помилка суми депозиту", e)
            raise e

        realsum = currate.convert(suma, currency, self._currency)
        self._balance += realsum

    def withdraw(self, suma : (int, float), currency : str = "UAH"):
        if currency not in self._suported_currency:
            e = ValueError(f"Значення {currency}, для валют не припустиме")
            log.exception("Некоректна валюта для рахунку", e)
            raise e

        if not isinstance(suma, (float, int)) or suma <= 0:
            e = Exception(f"Сума дезиту не може приймати знчення: {sum}")
            log.exception("Помилка суми депозиту", e)
            raise e


        realsum = currate.convert(suma, currency, self._currency)

        if self._balance < realsum:
            e = Exception("На рахунку недостатньо коштів")
            log.exception(f"На рахунку {self._account_id}, недостатньо коштів", e)
            raise e

        self._balance -= realsum

    def block_account(self):
        self._blocked = True

    def unblock_account(self):
        self._blocked = False

class Savings_account(Cheking_account):

    def __init__(self, user: User, period : int, percent : float, currency : str= "UAH") -> None:

        if not isinstance(period, int) or not isinstance(percent, float) or percent < 0 or percent > 100:
            log.exception("Не вірні типи данних в атрибутах period, percent", TypeError())
            raise TypeError("Не вірні типи данних в атрибутах period, percent")

        super().__init__(user, currency)
        self.__last_interest_date = datetime.date.today()
        self.__period = period
        self.__percent = percent

    def calculate_interest(self):
        today = datetime.date.today()
        months_passed = (today.year - self.__last_interest_date.year) * 12 + (
                    today.month - self.__last_interest_date.month)

        if today.day < self.__last_interest_date.day:
            months_passed -= 1

        full_periods = months_passed // self.__period

        if full_periods >= 1:
            initial_balance = self._balance
            for _ in range(full_periods):
                self._balance += self._balance * self.__percent

            self.__last_interest_date = today

            return self._balance - initial_balance
        else:
            return 0.0


class Credit_account(Savings_account):

    def __init__(self, limit : (float, int), user : User, period : int, percent : float, currency : str= "UAH") -> None:

        if not isinstance(limit, float) or limit <= 0:
            log.exception("Не вірні типи данних в атрибутi limit", TypeError())
            raise TypeError("Не вірні типи данних в атрибутi limit")

        super().__init__(user, period, percent, currency)
        self._currency = currency
        self._balance = limit
        self._limit = limit
        self._credit = 0

    def calculate_interest(self):
        if self._balance == 0:
            return 0.0

        today = datetime.date.today()
        months_passed = (today.year - self.__last_interest_date.year) * 12 + (
                    today.month - self.__last_interest_date.month)

        if today.day < self.__last_interest_date.day:
            months_passed -= 1

        full_periods = months_passed // self.__period

        if full_periods >= 1:
            initial_balance = self._limit - self._balance
            for _ in range(full_periods):
                initial_balance += initial_balance * self.__percent

            self.__last_interest_date = today
            return initial_balance
        else:
            return 0.0

    def withdraw(self, suma: float, currency: str = "UAH"):
        if not isinstance(suma, (float, int)) or suma <= 0:
            e = Exception(f"Сума дезиту не може приймати знчення: {suma}")
            log.exception("Помилка суми депозиту", e)
            raise e

        if currency not in self._suported_currency:
            e = TypeError(f"Значення {currency}, для валют не припустиме")
            log.exception("Некоректна валюта для рахунку", e)
            raise e

        realsum = currate.convert(suma, currency, self._currency)

        if self._balance - realsum < 0:
            e = ValueError("Операція відмінена через перевищення кредитного ліміту")
            log.exception(f"На рахунку {self._account_id}, перевищення кредитного ліміту, операція відмінена", e)
            raise e
        else:
            self._balance - realsum