import os
for root, dirs, files in os.walk("/opt"):
    print(root)