"""dmidecode 输出解析：主板信息（-t1）与内存条（-t17）。"""
import re

from .fields import parse_fields

# dmidecode 用这些占位符表示"没有这项信息"
_PLACEHOLDERS = {'Not Specified', 'Unknown', 'None', 'Undefined'}

_MAIN_BOARD_FIELDS = {
    'Manufacturer': 'manufacturer',
    'Product Name': 'model',
    'Serial Number': 'serial',
}

_MEMORY_FIELDS = {
    'Size': 'size',
    'Locator': 'slot',
    'Type': 'type',
    'Speed': 'speed',
    'Manufacturer': 'manufacturer',
    'Serial Number': 'serial',
}

_SIZE_RE = re.compile(r'(\d+)\s*(MB|GB)')
_NUMBER_RE = re.compile(r'\d+')


def parse_main_board(text):
    """返回主板信息；缺失的字段为 None。"""
    fields = parse_fields(text, _MAIN_BOARD_FIELDS)
    return {
        name: _clean(fields.get(name, ''))
        for name in _MAIN_BOARD_FIELDS.values()
    }


def parse_memory(text):
    """返回已安装的内存条列表。

    空槽位（Size: No Module Installed）不上报 —— 它不是内存条，
    报上去只会让消费端分不清"没装"和"容量为 0"。
    """
    modules = []
    for block in text.split('Memory Device')[1:]:
        fields = parse_fields(block, _MEMORY_FIELDS)
        capacity = _parse_capacity(fields.get('size', ''))
        if capacity is None:
            continue
        modules.append({
            'slot': fields.get('slot'),
            'type': _clean(fields.get('type', '')),
            'capacity_mb': capacity,
            'speed_mhz': _parse_number(fields.get('speed', '')),
            'manufacturer': _clean(fields.get('manufacturer', '')),
            'serial': _clean(fields.get('serial', '')),
        })
    return modules


def _clean(value):
    """占位符与空串一律转成 None，让"无"有唯一的表示。"""
    value = value.strip()
    if not value or value in _PLACEHOLDERS:
        return None
    return value


def _parse_capacity(value):
    """'1024 MB' -> 1024；'No Module Installed' -> None"""
    match = _SIZE_RE.search(value)
    if not match:
        return None
    number, unit = int(match.group(1)), match.group(2)
    return number * 1024 if unit == 'GB' else number


def _parse_number(value):
    """'667 MHz' -> 667"""
    match = _NUMBER_RE.search(value)
    return int(match.group()) if match else None
