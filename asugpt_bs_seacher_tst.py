import os
for root, dirs, files in os.walk("/opt"):
    for file in files:
        if file.endswith("*.log")
            print(os.path.join(root, file))