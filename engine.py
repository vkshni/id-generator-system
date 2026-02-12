from db import CounterFile, ConfigFile
from keyword import kwlist

# ID Generator

class IDGenerator:

    def __init__(self):
        self.counter = CounterFile()
        self.config = ConfigFile()

    def generate(self, id_type):

        try:

            counter_data = self.counter.json_handler.read_all()
            config_data = self.config.get_id_type_info(id_type)

            if counter_data is None:
                return False
            
            counter_data[id_type] += config_data["increment_step"]
            
            self.counter.json_handler.write_all(counter_data)
            counter = counter_data[id_type]
            prefix = config_data["prefix"]
            padding = int(config_data["padding"])

            return f"{prefix}{counter:0{padding}d}"
        
        except:
            return f"SOME ERROR OCCURED, Try again later..."
        
    def add_id_type(self, id_type, start_value, increment_step, prefix, padding):

        self.validate_id_type_name(id_type)

        config_data = self.config.json_handler.read_all()
        if id_type in config_data["id_types"]:
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

        self.validate_id_type_name(id_type)
        
        config_data = self.config.json_handler.read_all()
        if not id_type in config_data["id_types"]:
            raise ValueError(f"ID type '{id_type}' not found")
        
        updated_config = kwrgs
        self.config.update_config(id_type, updated_config)

        return True
    
    def delete_id_type(self, id_type, force = False):

        self.validate_id_type_name(id_type)

        config_data = self.config.json_handler.read_all()
        if not id_type in config_data["id_types"]:
            raise ValueError(f"ID type '{id_type}' not found")
        
        counter_data = self.counter.json_handler.read_all()
        current_count = counter_data.get(id_type, 0)
        start_value = config_data["id_types"][id_type]["start_value"]

        if current_count > start_value and not force:
            ids_generated = current_count - start_value
            raise ValueError(f"Cannot delete ID - {ids_generated} IDs generated")
        
        self.config.delete_id_type(id_type)
        self.counter.delete_counter(id_type)

        return True
    
    def reset_counter(self, id_type, force = False):
        
        self.validate_id_type_name(id_type)

        config_data = self.config.json_handler.read_all()
        if not id_type in config_data["id_types"]:
            raise ValueError(f"ID type '{id_type}' not found")
        
        counter_data = self.counter.json_handler.read_all()
        current_count = counter_data.get(id_type, 0)
        start_value = config_data["id_types"][id_type]["start_value"]

        if current_count > start_value and not force:
            ids_generated = current_count - start_value
            raise ValueError(f"Cannot reset ID - {ids_generated} IDs generated")
        
        self.counter.reset_counter(id_type, start_value)
        return True
    
    def validate_id_type_name(self, id_type):

        if not id_type or id_type.isspace():
            raise ValueError("Empty ID")
        
        if not all(c.isalnum() or c == "_" for c in id_type):
            raise ValueError("Only alphanumeric and underscore allowed")
        
        if len(id_type) < 3 or len(id_type) > 50:
            raise ValueError("Length of name should be lesser than 50 and greater or equal to 3")
        
        if id_type in kwlist:
            raise ValueError("Reserved words cannot be used")
        
        return True


        
