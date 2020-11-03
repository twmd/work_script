#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import re
# import argparse
from datetime import datetime


# Класс с переменными по умолчанию
class Default:
    # Директория с логами
    log_dir = '/opt'
    # Проверять все log файли или только последний
    last_log = True


class Base:
    def __init__(self, uin, log_dir, last_log):
        self.uin = uin
        self.log_dir = log_dir
        self.last_log = last_log

    # Поиск лог файлов в указанном каталоге
    def _search_log_files(self):
        log_files_list = []
        for root, dirs, files in os.walk(self.log_dir):
            for file in files:
                if self.last_log:
                    if file.endswith('GprsControlDebug.log'):
                        log_files_list.append(os.path.join(root, file))
                else:
                    if file.startswith('GprsControlDebug.log'):
                        log_files_list.append(os.path.join(root, file))
        return log_files_list

    # Ищет дату из лог строки
    def _search_last_date(self, log_string):
        regex_date = re.compile('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
        date_match = re.search(regex_date, log_string)
        return date_match.group()

    # сравнивает дату, и True если дата лога больше.
    def _compate_date(self, cur_date, log_date):
        log_date = datetime.strptime(log_date, '%Y-%m-%d %H:%M:%S')
        if cur_date < log_date:
            return True
        else:
            return False

    def search_uin_bs_in_files(self):
        #TODO: Переписать так что бы при каждом вызове экземпляма он не формировался заново
        log_file_list = self._search_log_files()
        UIN_strig = '(EquipmentUin{{0; {0}}}'.format(self.uin)
        # Новая дата в log файле
        last_log_date = datetime.strptime('1970-01-01 10:00:00', '%Y-%m-%d %H:%M:%S')
        gprs_control = ''
        gprs_controls_list = []
        for file in log_file_list:
            with open(file, 'r') as f:
                for line in f:
                    if UIN_strig in line:
                        date_from_log = self._search_last_date(line)
                        if self._compate_date(last_log_date, date_from_log):
                            last_log_date = datetime.strptime(date_from_log, '%Y-%m-%d %H:%M:%S')
                            gprs_control = file
            # Проверить что строка правильная.
            # if gprs_control and gprs_control not in gprs_controls_list:
            if gprs_control not in gprs_controls_list:
                gprs_controls_list.append(gprs_control)
        return gprs_controls_list

if __name__ == '__main__':
    uin = input('Enter UIN:')
    s_gprscontrol = Base(uin, Default.log_dir, Default.last_log)
    print(s_gprscontrol.search_uin_bs_in_files())