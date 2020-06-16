from SerialDataManager import SerialDataManager
from SequentialDataManager import SequentialDataManager
from DatabaseDataManager import DatabaseDataManager
from MySqlHandler import MySqlHandler
import os
import json

class DataDistributor:

    def __init__(self):
        self.db = None
        self.metadata = {
            "database_names" : [],
	        "database_column_names" : [],
            "search_combine_columns" : []
        }
        self.current_filepath = ""
        self.current_filename = ""

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
        self.metadata = metadata
        self.db.load_direct()
        self.metadata["database_names"] = metadata["database_names"]
        self.metadata["database_column_names"] = metadata["database_column_names"]
        self.metadata["search_combine_columns"] = metadata["search_combine_columns"]
        self.current_filename = os.path.basename(metadata_filepath)
        self.current_filepath = self.current_filename[:-len(self.current_filename)]
        self.current_filename = self.current_filename[:-len("_metadata.json")]

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
    
    def save(self, **kwargs):
        if kwargs:
            self.current_filepath = kwargs["path"]
            self.current_filename = kwargs["name"]
        
        if self.db is not None and type(self.db) is not DatabaseDataManager:
            self.db.save(self.current_filepath, self.current_filename)
    
    def get_state(self):
        state = {}
        if type(self.db) is DatabaseDataManager:
            state["type"] = "sql"
            state["host"] = MySqlHandler.host
            state["username"] = MySqlHandler.username
            state["password"] = MySqlHandler.password
            state["schema"] = MySqlHandler.schema
        else:
            state["type"] = "serial" if type(self.db) is SerialDataManager else "sequential"
            state["metadata_path"] = self.current_filepath + self.current_filename + "_metadata.json"
        
        return state
