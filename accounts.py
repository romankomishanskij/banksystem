import datetime
from user import User
from logger import Logger
log = Logger()

class Cheking_account:
    __id = 1

    def __init__(self, user : User, currency : str= "UAH") -> None:
        if not isinstance(user, User):
            log.exception(f"Неіснуючий користувач : {user}", TypeError())
            raise TypeError("Неіснуючий користувач")

        self._account_id = Cheking_account.change_id()
        self._balance = 0
        self.__owner = user
        self._blocked = False
        log.info(f"Рахунок з id = {self._account_id}, користувача {user}, було успішно створено!")

    @classmethod
    def change_id(cls):
        cls.__id += 1
        return cls.__id - 1

    def deposit(self, sum):
        self._balance += sum

    def withdraw(self, sum):
        self._balance -= sum

    def block_account(self):
        self._blocked = True

    def unblock_account(self):
        self._blocked = False

class Savings_account(Cheking_account):

    def __init__(self, user: User, period : int, percent : float) -> None:
        if not isinstance(period, int) or not isinstance(percent, float):
            log.exception("Не вірні типи данних в атрибутах period, percent", TypeError())
            raise TypeError("Не вірні типи данних в атрибутах period, percent")
        super().__init__(user)
        self.__last_interest_date = datetime.date.today()
        self.__period = period
        self.__percent = percent

    def calculate_interest(self):
        today = datetime.date.today()
        balance = self._balance

        months_passed = (today.year - self.__last_interest_date.year) * 12 + (today.month - self.__last_interest_date.month)
        if today.day < self.__last_interest_date.day:
            months_passed -= 1

        months_passed = int(months_passed / self.__period)


        if months_passed >= 1:
            for i in range(0, months_passed):
                balance += balance * self.__percent

            self.__last_interest_date = today

        return balance - self._balance

class Credit_account(Savings_account):

    def __init__(self, limit : float, user : User, period : int, percent : float) -> None:
        if not isinstance(limit, float):
            log.exception("Не вірні типи данних в атрибутi limit", TypeError())
            raise TypeError("Не вірні типи данних в атрибутi limit")
        super().__init__(user, period, percent)
        self._limit = -limit

    def calculate_interest(self):
        balance = self._balance
        if self._balance != 0:
            today = datetime.date.today()

            months_passed = (today.year - self.__last_interest_date.year) * 12 + (
                        today.month - self.__last_interest_date.month)
            if today.day < self.__last_interest_date.day:
                months_passed -= 1

            if months_passed >= 1:
                for i in range(0, months_passed):
                    self._balance += self._balance * self.__percent

                self.__last_interest_date = today
        return self._balance - balance