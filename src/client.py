import os

from src import log, settings
from src.api import upload
from src.collect import CollectError, collect


def _asset_id(collected_hostname):
    """以本地标识文件里的主机名为准。

    首次采集时把主机名写入标识文件；之后即使机器改名，
    上报的仍是当初的名字，从而对应到服务端上的同一条资产。
    """
    path = settings.ASSET_ID_FILE
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            saved = f.read().strip()
        if saved:
            return saved

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(collected_hostname)
    return collected_hostname


def run():
    try:
        payload = collect()
    except CollectError as e:
        log.error('采集失败: %s' % e)
        return

    payload['hostname'] = _asset_id(payload['hostname'])
    upload(payload)
