import os

def search_log_files():
    log_files_list = []
    for root, dirs, files in os.walk("/opt"):
        for file in files:
            if file.endswith(".log"):
                #print(os.path.join(root, file))
                log_files_list.append(os.path.join(root, file))
        print(log_files_list)

if __name__ == '__main__':
    search_log_files()