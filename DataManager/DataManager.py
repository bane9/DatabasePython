class DataManager:

    def __init__(self):
        self.data = []
        self.metadata = {
            "databases" : 0,
	        "database_column_names" : [],
            "search_combine_columns" : [],
	        "type" : "",
	        "linked_file" : ""
        }

    def add(self, val, db_index = 0):
        raise NotImplementedError()

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

    def search_all_keys(self, key, db_index = 0):
        raise NotImplementedError()

    def save(self, path, name):
        pass

    def load(self, path, name):
        pass