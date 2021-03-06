#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: Дописать если uin не нашелся

import os
import re
from datetime import datetime


# Ишет файлы с расширение log, и записывает их названия в список
##############################Раскоментировать что бы искал по всех log файлах!!!!!!!!!!!!! Функцию ниже закоментировать
# def search_log_files():
#     log_files_list = []
#     for root, dirs, files in os.walk("/opt"):
#         for file in files:
#             if '.log' in str(file):
#                 # print(os.path.join(root, file))
#                 log_files_list.append(os.path.join(root, file))
#     return log_files_list
def search_log_files():
    log_files_list = []
    for root, dirs, files in os.walk("/opt"):
        for file in files:
            ################Раскоментировать что бы искал во всех debug.log
            # if file.startswith('GprsControlDebug.log'):
            if file.endswith('.log'):
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
#Заменяет путь к файлу логов, на название control
def rename_gprs_control(gpts_control):
    gprs_control_list = ['gprscontrol_18221', 'gprscontrol_egts_gmon', 'gprscontrol_egts_prod', 'gprscontrol_egts_vega',
                         'gprscontrol_rs_old', 'gprscontrol_sec2', 'gprscontrol_stst', 'gprscontrol_18231',
                         'gprscontrol_egts_h2h_gpos', 'gprscontrol_egts_ritm', 'gprscontrol_ritm', 'gprscontrol_sc',
                         'gprscontrol_sec3', 'gprscontrol_ark', 'gprscontrol_egts_mircom', 'gprscontrol_egts_test',
                         'gprscontrol_rs', 'gprscontrol_sec', 'gprscontrol_sms']
    for i in gprs_control_list:
        if i in gpts_control:
            return i
#Проверяет существование файла, если есть удаляет.
def file_is_exec(file):
    if os.path.isfile(file):
        os.remove(file)

if __name__ == '__main__':
    # print(search_uin_bs_in_files(search_log_files()))
    gprs_control = ''
    file_is_exec('report_uin.txt')
    file_is_exec('no_gprs_in_log.txt')
    with open ('bo_uin.txt', 'r', encoding='UTF-8') as f_uin:
        for line in f_uin:
            cur_uin = line
            # cur_uin.replace(' ', '')
            cur_uin = re.sub("^\s+|\n|\r|\s+$", '', cur_uin)
            # print(cur_uin)
            gprs_control = search_uin_bs_in_files(search_log_files(), cur_uin)
            #Если gpts_control не пустой, то пишем данные
            if gprs_control:
                gprs_control = rename_gprs_control(gprs_control)
                with open ('report_uin.txt', 'a', encoding='UTF-8') as f_report:
                    cur_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                    # f_report.write('{0} | {1} | {2}\n'.format(str(cur_time), cur_uin, gprs_control))
                    f_report.write('{0} | {1}\n'.format(cur_uin, gprs_control))
                    # print('{0} | {1} | {2}'.format(str(cur_time), cur_uin, gprs_control))
                    print('{0} | {1}'.format(cur_uin, gprs_control))
            #Иначе заносим в фаил с исключениями
            else:
                with open('no_gprs_in_log.txt', 'a', encoding='UTF-8') as f_no_gprs:
                    f_no_gprs.write('{0}\n'.format(cur_uin))
    with open('report_uin.txt', 'a', encoding='UTF-8') as f_report:
        f_report.write('END OF WORK')