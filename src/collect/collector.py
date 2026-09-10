import importlib

from src import settings
from src.collect.plugins.basic import BasicPlugin


def collect_asset(hostname=None):
    """采集一台主机的资产数据并合并成一份。

    :param hostname: agent 模式传空表示本机；ssh/salt 模式传要连接的远程主机名
    :return: BaseResponse(data=合并后的资产 dict)
    """
    result = BasicPlugin(hostname).execute()
    if not result.status:
        return result

    for name, path in settings.PLUGINS_DICT.items():
        module_path, _, class_name = path.rpartition('.')
        plugin_class = getattr(importlib.import_module(module_path), class_name)
        result.data[name] = plugin_class(hostname).execute()

    return result


if __name__ == '__main__':
    ret = collect_asset()
    print(ret.__dict__)
