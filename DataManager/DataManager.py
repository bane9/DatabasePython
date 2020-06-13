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

    def add(self, val):
        raise NotImplementedError()

    def get(self, key):
        raise NotImplementedError()

    def delete(self, key):
        raise NotImplementedError()

    def modify(self, key, value):
        raise NotImplementedError()

    def search(self, keypart, row_index = 0):
        raise NotImplementedError()

    def _search(self, key):
        raise NotImplementedError()