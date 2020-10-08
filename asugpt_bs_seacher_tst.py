#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime
#Ишет файлы с расширение log, и записывает их названия в список
#TODO: Дописать что бы искал только Debug_Log
def search_log_files():
    log_files_list = []
    for root, dirs, files in os.walk("/opt"):
        for file in files:
            if file.endswith(".log"):
                #print(os.path.join(root, file))
                log_files_list.append(os.path.join(root, file))
    return log_files_list
#Ищет совпадения в файле
def search_uin_bs_in_files(log_file_list):
    a = '(EquipmentUin{0; 9129}'
    for file in log_file_list:
        with open(file, 'r') as f:
            for line in f:
                if a in line:
                    # print(line)
                    # print(file)
                    search_last_date(line)

def search_last_date(log_string):
    regex_date = re.compile('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
    date_match = re.search(regex_date, log_string)
    print(date_match.group())


if __name__ == '__main__':
    search_uin_bs_in_files(search_log_files())

