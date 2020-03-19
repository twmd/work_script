import os

file = os.path.join('data.txt')


def read_from_file(file):
    with open(file, 'r+', encoding='utf-8')as f:
        key = None
        for line in f:
            data_str = line.split()
            if data_str[0] == 'Текст:':
                key = data_str[1]
                #                write_to_files(link, key)
                write_to_files(path, key)
            else:
                site_name = data_str[0]
                link = data_str[1]
                path = '/var/www/{}/.well-known/acme-challenge/{}'.format(site_name, link)


#                path_tmp = '/' + os.path.join(path_tmp.split('/'))
#                print(path_tmp)
#                print(key)
#                write_to_files(path, key)
#                key = None


def write_to_files(filename, key):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(key))


# def del_file_exist(filename)
#     if os.path.isfile(filename):
#         os.remove(filename)


if __name__ == '__main__':
    read_from_file(file)
