import argparse

parser = argparse.ArgumentParser(description='Парсер входящих аргументов')
# parser.add_argument('-d', action='store',dest='delete', default=False , help= 'Удаляет файлы в директории', required=False)
parser.add_argument('-d', action='store_true', help='Удаляет файлы в каталогах')
parser.add_argument('-с', action='store_true', help='Создает каталоги, при указании этой опции')
args = parser.parse_args()



