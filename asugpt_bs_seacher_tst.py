import os
for f in os.listdir("/opt"):
    if f.endswith('*.log'):
        print(f)