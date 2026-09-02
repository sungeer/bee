#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .base import BasePlugin


class BasicPlugin(BasePlugin):
    """采集系统平台、版本与主机名"""

    def os_platform(self):
        """获取系统平台"""
        if self.test_mode:
            output = 'linux'
        else:
            output = self.exec_shell_cmd('uname')
        return output.strip()

    def os_version(self):
        """获取系统版本（样例数据与真实输出一致时只取第一行）"""
        if self.test_mode:
            output = 'CentOS release 6.6 (Final)\nKernel \r on an \\m'
        else:
            output = self.exec_shell_cmd('cat /etc/issue')
        return output.strip().split('\n')[0]

    def os_hostname(self):
        """获取主机名"""
        if self.test_mode:
            output = 'c1.com'
        else:
            output = self.exec_shell_cmd('hostname')
        return output.strip()

    def collect(self):
        return {
            'os_platform': self.os_platform(),
            'os_version': self.os_version(),
            'hostname': self.os_hostname(),
        }
