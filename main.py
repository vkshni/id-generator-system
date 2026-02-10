from engine import IDGenerator

idg = IDGenerator()

def main():
    while True:

        action = input("Generate? (y/n): ")

        if action != "y":
            break

        id_type = input("ID Type (order, user, invoice): ")

        print(idg.generate(id_type))

main()
