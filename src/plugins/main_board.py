#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .base import BasePlugin


class MainBoardPlugin(BasePlugin):
    """解析 dmidecode -t1 的主板信息输出"""

    def collect(self):
        output = self.capture('sudo dmidecode -t1', 'board.out')
        return self.parse(output)

    def parse(self, content):
        result = {}
        key_map = {
            'Manufacturer': 'manufacturer',
            'Product Name': 'model',
            'Serial Number': 'sn',
        }

        for item in content.split('\n'):
            row_data = item.strip().split(':')
            if len(row_data) == 2:
                if row_data[0] in key_map:
                    result[key_map[row_data[0]]] = row_data[1].strip() if row_data[1] else row_data[1]

        return result
