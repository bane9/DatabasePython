from PySide2 import QtWidgets, QtCore

class DbTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.metadata = None
        self.storage = None
        self.localdata = []
    
    def set_local_info(self, metadata, storage):
        self.beginResetModel()
        self.metadata = metadata
        self.storage = storage
        self.fetchlocal()
        self.endResetModel()

    def get_element(self, index):
        return self.localdata[index.row()]

    def rowCount(self, index):
        return len(self.localdata)

    def columnCount(self, index):
        return len(self.metadata["database_column_names"][self.metadata["db_index"]]) - 1

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if index.column() < len(self.localdata[0]):
                return self.localdata[index.row()][index.column()]

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.metadata["database_column_names"][self.metadata["db_index"]][section]

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            try:
                self.localdata[index.row()][index.column()] = value
                self.storage.modify(self.metadata["db_index"], self.localdata[index.row()], **self._getkey(index.row()))
                self.fetchlocal()
                return True
            except Exception as e:
                print(e)
                return False

        return False
    
    def delete(self, row):
        try:
            self.beginRemoveRows(QtCore.QModelIndex(), 0, 0)
            self.storage.delete(self.metadata["db_index"], **self._getkey(row))
            self.fetchlocal()
        except:
            raise
        finally:
            self.endRemoveRows()

    def append(self, data):
        try:
            self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
            self.storage.add(data, self.metadata["db_index"])
            self.fetchlocal()
        except:
            raise
        finally:
            self.endInsertRows()

    def _getkey(self, index):
        key = {}
        for x in self.metadata["search_combine_columns"][self.metadata["db_index"]]:
            key[self.metadata["database_column_names"][self.metadata["db_index"]][x]] = self.localdata[index][x]
        return key

    def fetchlocal(self):
        self.localdata = self.storage.get_all(self.metadata["db_index"]) 

    def flags(self, index):
        return super().flags(index) | QtCore.Qt.ItemIsEditable
