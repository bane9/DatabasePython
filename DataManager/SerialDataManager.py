from FileDataManager import FileDataManager

class SerialDataManager(FileDataManager):

    def __init__(self):
        super().__init__()
        self.metadata["type"] = "serial"

    def add(self, val, db_index = 0):
        key = ""
        for x in self.metadata["search_combine_columns"][db_index]:
            key += val[x]
        for i, x in enumerate(self.data[db_index]):
            if self._getkey(db_index, i) == key:
                raise ValueError("Key already exists")
        self.data[db_index].append(val)

    def _search(self, key, db_index = 0):
        for i, _ in enumerate(self.data[db_index]):
            if self._getkey(db_index, i) == key:
                return i
        return None
