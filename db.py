# File Methods

import json
from pathlib import Path
BASE_DIR = Path(__file__).parent

class JSONFile:

    def __init__(self, file_name):
        self.file_path = self.create_file(BASE_DIR, file_name)

    def create_file(self, BASE_DIR, file_name):

        path = BASE_DIR / file_name
        if not path.exists():
            with open(path, "x") as f:
                pass
        return path
    
    def read_all(self):

        with open(self.file_path, "r") as f:

            data = json.load(f)
            return data
        
    def write_all(self, data):

        with open(self.file_path,"w") as f:

            json.dump(data, f, indent = 4)
            return True

# Counter

class CounterFile:

    def __init__(self):
        self.json_handler = JSONFile("counter.json")
        self.config = ConfigFile()
        self.initialize_file()

    def initialize_file(self):
        
        try:
            self.json_handler.read_all()

        except:
            data = self.__initial_data()
            self.json_handler.write_all(data)
            return True
        
    def __initial_data(self):

        start_values = self.config.get_start_values()

        data = {
    "order": start_values["order"],
    "user": start_values["user"],
    "invoice": start_values["invoice"]
}
        return data

    def add_counter(self, new_id_type):
        
        data = self.json_handler.read_all()
        for id_type, config in new_id_type.items():
            data[id_type] = config["start_value"]
        
        self.json_handler.write_all(data)
        
        return True
               
    def delete_counter(self, id_type):

        data = self.json_handler.read_all()
        del data[id_type]

        self.json_handler.write_all(data)
        return True
    
    def reset_counter(self, id_type, start_value):

        data = self.json_handler.read_all()

        data[id_type] = start_value
        self.json_handler.write_all(data)
        return True

        

# Configuration

class ConfigFile:

    def __init__(self):
        self.json_handler = JSONFile("config.json")
        self.initialize_file()

    def initialize_file(self):

        try:
            self.json_handler.read_all()

        except:
            data = self.__initial_data()
            self.json_handler.write_all(data)
            return True
        

    def get_start_values(self):

        data = self.json_handler.read_all()
        id_types = data["id_types"]

        start_values = dict()
        for id_type, config in id_types.items():
            start_values[id_type] = config["start_value"]
        return start_values
    
    def get_id_type_info(self, id_type):

        data = self.json_handler.read_all()
        config = data["id_types"][id_type]
        return config

    def get_increment_step(self, id_type):

        data = self.json_handler.read_all()
        step = data["id_types"][id_type]["increment_step"]
        return step
    
    def get_prefix(self, id_type):

        data = self.json_handler.read_all()
        prefix = data["id_types"][id_type]["prefix"]
        return prefix
    
    def __initial_data(self):

        data = {
    "id_types": {
        "order": {
            "start_value": 1000,
            "increment_step": 1,
            "prefix": "ORD-",
            "padding": 10
        },
        "user": {
            "start_value": 1000,
            "increment_step": 1,
            "prefix": "USER-",
            "padding": 10
        },
        "invoice": {
            "start_value": 1000,
            "increment_step": 1,
            "prefix": "INV-",
            "padding": 10
        }
    }
}
        return data
    
    def add_config(self, new_id_type: dict):

        data = self.json_handler.read_all()
        for id_type, config in new_id_type.items():
            data["id_types"][id_type] = config
        

        self.json_handler.write_all(data)
        return True
    
    def update_config(self, id_type, updated_config):

        data = self.json_handler.read_all()
        for key, value in updated_config.items():
            data["id_types"][id_type][key] = value

        self.json_handler.write_all(data)
        return True
    
    def delete_id_type(self, id_type):

        data = self.json_handler.read_all()
        del data["id_types"][id_type]

        self.json_handler.write_all(data)

        return True