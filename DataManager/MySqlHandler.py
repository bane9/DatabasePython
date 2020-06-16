import mysql.connector

class MySqlHandler:
    db = None
    host = ""
    username = ""
    password = ""
    schema = "3vsZG0Al7YM84Qmc"

    @staticmethod
    def isConnected() -> bool:
        if MySqlHandler.db is None: return False
        else: return MySqlHandler.db.is_connected()

    @staticmethod
    def dissconnect() -> None:
        if MySqlHandler.isConnected():
           MySqlHandler.db.dissconnect()

    @staticmethod
    def connect(hostname : str, username : str, passw : str) -> None:
        if MySqlHandler.host == hostname and MySqlHandler.username == username and MySqlHandler.password == passw \
            and MySqlHandler.isConnected():
            return
        else:
            MySqlHandler.db = mysql.connector.connect(host=hostname, user=username, password=passw)
            MySqlHandler.host = hostname
            MySqlHandler.username = username
            MySqlHandler.password = passw

