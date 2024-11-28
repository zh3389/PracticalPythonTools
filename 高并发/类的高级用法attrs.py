import attr
from typing import List, Optional
from datetime import datetime, timedelta
import random


@attr.s(auto_attribs=True)
class Person:
    """
    描述一个人的类。

    属性:
        name (str): 名字。
        age (int): 年龄。
        height (float): 身高，单位cm。
    """
    name: str
    age: int
    height: float

    def greet(self) -> str:
        """
        生成问候语。
        :return: 问候语字符串。
        """
        return f"Hi, I'm {self.name}, {self.age} years old."


@attr.s(auto_attribs=True)
class Team:
    """
    描述一个团队的类，包含验证器功能。

    属性:
        name (str): 团队名称。
        members (List[str]): 成员名单。
        score (int): 团队得分，必须为正。
    """
    name: str
    members: List[str] = attr.ib(validator=attr.validators.instance_of(list))
    score: int = attr.ib(validator=lambda instance, attribute, value: value > 0)

    def add_member(self, member: str):
        """
        添加团队成员。
        :param member: 新成员的名字。
        """
        self.members.append(member)

    def update_score(self, new_score: int):
        """
        更新团队得分。
        :param new_score: 新得分，必须为正。
        """
        if new_score <= 0:
            raise ValueError("Score must be positive.")
        self.score = new_score


@attr.s(auto_attribs=True)
class Die:
    """
    描述一个骰子的类。

    属性:
        sides (int): 骰子的面数，默认6面。
        last_roll (int): 骰子的最后一次结果，随机生成。
    """
    sides: int = 6
    last_roll: int = attr.Factory(lambda: random.randint(1, 6))

    def roll(self) -> int:
        """
        投掷骰子，生成新结果。
        :return: 投掷结果。
        """
        self.last_roll = random.randint(1, self.sides)
        return self.last_roll


@attr.s(auto_attribs=True)
class Task:
    """
    描述一个任务的类。

    属性:
        name (str): 任务名称。
        description (str): 任务描述。
        due_date (datetime): 任务截止日期。
        is_completed (bool): 任务是否完成，默认未完成。
    """
    name: str
    description: str
    due_date: datetime
    is_completed: bool = False

    def complete(self):
        """
        标记任务为完成状态。
        """
        self.is_completed = True


@attr.s(auto_attribs=True)
class Project:
    """
    描述一个项目的类，包含多个任务。

    属性:
        name (str): 项目名称。
        tasks (List[Task]): 包含的任务列表。
        start_date (datetime): 项目开始时间，默认为当前时间。
        end_date (Optional[datetime]): 项目结束时间。
    """
    name: str
    tasks: List[Task] = attr.Factory(list)
    start_date: datetime = attr.Factory(datetime.now)
    end_date: Optional[datetime] = None

    def add_task(self, task: Task):
        """
        添加任务到项目中。
        :param task: Task 对象。
        """
        self.tasks.append(task)
        if self.end_date is None or task.due_date > self.end_date:
            self.end_date = task.due_date

    def complete_task(self, task_name: str):
        """
        根据名称标记任务为完成状态。
        :param task_name: 任务名称。
        """
        for task in self.tasks:
            if task.name == task_name:
                task.complete()
                break

    @property
    def progress(self) -> float:
        """
        计算项目进度。
        :return: 完成任务的百分比。
        """
        if not self.tasks:
            return 0.0
        return sum(task.is_completed for task in self.tasks) / len(self.tasks)


# 使用示例
if __name__ == "__main__":
    # 示例 1: Person 类
    alice = Person(name="Alice", age=30, height=165.0)
    print(alice.greet())

    # 示例 2: Team 类
    team = Team(name="Pythonistas", members=["Alice", "Bob"], score=10)
    team.add_member("Charlie")
    print(f"团队成员: {team.members}, 得分: {team.score}")

    # 示例 3: Die 类
    die = Die()
    print(f"初始投掷: {die.last_roll}")
    print(f"新投掷: {die.roll()}")

    # 示例 4: Project 类
    project = Project("Python魔法学习")
    project.add_task(Task("学习attrs", "深入理解attrs库", datetime.now() + timedelta(days=7)))
    project.add_task(Task("实践attrs", "在项目中应用attrs", datetime.now() + timedelta(days=14)))

    project.complete_task("学习attrs")
    print(f"项目进度：{project.progress:.0%}")
