"""采集编排：把各采集项的结果拼成一份可上报的 payload。"""
from collections import namedtuple
from datetime import datetime

from src import log
from src.parsers import cpu, disk, dmidecode, nic, system
from src.runner import fetch

# 上报数据结构版本，结构变更时递增
SCHEMA_VERSION = 1

# 采集项：名称（同时是 payload 里的字段名）、真实命令、样例文件、解析函数
Spec = namedtuple('Spec', 'name commands fixture parse')

SPECS = (
    Spec('cpu',        ('cat /proc/cpuinfo',),                   'cpu.out',       cpu.parse),
    Spec('main_board', ('sudo dmidecode -t1',),                  'main_board.out', dmidecode.parse_main_board),
    Spec('disks',      ('sudo MegaCli -PDList -aALL',),          'disk.out',      disk.parse),
    Spec('memory',     ('sudo dmidecode -q -t 17 2>/dev/null',), 'memory.out',    dmidecode.parse_memory),
    Spec('nics',       ('sudo ip link show', 'sudo ip addr show'), 'nic.out',      nic.parse),
)


class CollectError(Exception):
    """整机采集失败：基础信息都拿不到，调用方无法继续。"""


def collect():
    """采集本机资产，返回可上报的 payload。

    单个采集项失败只记进 errors，不影响其余项；连主机名都拿不到则整体失败。
    """
    identity = system.read_identity()
    if not identity['hostname']:
        raise CollectError('无法获取主机名')

    payload = {
        'schema_version': SCHEMA_VERSION,
        'collected_at': datetime.now().astimezone().isoformat(timespec='seconds'),
        **identity,
    }

    errors = {}
    for spec in SPECS:
        try:
            payload[spec.name] = spec.parse(fetch(spec.commands, spec.fixture))
        except Exception as e:
            log.error('%s 采集失败: %s' % (spec.name, e))
            errors[spec.name] = str(e)
    payload['errors'] = errors

    return payload
