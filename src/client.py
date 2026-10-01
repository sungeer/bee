import logging
import os

from src import settings
from src.core.logger import setup_logger
from src.core.api import upload
from src.collector.collect import CollectError, collect

logger = logging.getLogger(__name__)


def _asset_id(collected_hostname):
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
    setup_logger()

    try:
        payload = collect()
    except CollectError:
        logger.exception('采集失败')
        return

    payload['hostname'] = _asset_id(payload['hostname'])

    upload(payload)
