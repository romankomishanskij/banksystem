from user import User
from accounts import Cheking_account, Credit_account, Savings_account
from logger import log

class Bank:
    def __init__(self, name: str, address: str):
        if not isinstance(name, str) or not isinstance(address, str):
            log.exception("Неправильні типи даних для назви або адреси банку", TypeError())
            raise TypeError("Неправильні типи даних для назви або адреси банку")

        self._name = name
        self._address = address
        self._users = {}
        self._accounts = {}
        self.__transactions = []
        log.info(f"Створено банк '{self._name}' за адресою: {self._address}")

    def __str__(self):
        return f"Банк: {self._name}, адреса: {self._address}"

    def add_user(self, first_name: str, last_name: str, email: str = None, phone_number: str = None):

        user = User(first_name, last_name, email, phone_number)

        self._users[user.get_user_id()] = user

        log.info(f"Додано нового користувача: {user}")
        return user

    def get_user(self, user_id: int):
        if not isinstance(user_id, int):
            log.error("ID користувача повинен бути цілим числом.")
            raise TypeError("ID користувача повинен бути цілим числом")

        return self._users.get(user_id)

    def create_checking_account(self, user: User, currency: str = "UAH"):
        if not isinstance(user, User) or user.get_user_id() not in self._users:
            log.error(f"Користувача {user} не знайдено в банку.")
            raise ValueError(f"Користувача {user} не знайдено в банку.")

        account = Cheking_account(user, currency)

        self._accounts[account._account_id] = account
        user.add_account(account)

        log.info(f"Створено чековий рахунок #{account._account_id} для користувача {user}.")
        return account

    def create_savings_account(self, user: User, period: int, percent: float, currency: str = "UAH"):
        if not isinstance(user, User) or user.get_user_id() not in self._users:
            log.error(f"Користувача {user} не знайдено в банку.")
            raise ValueError(f"Користувача {user} не знайдено в банку.")

        account = Savings_account(user, period, percent, currency)

        self._accounts[account._account_id] = account
        user.add_account(account)

        log.info(f"Створено ощадний рахунок #{account._account_id} для користувача {user}.")
        return account

    def create_credit_account(self, user: User, limit: float, period: int, percent: float, currency: str = "UAH"):
        if not isinstance(user, User) or user.get_user_id() not in self._users:
            log.error(f"Користувача {user} не знайдено в банку.")
            raise ValueError(f"Користувача {user} не знайдено в банку.")

        account = Credit_account(limit, user, period, percent, currency)

        self._accounts[account._account_id] = account
        user.add_account(account)

        log.info(f"Створено кредитний рахунок #{account._account_id} для користувача {user}.")
        return account

    def get_account(self, account_id):
        if not isinstance(account_id, int):
            log.error("ID рахунку повинен бути цілим числом.")
            raise TypeError("ID рахунку повинен бути цілим числом")

        return self._accounts.get(account_id)

    def close_account(self, account: (Cheking_account, Credit_account, Savings_account)):
        if not isinstance(account, (Cheking_account, Credit_account, Savings_account)):
            e = Exception(
                f"account повинно бути об'єктом одного з класів: (Cheking_account, Credit_account, Savings_account), а не {account}")
            log.exception("Недопустиме значення аргументу", e)
            raise e
        if isinstance(account, Credit_account):
            if self._balance == self._limit and self._credit == 0:
                account.block_account()
        else:
            if self.balance == 0:
                account.block_account()




