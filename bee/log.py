"""运行日志与错误日志。

模块级配置天然就是单例，不需要单例类。
"""
import logging
import os

from . import settings


def _build_logger(name, path, level):
    logger = logging.getLogger(name)  # 同名 logger 全局唯一，重复调用拿到同一个
    if logger.handlers:               # 模块被重复导入时不重复挂 handler
        return logger
    logger.setLevel(level)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    handler = logging.FileHandler(path, encoding='utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s : %(message)s'))
    logger.addHandler(handler)
    return logger


_run = _build_logger('bee.run', settings.RUN_LOG_FILE, logging.INFO)
_error = _build_logger('bee.error', settings.ERROR_LOG_FILE, logging.ERROR)


def info(message):
    """写运行日志"""
    _run.info(message)


def error(message):
    """写错误日志"""
    _error.error(message)
