class Bank:
    def __init__(self, name : str, address : str):
        self._name = name
        self._address = address
        self._list_of_users = []
        self._list_of_accounts = []
