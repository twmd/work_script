#!/usr/bin/env python3
import shutil
import os

'''
Используется для прохождении аутентификации на сайте zerocert.
Берет фаил с ключами - на текущай момент data.txt и раскладывает ключи по папкам
'''
# TODO: Добавить создание папок автоматически в зависимости от названия сайта. Так же добавить проверку на существование.
# TODO: Добавить аргументы командной строки. Удаление файлов, путь к файлу с данными, создание конфига nginx
# TODO: Может быть имеет смысл вынести в классы, часть функций.
import shutil

file_name = os.path.join('data.txt')


def clear_folder(file_dict):
    for key, val_list in file_dict.items():
        # shutil.rmtree(val_list[0])
        print(os.listdir(val_list[0]))


def create_folder_in_www(file_dict):
    for key, val_list in file_dict.items():
        os.makedirs(val_list[0], mode=0o755, exist_ok=True)


def create_dict_from_file(file):
    '''Принимает имя файла, возвращает словарь вида
    (site_name: [путь к папке в которой размещается фаил, имя файла, ключ])'''
    file_dict = {}
    with open(file, 'r', encoding='utf-8')as f:
        for line in f:
            data_str = line.split()
            if data_str[0] != 'Текст:':
                link = data_str[1]
                site_name = data_str[0]
                path = '/var/www/{}/.well-known/acme-challenge/'.format(site_name, link)
                file_dict.update({site_name: ''})
            elif data_str[0] == 'Текст:':
                key = data_str[1]
                file_dict.update({site_name: [path, link, key]})
            # print(file_dict)
    return file_dict


def write_to_files(file_dict):
    '''Записывает данный в фаил из словаря'''
    for key, val_list in file_dict.items():
        path = val_list[0] + val_list[1]
        with open(path) as f:
            f.write(val_list[2])


if __name__ == '__main__':
    file_dict = create_dict_from_file(file_name)
    create_folder_in_www(file_dict)
    # write_to_files(file_dict)
    # clear_folder(file_dict)
