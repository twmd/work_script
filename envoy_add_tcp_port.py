#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
#TODO: Добавить проверку на существование файлов
#TODO: Добавить проверку на то что порт является числовым значением
#TODO: Удалить темвой файли после совмещения
file_name = 'envoy_test.yaml'
file_path = os.path.join(file_name)
file_path_tmp = os.path.join('cluster_tmp.yaml')
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
  clusters:
  - name: {0}
    connect_timeout: 5s
    hosts:
    - socket_address:
        address: 192.168.107.68
        port_value: {1}
'''
def write_admin_section(file_path):
    with open(file_path, 'a', encoding='UTF-8') as f:
        f.write(admin_template)

def write_listener_section(file_path, listener_name, port_number):
    with open(file_path, 'a', encoding='UTF-8') as f:
        f.write(listeners_name_template.format(listener_name, port_number))

def write_cluster_section(file_path_tmp, listener_name, port_number):
    with open(file_path_tmp, 'a', encoding='UTF-8') as f:
        f.write(clusters_name_template.format(listener_name, port_number))

if __name__ == '__main__':
    write_admin_section(file_path)
    while True:
        print('Вводите имя Listener и имя порта. Для выхода оставте имя Listener пустым и нажмите Enter')
        listener_name = input('Введите имя Listener:')
        if listener_name:
            port_number = input('Введите номер порта:')
            write_listener_section(file_path, listener_name, port_number)
            write_cluster_section(file_path_tmp, listener_name, port_number)
            listener_name = None
            port_number = None
        else:
            break