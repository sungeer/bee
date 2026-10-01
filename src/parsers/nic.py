"""ip link show / ip addr show 输出解析。"""
import re

# '2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 ...'
_IFACE_RE = re.compile(r'\d+:\s+(\S+?)(?:@\S+)?:\s+<([^>]*)>')
# '    link/ether 00:1c:42:a5:57:7a brd ff:ff:ff:ff:ff:ff'
_MAC_RE = re.compile(r'link/ether\s+(\S+)')
# '    inet 10.211.55.4/24 brd 10.211.55.255 scope global eth0'
_INET_RE = re.compile(r'inet\s+(\d+\.\d+\.\d+\.\d+/\d+)')

# 不采集的接口前缀：loopback 与虚拟网桥
_EXCLUDED_PREFIXES = ('lo', 'pan', 'v')


def parse(text):
    """返回网卡列表。

    输入是 ip link 与 ip addr 两段输出的拼接，同一接口会出现两次，
    按接口名合并。
    """
    interfaces = {}
    current = None

    for line in text.splitlines():
        match = _IFACE_RE.match(line)
        if match:
            name, flags = match.group(1), match.group(2)
            if name.startswith(_EXCLUDED_PREFIXES):
                current = None
                continue
            current = interfaces.setdefault(name, {
                'name': name,
                'up': 'UP' in flags.split(','),
                'mac': None,
                'ipv4': [],
            })
            continue

        if current is None:
            continue

        match = _MAC_RE.search(line)
        if match:
            current['mac'] = match.group(1)
            continue

        match = _INET_RE.search(line)
        if match:
            current['ipv4'].append(_parse_inet(match.group(1)))

    return list(interfaces.values())


def _parse_inet(value):
    """'10.211.55.4/24' -> {'address': '10.211.55.4', 'netmask': '255.255.255.0'}"""
    address, _, prefix = value.partition('/')
    return {'address': address, 'netmask': cidr_to_netmask(int(prefix))}


def cidr_to_netmask(bits):
    """24 -> '255.255.255.0'"""
    mask = (0xffffffff << (32 - bits)) & 0xffffffff
    return '.'.join(str((mask >> shift) & 0xff) for shift in (24, 16, 8, 0))
