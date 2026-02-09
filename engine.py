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
            start_value = self.config.get_start_value()
            data = {
                "counter" : start_value
            }
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
            data = {
                "start_value" : 1000,
                "increment_step" : 1
                }
            
            self.json_handler.write_all(data)
            return True
        
    def get_start_value(self):

        data = self.json_handler.read_all()
        return data["start_value"]
    
    def change_start_value(self, new_value):

        data = self.json_handler.read_all()

        data["start_value"] = new_value

        self.json_handler.write_all(data)

# ID Generator

class IDGenerator:

    def __init__(self):
        self.counter = CounterFile()
        self.config = ConfigFile()

    def generate(self):

        try:

            data = self.counter.json_handler.read_all()

            if data is None:
                return False
            
            data["counter"] += 1
            self.counter.json_handler.write_all(data)
            counter = data["counter"]

            return f"{counter:05d}"
        
        except:
            return f"SOME ERROR OCCURED, Try again later..."
        
    def set_counter_zero(self):

        try:

            data = self.json.read_all()

            if data is None:
                return False
            
            data["counter"] = 0
            self.json.write_all(data)

            return None
        
        except:
            return f"SOME ERROR OCCURED, Try again later..."
        
