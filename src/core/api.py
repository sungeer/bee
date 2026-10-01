"""资产 API 客户端
"""

import hashlib
import logging
import time

import requests
import urllib3

from src import settings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

# 服务端返回码
_CODE_SUCCESS = 1000


def _auth_headers():
    """认证头
    KEY 与时间戳拼接后的 md5 签名
    """
    key = settings.AUTH_KEY
    key_name = settings.AUTH_KEY_HEADER

    ha = hashlib.md5(key.encode('utf-8'))
    time_span = time.time()

    ha.update(bytes('%s|%f' % (key, time_span), encoding='utf-8'))
    encryption = ha.hexdigest()

    result = '%s|%f' % (encryption, time_span)

    auth_key = {
        key_name: result
    }
    return auth_key


def upload(payload):
    """提交一份采集结果
    返回是否成功
    """
    try:
        response = requests.post(
            settings.ASSET_API,
            headers=_auth_headers(),
            json=payload,
            timeout=(3.05, 5),
            verify=False
        )
        result = response.json()
    except Exception:
        logger.exception('上传失败')
        return False

    message = result.get('message', '')
    if result.get('code') == _CODE_SUCCESS:
        logger.info(message)
        return True
    logger.error(message)
    return False
