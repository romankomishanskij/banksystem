from user import User
from accounts import Cheking_account, Credit_account, Savings_account
from logger import log
"""
Модуль bank містить клас Bank для управління банківською системою.

Класи:
- Bank: Головний клас для роботи з користувачами та рахунками.
"""
class Bank:
    """
    Клас, що представляє банківську систему.

    Атрибути:
    - _name: Назва банку.
    - _address: Адреса банку.
    - _users: Словник користувачів банку (ключ - user_id).
    - _accounts: Словник рахунків банку (ключ - account_id).
    - __transactions: Список транзакцій.

    Методи:
    - __init__: Ініціалізує банк.
    - add_user: Додає нового користувача.
    - get_user: Отримує користувача за ID.
    - create_checking_account: Створює чековий рахунок.
    - create_savings_account: Створює ощадний рахунок.
    - create_credit_account: Створює кредитний рахунок.
    - get_account: Отримує рахунок за ID.
    """
    def __init__(self, name: str, address: str):
        """
            Ініціалізує новий банк.

            Аргументи:
                name (str): Назва банку.
                address (str): Адреса банку.

            Винятки:
                TypeError: Якщо name або address не є рядками.
        """
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
        """
            Повертає рядкове представлення банку.

            Повертає:
                str: Інформація про банк.
        """
        return f"Банк: {self._name}, адреса: {self._address}"

    def add_user(self, first_name: str, last_name: str, email: str = None, phone_number: str = None):
        """
            Додає нового користувача до банку.

            Аргументи:
                first_name (str): Ім'я користувача.
                last_name (str): Прізвище користувача.
                email (str, optional): Email користувача. За замовчуванням None.
                phone_number (str, optional): Номер телефону користувача. За замовчуванням None.

            Повертає:
                User: Створений об'єкт користувача.

            Винятки:
                TypeError: Якщо first_name або last_name не є рядками.
        """
        user = User(first_name, last_name, email, phone_number)

        self._users[user.get_user_id()] = user

        log.info(f"Додано нового користувача: {user}")
        return user

    def get_user(self, user_id: int):
        """
            Отримує користувача за ID.

            Аргументи:
                user_id (int): ID користувача.

            Повертає:
                User: Об'єкт користувача або None, якщо не знайдено.

            Винятки:
                TypeError: Якщо user_id не є цілим числом.
        """
        if not isinstance(user_id, int):
            log.error("ID користувача повинен бути цілим числом.")
            raise TypeError("ID користувача повинен бути цілим числом")

        return self._users.get(user_id)

    def create_checking_account(self, user: User, currency: str = "UAH"):
        """
            Створює чековий рахунок для користувача.

            Аргументи:
                user (User): Об'єкт користувача.
                currency (str, optional): Валюта рахунку. За замовчуванням "UAH".

            Повертає:
                Cheking_account: Створений чековий рахунок.

            Винятки:
                ValueError: Якщо користувач не зареєстрований у банку.
        """
        if not isinstance(user, User) or user.get_user_id() not in self._users:
            log.error(f"Користувача {user} не знайдено в банку.")
            raise ValueError(f"Користувача {user} не знайдено в банку.")

        account = Cheking_account(user, currency)

        self._accounts[account._account_id] = account
        user.add_account(account)

        log.info(f"Створено чековий рахунок #{account._account_id} для користувача {user}.")
        return account

    def create_savings_account(self, user: User, period: int, percent: float, currency: str = "UAH"):
        """
            Створює ощадний рахунок для користувача.

            Аргументи:
                user (User): Об'єкт користувача.
                period (int): Період нарахування відсотків (у місяцях).
                percent (float): Відсоткова ставка.
                currency (str, optional): Валюта рахунку. За замовчуванням "UAH".

            Повертає:
                Savings_account: Створений ощадний рахунок.

            Винятки:
                ValueError: Якщо користувач не зареєстрований у банку.
        """
        if not isinstance(user, User) or user.get_user_id() not in self._users:
            log.error(f"Користувача {user} не знайдено в банку.")
            raise ValueError(f"Користувача {user} не знайдено в банку.")

        account = Savings_account(user, period, percent, currency)

        self._accounts[account._account_id] = account
        user.add_account(account)

        log.info(f"Створено ощадний рахунок #{account._account_id} для користувача {user}.")
        return account

    def create_credit_account(self, user: User, limit: float, period: int, percent: float, currency: str = "UAH"):
        """
            Створює кредитний рахунок для користувача.

            Аргументи:
                user (User): Об'єкт користувача.
                limit (float): Кредитний ліміт.
                period (int): Період нарахування відсотків (у місяцях).
                percent (float): Відсоткова ставка.
                currency (str, optional): Валюта рахунку. За замовчуванням "UAH".

            Повертає:
                Credit_account: Створений кредитний рахунок.

            Винятки:
                ValueError: Якщо користувач не зареєстрований у банку.
        """
        if not isinstance(user, User) or user.get_user_id() not in self._users:
            log.error(f"Користувача {user} не знайдено в банку.")
            raise ValueError(f"Користувача {user} не знайдено в банку.")

        account = Credit_account(limit, user, period, percent, currency)

        self._accounts[account._account_id] = account
        user.add_account(account)

        log.info(f"Створено кредитний рахунок #{account._account_id} для користувача {user}.")
        return account

    def get_account(self, account_id : int):
        """
            Отримує рахунок за ID.

            Аргументи:
                account_id (int): ID рахунку.

            Повертає:
                Account: Об'єкт рахунку або None, якщо не знайдено.

            Винятки:
                TypeError: Якщо account_id не є цілим числом.
        """
        if not isinstance(account_id, int):
            log.error("ID рахунку повинен бути цілим числом.")
            raise TypeError("ID рахунку повинен бути цілим числом")

        return self._accounts.get(account_id)

    def close_account(self, account: (Cheking_account, Credit_account, Savings_account)):
        """
            Закриває рахунок в банку.

            Аргументи:
                account (Cheking_account, Credit_account, Savings_account): Об'єкт одного з класів рахунків.

            Винятки:
                    TypeError: Якщо account не є об'єктом потрібного класу .
        """
        if not isinstance(account, (Cheking_account, Credit_account, Savings_account)):
            e = Exception(
                f"account повинно бути об'єктом одного з класів: (Cheking_account, Credit_account, Savings_account), а не {account}")
            log.exception("Недопустиме значення аргументу", e)
            raise e
        if isinstance(account, Credit_account):
            if account._balance == account._limit and account._credit == 0:
                account.block_account()
            elif account._balance < account._limit:
                log.info(f"Рахунок #{account._account_id} не можливо закрити через присутні на ньому борг у розімрі: {account._limit - account._balance + account._credit} {account._currency}")
            else:
                log.info(f"Рахунок #{account._account_id} не можливо закрити через присутні на ньому кошти у розімрі: {account._balance - account._limit} {account._currency}")


        elif isinstance(account, (Savings_account, Cheking_account)):
            if account.balance == 0:
                account.block_account()
            else:
                log.info(f"Рахунок #{account._account_id} не можливо закрити через присутні на ньому кошти у розімрі: {account._balance} {account._currency}")




