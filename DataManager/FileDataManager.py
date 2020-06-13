from DataManager import DataManager
import json

class FileDataManager(DataManager):

    def __init__(self):
        super().__init__()

    def add(self, val, db_index = 0):
        raise NotImplementedError()

    def _search(self, key, db_index = 0):
        raise NotImplementedError()

    def get(self, key, db_index = 0):
        idx = self._search(key, db_index)
        if idx is None:
            raise ValueError("Key not in the database")
        return self.data[db_index][idx]

    def modify(self, key, value, db_index = 0):
        idx = self._search(key, db_index)
        if idx is None:
            raise ValueError("Key not in the database")
        if self._search(value[0]) is not None:
            raise ValueError("Key already exists")
        self.data[db_index][idx] = value

    def search(self, keypart, row_index = 0, db_index = 0):
        out = []
        for x in self.data[db_index]:
            if keypart in x[row_index]:
                out.append(x)
        return out

    def delete(self, key, db_index = 0):
        self.data[db_index].pop(self._search(key, db_index))

    def save(self, path, name):
        filepath = path + name
        json_filepath = filepath + "_metadata.json"
        data_filepath = filepath + "_data.json"
        self.metadata["linked_file"] = data_filepath
        with open(json_filepath, "w") as F:
            json.dump(self.metadata, F, indent=1)
        with open(data_filepath, "w") as F:
            json.dump(self.data, F, indent=1)

    def load(self, metadata_filepath):
        with open(metadata_filepath, "r") as F0:
            self.metadata = json.load(F0)
            with open(self.metadata["linked_file"], "r") as F1:
                self.data = json.load(F1)

    def load_direct(self):
        with open(self.metadata["linked_file"], "r") as F:
            self.data = json.load(F)

    def _getkey(self, db_index, row):
        key = ""
        for x in self.metadata["search_combine_columns"][db_index]:
            key += self.data[db_index][row][x]
        return key
    
    def search_all_keys(self, key, db_index=-1):
        out = []
        if db_index == -1:
            for x in self.data:
                for y in x:
                    if y[0] == key:
                        out.append(y)
        else:
            for x in self.data[db_index]:
                if x[0] == key:
                    out.append(x)
        return out
    