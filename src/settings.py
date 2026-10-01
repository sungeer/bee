import os
from pathlib import Path

from dotenv import load_dotenv

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

_dotenv_path = BASE_DIR / '.env'
if _dotenv_path.exists():
    load_dotenv(_dotenv_path)


def _require(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f'Missing required environment variables: {name}')
    return value


VERSION = '26.1001.1850'

# 环境
_ENVIRONMENTS = ('development', 'testing', 'production')
ENVIRONMENT = _require('ENVIRONMENT')
if ENVIRONMENT not in _ENVIRONMENTS:
    raise ValueError(f'Invalid ENVIRONMENT: {ENVIRONMENT}，only allowed {sorted(_ENVIRONMENTS)}')

# 日志
LOG_DIR = Path(os.getenv('LOG_DIR', default=str(BASE_DIR / 'logs')))

# 资产 API
ASSET_API = 'http://127.0.0.1:8848/api/asset'

# API 认证 请求头名称与密钥
AUTH_KEY_HEADER = 'X-Auth-Key'
AUTH_KEY = '299095cc-1330-11e5-b06a-a45e60bec08b'

# Linux 部署可用 BEE_DATA_DIR 指向 /var/lib/bee 等系统目录
DATA_DIR = os.environ.get('BEE_DATA_DIR') or os.path.join(BASE_DIR, 'data')

# 本机资产标识文件：首次采集时写入主机名，之后以它为准
ASSET_ID_FILE = os.path.join(DATA_DIR, 'asset_id')

# 采集项的样例输出目录
FIXTURE_DIR = os.path.join(BASE_DIR, 'files')
