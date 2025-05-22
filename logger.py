import datetime
import os

class Logger:

    def __init__(self, filename : str= "banksystem.log", create : bool = True) -> None:
        if not isinstance(filename, str) and isinstance(create, bool):
            raise TypeError("Не правильні типи данних в назві файлу та заченні створеннні файлу")

        self.filename = filename
        if create and not os.path.exists(filename):
            with open(filename, "w") as file:
                file.write("=== Bank System Log ===\n")

    def _write(self, level : str, message : str):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{now} [{level.upper()}] {message}\n"
        with open(self.filename, "a") as file:
            file.write(entry)


    def info(self, message: str):
        self._write("INFO", message)

    def warning(self, message: str):
        self._write("WARNING", message)

    def error(self, message: str):
        self._write("ERROR", message)

    def exception(self, message: str, exc: Exception):
        self._write("EXCEPTION", f"{message}: {type(exc).__name__} - {exc}")



