import sys
import time
print("Simple Test Starting...", flush=True)
sys.stdout.flush()
for i in range(100):
    print(f"Tick {i}", flush=True)
    time.sleep(1)
