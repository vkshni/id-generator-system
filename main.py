from engine import IDGenerator

idg = IDGenerator()
# print(idg.add_id_type("product",1000,1,"PRD", 10))
# print(idg.update_id_type("product", start_value = 500 ))
# print(idg.delete_id_type("order"))
# print(idg.reset_counter("invoice"))
# print(idg.validate_id_type_name("and"))

def main():
    while True:

        try:

            action = input("Generate? (y/n): ")

            if action != "y":
                break

            id_type = input("ID Type (order, user, invoice): ")

            print(idg.generate(id_type))
        
        except Exception as e:

            print(f"[Error]: {str(e)}")

main()
