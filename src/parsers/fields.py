"""从 'key: value' 形式的文本中提取字段。

MegaCli 和 dmidecode 的输出都是这种形状，共用这一份提取逻辑。
"""


def parse_fields(text, field_map):
    """按 field_map 提取字段，返回 {输出字段名: 值}。

    :param field_map: 原始标签 -> 输出字段名。不在表内的行会被忽略，
                      所以同一份输出里夹带的无关字段不会混进来。
    """
    fields = {}
    for line in text.splitlines():
        label, sep, value = line.partition(':')
        if not sep:
            continue
        name = field_map.get(label.strip())
        if name:
            fields[name] = value.strip()
    return fields
