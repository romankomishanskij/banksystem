import datetime
from user import User
from logger import Logger
from currency import currate

log = Logger()

class Cheking_account:
    __id = 1
    suported_currency = ["UAH", "USD", "EUR"]

    def __init__(self, user : User, currency : str= "UAH") -> None:
        if currency not in self.suported_currency:
            e = TypeError(f"Значення {currency}, для валют не припустиме")
            log.exception("Некоректна валюта для рахунку", e)
            raise e

        if not isinstance(user, User):
            log.exception(f"Неіснуючий користувач : {user}", TypeError())
            raise TypeError("Неіснуючий користувач")

        self._account_id = Cheking_account.change_id()
        self._currency = currency
        self._balance = 0
        self.__owner = user
        self._blocked = False
        log.info(f"Рахунок з id = {self._account_id}, користувача {user}, було успішно створено!")

    @classmethod
    def change_id(cls):
        cls.__id += 1
        return cls.__id - 1

    def deposit(self, suma, currency : str = "UAH"):
        if not isinstance(suma, (float, int)) or suma <= 0:
            e = Exception(f"Сума дезиту не може приймати знчення: {sum}")
            log.exception("Помилка суми депозиту", e)
            raise e

        if currency not in self.suported_currency:
            e = TypeError(f"Значення {currency}, для валют не припустиме")
            log.exception("Некоректна валюта для рахунку", e)
            raise e

        realsum = currate.convert(suma, currency, self._currency)
        self._balance += realsum

    def withdraw(self, suma : float, currency : str = "UAH"):
        if not isinstance(suma, (float, int)) or suma <= 0:
            e = Exception(f"Сума дезиту не може приймати знчення: {sum}")
            log.exception("Помилка суми депозиту", e)
            raise e

        if currency not in self.suported_currency:
            e = TypeError(f"Значення {currency}, для валют не припустиме")
            log.exception("Некоректна валюта для рахунку", e)
            raise e

        realsum = currate.convert(suma, currency, self._currency)

        if self._balance < realsum:
            e = ValueError("На рахунку недостатньо коштів")
            log.exception(f"На рахунку {self._account_id}, недостатньо коштів", e)
            raise e

        self._balance -= realsum

    def block_account(self):
        self._blocked = True

    def unblock_account(self):
        self._blocked = False

class Savings_account(Cheking_account):

    def __init__(self, user: User, period : int, percent : float, currency : str= "UAH") -> None:
        if not isinstance(period, int) or not isinstance(percent, float):
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

    def __init__(self, limit : float, user : User, period : int, percent : float, currency : str= "UAH") -> None:
        if not isinstance(limit, float):
            log.exception("Не вірні типи данних в атрибутi limit", TypeError())
            raise TypeError("Не вірні типи данних в атрибутi limit")
        super().__init__(user, period, percent, currency)
        self._limit = -limit

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
            initial_balance = self._balance
            for _ in range(full_periods):
                self._balance += self._balance * self.__percent

            self.__last_interest_date = today
            return self._balance - initial_balance
        else:
            return 0.0

    def withdraw(self, suma: float, currency: str = "UAH"):
        if not isinstance(suma, (float, int)) or suma <= 0:
            e = Exception(f"Сума дезиту не може приймати знчення: {suma}")
            log.exception("Помилка суми депозиту", e)
            raise e

        if currency not in self.suported_currency:
            e = TypeError(f"Значення {currency}, для валют не припустиме")
            log.exception("Некоректна валюта для рахунку", e)
            raise e

        realsum = currate.convert(suma, currency, self._currency)

        if self._balance - realsum < self._limit:
            e = ValueError("На рахунку недостатньо коштів")
            log.exception(f"На рахунку {self._account_id}, недостатньо коштів", e)
            raise e