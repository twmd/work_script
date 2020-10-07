#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
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

def search_uin_bs_in_files(log_file_list):
    a = '(EquipmentUin{0; 9129}'
    for file in log_file_list:
        with open(file, 'r') as f:
            for line in f:
                if a in line:
                    print(line)


if __name__ == '__main__':
    search_uin_bs_in_files(search_log_files())

