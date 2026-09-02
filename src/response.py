#!/usr/bin/env python
# -*- coding:utf-8 -*-


class BaseResponse(object):
    """采集 / 执行的统一返回容器"""

    def __init__(self):
        self.status = True
        self.message = None
        self.data = None
        self.error = None
