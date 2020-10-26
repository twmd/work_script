#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import re
import argparse
from datetime import datetime


class Base:
    def __init__(self, UIN):
        self.UIN = UIN

    @staticmethod
    def _search_log_files():
        log_files_list = []
        for root, dirs, files in os.walk("/opt"):
            for file in files:
                ################Раскоментировать что бы искал во всех debug.log
                # if file.startswith('GprsControlDebug.log'):
                if file.endswith('.log'):
                    # print(os.path.join(root, file))
                    log_files_list.append(os.path.join(root, file))
        return log_files_list
