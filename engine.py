from db import CounterFile, ConfigFile
from keyword import kwlist
import threading
import string, random
from exceptions import *
from logger import setup_logger

# ID Generator

class IDGenerator:

    """
    Generates unique sequential IDs with configurable prefixes and padding.
    
    Supports multiple ID types (order, user, invoice) with independent counters.
    Persists state to JSON files for durability across restarts.
    """

    def __init__(self):

        self.counter = CounterFile()
        self.config = ConfigFile()
        self.lock = threading.Lock()
        self.logger = setup_logger()

    def generate(self, id_type: str) -> str:
        """
        Generates new ID for the given type
        
        Args:
            id_type (str): Name of the ID type (e.g. "order", "user")
            
        Returns:
            str: Generated ID
        """

        with self.lock:

            counter_data = self.counter.json_handler.read_all()
            config_data = self.config.get_id_type_info(id_type)
            if config_data is None:
                self.logger.warning(f"Failed to access ID type '{id_type}': not found")
                raise IDTypeNotFoundError(f"ID type '{id_type}' not found")

            if counter_data is None:
                self.logger.warning(f"Failed to access ID type '{id_type}': not found")
                raise IDTypeNotFoundError(f"ID type '{id_type}' not found")
            
            counter_data[id_type] += config_data["increment_step"]
            
            self.counter.json_handler.write_all(counter_data)
            counter = counter_data[id_type]
            prefix = config_data["prefix"]
            padding = int(config_data["padding"])

            result = f"{prefix}{counter:0{padding}d}"

            self.logger.info(f"Generated ID: {result} for type '{id_type}'")

            return result
            
        
    def add_id_type(self, id_type, start_value, increment_step, prefix, padding):

        with self.lock:

            self.validate_id_type_name(id_type)

            config_data = self.config.json_handler.read_all()
            if id_type in config_data["id_types"]:
                self.logger.warning(f"Failed to add ID type '{id_type}': already exists")
                raise IDTypeExistsError(f"ID type '{id_type}' already exists")
            
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

            self.logger.info(f"Added ID type: '{id_type}' with prefix '{prefix}'")

            return True
    
    def update_id_type(self, id_type, **kwrgs):

        with self.lock:

            self.validate_id_type_name(id_type)
            
            config_data = self.config.json_handler.read_all()
            if not id_type in config_data["id_types"]:
                self.logger.warning(f"Failed to access ID type '{id_type}': not found")
                raise IDTypeNotFoundError(f"ID type '{id_type}' not found")
            
            updated_config = kwrgs
            self.config.update_config(id_type, updated_config)
            
            self.logger.info(f"Updated ID type: '{id_type}' with new config '{updated_config}'")

            return True
    
    def delete_id_type(self, id_type, force = False):

        with self.lock:

            self.validate_id_type_name(id_type)

            config_data = self.config.json_handler.read_all()
            if not id_type in config_data["id_types"]:
                self.logger.warning(f"Failed to access ID type '{id_type}': not found")
                raise IDTypeNotFoundError(f"ID type '{id_type}' not found")
                        
            counter_data = self.counter.json_handler.read_all()
            current_count = counter_data.get(id_type, 0)
            start_value = config_data["id_types"][id_type]["start_value"]

            if current_count > start_value and not force:
                ids_generated = current_count - start_value
                self.logger.error(f"Counter reset prevented for ID type '{id_type}'")
                raise CounterResetError(f"Cannot reset - {ids_generated} IDs generated. Use --force")
            
            self.config.delete_id_type(id_type)
            self.counter.delete_counter(id_type)

            self.logger.info(f"Deleted ID type: '{id_type}'")

            return True
    
    def reset_counter(self, id_type: str, force: bool = False) -> bool:

        with self.lock:
        
            self.validate_id_type_name(id_type)

            config_data = self.config.json_handler.read_all()
            if not id_type in config_data["id_types"]:
                self.logger.warning(f"Failed to access ID type '{id_type}': not found")
                raise IDTypeNotFoundError(f"ID type '{id_type}' not found")
            
            counter_data = self.counter.json_handler.read_all()
            current_count = counter_data.get(id_type, 0)
            start_value = config_data["id_types"][id_type]["start_value"]

            if current_count > start_value and not force:
                ids_generated = current_count - start_value
                self.logger.error(f"Counter reset prevented for ID type '{id_type}'")
                raise CounterResetError(f"Cannot reset - {ids_generated} IDs generated. Use --force")
            
            self.counter.reset_counter(id_type, start_value)
            self.logger.info(f"Reset counter for ID type: '{id_type}'")

            return True
    
    def validate_id_type_name(self, id_type: str) -> bool:
        """Validates ID type names, throws ValueError if invalid"""

        if not id_type or id_type.isspace():
            self.logger.error(f"Invalid Name for ID type: '{id_type}'")
            raise InvalidIDTypeNameError("ID name cannot be empty")
        
        if not all(c.isalnum() or c == "_" for c in id_type):
            self.logger.error(f"Invalid Name for ID type: '{id_type}'")
            raise InvalidIDTypeNameError("Only alphanumeric and underscore allowed in ID name")
        
        if len(id_type) < 3 or len(id_type) > 50:
            self.logger.error(f"Invalid Name for ID type: '{id_type}'")
            raise InvalidIDTypeNameError("Length of name should be lesser than 50 and greater or equal to 3")
        
        if id_type in kwlist:
            self.logger.error(f"Invalid Name for ID type: '{id_type}'")
            raise InvalidIDTypeNameError("Reserved words cannot be used")
        
        return True

    def generate_password(self, pwd_len: int = 4):

        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        digits = string.digits
        specials = "!@#$%^&*_"

        password_chars = [
            random.choice(lower),
            random.choice(upper),
            random.choice(digits),
            random.choice(specials)
        ]

        all_chars = lower + upper + digits + specials
        for i in range(pwd_len - 4):
            password_chars.append(random.choice(all_chars))

        random.shuffle(password_chars)
        password = "".join(password_chars)

        self.logger.info(f"Generated Password: '{password}' of length {pwd_len}")

        return password

    def list_id_types(self):
        """
        List all ID types with their current status.
        
        Returns:
            list: List of dicts with id_type info
        """
        with self.lock:
            config_data = self.config.json_handler.read_all()
            counter_data = self.counter.json_handler.read_all()
            
            id_types = []
            for id_type, config in config_data["id_types"].items():
                id_types.append({
                    "name": id_type,
                    "prefix": config["prefix"],
                    "counter": counter_data.get(id_type, 0),
                    "start_value": config["start_value"],
                    "increment_step": config["increment_step"],
                    "padding": config["padding"]
                })
            
            self.logger.info(f"Listed {len(id_types)} ID types")
            return id_types
        
