#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import re
import argparse
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

    def search_log_files(self):
        log_files_list = []
        for root, dirs, files in os.walk(self.log_dir):
            for file in files:
                if self.last_log:
                    if file.endswith('GprsControlDebug.log'):
                        log_files_list.append(os.path.join(root, file))
                else:
                    if file.startswith('GprsControlDebug.log'):
                        log_files_list.append(os.path.join(root, file))
        # return log_files_list
        print(log_files_list)


a = Base(123, Default.log_dir, Default.last_log)
a.search_log_files()
print('\n###################################\n')

b = Base(123, Default.log_dir, False)
b.search_log_files()
