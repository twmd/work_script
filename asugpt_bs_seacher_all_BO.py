#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TODO: Дописать если uin не нашелся

import os
import re
from datetime import datetime


# Ишет файлы с расширение log, и записывает их названия в список
# TODO: Дописать что бы искал только Debug_Log
def search_log_files():
    log_files_list = []
    for root, dirs, files in os.walk("/opt"):
        for file in files:
            if '.log' in str(file):
                # print(os.path.join(root, file))
                log_files_list.append(os.path.join(root, file))
    return log_files_list


# Ищет совпадения в файле
def search_uin_bs_in_files(log_file_list, UIN):
    # UIN = input('Введите UIN:')
    UIN_strig = '(EquipmentUin{{0; {0}}}'.format(UIN)
    # Новая дата в log файле
    last_log_date = datetime.strptime('1970-01-01 10:00:00', '%Y-%m-%d %H:%M:%S')
    gprs_control = ''
    for file in log_file_list:
        with open(file, 'r') as f:
            for line in f:
                if UIN_strig in line:
                    date_from_log = search_last_date(line)
                    if compate_date(last_log_date, date_from_log):
                        last_log_date = datetime.strptime(date_from_log, '%Y-%m-%d %H:%M:%S')
                        gprs_control = file
    return gprs_control


# выбирает дату из строки
def search_last_date(log_string):
    regex_date = re.compile('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
    date_match = re.search(regex_date, log_string)
    return date_match.group()


# сравнивает дату, и True если дата лога больше.
def compate_date(cur_date, log_date):
    log_date = datetime.strptime(log_date, '%Y-%m-%d %H:%M:%S')
    if cur_date < log_date:
        return True
    else:
        return False


if __name__ == '__main__':
    # print(search_uin_bs_in_files(search_log_files()))
    gprs_control = ''
    with open ('bo_uin.txt', 'r', encoding='UTF-8') as f_uin:
        for line in f_uin:
            cur_uin = line
            gprs_control = search_uin_bs_in_files(search_log_files(), cur_uin)
            with open ('report_uin.txt', 'w', encoding='UTF-8') as f_report:
                cur_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                f_report.write('{0} | {1} | {2}'.format(str(cur_time), cur_uin, gprs_control))
                print('{0} | {1} | {2}'.format(str(cur_time), cur_uin, gprs_control))
