#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json as default_json
from json.encoder import JSONEncoder

from src.response import BaseResponse


class JsonEncoder(JSONEncoder):
    """将 BaseResponse 序列化为其 __dict__，用于拼接采集上报数据"""

    def default(self, o):
        if isinstance(o, BaseResponse):
            return o.__dict__
        return JSONEncoder.default(self, o)


class Json(object):

    @staticmethod
    def dumps(response, ensure_ascii=True):
        return default_json.dumps(response, ensure_ascii=ensure_ascii, cls=JsonEncoder)
