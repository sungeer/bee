#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib
import time

import requests

from src import settings
from src.logger import Logger
from src.serialize import Json


class AssetAPI(object):
    """资产 API 客户端：认证、拉取待采集主机、提交采集结果"""

    def __init__(self):
        self.api = settings.ASSET_API
        self.logger = Logger()

    def auth_headers(self):
        """生成认证请求头（KEY + 时间戳的 md5 签名）"""
        time_span = time.time()
        encryption = hashlib.md5(
            ('%s|%f' % (settings.KEY, time_span)).encode('utf-8')
        ).hexdigest()
        return {settings.AUTH_KEY_NAME: '%s|%f' % (encryption, time_span)}

    def fetch_todo(self):
        """拉取待采集的主机名列表；请求失败或无任务时返回空列表"""
        try:
            response = requests.get(self.api, headers=self.auth_headers())
            task = response.json()
        except Exception as e:
            self.logger.log('fetch asset list failed: %s' % e, False)
            return []
        if not task.get('status'):
            self.logger.log(task.get('message'), False)
            return []
        return task.get('data', [])

    def submit(self, payload):
        """提交一条采集结果。

        :param payload: dict，含 BaseResponse 对象，用自定义 Json 编码器序列化
        :return: 是否提交成功
        """
        headers = self.auth_headers()
        headers['Content-Type'] = 'application/json'
        try:
            response = requests.post(self.api, headers=headers, data=Json.dumps(payload))
            result = response.json()
        except Exception as e:
            self.logger.log(str(e), False)
            return False

        if result.get('code') == 1000:
            self.logger.log(result.get('message'), True)
            return True
        self.logger.log(result.get('message'), False)
        return False
