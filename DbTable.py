import sys
sys.path.append('DataManager')

from DbTableModel import DbTableModel
from DataDistributor import DataDistributor
from PySide2 import QtWidgets, QtGui, QtCore

class DbTable:

    def __init__(self):
        self.storage = DataDistributor()
        self.metadata = None
        self.primary_table = {}
        self.secondary_tables = []
        self.current_filepath = ""
        self.current_filename = ""
    
    def load_file(self, metadata_filepath : str):
        if not metadata_filepath.endswith("_metadata.json"):
            raise ValueError("Path does not end with .json")
        if self.storage is not None:
            self.storage.save(self.current_filepath, self.current_filename)
        self.storage.load_file(metadata_filepath)
        self.metadata = self.storage.metadata

    def database_login(self, host, username, password, metadata):
        self.metadata = metadata
        self.storage.connect_to_sql(host, username, password)
        self.storage.set_metadata(metadata)
        self.storage.db.schema_init()
    
    def new_file(self, path, name, data_type, metadata):
        self.current_filepath = path
        self.current_filename = name
        self.storage.new(data_type)
        self.storage.set_metadata(metadata)
        self.metadata = metadata
    
    def form_tables(self, table_parnet = None, model_parent = None):
        if self.primary_table:
            self.primary_table["data"].storage.save(self.current_filepath, self.current_filename)
        
        for x in self.secondary_tables:
            x["data"].storage.save(self.current_filepath, self.current_filename)

        self.primary_table = {}
        self.secondary_tables = []

        metadata = self.metadata
        metadata["db_index"] = 0
        self.primary_table["table_name"] = self.metadata["database_names"][0]
        self.primary_table["data"] = DbTableModel(model_parent)
        self.primary_table["data"].set_local_info(metadata, self.storage.db)
        self.primary_table["table"] = QtWidgets.QTableView(table_parnet)
        self.primary_table["table"].setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.primary_table["table"].setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.primary_table["table"].setModel(self.primary_table["data"])

        for i in range(1, len(self.metadata["database_names"])):
            table = {}
            metadata["db_index"] = i
            table["table_name"] = self.metadata["database_names"][i]
            table["data"] = DbTableModel(model_parent)
            table["data"].set_local_info(metadata, self.storage.db)
            table["table"] = QtWidgets.QTableView(table_parnet)
            table["table"].setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            table["table"].setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            table["table"].setModel(self.primary_table["data"])
            self.secondary_tables.append(table)

