"""本机标识
主机名与操作系统信息
"""

from src.core.runner import fetch


def read_identity():
    version = fetch(('cat /etc/issue',), 'issue.out').strip()

    data = {
        'hostname': fetch(('hostname',), 'hostname.out').strip(),
        'os': {
            'platform': fetch(('uname',), 'uname.out').strip(),
            'version': version.splitlines()[0] if version else '',
        },
    }

    return data
