from MySqlHandler import MySqlHandler
from DataManager import DataManager

class DatabaseDataManager(DataManager):
    
    def __init__(self):
        super().__init__()

    def __exec(self, sql_generator):
        for _ in sql_generator:
            pass

    def schema_init(self):
        query = f"CREATE SCHEMA IF NOT EXISTS {MySqlHandler.schema};"
        for i in range(len(self.metadata["database_names"])):
            if i == 0:
                query += f"CREATE TABLE IF NOT EXISTS {MySqlHandler.schema}.{self.metadata['database_names'][0]} (\n"
                for x in self.metadata["database_column_names"][0]:
                    query += f"`{x}` VARCHAR(45) NOT NULL,\n"
                query += f"PRIMARY KEY (`{self.metadata['database_column_names'][0][0]}`));\n"
            else:
                query += f"CREATE TABLE IF NOT EXISTS {MySqlHandler.schema}.{self.metadata['database_names'][i]} ("
                for x in self.metadata["database_column_names"][i]:
                    query += f"`{x}` VARCHAR(45) NOT NULL,\n"
                query += f'''
                    INDEX `fk{i}_idx` (`{self.metadata["database_column_names"][0][0]}` ASC) VISIBLE,
                    CONSTRAINT `fk{i}`
                        FOREIGN KEY (`{self.metadata["database_column_names"][0][0]}`)
                        REFERENCES {MySqlHandler.schema}.{self.metadata["database_names"][0]} (`{self.metadata["database_column_names"][0][0]}`));''' 

        self.__exec(MySqlHandler.db.cursor().execute(query, multi=True))

    def add(self, val, db_index = 0):
        query = f"INSERT INTO {MySqlHandler.schema}.{self.metadata['database_names'][db_index]} ("
        for i, x in enumerate(self.metadata["database_column_names"][db_index]):
            query += x
            if i != len(self.metadata["database_column_names"][db_index]) - 1:
                query += ","
        query += ") VALUES("
        for i, x in enumerate(val):
            query += f"'{x}'"
            if i != len(val) - 1:
                query += ","
        query += ");"
        MySqlHandler.db.cursor().execute(query)
        MySqlHandler.db.commit()

    def get(self, key, db_index = 0):
        cursor = MySqlHandler.db.cursor()
        cursor.execute(f"SELECT * FROM {MySqlHandler.schema}.{self.metadata['database_names'][db_index]} \
            WHERE {self.metadata['database_column_names'][db_index][0]}='{key}';")
        return cursor.fetchall()

    def delete(self, key, db_index = 0):
        raise NotImplementedError()

    def modify(self, key, value, db_index = 0):
        raise NotImplementedError()

    def search(self, keypart, row_index = 0, db_index = 0):
        raise NotImplementedError()

    def search_all_keys(self, key, db_index = -1):
        raise NotImplementedError()
