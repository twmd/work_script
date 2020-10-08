#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
#TODO: Добавить проверку на то что порт является числовым значением
file_name = (input('Введите название файла конфигурации:'))
file_path = os.path.join(file_name)
#TODO Вынести куда нибудь.
#Проверка существования файлов
if os.path.isfile(file_path):
    os.remove(file_path)

file_path_tmp = os.path.join('envoy_cluster_tmp.yaml')
listener_name = ''
port_number = 0
admin_template ='''
admin:
  access_log_path: /tmp/admin_access.log
  address:
    socket_address:
      protocol: TCP
      address: 0.0.0.0
      port_value: 8080
static_resources:
  listeners:'''

listeners_name_template = '''
  - name: {0}
    address:
      socket_address: {{ address: 0.0.0.0, port_value: {1} }}
    filter_chains:
    - filters:
      - name: envoy.filters.network.tcp_proxy
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.network.tcp_proxy.v3.TcpProxy
          stat_prefix: tcp_stats
          cluster: "{0}"
          max_connect_attempts: 3
          access_log:
          - name: envoy.access_loggers.file
            typed_config:
              "@type": "type.googleapis.com/envoy.config.accesslog.v2.FileAccessLog"
              json_format:
                START_TIME: "%START_TIME%"
                BYTE_RECIEVED: "%BYTES_RECEIVED%"
                BYTE_SEND: "%BYTES_SENT%"
                DURATION: "%DURATION%"
                DST_IP_PORT: "%UPSTREAM_HOST%"
                PROXY_IP_PORT: "%UPSTREAM_LOCAL_ADDRESS%"
                SRV_IP_PORT: "%DOWNSTREAM_REMOTE_ADDRESS%"
              path: /var/log/envoy/{0}.log'''

clusters_name_template = '''
  - name: {0}
    connect_timeout: 5s
    hosts:
    - socket_address:
        address: 192.168.107.68
        port_value: {1}
'''
#Записывает административную секцию
def write_admin_section(file_path):
    with open(file_path, 'a', encoding='UTF-8') as f:
        f.write(admin_template)
#Записывает секцию Listener
def write_listener_section(file_path, listener_name, port_number):
    with open(file_path, 'a', encoding='UTF-8') as f:
        f.write(listeners_name_template.format(listener_name, port_number))
#Создает временный фаил с секцией cluster
def write_cluster_section(file_path_tmp, listener_name, port_number):
    with open(file_path_tmp, 'a', encoding='UTF-8') as f:
        f.write(clusters_name_template.format(listener_name, port_number))
#Объединяет файлы
def union_file (file_path, file_path_tmp):
    with open(file_path, 'a', encoding='UTF-8') as in_f:
        in_f.write('\n  clusters:')
    with open(file_path_tmp, 'r', encoding='UTF-8') as out_f:
        for line in out_f:
            with open(file_path, 'a', encoding='UTF-8') as in_f:
                in_f.write(line)
    os.remove(file_path_tmp)

if __name__ == '__main__':
    write_admin_section(file_path)
    print('Вводите имя Listener и имя порта. Для выхода оставте имя Listener пустым и нажмите Enter')
    while True:
        listener_name = input('Введите имя Listener:')
        if listener_name:
            port_number = input('Введите номер порта:')
            write_listener_section(file_path, listener_name, port_number)
            write_cluster_section(file_path_tmp, listener_name, port_number)
            listener_name = None
            port_number = None
        else:
            break
    union_file(file_path, file_path_tmp)