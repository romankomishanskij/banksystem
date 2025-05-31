from logger import log
from accounts import Cheking_account, Credit_account, Savings_account

class User:
    __id = 1

    @classmethod
    def _generate_user_id(cls):
        user_id = cls.__id
        cls.__id += 1
        return user_id

    def __init__(self, first_name: str, last_name: str, email: str = None, phone_number: str = None):
        if not isinstance(first_name, str) or not isinstance(last_name, str):
            log.exception("Неправильні типи даних для імені або прізвища користувача", TypeError())
            raise TypeError("Неправильні типи даних для імені або прізвища користувача")

        self._user_id = User._generate_user_id()
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._phone_number = phone_number
        self._accounts_list = {}
        log.info(f"Створено нового користувача з ID: {self._user_id}, ім'я: {self._first_name} {self._last_name}")

    def __str__(self):
        return f"Користувач #{self._user_id}: {self._first_name} {self._last_name}"

    def get_user_id(self):
        return self._user_id

    def get_full_name(self):
        return f"{self._first_name} {self._last_name}"

    def add_account(self, account : (Cheking_account, Savings_account, Credit_account)) -> None:
        if not isinstance(account, (Cheking_account, Savings_account, Credit_account)):
            log.exception("Неіснуючий акаунт", TypeError())
            raise TypeError
        self._accounts_list[account._account_id] = account
