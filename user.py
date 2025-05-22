import datetime

class User:
    __id = 1

    @classmethod
    def change_id(cls):
        cls.__id += 1
        return cls.__id - 1

    def __init__(self, user_name : str, user_last_name : str) -> None :
        self.__user_id = User.change_id()
        self.__user_name = user_name
        self.__user_last_name = user_last_name
        self.list_of_accounts = []

    def __str__(self):
        return f"{self.__user_id} - {self.__user_name} {self.__user_last_name}"







