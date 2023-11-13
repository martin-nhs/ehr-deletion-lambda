class DatabaseConnection:
    def __init__(self, database_name: str, hostname: str, username: str, password: str, port: int):
        self._database_name = database_name
        self._hostname = hostname
        self._username = username
        self._password = password
        self._port = port

    @property
    def connection_dictionary(self) -> dict:
        return {
            "host": self._hostname,
            "user": self._username,
            "password": self._password,
            "port": self._port,
            "database": self._database_name
        }
