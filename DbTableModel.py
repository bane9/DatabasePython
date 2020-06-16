from PySide2 import QtWidgets, QtCore

class DbTableModel(QtCore.QAbstractTableModel):
    def __init__(self, db_index, parent = None, foreign_key = None):
        super().__init__(parent)
        self.metadata = None
        self.storage = None
        self.localdata = []
        self.db_index = db_index
        self.foreign_key = foreign_key
    
    def set_local_info(self, metadata, data_distributor):
        self.beginResetModel()
        self.metadata = metadata
        self.data_distributor = data_distributor
        self.storage = data_distributor.db
        self.fetchlocal()
        self.endResetModel()

    def get_element(self, index):
        return self.localdata[index.row()]

    def rowCount(self, index):
        return len(self.localdata)

    def columnCount(self, index):
        return len(self.metadata["database_column_names"][self.db_index]) - self._db_offset()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return self.localdata[index.row()][index.column() + self._db_offset()]

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.metadata["database_column_names"][self.db_index][section + self._db_offset()]

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole and value:
            try:
                offset = self._db_offset()
                self.localdata[index.row()][index.column() + offset] = value
                self.storage.modify(self.db_index, self.localdata[index.row()], **self._getkey(index.row()))
                self.fetchlocal()
                return True
            except Exception as e:
                print(e)
                return False

        return False
    
    def delete(self, row):
        try:
            self.beginRemoveRows(QtCore.QModelIndex(), 0, 0)
            self.storage.delete(self.db_index, **self._getkey(row))
            self.fetchlocal()
        except:
            raise
        finally:
            self.endRemoveRows()

    def append(self, data):
        try:
            self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
            self.storage.add(data, self.db_index)
            self.fetchlocal()
        except:
            raise
        finally:
            self.endInsertRows()

    def _getkey(self, index):
        key = {}
        for x in self.metadata["search_combine_columns"][self.db_index]:
            key[self.metadata["database_column_names"][self.db_index][x]] = self.localdata[index][x]
        return key

    def _db_offset(self):
        return 0 if self.db_index == 0 else 1

    def fetchlocal(self):
        if self.foreign_key is None:
            self.localdata = self.storage.get_all(self.db_index)
        else:
            self.localdata = [x for x in self.storage.get_all(self.db_index) if x[0] == self.foreign_key]

    def flags(self, index):
        return super().flags(index) | QtCore.Qt.ItemIsEditable
