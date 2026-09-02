import os

# 应用版本
VERSION = '26.0903.0723'

# 项目根目录（本文件位于 src/ 下，父目录的父目录即项目根）
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 用于 API 认证的 KEY
KEY = '299095cc-1330-11e5-b06a-a45e60bec08b'
# 用于 API 认证的请求头名称
AUTH_KEY_NAME = 'auth-key'

# 错误日志 / 运行日志
ERROR_LOG_FILE = os.path.join(BASEDIR, 'logs', 'error.log')
RUN_LOG_FILE = os.path.join(BASEDIR, 'logs', 'run.log')

# Agent 模式保存服务器唯一 ID 的文件
CERT_FILE_PATH = os.path.join(BASEDIR, 'config', 'cert')

# 测试模式：为 True 时插件从 files/ 目录读取样例输出，不执行真实命令
TEST_MODE = True

# 采集方式，选项有：agent(本机)、salt、ssh(远程)
VALID_MODES = ('agent', 'ssh', 'salt')
MODE = 'ssh'
if MODE not in VALID_MODES:
    raise ValueError('MODE must be one of %s' % ', '.join(VALID_MODES))

# 如果采用 ssh 方式，则需要配置 ssh 的 KEY 和 USER
SSH_PRIVATE_KEY = '/home/auto/.ssh/id_rsa'
SSH_USER = 'root'
SSH_PORT = 22

# 采集硬件数据的插件：名称 -> 插件类路径，新增采集项在此注册
PLUGINS_DICT = {
    'cpu': 'src.plugins.cpu.CpuPlugin',
    'disk': 'src.plugins.disk.DiskPlugin',
    'main_board': 'src.plugins.main_board.MainBoardPlugin',
    'memory': 'src.plugins.memory.MemoryPlugin',
    'nic': 'src.plugins.nic.NicPlugin',
}

# 资产信息 API
ASSET_API = 'http://127.0.0.1:8000/api/asset'
"""
POST 返回值约定：{'code': xx, 'message': 'xx'}
  - 1000 成功
  - 1001 接口授权失败
  - 1002 数据库中资产不存在
"""
