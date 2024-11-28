from rq import Queue, Worker
from redis import Redis
from datetime import datetime, timedelta
import time


class RQTaskManager:
    """
    RQ (Redis Queue) 任务管理器，封装基本操作，包括任务队列管理、任务执行和异常处理。
    """

    def __init__(self, redis_host='localhost', redis_port=6379, queue_name='default'):
        """
        初始化任务管理器，连接 Redis 并创建任务队列。

        :param redis_host: Redis 主机地址
        :param redis_port: Redis 端口
        :param queue_name: 队列名称，默认为 'default'
        """
        self.redis_conn = Redis(host=redis_host, port=redis_port)
        self.queue = Queue(queue_name, connection=self.redis_conn)

    def enqueue_task(self, func, *args, timeout=None, schedule_time=None, **kwargs):
        """
        将任务添加到队列。

        :param func: 要执行的任务函数
        :param args: 任务函数的位置参数
        :param timeout: 超时时间，单位秒
        :param schedule_time: 任务的计划执行时间（datetime 对象）
        :param kwargs: 任务函数的关键字参数
        :return: 任务对象
        """
        if schedule_time:
            return self.queue.enqueue_at(schedule_time, func, *args, **kwargs)
        return self.queue.enqueue(func, *args, timeout=timeout, **kwargs)

    def fetch_job(self, job_id):
        """
        获取任务对象。

        :param job_id: 任务 ID
        :return: 任务对象
        """
        return self.queue.fetch_job(job_id)

    @staticmethod
    def get_job_status(job):
        """
        获取任务状态信息。

        :param job: 任务对象
        :return: 包含任务状态的字典
        """
        return {
            "is_finished": job.is_finished,
            "is_failed": job.is_failed,
            "result": job.result,
            "exception": job.exc_info,
        }

    @staticmethod
    def start_worker(queue_names=('default',)):
        """
        启动工作进程。

        :param queue_names: 要监听的队列名称列表
        """
        Worker(queue_names).work()


# 示例任务函数
def send_mail(to, subject):
    """
    模拟发送邮件任务。
    """
    time.sleep(5)  # 模拟耗时操作
    return f"邮件发送成功：{to}, 主题：{subject}"


def risky_job():
    """
    模拟可能会失败的任务。
    """
    raise Exception("任务失败了！")


if __name__ == "__main__":
    # 初始化任务管理器
    manager = RQTaskManager(queue_name="high")

    # 添加任务到队列
    print("添加普通任务")
    job = manager.enqueue_task(send_mail, "xiaoming@qq.com", "周末约饭")
    print(f"任务 ID: {job.id}")

    # 查看任务状态
    job_info = manager.get_job_status(job)
    print(f"任务状态: {job_info}")

    # 添加定时任务
    print("添加定时任务")
    future_time = datetime.now() + timedelta(seconds=30)
    job = manager.enqueue_task(send_mail, "xiaoming@qq.com", "定时邮件", schedule_time=future_time)
    print(f"定时任务 ID: {job.id}")

    # 处理任务异常
    print("添加可能失败的任务")
    job = manager.enqueue_task(risky_job)
    job_info = manager.get_job_status(job)
    print(f"异常信息: {job_info.get('exception')}")

    # 提示：运行工作进程需要在命令行中单独启动：
    # rq worker high default
