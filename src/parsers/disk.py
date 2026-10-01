"""MegaCli -PDList -aALL 输出解析。"""
import re

from src.parsers.fields import parse_fields

# 每块物理盘之间以四个换行分隔
_BLOCK_SEPARATOR = '\n\n\n\n'

_DISK_FIELDS = {
    'Slot Number': 'slot',
    'PD Type': 'type',
    'Raw Size': 'size',
    'Inquiry Data': 'model',
}

_SIZE_RE = re.compile(r'([\d.]+)\s*GB')


def parse(text):
    """返回磁盘列表。"""
    disks = []
    for block in text.split(_BLOCK_SEPARATOR):
        fields = parse_fields(block, _DISK_FIELDS)
        if 'slot' not in fields:
            continue  # 尾部的 Exit Code 之类没有槽位的段落
        disks.append({
            'slot': fields['slot'],
            'type': fields.get('type'),
            'capacity_mb': _to_mb(fields.get('size', '')),
            'model': ' '.join(fields.get('model', '').split()) or None,
        })
    return disks


def _to_mb(value):
    """'279.396 GB [0x22ecb25c Sectors]' -> 286102（MB 整数）"""
    match = _SIZE_RE.search(value)
    if not match:
        return None
    return round(float(match.group(1)) * 1024)
