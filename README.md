Рабочие скрипты.

zcert_utils.py - фаил генератор для создания файлов ключей для nginx, для какого то там сертификационного сайта.

envoy_add_tcp_port.py - генератор конфига для envoy-proxy

asugpt_bs_seacher.py - поиск gprscontrol по 1 UIN

asugpt_bs_seacher_all_BO.py - массовый поиск gprscontrol по списку UIN (далее будет обьеденено с asugpt_bs_seacher.py )

    - Входящий фаил со списком UIN (каждый UIN на отдельной строке) имя файла bo_uin.txt
    
    - report_uin.txt - фаил со списком UIN и gprscontrol (пересоздается при каждом запуске скрипта)
    
    - no_gprs_in_log.txt - фаил со списком UIN для которых не нашелся gprscontrol
    
    !В стандартной конфигурации ищется только файлы /opt/...////.log, для изменения (только GprsControlDebug.log или включение поиска и по файлам типа *.log.1, *.log.2..) необходимо раскоментировать/закоментировать 
    соответствующие разделы (есть коментарии) в функции search_log_files (будет исправленно)
    
