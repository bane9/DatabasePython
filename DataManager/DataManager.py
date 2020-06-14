class DataManager:

    def __init__(self):
        self.data = []
        self.metadata = {
            "database_names" : [],
	        "database_column_names" : [],
            "search_combine_columns" : [],
	        "type" : "",
	        "linked_file" : ""
        }

    def add(self, val, db_index = 0):
        raise NotImplementedError()

    def get(self, key, db_index = 0):
        raise NotImplementedError()

    def delete(self, db_index, **kwargs):
        raise NotImplementedError()

    def modify(self, db_index, value, **kwargs):
        raise NotImplementedError()

    def search(self, keypart, row_index = 0, db_index = 0):
        raise NotImplementedError()

    def _search(self, key, db_index = 0):
        raise NotImplementedError()

    def save(self, path, name):
        pass

    def load(self, path, name):
        pass