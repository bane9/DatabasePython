import mysql.connector

class MySqlHandler:
    db = None
    __host = ""
    __username = ""
    __password = ""
    schema = "uni_proj_189"

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
        if MySqlHandler.__host == hostname and MySqlHandler.__username == username and MySqlHandler.__password == passw \
            and MySqlHandler.isConnected():
            return
        else:
            MySqlHandler.db = mysql.connector.connect(host=hostname, user=username, password=passw)
            MySqlHandler.__host = hostname
            MySqlHandler.__username = username
            MySqlHandler.__password = passw

