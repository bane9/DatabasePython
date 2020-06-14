from PySide2 import QtWidgets, QtGui, QtCore
from DbTable import DbTable

class WorkspaceWidget(QtWidgets.QWidget):

    def __init__(self, parent, main_window):
        super().__init__(parent)

        self.main_window = main_window
        self.parent = parent

        self.main_layout = QtWidgets.QVBoxLayout()
        self.tab_widget = None

        self.create_tab_widget()

        self.tables = DbTable()

    def reset_tables(self):
        self.tables.form_tables()

        horizontalStudentTable = QtWidgets.QHBoxLayout()
        addStudentButton = QtWidgets.QPushButton()
        addStudentButton.setText("+")
        addStudentButton.clicked.connect(lambda : None)

        removeStudentButton = QtWidgets.QPushButton()
        removeStudentButton.setText("-")
        removeStudentButton.clicked.connect(lambda : None)

        horizontalStudentTable.addWidget(addStudentButton)
        horizontalStudentTable.addWidget(removeStudentButton)

        verticalStudentTable = QtWidgets.QVBoxLayout()

        verticalStudentTable.addLayout(horizontalStudentTable)
        verticalStudentTable.addWidget(self.tables.primary_table["table"])

        self.main_layout.addLayout(verticalStudentTable)

        for x in self.tables.secondary_tables:
            self.tab_widget.addTab(x["table"], x["table_name"])
        
        horizontalSubjectsTable = QtWidgets.QHBoxLayout()
        addSubjectsButton = QtWidgets.QPushButton()
        addSubjectsButton.setText("+")
        addSubjectsButton.clicked.connect(lambda : None)

        removeSubjectsButton = QtWidgets.QPushButton()
        removeSubjectsButton.setText("-")
        removeSubjectsButton.clicked.connect(lambda : None)

        horizontalSubjectsTable.addWidget(addSubjectsButton)
        horizontalSubjectsTable.addWidget(removeSubjectsButton)

        verticalSubjectsTable = QtWidgets.QVBoxLayout()

        verticalSubjectsTable.addLayout(horizontalSubjectsTable)
        verticalSubjectsTable.addWidget(self.tab_widget)

        self.main_layout.addLayout(verticalSubjectsTable)
        self.setLayout(self.main_layout)
    
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
