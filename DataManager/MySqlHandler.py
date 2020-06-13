import mysql.connector

class MySqlHandler:
    __db = None
    __host = ""
    __username = ""
    __password = ""

    def __init__(self, hostname = "", user = "", passw = ""):
        if hostname == "" or user == "" or passw == "": 
            return
        
        self.connect(hostname, user, passw)

    def isConnected(self) -> bool:
        if MySqlHandler.__db is None: return False
        else: return MySqlHandler.__db.is_connected()

    
    def dissconnect(self) -> None:
        if self.isConnected():
           MySqlHandler.__db.dissconnect()

    def connect(self, hostname : str, username : str, passw : str) -> None:
        if MySqlHandler.__host == hostname and MySqlHandler.__username == username and MySqlHandler.__password == passw \
            and self.isConnected():
            return
        else:
            MySqlHandler.__db = mysql.connector.connect(host=hostname, user=username, password=passw)
            MySqlHandler.__host = hostname
            MySqlHandler.__username = username
            MySqlHandler.__password = passw

    def __call__(self):
        if not self.isConnected():
            raise Exception("Not connected")
        else: return MySqlHandler.__db
