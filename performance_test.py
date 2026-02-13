import time
import threading
from engine import IDGenerator

gen = IDGenerator()

def generate_bulk(count):
    for _ in range(count):
        gen.generate("order")

# Test: Generate 1000 IDs with 10 threads
start = time.time()

threads = []
for i in range(10):
    t = threading.Thread(target=generate_bulk, args=(100,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end = time.time()
duration = end - start

print(f"Generated 1000 IDs in {duration:.2f} seconds")
print(f"Throughput: {1000/duration:.0f} IDs/second")