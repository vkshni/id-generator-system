from engine import IDGenerator

idg = IDGenerator()
print(idg.add_id_type("product",1000,1,"PRD", 10))

def main():
    while True:

        action = input("Generate? (y/n): ")

        if action != "y":
            break

        id_type = input("ID Type (order, user, invoice): ")

        print(idg.generate(id_type))

main()
