import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys
import subprocess


class HotReloader:
    """
    热加载器类：实现对指定目录下 Python 脚本的监控，并在文件变化时重新加载和执行目标脚本。

    Attributes:
        script_path (str): 需要监控并执行的目标脚本路径。
        watch_path (str): 需要监控的文件夹路径。
    """

    class _ChangeHandler(FileSystemEventHandler):
        """
        内部类，用于处理文件变化事件。
        """

        def __init__(self, script_path):
            """
            初始化事件处理器。

            Args:
                script_path (str): 目标脚本路径。
            """
            self.script_path = script_path
            self.process = None
            self._start_script()

        def _start_script(self):
            """
            启动目标脚本。
            """
            self.process = subprocess.Popen([sys.executable, self.script_path])
            print(f"Started script: {self.script_path}")

        def _restart_script(self):
            """
            重新启动目标脚本。
            """
            print("Restarting script...")
            self.process.terminate()  # 终止进程
            self.process.wait()       # 等待进程终止
            self._start_script()      # 重启脚本

        def on_modified(self, event):
            """
            当监控目录内文件被修改时触发。

            Args:
                event (FileSystemEvent): 文件系统事件。
            """
            if not event.is_directory and event.src_path.endswith('.py'):
                print(f"File modified: {event.src_path}")
                self._restart_script()

    def __init__(self, script_path: str, watch_path: str = "."):
        """
        初始化热加载器。

        Args:
            script_path (str): 目标脚本路径。
            watch_path (str): 监控文件夹路径，默认为当前目录。
        """
        self.script_path = script_path
        self.watch_path = watch_path
        self.observer = Observer()
        self.event_handler = self._ChangeHandler(script_path)

    def start(self):
        """
        启动监控器。
        """
        print(f"Watching directory: {os.path.abspath(self.watch_path)}")
        self.observer.schedule(self.event_handler, path=self.watch_path, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping observer...")
            self.observer.stop()
        self.observer.join()


if __name__ == "__main__":
    # 示例用法
    target_script = "main.py"  # 需要监控和执行的脚本
    watch_directory = "."      # 监控当前目录

    reloader = HotReloader(script_path=target_script, watch_path=watch_directory)
    reloader.start()
