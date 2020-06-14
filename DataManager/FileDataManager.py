from DataManager import DataManager
import json

class FileDataManager(DataManager):

    def __init__(self):
        super().__init__()

    def add(self, val, db_index = 0):
        raise NotImplementedError()

    def _search(self, key, db_index = 0):
        raise NotImplementedError()

    def get(self, db_index, **kwargs):
        key = ""
        for x in kwargs.values():
            key += x
        if len(kwargs) > 1 or db_index == 0:
            idx = self._search(key, db_index)
            if idx is None:
                raise ValueError("Key not in the database")
            return self.data[db_index][idx]
        else:
            out = []
            for x in self.data[db_index]:
                if x[0] == key:
                    out.append(x)
            return out


    def modify(self, db_index, value, **kwargs):
        key = ""
        for x in kwargs.values():
            key += x
        newKey = self._get_key_from_list(db_index, value)
        if self._search(newKey, db_index) is not None and key != newKey:
            raise ValueError("Key already exists")
        idx = self._search(key, db_index)
        if idx is not None:
            self.data[db_index][idx] = value

    def delete(self, db_index, **kwargs):
        key = ""
        for x in kwargs.values():
            key += x
        if len(kwargs) > 1 or db_index == 0:
            idx = self._search(key, db_index)
            if idx is not None:
                self.data[db_index].pop(idx)
        else:
            i = 0
            while i < len(self.data[db_index]):
                if self.data[db_index][i][0] == key:
                  self.data[db_index].pop(i)
                else:
                    i += 1  

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

    def _get_key_from_list(self, db_index, list):
        key = ""
        for x in self.metadata["search_combine_columns"][db_index]:
            key += list[x]
        return key
