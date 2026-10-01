"""本机标识：主机名与操作系统信息。

与其他解析模块不同，它执行多条命令，且结果直接进 payload 顶层
（不是 payload 下的某个采集项），所以不套用 parse(text) 的形状。
"""
from src.runner import fetch


def read_identity():
    """返回 {'hostname': ..., 'os': {...}}"""
    version = fetch(('cat /etc/issue',), 'issue.out').strip()
    return {
        'hostname': fetch(('hostname',), 'hostname.out').strip(),
        'os': {
            'platform': fetch(('uname',), 'uname.out').strip(),
            'version': version.splitlines()[0] if version else '',
        },
    }
