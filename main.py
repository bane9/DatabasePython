import sys
sys.path.append('DataManager')

from PySide2 import QtWidgets, QtGui, QtCore
import sys
from WorkspaceWidget import WorkspaceWidget
from StudentMetadata import student_metadata
from MySqlHandler import MySqlHandler

import os
import json

if __name__ == "__main__":

    workspace = None

    def file_clicked(index):
        try:
            if not file_system_model.filePath(index).endswith("_metadata.json"):
                return
            workspace.tables.save_all()
            workspace.tables.storage.load_file(file_system_model.filePath(index))
            workspace.tables.metadata = workspace.tables.storage.metadata
            workspace.reset_tables()
        except Exception as e:
            print(e)

    def attempt_db_connect(parent, host, username, passw):
        try:
            workspace.tables.database_login(host, username, passw, student_metadata)
            workspace.reset_tables()
            msg = QtWidgets.QMessageBox()
            msg.setText("Ok")
            msg.setWindowTitle("Ok")
            msg.setIcon(QtWidgets.QMessageBox.Icon().Information)
            msg.exec_()
            if parent:
                parent.close()
        except Exception as e:
            print(e)

    def db_connect_menu():
        subWindow = QtWidgets.QDialog(main_window)
        subWindow.setModal(True)
        subWindow.resize(320, 100)
        subWindow.setWindowTitle("Database")
        layout = QtWidgets.QVBoxLayout()
        subWindow.setLayout(layout)
        host = QtWidgets.QLineEdit()
        layout.addWidget(host)
        username = QtWidgets.QLineEdit()
        layout.addWidget(username)
        passw = QtWidgets.QLineEdit()
        passw.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        layout.addWidget(passw)
        host.setText("127.0.0.1")
        username.setText("root")
        passw.setText("pass")
        button = QtWidgets.QPushButton()
        button.setText("Connect to database")
        button.clicked.connect(lambda : attempt_db_connect(subWindow, host.text(), username.text(), passw.text()))
        layout.addWidget(button)
        subWindow.show()

    def add_file(filepath, parent, file_type):
        try:
            filename = os.path.basename(filepath)
            path = filename[:-len(filename)]
            workspace.tables.new_file(path, filename, file_type, student_metadata)
            workspace.tables.load_file(filepath + "_metadata.json")
            workspace.tables.metadata = workspace.tables.storage.metadata
            workspace.reset_tables()
            msg = QtWidgets.QMessageBox()
            msg.setText("Ok")
            msg.setWindowTitle("Ok")
            msg.setIcon(QtWidgets.QMessageBox.Icon().Information)
            msg.exec_()
            parent.close()
        except Exception as e:
            print(e)
            QtWidgets.QErrorMessage(parent).showMessage("Creating the file failed", "Error")

    def add_file_menu(index = None):
        subWindow = QtWidgets.QDialog(main_window)
        subWindow.setModal(True)
        subWindow.resize(320, 100)
        layout = QtWidgets.QVBoxLayout()
        subWindow.setLayout(layout)
        textBox = QtWidgets.QLineEdit()
        layout.addWidget(textBox)
        button = QtWidgets.QPushButton()
        button.setText("Add file")
        seqfh_radio = QtWidgets.QRadioButton("Sequential", subWindow)
        serialfh_radio = QtWidgets.QRadioButton("Serial", subWindow)
        layout_radio = QtWidgets.QHBoxLayout()
        seqfh_radio.toggle()
        layout_radio.addWidget(seqfh_radio)
        layout_radio.addWidget(serialfh_radio)
        button.clicked.connect(lambda : add_file(textBox.text(), subWindow,
        "sequential" if seqfh_radio.isDown() else "serial"))
        layout.addWidget(button)
        layout.addLayout(layout_radio)
        subWindow.show()

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    main_window.resize(640, 480)
    main_window.setWindowTitle("Editor")

    def closeEvent(event):
        try:
            if workspace.tables.storage.db:    
                workspace.tables.save_all()
                state = workspace.tables.storage.get_state()
                row = workspace.tables[0]["table"].selectionModel().selectedRows()
                if row and row[0]:
                    state["primary_selected"] = row[0].row()
                    state["secondary_tab_index"] = workspace.tab_widget.currentIndex()

                with open("state.json", "w") as F:
                    json.dump(state, F, indent=1)

        except Exception as e:
            print(e)
        finally:
            event.accept()

    main_window.closeEvent = closeEvent

    menu_bar = QtWidgets.QMenuBar(main_window)
    
    file_menu = QtWidgets.QMenu("File", menu_bar)
    edit_menu = QtWidgets.QMenu("Edit", menu_bar)
    view_menu = QtWidgets.QMenu("View", menu_bar)
    help_menu = QtWidgets.QMenu("Help", menu_bar)

    menu_bar.addMenu(file_menu)
    menu_bar.addMenu(edit_menu)
    menu_bar.addMenu(view_menu)
    menu_bar.addMenu(help_menu)

    tool_bar = QtWidgets.QToolBar(main_window)

    central_widget = QtWidgets.QTabWidget(main_window)
    workspace = WorkspaceWidget(central_widget, main_window)
    central_widget.addTab(workspace, "Table view")
    
    file_menu.addAction("Create File", add_file_menu)
    file_menu.addAction("Connect to database", db_connect_menu)

    structure_dock = QtWidgets.QDockWidget("Structure dock", main_window)

    file_system_model = QtWidgets.QFileSystemModel()
    file_system_model.setRootPath(QtCore.QDir.currentPath())

    tree_view = QtWidgets.QTreeView()
    tree_view.setModel(file_system_model)

    tree_view.setRootIndex(file_system_model.index(QtCore.QDir.currentPath()))

    structure_dock.setWidget(tree_view)

    tree_view.clicked.connect(file_clicked)

    status_bar = QtWidgets.QStatusBar(main_window)

    central_widget.setTabsClosable(True)

    main_window.setMenuBar(menu_bar)
    main_window.addToolBar(tool_bar)
    main_window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, structure_dock)
    main_window.setCentralWidget(central_widget)
    main_window.setStatusBar(status_bar)
    main_window.show()

    try:
        state = {}
        with open("state.json", "r") as F:
            state = json.load(F)
        if state["type"] == "sql":
            workspace.tables.database_login(state["host"], state["username"], \
                state["password"], student_metadata)
        else:
            workspace.tables.storage.load_file(state["metadata_path"])
            workspace.tables.metadata = workspace.tables.storage.metadata
        workspace.reset_tables()
        if "primary_selected" in state:
            workspace.tables[0]["table"].selectRow(state["primary_selected"])
            workspace._primary_selected(state["primary_selected"])
            workspace.tab_widget.setCurrentIndex(state["secondary_tab_index"])
    except Exception as e:
        print(f"Loading config file failed:\n\t{e}")

    sys.exit(app.exec_())
