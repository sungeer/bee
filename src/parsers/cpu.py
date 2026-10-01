"""/proc/cpuinfo 解析。"""


def parse(text):
    """返回 CPU 型号、物理颗数与逻辑处理器数。"""
    logical_processors = 0
    sockets = set()
    model = ''

    for line in text.splitlines():
        label, sep, value = line.partition(':')
        if not sep:
            continue
        label = label.strip()
        value = value.strip()
        if label == 'processor':
            logical_processors += 1
        elif label == 'physical id':
            sockets.add(value)
        elif label == 'model name' and not model:
            model = value

    return {
        'model': model,
        'sockets': len(sockets),
        'logical_processors': logical_processors,
    }
