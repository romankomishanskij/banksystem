# Bank System Documentation
Це проект, який складається з різних модулів для управління банківськими системами але також кожна його частина може використовуватись окремо від інших за рахунок розбиття структури на модулі 

## Як почати працювати?
* **Підключення до вашої системи**:

  ```python
     from bank import Bank # для сворення банку
     from user import User # для створення користувачів
     from logger import Logger # для підключення логування
     from transaction import TransferTransaction, WithdrawTransaction, CalculateInterestTransaction, DepositTransaction # для роботи з рухунками 
     from accounts import Cheking_account, Savings_account, Credit_account # для ініціалізації рахунків
     from currency import CurrencyRates # для підтягування валют
  ```
## accounts.py

Цей модуль містить класи для роботи з банківськими рахунками: `Cheking_account`, `Savings_account` та `Credit_account`(для операціїй з рахунками(окрім створення) доцільніше використовувати модуль транзакцій) .

### `Cheking_account`

Клас для представлення чекового рахунку.

#### Атрибути класу

-   `__id`: Лічильник для генерації унікальних ID рахунків.
-   `_suported_currency`: Список підтримуваних валют ("UAH", "USD", "EUR").

#### Атрибути екземпляра

-   `_account_id`: Унікальний ID рахунку.
-   `_currency`: Валюта рахунку.
-   `_balance`: Поточний баланс.
-   `_owner`: Власник рахунку (`User`).
-   `_blocked`: Статус блокування.

#### Методи

##### `__init__(self, user: User, currency: str = "UAH") -> None`

Ініціалізує новий чековий рахунок.

* **Можливі помилки**:
    * `ValueError`: Якщо валюта не підтримується.
    * `TypeError`: Якщо `user` не є об'єктом `User`.
* **Приклад використання у коді**:
    
  ```python
        acc = Cheking_account(user123, "UAH") # Гривневий рахунок з нульовим балансом власником якого є user123
    ```
##### `change_id(cls)`

Генерує унікальний ID для рахунку (класовий метод).
* **Приклад використання у коді**:
    
  ```python
        account_id1 = Cheking_account.change_id()
        account_id2 = Cheking_account.change_id()
        print(f"Account ID 1: {account_id1}, Account ID 2: {account_id2}") # Account ID 1: 1, Account ID 2: 2
    ```
##### `deposit(self, suma: (int, float), currency: str = "UAH")`

Поповнює рахунок.

* **Можливі помилки**:
    * `ValueError`: Якщо валюта не підтримується.
    * `Exception`: Якщо `suma` не є числом або менше/дорівнює 0.05.
  
* **Приклад використання у коді**:
    
  ```python
        acc.deposit(1000, "UAH") # баланс поповнили на 1000 грн
        # можливі поповення різними валютами
        acc.deposit(1000, "EUR") # баланс поповнили на 1000 євро
        acc.deposit(1000, "USD") # баланс поповнили на 1000 доларів
    ```

##### `withdraw(self, suma: (int, float), currency: str = "UAH")`

Знімає кошти з рахунку.

* **Можливі помилки**:
    * `ValueError`: Якщо валюта не підтримується.
    * `Exception`: Якщо `suma` не є числом або менше/дорівнює 0.
    * `Exception`: Якщо на рахунку недостатньо коштів.

* **Приклад використання у коді**:
    
  ```python
        acc.withdraw(1000, "UAH") # з балансу зняли 1000 грн
        # можливі поповення різними валютами
        acc.withdraw(1000, "EUR") # з балансу зняли 1000 євро
        acc.withdraw(1000, "USD") # з балансу зняли 1000 доларів
  ```

##### `block_account(self)`

Блокує рахунок.
* **Приклад використання у коді**:
    
  ```python
        acc.block_account()
  ```
##### `unblock_account(self)`

Розблоковує рахунок.
* **Приклад використання у коді**:
    
  ```python
        acc.unblock_account()
  ```
### `Savings_account(Cheking_account)`

Клас для ощадних рахунків, успадкований від `Cheking_account` також можу використовувати методи з Cheking_account.

#### Атрибути екземпляра

-   `__last_interest_date`: Дата останнього нарахування відсотків.
-   `__period`: Період нарахування відсотків (у місяцях).
-   `__percent`: Відсоткова ставка.

#### Методи

##### `__init__(self, user: User, period: int, percent: float, currency: str = "UAH") -> None`

Ініціалізує ощадний рахунок.

* **Можливі помилки**:
    * `TypeError`: Якщо `period` або `percent` мають невірний тип.
* **Приклад використання у коді**:
    
  ```python
        auser = User("Oleh", "Shevchenko")
        savings = Savings_account(user, period=6, percent=5.0, currency="USD")
  ```
##### `calculate_interest(self)`

Розраховує та нараховує відсотки.
* **Приклад використання у коді**:
    
  ```python
        savings.calculate_interest()
  ```
### `Credit_account(Savings_account)`

Клас для кредитних рахунків, успадкований від `Savings_account`, також може використовувати методи з "Cheking_account".

#### Атрибути екземпляра

-   `_limit`: Кредитний ліміт.
-   `_credit`: Поточний розмір кредиту.

#### Методи

##### `__init__(self, limit: (float, int), user: User, period: int, percent: float, currency: str = "UAH") -> None`

Ініціалізує кредитний рахунок.

* **Можливі помилки**:
    * `TypeError`: Якщо `limit` має невірний тип.
* **Приклад використання у коді**:
    
  ```python
        user = User("Maria", "Ivanova")
        credit = Credit_account(10000, user, period=12, percent=18.0, currency="UAH")
  ```
##### `calculate_interest(self)`

Розраховує відсотки за кредитом.
* **Приклад використання у коді**:
    
  ```python
        credit.calculate_interest()
  ```
##### `withdraw(self, suma: float, currency: str = "UAH")`

Знімає кошти з рахунку, враховуючи кредитний ліміт.

* **Можливі помилки**:
    * `Exception`: Якщо `suma` не є числом або менше/дорівнює 0.
    * `TypeError`: Якщо валюта не підтримується.
    * `ValueError`: Якщо перевищено кредитний ліміт.
* **Приклад використання у коді**:
    
  ```python
        credit.withdraw(5000, "UAH")
  ```
## bank.py

Цей модуль містить клас `Bank` для управління банківською системою.

### `Bank`

Клас для представлення банківської системи.

#### Атрибути

-   `_name`: Назва банку.
-   `_address`: Адреса банку.
-   `_users`: Словник користувачів банку (ключ - user\_id).
-   `_accounts`: Словник рахунків банку (ключ - account\_id).
-   `__transactions`: Список транзакцій.

#### Методи

##### `__init__(self, name: str, address: str)`

Ініціалізує новий банк.

* **Можливі помилки**:
    * `TypeError`: Якщо `name` або `address` не є рядками.
* **Приклад використання у коді**:
    
  ```python
        bank = Bank("MonoBank", "Kyiv, Ukraine")
  ```
##### `__str__(self)`

Повертає рядкове представлення банку.

##### `add_user(self, first_name: str, last_name: str, email: str = None, phone_number: str = None)`

Додає нового користувача(також одразу додає його до списку користувачів).

* **Можливі помилки**:
    * `TypeError`: Якщо `first_name` або `last_name` не є рядками.
* **Приклад використання у коді**:
    
  ```python
        user = bank.add_user("Anna", "Koval", email="anna@example.com")
  ```
##### `get_user(self, user_id: int)`

Отримує користувача за ID.

* **Можливі помилки**:
    * `TypeError`: Якщо `user_id` не є цілим числом.
* **Приклад використання у коді**:
    
  ```python
        user = bank.get_user(27)
  ```
##### `create_checking_account(self, user: User, currency: str = "UAH")`

Створює чековий рахунок для користувача(і додає його до списку).

* **Можливі помилки**:
    * `ValueError`: Якщо користувач не зареєстрований у банку.
* **Приклад використання у коді**:
    
  ```python
        account = bank.create_checking_account(user, currency="USD")
  ```
##### `create_savings_account(self, user: User, period: int, percent: float, currency: str = "UAH")`

Створює ощадний рахунок для користувача(і додає його до списку).

* **Можливі помилки**:
    * `ValueError`: Якщо користувач не зареєстрований у банку.
* **Приклад використання у коді**:
    
  ```python
        savings = bank.create_savings_account(user, period=6, percent=3.5, currency="UAH")
  ```
##### `create_credit_account(self, user: User, limit: float, period: int, percent: float, currency: str = "UAH")`

Створює кредитний рахунок для користувача(і додає його до списку).

* **Можливі помилки**:
    * `ValueError`: Якщо користувач не зареєстрований у банку.
* **Приклад використання у коді**:
    
  ```python
        credit = bank.create_credit_account(user, limit=15000, period=12, percent=15.0, currency="EUR")
  ```
##### `get_account(self, account_id)`

Отримує рахунок за ID.

* **Можливі помилки**:
    * `TypeError`: Якщо `account_id` не є цілим числом.
* **Приклад використання у коді**:
    
  ```python
        ac = bank.get_account(79)
  ```
## currency.py

Цей модуль містить клас `CurrencyRates` для отримання та конвертації курсів валют.

### `CurrencyRates`

Клас для роботи з курсами валют.

#### Атрибути

-   `rates`: Словник з курсами валют.
-   `_last_usage`: Час останнього оновлення курсів.

#### Методи

##### `__init__(self)`

Ініціалізує об'єкт та оновлює курси долара та євро відносно гривні.
* **Приклад використання у коді**:
    
  ```python
        cr = CurrencyRates()
  ```
##### `update_rates(self)`

Оновлює курси валют через API ПриватБанку.
* **Приклад використання у коді**:
    
  ```python
        cr.update_rates()
  ```
##### `convert(self, amount: float, from_currency: str, to_currency: str)`

Конвертує суму з однієї валюти в іншу.

* **Можливі помилки**:
    * `Exception`: Якщо валюта не підтримується.
* **Приклад використання у коді**:
    
  ```python
        uah_to_usd = cr.convert(1000, "UAH", "USD")
  ```
## logger.py

Цей модуль містить клас `Logger` для логування подій у системі для подальшого їх опрацювання(у системі вже створено об'єкт цього класу який вона використвоує для логування всіх її подій).

### `Logger`

Клас для запису логів у файл.

#### Атрибути

-   `filename`: Ім'я файлу для логування(за замовчуванням banksystem.log).

#### Методи

##### `__init__(self, filename: str = "banksystem.log", create: bool = True) -> None`

Ініціалізує об'єкт логера.

* **Можливі помилки**:
    * `TypeError`: Якщо `filename` не є рядком або `create` не є булевим значенням.
* **Приклад використання у коді**:
    
  ```python
        log = Logger("activity.log")
  ```
##### `_write(self, level: str, message: str)`

Записує повідомлення у файл логу.
* **Приклад використання у коді**:
    
  ```python
        log._write("DEBUG", "This is a debug message")
  ```
##### `info(self, message: str)`

Записує інформаційне повідомлення в лог.
* **Приклад використання у коді**:
    
  ```python
        log.info("User created successfully")
  ```
##### `warning(self, message: str)`

Записує попередження у лог.
* **Приклад використання у коді**:
    
  ```python
        log.warning("Low balance warning")
  ```
##### `error(self, message: str)`

Записує повідомлення про помилку у лог.
* **Приклад використання у коді**:
    
  ```python
        log.error("Invalid account access attempt")
  ```
##### `exception(self, message: str, exc: Exception)`

Записує інформацію про виняток у лог.
* **Приклад використання у коді**:
    
  ```python
    try:
        raise ValueError("Something went wrong")
    except Exception as e:
        log.exception("Caught exception", e)
  ```
## transaction.py

Цей модуль містить класи для роботи з транзакціями: `Transaction`, `DepositTransaction`, `TransferTransaction`, `WithdrawTransaction` та `CalculateInterestTransaction`.

### `Transaction`

Абстрактний, базовий клас для транзакцій.

#### Атрибути класу

-   `__id`: Лічильник для генерації унікальних ID транзакцій 

#### Атрибути екземпляра

-   `_transaction_id`: Унікальний ID транзакції.
-   `_source`: Вихідний рахунок.
-   `_target`: Цільовий рахунок.
-   `_amount`: Сума транзакції.
-   `_data`: Дата та час транзакції.

#### Методи

##### `__init__(self, amount: (float, int), source: (Credit_account, Cheking_account, Savings_account) = None, target: (Credit_account, Cheking_account, Savings_account) = None) -> None`

Ініціалізує нову транзакцію.

* **Можливі помилки**:
    * `Exception`: Якщо amount не є числом або менше 0.
    * `Exception`: Якщо source або target мають невірний тип.
* **Приклад використання у коді**:
    
  ```python
    tx = Transaction(100.0, source_account, target_account)
  ```
##### `change_id(cls)`

Генерує унікальний ID для транзакції (класовий метод).
* **Приклад використання у коді**:
    
  ```python
        new_id = Transaction.change_id()
  ```
##### `__str__(self)`

Повертає рядкове представлення транзакції.
* **Приклад використання у коді**:
    
  ```python
        print(str(tx))
  ```
##### `execute(self)`

Абстрактний метод для виконання транзакції(нічого не виконує).
* **Приклад використання у коді**:
    
  ```python
        dep.execute()
  ```
##### `_check_blocked(self)`

Перевіряє, чи заблоковані рахунки.

* **Можливі помилки**:
    * `Exception`: Якщо вихідний або цільовий рахунок заблоковано.
* **Приклад використання у коді**:
    
  ```python
        tx._check_blocked()
  ```
### `DepositTransaction(Transaction)`

Клас для депозитних транзакцій.

#### Методи

##### `__init__(self, amount: float, target: (Credit_account, Cheking_account, Savings_account))`

Ініціалізує депозитну транзакцію.
* **Приклад використання у коді**:
    
  ```python
        credit.withdraw(5000, "UAH")
  ```
##### `execute(self)`

Виконує депозит.

* **Можливі помилки**:
    * `Exception`: Якщо рахунок заблоковано.

### `TransferTransaction(Transaction)`

Клас для транзакцій переказу.

#### Методи

##### `__init__(self, amount: float, source: (Credit_account, Cheking_account, Savings_account), target: (Credit_account, Cheking_account, Savings_account)) -> None`

Ініціалізує транзакцію переказу.

* **Можливі помилки**:
    * `TypeError`: Якщо source або target є None.
* **Приклад використання у коді**:
    
  ```python
        dep = DepositTransaction(500.0, target=account)
  ```
##### `execute(self)`

Виконує переказ між рахунками з конвертацією валют.

* **Можливі помилки**:
    * `Exception`: Якщо рахунки заблоковано.
* **Приклад використання у коді**:
    
  ```python
        dep.execute()
  ```
### `WithdrawTransaction(Transaction)`

Клас для транзакцій зняття коштів.

#### Методи

##### `__init__(self, amount: float, source: (Credit_account, Cheking_account, Savings_account))`

Ініціалізує транзакцію зняття коштів.
* **Приклад використання у коді**:
    
  ```python
        wd = WithdrawTransaction(100.0, source=account)
  ```
##### `execute(self)`

Виконує зняття коштів з рахунку.

* **Можливі помилки**:
    * `Exception`: Якщо рахунок заблоковано.
* **Приклад використання у коді**:
    
  ```python
        wd.execute()
  ```
### `CalculateInterestTransaction(Transaction)`

Клас для транзакцій нарахування відсотків.

#### Методи

##### `__init__(self, target: (Credit_account, Savings_account))`

Ініціалізує транзакцію нарахування відсотків.

* **Можливі помилки**:
    * `Exception`: Якщо target має невірний тип.
* **Приклад використання у коді**:
    
  ```python
        interest = CalculateInterestTransaction(target=savings)
  ```
##### `execute(self)`

Виконує нарахування відсотків на рахунок.

* **Можливі помилки**:
    * `Exception`: Якщо виникла помилка під час нарахування.
* **Приклад використання у коді**:
    
  ```python
        interest.execute()
  ```
## user.py

Цей модуль містить клас для роботи з користувачами банку.

### `User`

Клас, що представляє користувача банку.

#### Атрибути класу

-   `__id`: Лічильник для генерації унікальних ID користувачів.

#### Атрибути екземпляра

-   `_user_id`: Унікальний ідентифікатор користувача.
-   `_first_name`: Ім'я користувача.
-   `_last_name`: Прізвище користувача.
-   `_email`: Email користувача.
-   `_phone_number`: Номер телефону користувача.
-   `_accounts_list`: Словник рахунків користувача.

#### Методи

##### `__init__(self, first_name: str, last_name: str, email: str = None, phone_number: str = None)`

Ініціалізує нового користувача.

* **Можливі помилки**:
    * `TypeError`: Якщо first\_name або last\_name не є рядками.
* **Приклад використання у коді**:
    
  ```python
        user = User("Taras", "Bulba", email="taras@ukr.net", phone_number="0500000000")
  ```
##### `_change_id(cls)`

Генерує унікальний ID для користувача (класовий метод).
* **Приклад використання у коді**:
    
  ```python
        uid = User._change_id()
  ```
##### `__str__(self)`

Повертає рядкове текстовий вивід данних користувача.
* **Приклад використання у коді**:
    
  ```python
        print(str(user))
  ```
##### `get_user_id(self)`

Повертає ID користувача.
* **Приклад використання у коді**:
    
  ```python
        uid = user.get_user_id()
  ```
##### `get_full_name(self)`

Повертає повне ім'я користувача.
* **Приклад використання у коді**:
    
  ```python
        print(user.get_full_name())  # Taras Bulba
  ```
##### `add_account(self, account: (Cheking_account, Savings_account, Credit_account)) -> None`

Додає рахунок до списку рахунків користувача.

* **Можливі помилки**:
    * `TypeError`: Якщо account має невірний тип.
* **Приклад використання у коді**:
    
  ```python
        user.add_account(acc)
  ```
# Дякуємо що користуєтеся нашою системою 