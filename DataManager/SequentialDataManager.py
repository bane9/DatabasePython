from FileDataManager import FileDataManager

class SequentialDataManager(FileDataManager):

    def __init__(self):
        super().__init__()
        self.metadata["type"] = "sequential"

    def add(self, val, db_index = 0):
        for i, x in enumerate(self.data[db_index]):
            if x > val:
                self.data[db_index].insert(i, val)
                return
        self.data[db_index].append(val)

    def _search(self, key, db_index = 0):
        start = 0
        end = len(self.data[db_index])

        while start < end: 
            mid = start + (end - start) // 2
            if self._getkey(db_index, mid) == key: return mid  
            elif self._getkey(db_index, mid): start = mid + 1
            else: end = mid - 1
        
        return None
