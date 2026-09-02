#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import os

from src import settings


class Logger(object):
    """采集日志单例：运行日志与错误日志分开落盘"""

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.run_log_file = settings.RUN_LOG_FILE
        self.error_log_file = settings.ERROR_LOG_FILE
        self.run_logger = None
        self.error_logger = None

        self.initialize_run_log()
        self.initialize_error_log()

    @staticmethod
    def check_path_exist(log_abs_file):
        log_path = os.path.split(log_abs_file)[0]
        if log_path and not os.path.exists(log_path):
            os.makedirs(log_path)

    def initialize_run_log(self):
        self.check_path_exist(self.run_log_file)
        handler = logging.FileHandler(self.run_log_file, 'a', encoding='utf-8')
        fmt = logging.Formatter(fmt='%(asctime)s - %(levelname)s :  %(message)s')
        handler.setFormatter(fmt)
        run_logger = logging.Logger('run_log', level=logging.INFO)
        run_logger.addHandler(handler)
        self.run_logger = run_logger

    def initialize_error_log(self):
        self.check_path_exist(self.error_log_file)
        handler = logging.FileHandler(self.error_log_file, 'a', encoding='utf-8')
        fmt = logging.Formatter(fmt='%(asctime)s  - %(levelname)s :  %(message)s')
        handler.setFormatter(fmt)
        error_logger = logging.Logger('error_log', level=logging.ERROR)
        error_logger.addHandler(handler)
        self.error_logger = error_logger

    def log(self, message, mode=True):
        """写日志：mode=True 写运行日志，mode=False 写错误日志"""
        if mode:
            self.run_logger.info(message)
        else:
            self.error_logger.error(message)
