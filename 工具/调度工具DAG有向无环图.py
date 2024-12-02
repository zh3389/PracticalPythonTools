from airflow import DAG  # pip install apache-airflow
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import random


class AirflowWorkflow:
    """
    一个面向对象的Airflow工作流示例，帮助初学者快速了解DAG、任务和依赖关系。
    """

    def __init__(self, dag_id, description, start_date, schedule_interval, default_args):
        """
        初始化工作流参数。
        :param dag_id: DAG的唯一标识符
        :param description: 描述DAG的用途
        :param start_date: 工作流开始的时间
        :param schedule_interval: 定时调度间隔
        :param default_args: 默认参数设置
        """
        self.dag = DAG(
            dag_id=dag_id,
            description=description,
            start_date=start_date,
            schedule_interval=schedule_interval,
            default_args=default_args,
        )

    def create_task(self, task_id, python_callable):
        """
        创建一个Python任务。
        :param task_id: 任务的唯一标识符
        :param python_callable: 执行任务的Python函数
        :return: 一个PythonOperator对象
        """
        return PythonOperator(
            task_id=task_id,
            python_callable=python_callable,
            dag=self.dag,
        )

    def get_dag(self):
        """
        获取DAG对象以供Airflow调度器使用。
        """
        return self.dag


# 自定义任务逻辑
def extract_data():
    print("开始提取数据...")


def transform_data():
    print("开始转换数据...")


def load_data():
    print("开始加载数据...")


def generate_random_number():
    random_number = random.randint(1, 100)
    print(f"生成的随机数是: {random_number}")
    return random_number


def check_even_odd(**context):
    random_number = context['task_instance'].xcom_pull(task_ids='generate_random_number')
    if random_number % 2 == 0:
        print(f"{random_number} 是偶数")
    else:
        print(f"{random_number} 是奇数")


# 定义默认参数
default_args = {
    'owner': 'myself',
    'depends_on_past': False,
    'email': ['your_email@example.com'],
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# 初始化工作流
workflow = AirflowWorkflow(
    dag_id='daily_data_pipeline',
    description='每日数据处理流程',
    start_date=datetime(2024, 1, 1),
    schedule_interval='0 1 * * *',
    default_args=default_args,
)

# 创建任务
task_extract = workflow.create_task('extract_data', extract_data)
task_transform = workflow.create_task('transform_data', transform_data)
task_load = workflow.create_task('load_data', load_data)

# 随机数生成与判断任务
task_generate_random = workflow.create_task('generate_random_number', generate_random_number)
task_check_even_odd = workflow.create_task('check_even_odd', check_even_odd)

# 设置依赖关系
task_extract >> task_transform >> task_load
task_generate_random >> task_check_even_odd

# 提供DAG对象供Airflow调度
dag = workflow.get_dag()
