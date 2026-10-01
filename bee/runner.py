"""取得采集项的原始输出：测试模式读样例文件，否则执行真实命令。

这是整条链路上唯一执行外部命令的地方。
"""
import os
import subprocess

from . import settings


def fetch(commands, fixture):
    """返回一条或多条命令的原始输出。

    多条命令的输出按顺序用换行拼接 —— 网卡信息需要 ip link 与 ip addr 两段。
    """
    if settings.TEST_MODE:
        return _read_fixture(fixture)
    return '\n'.join(subprocess.getoutput(cmd) for cmd in commands)


def _read_fixture(name):
    path = os.path.join(settings.FIXTURE_DIR, name)
    with open(path, encoding='utf-8') as f:
        return f.read()
