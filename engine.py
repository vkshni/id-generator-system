from db import CounterFile, ConfigFile

# ID Generator

class IDGenerator:

    def __init__(self):
        self.counter = CounterFile()
        self.config = ConfigFile()

    def generate(self, id_type):

        try:

            data = self.counter.json_handler.read_all()
            info = self.config.get_id_type_info(id_type)

            if data is None:
                return False
            
            data[id_type] += info["increment_step"]
            
            self.counter.json_handler.write_all(data)
            counter = data[id_type]
            prefix = info["prefix"]
            padding = int(info["padding"])

            return f"{prefix}{counter:0{padding}d}"
        
        except:
            return f"SOME ERROR OCCURED, Try again later..."
        
    def add_id_type(self, id_type, start_value, increment_step, prefix, padding):

        data = self.config.json_handler.read_all()
        if id_type in data["id_types"]:
            raise ValueError(f"ID Type{id_type} exists...")
        
        new_id_type = {
            id_type: {
            "start_value": start_value,
            "increment_step": increment_step,
            "prefix": prefix,
            "padding": padding
            }
        }

        self.config.add_config(new_id_type)
        self.counter.add_counter(new_id_type)

        return True
    
    def update_id_type(self, id_type, **kwrgs):
        
        data = self.config.json_handler.read_all()
        if not id_type in data["id_types"]:
            raise ValueError(f"ID type{id_type} doesn't exist...")
        
        updated_config = kwrgs
        self.config.update_config(id_type, updated_config)

        return True


        
