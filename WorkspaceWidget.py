from PySide2 import QtWidgets, QtGui, QtCore
from DbTable import DbTable
from DbTableModel import DbTableModel


class WorkspaceWidget(QtWidgets.QWidget):

    def __init__(self, parent, main_window):
        super().__init__(parent)

        self.main_window = main_window
        self.parent = parent

        self.main_layout = QtWidgets.QVBoxLayout()
        self.tab_widget = None

        self.create_tab_widget()

        self.tables = DbTable()

        self.primary_key = ""

    def reset_tables(self):
        for i in reversed(range(self.main_layout.count())):
            layout = self.main_layout.itemAt(i).layout()
            if layout is not None:
                layout.deleteLater()
            widget = self.main_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.tables.form_primary_table()

        self.tables[0]["table"].clicked.connect(self._primary_selected)

        horizontalPrimaryTable = QtWidgets.QHBoxLayout()
        addSecondaryButton = QtWidgets.QPushButton()
        addSecondaryButton.setText("Add")
        addSecondaryButton.clicked.connect(lambda : self._add_dialog())

        removePrimaryButton = QtWidgets.QPushButton()
        removePrimaryButton.setText("Remove")
        removePrimaryButton.clicked.connect(lambda : self._remove_row())

        horizontalPrimaryTable.addWidget(addSecondaryButton)
        horizontalPrimaryTable.addWidget(removePrimaryButton)

        verticalPrimaryTable = QtWidgets.QVBoxLayout()

        verticalPrimaryTable.addLayout(horizontalPrimaryTable)
        verticalPrimaryTable.addWidget(self.tables.primary_table["table"])

        self.main_layout.addLayout(verticalPrimaryTable)
        
        horizontalSecondaryTable = QtWidgets.QHBoxLayout()
        addSecondaryButton = QtWidgets.QPushButton()
        addSecondaryButton.setText("Add")
        addSecondaryButton.clicked.connect(lambda : self._add_dialog(False))

        removeSubjectsButton = QtWidgets.QPushButton()
        removeSubjectsButton.setText("Remove")
        removeSubjectsButton.clicked.connect(lambda : self._remove_row(False))

        horizontalSecondaryTable.addWidget(addSecondaryButton)
        horizontalSecondaryTable.addWidget(removeSubjectsButton)

        verticalSecondaryTable = QtWidgets.QVBoxLayout()

        verticalSecondaryTable.addLayout(horizontalSecondaryTable)
        verticalSecondaryTable.addWidget(self.tab_widget)

        self.main_layout.addLayout(verticalSecondaryTable)
        self.setLayout(self.main_layout)

        while self.tab_widget.count():
            self.tab_widget.removeTab(0)

        self.tab_widget.addTab(QtWidgets.QTableView(None), "")
        self.tab_widget.setTabsClosable(False)

    def _primary_selected(self, index):
        self.primary_key = self.tables[0]["data"].localdata[index.row()][0]
        self.tables.form_secondary_tables(self.primary_key)

        while self.tab_widget.count():
            self.tab_widget.removeTab(0)

        for x in self.tables.secondary_tables:
            self.tab_widget.addTab(x["table"], x["table_name"])

        self.tab_widget.setTabsClosable(True)
    

    def _remove_row(self, primary = True):
        db_index = 0
        if not primary:
            db_index = self.tab_widget.currentIndex() + 1

        if not self.tables.primary_table or not self.tables.secondary_tables or\
             not self.tables[db_index] or not self.tables[db_index]["table"]:
            return

        self.tables[db_index]["table"].selectionModel()

        row = self.tables[db_index]["table"].selectionModel().selectedRows()
        if row:
            row = row[0]

        if not row:
            return

        self.tables[db_index]["data"].delete(row.row())
        if self.tables[db_index]["data"].localdata:
            self._primary_selected(QtCore.QModelIndex())
        else:
            while self.tab_widget.count():
                self.tab_widget.removeTab(0)

    def _add_dialog(self, primary = True):
        if not primary and not self.primary_key:
            return

        db_index = 0
        if not primary:
            db_index = self.tab_widget.currentIndex() + 1
        subWindow = QtWidgets.QDialog(self.main_window)
        subWindow.setModal(True)
        subWindow.resize(450, 300)
        layout = QtWidgets.QVBoxLayout()
        subWindow.setLayout(layout)

        labels = [QtWidgets.QLabel(x) for x in self.tables.metadata["database_column_names"][db_index]]
        textboxes = [QtWidgets.QLineEdit() for _ in range(len(self.tables.metadata["database_column_names"][db_index]))]
        layouts = []
        
        if not primary:
            textboxes[0].setText(self.primary_key)
            textboxes[0].setReadOnly(True)
            textboxes[0].setStyleSheet("QLineEdit { background: rgb(224, 224, 224); }")

        for x, y in zip(labels, textboxes):
            tempLayout = QtWidgets.QHBoxLayout()
            tempLayout.addWidget(x)
            tempLayout.addWidget(y)
            layouts.append(tempLayout)

        #if not primary: layouts.pop(0)

        for x in layouts:
            layout.addLayout(x)
        
        button = QtWidgets.QPushButton()
        button.setText(f"Add into {self.tables.metadata['database_names'][db_index]}")

        try:
            msg = QtWidgets.QMessageBox()
            msg.setText("Ok")
            msg.setWindowTitle("Ok")
            msg.setIcon(QtWidgets.QMessageBox.Icon().Information)
            button.clicked.connect(lambda : (
                self.tables[db_index]["data"].append([x.text() for x in textboxes]),
                msg.exec_(),
                subWindow.close()
            ))
        except Exception as e:
            print(e)
            QtWidgets.QErrorMessage(subWindow).showMessage("Index already exists", "Error")
        layout.addWidget(button)
        subWindow.show()
    
    def create_table(self, rows, columns):
        table_widget = QtWidgets.QTableWidget(rows, columns, self)

        for i in range(rows):
            for j in range(columns):
                table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(f"Row {i}{j}"))
        labels = []
        for i in range(columns):
            labels.append(f"Column {i}")
        table_widget.setHorizontalHeaderLabels(labels)
        return table_widget
    
    def create_tab_widget(self):
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.delete_tab)

    def delete_tab(self, index):
        self.tab_widget.removeTab(index)

    