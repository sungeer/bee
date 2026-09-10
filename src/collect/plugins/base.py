import os
import traceback

from src import settings
from src.common.logger import Logger
from src.common.response import BaseResponse


class BasePlugin:
    """插件基类：统一命令执行方式与采集异常的返回容器。

    子类只需实现 collect()，返回解析后的数据(dict/list)即可；
    shell 命令在本地/ssh/salt 间切换、测试模式读样例文件、异常转 BaseResponse
    等通用逻辑都收敛在本类。
    """

    VALID_MODES = ('agent', 'ssh', 'salt')

    def __init__(self, hostname=''):
        self.logger = Logger()
        self.test_mode = settings.TEST_MODE
        self.mode = getattr(settings, 'MODE', 'agent')
        self.hostname = hostname

    # ----- 命令执行：按采集方式分派 -----

    def salt(self, cmd):
        import salt.client

        local = salt.client.LocalClient()
        result = local.cmd(self.hostname, 'cmd.run', [cmd])
        return result[self.hostname]

    def ssh(self, cmd):
        import paramiko

        private_key = paramiko.RSAKey.from_private_key_file(settings.SSH_PRIVATE_KEY)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, port=settings.SSH_PORT, username=settings.SSH_USER, pkey=private_key)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        ssh.close()
        return result

    def agent(self, cmd):
        import subprocess

        output = subprocess.getoutput(cmd)
        return output

    def exec_shell_cmd(self, cmd):
        """按 settings.MODE 选择执行方式运行 shell 命令"""
        if self.mode not in self.VALID_MODES:
            raise ValueError("settings.MODE must be one of ['agent', 'salt', 'ssh']")
        func = getattr(self, self.mode)
        return func(cmd)

    # ----- 样例数据 / 采集样板 -----

    def read_fixture(self, fixture):
        """读取 files/ 目录下的样例输出（测试模式使用）"""
        path = os.path.join(settings.BASEDIR, 'files', fixture)
        with open(path, encoding='utf-8') as f:
            return f.read()

    def capture(self, command, fixture):
        """获取原始输出：测试模式读样例文件，否则执行真实 shell 命令"""
        if self.test_mode:
            return self.read_fixture(fixture)
        return self.exec_shell_cmd(command)

    def execute(self):
        """对外采集入口：调用 collect()，把异常统一封装成 BaseResponse"""
        response = BaseResponse()
        try:
            response.data = self.collect()
        except Exception:
            message = '%s %s plugin error: %s' % (
                self.hostname, type(self).__name__, traceback.format_exc())
            self.logger.log(message, False)
            response.status = False
            response.error = message
        return response

    def collect(self):
        """子类实现采集逻辑；异常由 execute() 统一处理"""
        raise NotImplementedError('You must implement collect method.')
