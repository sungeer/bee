"""运行配置。

部署相关的可变项集中在这里。采集项本身的定义在 collect.py ——
那是代码结构（改了要重新发布），不是配置。
"""
import os

# 项目根目录（本文件位于 bee/ 下，父目录即项目根）
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VERSION = '26.1001.1731'

# 资产 API
ASSET_API = 'http://127.0.0.1:8000/api/asset'
# API 认证：请求头名称与密钥
AUTH_KEY_HEADER = 'auth-key'
AUTH_KEY = '299095cc-1330-11e5-b06a-a45e60bec08b'

# 日志
RUN_LOG_FILE = os.path.join(BASEDIR, 'logs', 'run.log')
ERROR_LOG_FILE = os.path.join(BASEDIR, 'logs', 'error.log')

# 数据目录：默认在项目 data/ 下；
# Linux 部署可用 BEE_DATA_DIR 指向 /var/lib/bee 等系统目录
DATA_DIR = os.environ.get('BEE_DATA_DIR') or os.path.join(BASEDIR, 'data')

# 本机资产标识文件：首次采集时写入主机名，之后以它为准
ASSET_ID_FILE = os.path.join(DATA_DIR, 'asset_id')

# 采集项的样例输出目录
FIXTURE_DIR = os.path.join(BASEDIR, 'files')

# 测试模式：为 True 时从 FIXTURE_DIR 读样例输出，不执行真实命令
TEST_MODE = True
