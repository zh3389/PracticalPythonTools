"""
pip install fabric
"""

from fabric import Connection, SerialGroup
from invoke.exceptions import UnexpectedExit
import time
import os


class FabricDeployer:
    """
    FabricDeployer 是一个基于 Fabric 的自动化部署工具类，用于简化项目部署流程。
    """

    def __init__(self, host, user, ssh_key_path):
        """
        初始化连接信息。

        :param host: 远程服务器地址
        :param user: 登录用户名
        :param password: 登录密码
        :param ssh_key_path: SSH 私钥路径
        """
        self.connection = Connection(
            host=f"{user}@{host}",
            # connect_kwargs={"password": password}
            connect_kwargs={"key_filename": ssh_key_path}
        )

    def execute_command(self, command):
        """
        在远程服务器上执行命令。

        :param command: 要执行的命令
        :return: 命令输出
        """
        try:
            result = self.connection.run(command, hide=True)
            print(f"[Success] {command}: {result.stdout.strip()}")
            return result.stdout.strip()
        except UnexpectedExit as e:
            print(f"[Error] {command} failed: {e.result.stderr.strip()}")
            return None

    def upload_file(self, local_path, remote_path):
        """
        上传文件到远程服务器。

        :param local_path: 本地文件路径
        :param remote_path: 远程目标路径
        """
        self.connection.put(local_path, remote=remote_path)
        print(f"[Success] Uploaded {local_path} to {remote_path}")

    def download_file(self, remote_path, local_path):
        """
        从远程服务器下载文件。

        :param remote_path: 远程文件路径
        :param local_path: 本地目标路径
        """
        self.connection.get(remote_path, local=local_path)
        print(f"[Success] Downloaded {remote_path} to {local_path}")

    def deploy_app(self, local_dist, remote_dir):
        """
        自动部署应用。

        :param local_dist: 本地构建目录
        :param remote_dir: 远程部署目录
        """
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        backup_path = f"{remote_dir}_backup_{timestamp}"

        # 备份当前版本
        self.execute_command(f"cp -r {remote_dir} {backup_path}")
        print(f"[Info] Backup created at {backup_path}")

        # 上传新代码
        self.upload_file(local_dist, remote_dir)

        # 重启服务
        self.execute_command("systemctl restart nginx")
        print("[Info] Deployment completed!")


class BatchDeployer:
    """
    BatchDeployer 是一个支持批量操作的工具类，用于同时管理多台服务器。
    """

    def __init__(self, hosts):
        """
        初始化批量服务器信息。

        :param hosts: 服务器地址列表
        """
        self.group = SerialGroup(*hosts)

    def execute_batch_command(self, command):
        """
        在所有服务器上执行命令。

        :param command: 要执行的命令
        """
        results = self.group.run(command, hide=True)
        for conn, result in results.items():
            print(f"[{conn.host}] {result.stdout.strip()}")


# 使用示例
if __name__ == "__main__":
    # 单服务器部署示例
    deployer = FabricDeployer(host="43.142.4.76", user="root", ssh_key_path="/Users/zh/.ssh/id_rsa")
    deployer.execute_command("uname -a")
    deployer.execute_command("ls -l")
    # deployer.deploy_app(local_dist="./dist/", remote_dir="/var/www/app")

    # 批量操作示例
    # batch_deployer = BatchDeployer(hosts=["web1.com", "web2.com", "web3.com"])
    # batch_deployer.execute_batch_command("uname -a")
