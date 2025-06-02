from logger import log
from accounts import Cheking_account, Credit_account, Savings_account
"""
Модуль user містить клас для роботи з користувачами банку.

Класи:
- User: Клас, що представляє користувача банку.
"""
class User:
    """
        Клас, що представляє користувача банку.

        Атрибути класу:
        - __id: Лічильник для генерації унікальних ID користувачів.

        Атрибути екземпляра:
        - _user_id: Унікальний ідентифікатор користувача.
        - _first_name: Ім'я користувача.
        - _last_name: Прізвище користувача.
        - _email: Email користувача.
        - _phone_number: Номер телефону користувача.
        - _accounts_list: Словник рахунків користувача.

        Методи:
        - __init__: Ініціалізує користувача.
        - _change_id: Змінює ID користувача (класовий метод).
        - get_user_id: Повертає ID користувача.
        - get_full_name: Повертає повне ім'я користувача.
        - add_account: Додає рахунок до списку користувача.
    """
    __id = 1

    @classmethod
    def _generate_user_id(cls):
        """
            Генерує унікальний ID для користувача.

            Повертає:
                int: Новий ID користувача.
        """
        user_id = cls.__id
        cls.__id += 1
        return user_id

    def __init__(self, first_name: str, last_name: str, email: str = None, phone_number: str = None):
        """
            Ініціалізує нового користувача.

            Аргументи:
                first_name (str): Ім'я користувача.
                last_name (str): Прізвище користувача.
                email (str, optional): Email користувача. За замовчуванням None.
                phone_number (str, optional): Номер телефону користувача. За замовчуванням None.

            Винятки:
                TypeError: Якщо first_name або last_name не є рядками.
        """
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
        """
            Повертає рядкове представлення користувача.

            Повертає:
                str: Інформація про користувача.
        """
        return f"Користувач #{self._user_id}: {self._first_name} {self._last_name}"

    def get_user_id(self):
        """
            Повертає ID користувача.

            Повертає:
                int: ID користувача.
        """
        return self._user_id

    def get_full_name(self):
        """
            Повертає повне ім'я користувача.

            Повертає:
                str: Повне ім'я у форматі "Ім'я Прізвище".
        """
        return f"{self._first_name} {self._last_name}"

    def add_account(self, account : (Cheking_account, Savings_account, Credit_account)) -> None:
        """
            Додає рахунок до списку користувача.

            Аргументи:
                account (Account): Об'єкт рахунку.

            Винятки:
                TypeError: Якщо account має невірний тип.
        """
        if not isinstance(account, (Cheking_account, Savings_account, Credit_account)):
            e = TypeError("Об'єкт не є дійсним типом банківського рахунку")
            log.exception("Неіснуючий акаунт", e)
            raise e

        self._accounts_list[account._account_id] = account
