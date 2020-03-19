#!/usr/bin/env python3
'''
Используется для прохождении аутентификации на сайте zerocert.
Берет фаил с ключами - на текущай момент data.txt и раскладывает ключи по папка
'''
#TODO: Добавить создание папок автоматически в зависимости от названия сайта. Так же добавить проверку на существование.
#TODO: Добавить аргументы командной строки. Удаление файлов, путь к файлу с данными, создание конфига nginx

import os

file = os.path.join('data.txt')


def read_from_file(file):
    with open(file, 'r+', encoding='utf-8')as f:
        key = None
        for line in f:
            data_str = line.split()
            if data_str[0] == 'Текст:':
                key = data_str[1]
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
