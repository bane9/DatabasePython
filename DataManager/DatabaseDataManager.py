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
        for i in range(self.metadata["databases"]):
            if i == 0:
                query += f'''
                    CREATE TABLE IF NOT EXISTS {MySqlHandler.schema}.db0 (\n
                '''
                for x in self.metadata["database_column_names"][0]:
                    query += f"`{x}` VARCHAR(45) NOT NULL,\n"
                query += f"PRIMARY KEY (`{self.metadata['database_column_names'][0][0]}`));\n"
            else:
                query += f'''
                    CREATE TABLE IF NOT EXISTS {MySqlHandler.schema}.db{i} (\n
                '''
                for x in self.metadata["database_column_names"][i]:
                    query += f"`{x}` VARCHAR(45) NOT NULL,\n"
                query += f'''
                    INDEX `fk{i}_idx` (`{self.metadata["database_column_names"][0][0]}` ASC) VISIBLE,
                    CONSTRAINT `fk{i}`
                        FOREIGN KEY (`{self.metadata["database_column_names"][0][0]}`)
                        REFERENCES {MySqlHandler.schema}.db0 (`{self.metadata["database_column_names"][0][0]}`));''' 

        self.__exec(MySqlHandler.db.cursor().execute(query, multi=True))

    def add(self, val, db_index = 0):
        pass

    def get(self, key, db_index = 0):
        raise NotImplementedError()

    def delete(self, key, db_index = 0):
        raise NotImplementedError()

    def modify(self, key, value, db_index = 0):
        raise NotImplementedError()

    def search(self, keypart, row_index = 0, db_index = 0):
        raise NotImplementedError()

    def _search(self, key, db_index = 0):
        raise NotImplementedError()

    def search_all_keys(self, key, db_index = -1):
        raise NotImplementedError()
