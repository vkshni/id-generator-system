# ID Generator

counter = 0

class IDGenerator:

    def __init__(self):
        self.counter = 0

    def generate(self):

        self.counter += 1
        return f"{self.counter:05d}"

idg = IDGenerator()

print(idg.generate())
print(idg.generate())
print(idg.generate())
print(idg.generate())
