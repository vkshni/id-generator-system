from engine import IDGenerator

idg = IDGenerator()

while True:

    try:

        action = input("Generate? (y/n): ")

        if action != "y":
            break

        print(idg.generate())
    except ValueError:
        print("INVALID INPUT!")
