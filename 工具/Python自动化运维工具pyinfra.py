"""
封装 pyinfra 常用功能的 Python 类，便于实现自动化运维。
适用于服务器管理、批量部署应用、自动化操作等场景。
pip install pyinfra

执行方式：保存为 XXX.py 后，在终端运行：pyinfra XXX.py
"""

from pyinfra.operations import server, apt, files


class PyinfraHelper:
    """
    PyinfraHelper 是一个封装 pyinfra 常用功能的工具类。
    """

    def __init__(self, targets):
        """
        初始化 PyinfraHelper 实例。

        :param targets: list，目标服务器地址列表（格式为 'user@ip'）
        """
        self.targets = targets

    def execute_command(self, command):
        """
        在目标服务器上远程执行命令。

        :param command: str，要执行的命令
        """
        server.shell(hosts=self.targets, commands=command)
        print(f"命令 `{command}` 已在服务器 {self.targets} 上执行。")

    def install_packages(self, packages, update=False):
        """
        在目标服务器上安装指定的软件包。

        :param packages: list，要安装的软件包名称列表
        :param update: bool，是否先更新包管理器（默认为 False）
        """
        apt.packages(
            hosts=self.targets,
            packages=packages,
            update=update
        )
        print(f"软件包 {packages} 已在服务器 {self.targets} 上安装。")

    def upload_file(self, local_path, remote_path):
        """
        将本地文件上传到目标服务器。

        :param local_path: str，本地文件路径
        :param remote_path: str，远程服务器目标路径
        """
        files.put(
            hosts=self.targets,
            src=local_path,
            dest=remote_path
        )
        print(f"文件 {local_path} 已上传到服务器 {self.targets} 的 {remote_path}。")

    def deploy_web_app(self, app_local_path, remote_path, restart_command=None):
        """
        将 Web 应用部署到目标服务器，并重启相关服务。

        :param app_local_path: str，本地应用目录路径
        :param remote_path: str，远程目标路径
        :param restart_command: str，可选，重启服务的命令（例如 'systemctl restart nginx'）
        """
        # 上传应用目录到服务器
        self.upload_file(app_local_path, remote_path)

        # 重启服务
        if restart_command:
            self.execute_command(restart_command)
        print(f"Web 应用已部署到服务器 {self.targets}，并完成服务重启（如指定）。")


if __name__ == '__main__':
    # 示例使用
    pyinfra_helper = PyinfraHelper(targets=['root@43.142.4.76'])
    pyinfra_helper.execute_command('ls -l')
    pyinfra_helper.execute_command('echo "Hello from pyinfra!"')
    pyinfra_helper.install_packages(['python3', 'git'])
    pyinfra_helper.deploy_web_app('/path/to/app', '/var/www/html', 'systemctl restart nginx')
