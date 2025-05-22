import datetime
from accounts import Cheking_account, Credit_account, Savings_account
from logger import Logger
from user import User
log = Logger()

class Transaction:
    __id = 1

    @classmethod
    def change_id(cls):
        cls.__id += 1
        return cls.__id - 1

    def __init__(self, amount: float, source : (Credit_account, Cheking_account, Savings_account) = None,
                 target : (Credit_account, Cheking_account, Savings_account) = None) -> None :

        if not isinstance(amount, float) or not (source is None or isinstance(source, (Credit_account, Cheking_account, Savings_account))) or not (target is None or isinstance(target, (Credit_account, Cheking_account, Savings_account))):
            log.exception("Неправильні типи данних в атрибутах: amount, source, targer або через недопустиме значення в amount", TypeError())
            raise TypeError("Неправильні типи данних в атрибутах: amount, source, targer або через недопустиме значення в amount")

        if amount < 0:
            log.exception(
                "amount повинен бути більше 0",
                ValueError())
            raise TypeError(
                "amount повинен бути більше 0")

        self._transaction_id = Transaction.change_id()
        self._source = source
        self._target = target
        self._amount = amount
        self._data = datetime.datetime.now()
        log.info(f"Була створена транзакція з id : {self._transaction_id}")

    def __str__(self):
        return f"Transaction #{self._transaction_id}: amount = {self._amount}, date = {self._data}"

    def execute(self):
        pass

    def _check_blocked(self):
        if self._source and self._source._blocked:
            raise Exception(f"Акаунт #{self._source._account_id} Заблоковано")
        if self._target and self._target._blocked:
            raise Exception(f"Акаунт #{self._target._account_id} Заблоковано")


class DepositTransaction(Transaction):
    def __init__(self, amount : float, target : (Credit_account, Cheking_account, Savings_account)):
        super().__init__(amount,None, target)


    def execute(self):
        try:
            self._check_blocked()
        except Exception as e:
            log.exception(f"Помилка транзакції #{self._transaction_id}", e)
            raise e

        self._target.deposit(self._amount)
        log.info(f"Була проведена транзакція з id : {self._transaction_id}")

class TransferTransaction(Transaction):
    def __init__(self, amount : float, source : (Credit_account, Cheking_account, Savings_account) = None , target : (Credit_account, Cheking_account, Savings_account) = None) -> None:
        super().__init__(amount, source, target)

    def execute(self):
        try:
            self._check_blocked()
        except Exception as e:
            log.exception(f"Помилка транзакції #{self._transaction_id}", e)
            raise e

        self._source.withdraw(self._amount)
        self._target.deposit(self._amount)
        log.info(f"Була проведена транзакція з id : {self._transaction_id}")

class WithdrawTransaction(Transaction):
    def __init__(self, amount : float, source : (Credit_account, Cheking_account, Savings_account)):
        super().__init__(amount, source, None)


    def execute(self):
        try:
            self._check_blocked()
        except Exception as e:
            log.exception(f"Помилка транзакції #{self._transaction_id}", e)
            raise e

        self._source.withdraw(self._amount)
        log.info(f"Була проведена транзакція з id : {self._transaction_id}")

class CalculateInterestTransaction(Transaction):

    def __init__(self, target : (Credit_account, Cheking_account, Savings_account)):
        super().__init__(1, None, target)


    def execute(self):
        try:
            self._check_blocked()
        except Exception as e:
            log.exception(f"Помилка транзакції #{self._transaction_id}", e)
            raise e

        self._amount = self._target.calculate_interest()
        self._target.deposit(self._amount)
        log.info(f"Нараховано {self._amount} грн відсотків. Транзакція #{self._transaction_id}")




