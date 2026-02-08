# File Methods

import json
from pathlib import Path
BASE_DIR = Path(__file__).parent

class JSONFile:

    def __init__(self):
        self.file_path = self.create_file(BASE_DIR)

    def create_file(self, BASE_DIR):

        path = BASE_DIR / "counter.json"
        if not path.exists():
            with open(path, "x") as f:
                json.dump({"counter":0},f)
        return path
    
    def read_all(self):

        try:
            with open(self.file_path, "r") as f:

                data = json.load(f)
                return data
            
        except Exception as e:
            print(f"[SOME ERROR OCCURED] : {str(e)}")
        

    def write_all(self, data):

        try:
            with open(self.file_path,"w") as f:

                json.dump(data, f, indent = 4)
                return True
        except Exception as e:
            print(f"[SOME ERROR OCCURED] : {str(e)}")

            
    def get_counter(self):

        try:
            data = self.read_all()

            return data["counter"]
        except Exception as e:
            print(f"[SOME ERROR OCCURED] : {str(e)}")

    
    def update_counter(self, new_value):

        data = self.read_all()
        data['counter'] = new_value

        self.write_all(data)


# ID Generator

class IDGenerator:

    def __init__(self):
        self.json = JSONFile()

    def generate(self):

        try:

            data = self.json.read_all()

            if data is None:
                return False
            
            data["counter"] += 1
            self.json.write_all(data)
            counter = data["counter"]

            return f"{counter:05d}"
        
        except:
            print(f"SOME ERROR OCCURED, Try again later...")

