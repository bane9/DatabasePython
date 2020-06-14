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
        end = len(self.data[db_index]) - 1

        while start <= end: 
            mid = start + (end - start) // 2
            search_key = self._getkey(db_index, mid)
            if search_key == key: return mid  
            elif search_key: start = mid + 1
            else: end = mid - 1
        
        return None
