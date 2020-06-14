from SerialDataManager import SerialDataManager
from SequentialDataManager import SequentialDataManager
from DatabaseDataManager import DatabaseDataManager
from MySqlHandler import MySqlHandler
from os import path
import json

class DataDistributor:

    def __init__(self):
        self.db = None
        self.metadata = {
            "database_names" : [],
	        "database_column_names" : [],
            "search_combine_columns" : []
        }

    def connect_to_sql(self, host, username, password):
        MySqlHandler.connect(host, username, password)
        if type(self.db) is not DatabaseDataManager:
            self.db = DatabaseDataManager()

    def load_file(self, metadata_filepath):
        metadata = None
        with open(metadata_filepath, "r") as F:
            metadata = json.load(F)
        if metadata["type"] == "serial":
            self.db = SerialDataManager()
        else:
            self.db = SequentialDataManager()
        self.db.metadata = metadata
        self.db.load_direct()
        self.metadata["database_names"] = metadata["database_names"]
        self.metadata["database_column_names"] = metadata["database_column_names"]

    def set_metadata(self, metadata):
        if self.db:
            self.db.metadata["database_names"] = metadata["database_names"]
            self.db.metadata["database_column_names"] = metadata["database_column_names"]
            self.db.metadata["search_combine_columns"] = metadata["search_combine_columns"]
            for _ in range(len(metadata["database_names"])):
                self.db.data.append([])
            if "schema_name" in metadata:
                MySqlHandler.schema = metadata["schema_name"]
        self.metadata = metadata

    def new(self, data_type):
        if data_type == "sql":
            self.db = DatabaseDataManager()
        elif data_type == "serial":
            self.db = SerialDataManager()
        else:
            self.db = SequentialDataManager()
    
    def save(self, path, name):
        if self.db is not None and type(self.db) is not DatabaseDataManager:
            self.db.save(path, name)
    
