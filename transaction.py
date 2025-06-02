import datetime
from types import NoneType
from accounts import Cheking_account, Credit_account, Savings_account
from logger import log
from currency import currate

class Transaction:
    __id = 1

    @classmethod
    def change_id(cls):
        cls.__id += 1
        return cls.__id - 1

    def __init__(self, amount: (float, int), source : (Credit_account, Cheking_account, Savings_account) = None,
                 target : (Credit_account, Cheking_account, Savings_account) = None) -> None :

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
    def __init__(self, amount : float, source : (Credit_account, Cheking_account, Savings_account), target : (Credit_account, Cheking_account, Savings_account)) -> None:
        if source is None or target is None:
            e = TypeError("source, target - не можуть бути None")
            log.exception("Неприпустиме значення атрибутів", e)
            raise e
        super().__init__(amount, source, target)

    def execute(self):
        try:
            self._check_blocked()
        except Exception as e:
            log.exception(f"Помилка транзакції #{self._transaction_id}", e)
            raise e

        real_amount = currate.convert(self._amount, self._source._currency, self._target._suported_currency)
        self._source.withdraw(self._amount)
        self._target.deposit(real_amount)
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
        if not isinstance(target, (Credit_account, Savings_account)):
            e = Exception(f"target повинно бути об'єктом одного з класів: (Credit_account, Savings_account), а не {target}")
            log.exception("Недопустиме значення аргументу", e)
            raise e
        amount = self._target.calculate_interest()
        super().__init__(None, None, target)


    def execute(self):
        try:
            if isinstance(self._target, Credit_account):
                self._target._credit += self._target.calculate_interest()

            if isinstance(self._target, Savings_account):
                self._target.deposit(self._target.calculate_interest())

        except Exception as e:
            log.exception(f"Помилка транзакції #{self._transaction_id}", e)
            raise e

        self._amount = self._target.calculate_interest()
        self._target.deposit(self._amount)
        log.info(f"Нараховано {self._amount} грн відсотків. Транзакція #{self._transaction_id}")




