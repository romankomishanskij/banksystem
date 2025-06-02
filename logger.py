import datetime
import os

class Logger:
    """
    Модуль logger містить клас для логування подій у системі.

    Класи:
    - Logger: Клас для запису логів у файл.
    """

    def __init__(self, filename : str= "banksystem.log", create : bool = True) -> None:
        """
            Клас для логування подій у файл.

            Атрибути:
            - filename: Ім'я файлу для логування.

            Методи:
            - __init__: Ініціалізує об'єкт логера.
            - _write: Записує повідомлення у файл.
            - info: Записує інформаційне повідомлення.
            - warning: Записує попередження.
            - error: Записує повідомлення про помилку.
            - exception: Записує інформацію про виняток.
        """
        if not isinstance(filename, str) or not isinstance(create, bool):
            raise TypeError("Неправильні типи даних: назва файлу має бути рядком, а create — логічним значенням (bool).")

        self.filename = filename
        if create and not os.path.exists(filename):
            with open(filename, "w") as file:
                file.write("=== Bank System Log ===\n")

    def _write(self, level : str, message : str):
        """
            Записує повідомлення у файл логу.

            Аргументи:
                level (str): Рівень логу (INFO, WARNING, ERROR, EXCEPTION).
                message (str): Текст повідомлення.
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{now} [{level.upper()}] {message}\n"
        with open(self.filename, "a") as file:
            file.write(entry)


    def info(self, message: str):
        """
            Записує інформаційне повідомлення та вказує рівень логу.

            Аргументи:
                message (str): Текст повідомлення.
        """
        self._write("INFO", message)

    def warning(self, message: str):
        """
            Записує інформаційне повідомлення та вказує рівень логу.

            Аргументи:
                message (str): Текст повідомлення.
        """
        self._write("WARNING", message)

    def error(self, message: str):
        """
            Записує інформаційне повідомлення та вказує рівень логу.

            Аргументи:
                message (str): Текст повідомлення.
        """
        self._write("ERROR", message)

    def exception(self, message: str, exc: Exception):
        """
            Записує інформаційне повідомлення та вказує рівень логу.

            Аргументи:
                message (str): Текст повідомлення.
                exc (Exception): Об'єкт винятку.
        """
        self._write("EXCEPTION", f"{message}: {type(exc).__name__} - {exc}")

log = Logger()


