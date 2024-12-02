"""
pip install luigi
"""

import luigi


class FetchDataTask(luigi.Task):
    """
    获取数据的任务。
    用法：从指定日期的源系统中获取数据并保存为本地文件。

    参数：
        date (str): 数据获取日期。
    """
    date = luigi.Parameter()  # 定义任务的参数

    def output(self):
        """
        定义任务的输出。
        输出：存储为 data_<date>.txt 文件。
        """
        return luigi.LocalTarget(f"data_{self.date}.txt")

    def run(self):
        """
        任务具体的执行逻辑。
        模拟获取数据并保存。
        """
        with self.output().open("w") as f:
            f.write("Hello, Luigi!")  # 模拟获取数据


class ProcessDataTask(luigi.Task):
    """
    处理数据的任务。
    用法：读取 `FetchDataTask` 的输出，进行简单的字符串处理，并保存结果。

    参数：
        date (str): 数据处理日期。
    """
    date = luigi.Parameter()

    def requires(self):
        """
        定义任务的依赖关系。
        本任务依赖于 FetchDataTask。
        """
        return FetchDataTask(date=self.date)

    def output(self):
        """
        定义任务的输出。
        输出：存储为 processed_<date>.txt 文件。
        """
        return luigi.LocalTarget(f"processed_{self.date}.txt")

    def run(self):
        """
        任务具体的执行逻辑。
        模拟处理数据并保存。
        """
        with self.input().open("r") as infile, self.output().open("w") as outfile:
            data = infile.read()
            outfile.write(f"Processed: {data}")  # 模拟处理数据


class ETLWorkflow:
    """
    一个完整的ETL工作流示例，包含数据提取、转换和加载的任务。
    """

    class ExtractDataTask(luigi.Task):
        """
        提取数据的任务。
        模拟从数据库提取原始数据。
        """

        def output(self):
            return luigi.LocalTarget("raw_data.csv")

        def run(self):
            data = [["id", "value"], ["1", "10"], ["2", "20"]]
            with self.output().open("w") as f:
                for row in data:
                    f.write(",".join(row) + "\n")

    class TransformDataTask(luigi.Task):
        """
        转换数据的任务。
        读取原始数据文件并对数值列进行简单的倍增操作。
        """

        def requires(self):
            return ETLWorkflow.ExtractDataTask()

        def output(self):
            return luigi.LocalTarget("transformed_data.csv")

        def run(self):
            with self.input().open("r") as infile, self.output().open("w") as outfile:
                next(infile)  # 跳过表头
                for line in infile:
                    id_, value = line.strip().split(",")
                    new_value = int(value) * 2
                    outfile.write(f"{id_},{new_value}\n")


if __name__ == "__main__":
    # 示例1：运行简单任务链
    luigi.build([ProcessDataTask(date="2024-03-20")], local_scheduler=True)

    # 示例2：运行完整ETL流程
    luigi.build([ETLWorkflow.TransformDataTask()], local_scheduler=True)
