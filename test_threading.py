import threading
from engine import IDGenerator

# Create one generator instance
gen = IDGenerator()

# Function that generates 10 IDs
def generate_ids(thread_name):
    for i in range(10):
        id_val = gen.generate("order")
        print(f"{thread_name}: {id_val}")

# Create 5 threads that all generate IDs simultaneously
threads = []
for i in range(5):
    t = threading.Thread(target=generate_ids, args=(f"Thread-{i}",))
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

print("\nDone! Check if all IDs are unique (no duplicates)")