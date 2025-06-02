import datetime
from types import NoneType
from accounts import Cheking_account, Credit_account, Savings_account
from logger import log
from currency import currate

"""
Модуль transaction містить класи для роботи з транзакціями.

Класи:
- Transaction: Базовий клас для транзакцій.
- DepositTransaction: Клас для депозитних транзакцій.
- TransferTransaction: Клас для переказів.
- WithdrawTransaction: Клас для зняття коштів.
- CalculateInterestTransaction: Клас для нарахування відсотків.
"""

class Transaction:
    """
        Базовий клас для транзакцій.

        Атрибути класу:
        - __id: Лічильник для генерації унікальних ID транзакцій.

        Атрибути екземпляра:
        - _transaction_id: Унікальний ідентифікатор транзакції.
        - _source: Вихідний рахунок.
        - _target: Цільовий рахунок.
        - _amount: Сума транзакції.
        - _data: Дата та час транзакції.

        Методи:
        - __init__: Ініціалізує транзакцію.
        - change_id: Змінює ID транзакції (класовий метод).
        - execute: Виконує транзакцію (абстрактний метод).
        - _check_blocked: Перевіряє, чи заблоковані рахунки.
        """

    __id = 1

    @classmethod
    def change_id(cls):
        """
                Генерує унікальний ID для транзакції.

                Повертає:
                    int: Новий ID транзакції.
        """
        cls.__id += 1
        return cls.__id - 1

    def __init__(self, amount: (float, int), source : (Credit_account, Cheking_account, Savings_account) = None,
                 target : (Credit_account, Cheking_account, Savings_account) = None) -> None :
        """
                Ініціалізує нову транзакцію.

                Аргументи:
                    amount (float, int): Сума транзакції.
                    source (Account, optional): Вихідний рахунок. За замовчуванням None.
                    target (Account, optional): Цільовий рахунок. За замовчуванням None.

                Винятки:
                    Exception: Якщо amount не є числом або менше 0.
                    Exception: Якщо source або target мають невірний тип.
                """

        if not isinstance(amount, (float, int, NoneType)) or amount < 0:
            e = Exception(f"amount повинно бути числом більше 0, а не {amount}")
            log.exception("Недопустиме значення аргументу", e)
            raise e

        if not isinstance(source, (Cheking_account, Credit_account, Savings_account, NoneType)):
            e = Exception(f"source повинно бути об'єктом одного з класів: (Cheking_account, Credit_account, Savings_account, NoneType), а не {source}")
            log.exception("Недопустиме значення аргументу", e)
            raise e

        if not isinstance(target, (Cheking_account, Credit_account, Savings_account, NoneType)):
            e = Exception(f"target повинно бути об'єктом одного з класів: (Cheking_account, Credit_account, Savings_account, NoneType), а не {target}")
            log.exception("Недопустиме значення аргументу", e)
            raise e


        self._transaction_id = Transaction.change_id()
        self._source = source
        self._target = target
        self._amount = amount
        self._data = datetime.datetime.now()
        log.info(f"Була створена транзакція з id : {self._transaction_id}")

    def __str__(self):
        """
                Повертає рядкове представлення транзакції.

                Повертає:
                    str: Інформація про транзакцію.
        """
        return f"Transaction #{self._transaction_id}: amount = {self._amount}, date = {self._data}"

    def execute(self):
        """Абстрактний метод для виконання транзакції."""
        pass

    def _check_blocked(self):
        """
                Перевіряє, чи заблоковані рахунки.

                Винятки:
                    Exception: Якщо вихідний або цільовий рахунок заблоковано.
        """
        if self._source and self._source._blocked:
            raise Exception(f"Акаунт #{self._source._account_id} Заблоковано")
        if self._target and self._target._blocked:
            raise Exception(f"Акаунт #{self._target._account_id} Заблоковано")


class DepositTransaction(Transaction):
    """
        Клас для депозитних транзакцій.

        Методи:
        - __init__: Ініціалізує депозитну транзакцію.
        - execute: Виконує депозит.
        """
    def __init__(self, amount : float, target : (Credit_account, Cheking_account, Savings_account)):
        """
                Ініціалізує депозитну транзакцію.

                Аргументи:
                    amount (float): Сума депозиту.
                    target (Account): Цільовий рахунок.
        """
        super().__init__(amount,None, target)


    def execute(self):
        """
                Виконує депозит на цільовий рахунок.

                Винятки:
                    Exception: Якщо рахунок заблоковано.
        """
        try:
            self._check_blocked()
        except Exception as e:
            log.exception(f"Помилка транзакції #{self._transaction_id}", e)
            raise e

        self._target.deposit(self._amount)
        log.info(f"Була проведена транзакція з id : {self._transaction_id}")

class TransferTransaction(Transaction):
    """
        Клас для транзакцій переказу.

        Методи:
        - __init__: Ініціалізує транзакцію переказу.
        - execute: Виконує переказ.
    """
    def __init__(self, amount : float, source : (Credit_account, Cheking_account, Savings_account), target : (Credit_account, Cheking_account, Savings_account)) -> None:
        """
            Ініціалізує транзакцію переказу.

            Аргументи:
                amount (float): Сума переказу.
                source (Account): Вихідний рахунок.
                target (Account): Цільовий рахунок.

            Винятки:
                TypeError: Якщо source або target є None.
        """
        if source is None or target is None:
            e = TypeError("source, target - не можуть бути None")
            log.exception("Неприпустиме значення атрибутів", e)
            raise e
        super().__init__(amount, source, target)

    def execute(self):
        """
            Виконує переказ між рахунками з конвертацією валют.

            Винятки:
                Exception: Якщо рахунки заблоковано.
        """
        try:
            self._check_blocked()
        except Exception as e:
            log.exception(f"Помилка транзакції #{self._transaction_id}", e)
            raise e

        real_amount = currate.convert(self._amount, self._source._currency, self._target._currency)
        self._source.withdraw(self._amount)
        self._target.deposit(real_amount)
        log.info(f"Була проведена транзакція з id : {self._transaction_id}")

class WithdrawTransaction(Transaction):
    """
    Клас для транзакцій зняття коштів.

    Методи:
    - __init__: Ініціалізує транзакцію зняття.
    - execute: Виконує зняття коштів.
    """
    def __init__(self, amount : float, source : (Credit_account, Cheking_account, Savings_account)):
        """
            Ініціалізує транзакцію зняття коштів.

            Аргументи:
                amount (float): Сума для зняття.
                source (Account): Вихідний рахунок.
        """
        super().__init__(amount, source, None)


    def execute(self):
        """
            Виконує зняття коштів з рахунку.

            Винятки:
                Exception: Якщо рахунок заблоковано.
        """
        try:
            self._check_blocked()
        except Exception as e:
            log.exception(f"Помилка транзакції #{self._transaction_id}", e)
            raise e

        self._source.withdraw(self._amount)
        log.info(f"Була проведена транзакція з id : {self._transaction_id}")

class CalculateInterestTransaction(Transaction):
    """
        Клас для транзакцій нарахування відсотків.

        Методи:
        - __init__: Ініціалізує транзакцію нарахування відсотків.
        - execute: Виконує нарахування відсотків.
    """
    def __init__(self, target : (Credit_account, Cheking_account, Savings_account)):
        """
            Ініціалізує транзакцію нарахування відсотків.

            Аргументи:
                target (Account): Цільовий рахунок (кредитний або ощадний).

            Винятки:
                 Exception: Якщо target має невірний тип.
        """
        if not isinstance(target, (Credit_account, Savings_account)):
            e = Exception(f"target повинно бути об'єктом одного з класів: (Credit_account, Savings_account), а не {target}")
            log.exception("Недопустиме значення аргументу", e)
            raise e
        super().__init__(None, None, target)
        self._amount = self._target.calculate_interest()

    def execute(self):
        """
            Виконує нарахування відсотків на рахунок.

            Винятки:
                Exception: Якщо виникла помилка під час нарахування.
        """
        try:
            if isinstance(self._target, Credit_account):
                self._target._credit += self._amount

            if isinstance(self._target, Savings_account):
                self._target.deposit(self._amount)

            log.info(f"Нараховано {self._amount} грн відсотків. Транзакція #{self._transaction_id}")

        except Exception as e:
            log.exception(f"Помилка транзакції #{self._transaction_id}", e)
            raise e