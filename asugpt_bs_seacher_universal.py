#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import re
# import argparse
from datetime import datetime
from tqdm import tqdm
from collections import defaultdict
import json

# Класс с переменными по умолчанию
class Default:
    # Директория с логами
    log_dir = 'c:\_tmp\ASUGPT\comm\opt'
    # Проверять все log файли или только последний
    last_log = True
    uin_file = 'bo_uin_small.txt'
    report_uin = 'report_uin_u.json'
    report_no_gprs = 'report_no_gprs_u.txt'

class Base:
    def __init__(self, log_dir, last_log):
        # self.uin = uin
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

    def _rename_gprs_control(self, gpts_control):
        gprs_control_list = ['gprscontrol_18221', 'gprscontrol_egts_gmon', 'gprscontrol_egts_prod',
                             'gprscontrol_egts_vega',
                             'gprscontrol_rs_old', 'gprscontrol_sec2', 'gprscontrol_stst', 'gprscontrol_18231',
                             'gprscontrol_egts_h2h_gpos', 'gprscontrol_egts_ritm', 'gprscontrol_ritm', 'gprscontrol_sc',
                             'gprscontrol_sec3', 'gprscontrol_ark', 'gprscontrol_egts_mircom', 'gprscontrol_egts_test',
                             'gprscontrol_rs', 'gprscontrol_sec', 'gprscontrol_sms']
        for i in gprs_control_list:
            if i in gpts_control:
                return i

    # Поиск одного UIN  в log файлах
    def search_uin_bs_in_files(self, uin):
        log_file_list = self._search_log_files()
        UIN_strig = '(EquipmentUin{{0; {0}}}'.format(uin)
        # Новая дата в log файле
        last_log_date = datetime.strptime('1970-01-01 10:00:00', '%Y-%m-%d %H:%M:%S')
        gprs_control = ''
        gprs_controls_list = []
        for file in tqdm(log_file_list):
            with open(file, 'r', encoding='UTF-8') as f:
                log_in_memory = f.readlines()
                for line in log_in_memory:
                    if UIN_strig in line:
                        date_from_log = self._search_last_date(line)
                        if self._compate_date(last_log_date, date_from_log):
                            last_log_date = datetime.strptime(date_from_log, '%Y-%m-%d %H:%M:%S')
                            gprs_control = file
            # Проверить что строка правильная.
            # if gprs_control and gprs_control not in gprs_controls_list:
            del log_in_memory
            if gprs_control:
                gprs_control = self._rename_gprs_control(gprs_control)
                if gprs_control not in gprs_controls_list:
                    gprs_controls_list.append(gprs_control)
        return gprs_controls_list

    # Поиск списка uin из файлов
    def search_all_uins_in_files(self, set_uins):
        data_dict = defaultdict(list)
        log_file_list = self._search_log_files()
        last_log_date = datetime.strptime('1970-01-01 10:00:00', '%Y-%m-%d %H:%M:%S')
        gprs_control = str()
        # uin_not_find = set()
        for file in log_file_list:
            with open(file, 'r', encoding='UTF-8') as f:
                log_in_memory = f.readlines()
                for uin_number in tqdm(set_uins):
                    uin_strig = '(EquipmentUin{{0; {0}}}'.format(uin_number)
                    for line in log_in_memory:
                        if uin_strig in line and 'PointGeoData' in line:
                            date_from_log = self._search_last_date(line)
                            if self._compate_date(last_log_date, date_from_log):
                                last_log_date = datetime.strptime(date_from_log, '%Y-%m-%d %H:%M:%S')
                                gprs_control = self._rename_gprs_control(file)
                    if gprs_control:
                        data_dict[uin_number].append({str(last_log_date): gprs_control})
                    # else:
                    #     uin_not_find.add(uin_number)
                    last_log_date = datetime.strptime('1970-01-01 10:00:00', '%Y-%m-%d %H:%M:%S')
                    gprs_control = str()

            del log_in_memory
        return data_dict


class SearchFromFile(Base):

    def __init__(self, log_dir, last_log):
        self.set_uin = set()
        super().__init__(log_dir, last_log)

    # Поиск UIN которые не нашлись в логах.
    def _find_unknow_uin(self, data_dict, set_uin):
        set_know_uin = set()
        for key in data_dict:
            set_know_uin.add(key)
        set_unknow_uin = set_uin ^ set_know_uin
        # for i in set_unknow_uin:
        #     print(i, '\n')
        return set_unknow_uin
    # Печать словаря
    # def parse_data_dict(self, data_dict):
    #     i = 1
    #     for key in data_dict:
    #         print(i, '\n')
    #         print(key, '->', data_dict[key])
    #         print('\n')
    #         i += 1
    # Создает множество из файла
    def _create_set_uins(self):
        # uin_set = set()
        with open(Default.uin_file, 'r', encoding='UTF-8') as f:
            for line in f:
                cur_uin = line
                cur_uin = re.sub("^\s+|\n|\r|\s+$", '', cur_uin)
                self.set_uin.add(cur_uin)
        return self.set_uin


    def search_uins_main(self):
        uin_set = self._create_set_uins()
        data_dict = self.search_all_uins_in_files(uin_set)
        unknow_uin = self._find_unknow_uin(data_dict, uin_set)
        with open(Default.report_no_gprs, 'w', encoding='UTF-8') as f:
            for uin in unknow_uin:
                f.write('{}\n'.format(uin))
        data_dict_json = json.dumps(data_dict)
        with open(Default.report_uin, 'w', encoding='UTF-8') as f:
            f.write(data_dict_json)

if __name__ == '__main__':
    s_gprscontrol = SearchFromFile(Default.log_dir, Default.last_log)
    s_gprscontrol.search_uins_main()

# uin = input('Enter UIN:')
# s_gprscontrol = Base(Default.log_dir, Default.last_log)
# print(s_gprscontrol.search_uin_bs_in_files(uin))

# s_gprscontrol = Base(Default.log_dir, Default.last_log)
# data_dict = s_gprscontrol.search_all_uins_in_files(uin_set)
# parse_data_dict(data_dict)
# find_unknow_uin(uin_set, data_dict)
