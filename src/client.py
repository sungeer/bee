import os
from concurrent.futures import ThreadPoolExecutor

from src import settings
from src.collect.collector import collect_asset
from src.common.logger import Logger
from src.report.reporter import AssetAPI


def run():
    """采集入口
    按 settings.MODE 选择采集方式并上报资产
    """
    if settings.MODE == 'agent':
        _agent()
    elif settings.MODE in ('ssh', 'salt'):
        _remote()
    else:
        raise ValueError('无效的采集模式：%s，请配置为 agent/ssh/salt' % settings.MODE)


def _agent():
    """采集本机资产并上报
    通过本地 cert 文件识别新老资产
    """
    result = collect_asset()
    if not result.status:
        return

    data = result.data
    local_cert = _load_cert()
    if local_cert is None:
        _write_cert(data['hostname'])
    elif local_cert != data['hostname']:
        data['hostname'] = local_cert
    AssetAPI().submit(data)


def _remote():
    """从 API 拉取待采集主机
    并发采集并逐个上报
    """
    api = AssetAPI()
    todo = api.fetch_todo()
    if not todo:
        return

    with ThreadPoolExecutor(max_workers=10) as pool:
        for item in todo:
            pool.submit(_collect_one, api, item['hostname'])


def _collect_one(api, hostname):
    """采集单个远程主机并上报"""
    logger = Logger()
    result = collect_asset(hostname)
    if not result.status:
        logger.log('collect %s failed: %s' % (hostname, result.error), False)
        return
    api.submit(result.data)


def _load_cert():
    """读取本地标识文件
    返回主机名
    文件不存在或为空返回 None
    """
    path = settings.CERT_FILE_PATH
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as f:
        content = f.read()
    return content.strip() or None


def _write_cert(hostname):
    """把主机名写入本地标识文件
    用于首次采集时向服务器注册
    """
    path = settings.CERT_FILE_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(hostname)
