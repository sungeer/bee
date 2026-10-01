"""资产 API 客户端。"""
import hashlib
import time

import requests

from . import log, settings

# 服务端返回码
_CODE_SUCCESS = 1000


def _auth_headers():
    """认证头：KEY 与时间戳拼接后的 md5 签名。"""
    stamp = time.time()
    signature = hashlib.md5(('%s|%f' % (settings.AUTH_KEY, stamp)).encode('utf-8')).hexdigest()
    return {settings.AUTH_KEY_HEADER: '%s|%f' % (signature, stamp)}


def upload(payload):
    """提交一份采集结果，返回是否成功。"""
    try:
        response = requests.post(settings.ASSET_API, headers=_auth_headers(), json=payload)
        result = response.json()
    except Exception as e:
        log.error('上传失败: %s' % e)
        return False

    message = result.get('message', '')
    if result.get('code') == _CODE_SUCCESS:
        log.info(message)
        return True
    log.error(message)
    return False
