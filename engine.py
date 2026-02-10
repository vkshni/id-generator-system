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
        
