"""
这个模块包含了一些关于 Python 描述器（Descriptor）特性的示例。
通过这些示例可以学习描述器的定义、使用场景和最佳实践。

描述器是一种实现了特殊方法（如 __get__、__set__ 等）的类，
可以用来自定义对象属性的访问行为。

模块内容：
1. 数据描述器示例（DataDescriptor）
2. 非数据描述器示例（LazyLoader）
3. 属性验证描述器（RangeValidator）
4. 缓存属性描述器（CachedProperty）
5. 自定义 property 描述器（CustomProperty）
"""


# 数据描述器示例：对属性赋值时进行类型检查
class DataDescriptor:
    """
    数据描述器示例，确保属性值是整数。
    """

    def __get__(self, obj, objtype=None):
        return self._value

    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise TypeError("值必须是整数")
        self._value = value


# 非数据描述器示例：延迟加载属性
class LazyLoader:
    """
    非数据描述器示例，实现延迟加载。

    用法：
        - 将描述器作为装饰器，用于需要延迟加载的属性。
    """

    def __init__(self, loader_func):
        self.loader_func = loader_func
        self.loaded_value = None

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.loaded_value is None:
            self.loaded_value = self.loader_func(obj)
        return self.loaded_value


# 属性验证描述器
class RangeValidator:
    """
    属性验证描述器，用于验证属性值是否在指定范围内。

    参数：
        min_value (float, optional): 最小值
        max_value (float, optional): 最大值
    """

    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name}的值不能小于{self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name}的值不能大于{self.max_value}")
        obj.__dict__[self.name] = value


# 缓存属性描述器
class CachedProperty:
    """
    缓存属性描述器，用于缓存复杂计算结果，避免重复计算。

    用法：
        - 用装饰器的方式为类方法添加缓存功能。
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if obj not in self.cache:
            self.cache[obj] = self.func(obj)
        return self.cache[obj]


# 自定义 property 描述器
class CustomProperty:
    """
    自定义 property 描述器，用于实现 getter 和 setter 方法。

    参数：
        fget (callable): 获取属性值的方法
        fset (callable, optional): 设置属性值的方法
        fdel (callable, optional): 删除属性值的方法
    """

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("无法读取属性")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("无法设置属性")
        self.fset(obj, value)

    def setter(self, func):
        return type(self)(self.fget, func, self.fdel, self.__doc__)


# 示例使用
class ExampleUsage:
    """
    结合描述器的示例类。
    """

    # 使用数据描述器
    int_field = DataDescriptor()

    # 使用属性验证描述器
    age = RangeValidator(min_value=0, max_value=150)
    score = RangeValidator(min_value=0, max_value=100)

    # 使用延迟加载描述器
    @LazyLoader
    def large_dataset(self):
        print("加载大型数据集...")
        return [i for i in range(1000000)]  # 模拟大数据加载

    # 使用缓存属性描述器
    @CachedProperty
    def complex_calculation(self):
        print("执行复杂计算...")
        return sum(i * i for i in range(1000))

    # 使用自定义 property 描述器
    def __init__(self):
        self._name = ""

    @CustomProperty
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("名字必须是字符串")
        self._name = value


if __name__ == "__main__":
    # 示例测试
    student = ExampleUsage()

    # 测试属性验证
    student.age = 25
    student.score = 90

    # 测试延迟加载
    print(student.large_dataset[:5])

    # 测试缓存计算
    print(student.complex_calculation)
    print(student.complex_calculation)  # 再次访问，避免重新计算

    # 测试自定义 property
    student.name = "Alice"
    print(student.name)
