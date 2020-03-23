#!/usr/bin/env python3
import argparse
import os

'''
Используется для прохождении аутентификации на сайте zerocert.
Берет фаил с ключами - на текущай момент data.txt и раскладывает ключи по папкам
'''
# TODO: Добавить создание папок автоматически в зависимости от названия сайта. Так же добавить проверку на существование.
# TODO: Добавить аргументы командной строки. Удаление файлов, путь к файлу с данными, создание конфига nginx
# TODO: Может быть имеет смысл вынести в классы, часть функций.

file_name = os.path.join('data.txt')


def clear_folder(file_dict):
    for key, val_list in file_dict.items():
        file_list = [f for f in os.listdir(val_list[0])]
        for f in file_list:
            # print(os.path.join(val_list[0], f))
            os.remove(os.path.join(val_list[0], f))


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
        with open(path, 'w+', encoding='utf-8') as f:
            f.write(val_list[2])


if __name__ == '__main__':
    file_dict = create_dict_from_file(file_name)
    parser = argparse.ArgumentParser(description='Парсер входящих аргументов')
    parser.add_argument('-d', action='store_true', help='Удаляет файлы в каталогах')
    parser.add_argument('-с', action='store_true', help='Создает каталоги, при указании этой опции')
    args = parser.parse_args()
    if args.d:
        clear_folder(file_dict)
    elif args.c:
        create_folder_in_www(file_dict)
    write_to_files(file_dict)
