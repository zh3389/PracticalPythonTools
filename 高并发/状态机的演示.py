from enum import Enum
from typing import Dict, List, Optional, Callable
import logging
import unittest


"""在生产环境中，适当的日志记录对于问题排查至关重要"""
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
什么是状态机？
状态机（也称有限状态机，Finite State Machine，FSM）是一个抽象的机器，它在任一时刻只能处于一个状态，并且可以通过某些条件从一个状态转换到另一个状态。
状态机主要包含三个核心要素：
• 状态（State）：对象在某一时刻的具体状态
• 事件（Event）：触发状态转换的条件
• 转换（Transition）：从一个状态到另一个状态的过程

状态机的分类状态机主要可以分为两类：
1. Moore状态机：输出只依赖于当前状态。例如，电梯门在每层楼停下时都会打开，这个动作只取决于"停止"这个状态。
2. Mealy状态机：输出不仅依赖于当前状态，还依赖于输入。例如，电梯在某一层是否停止，不仅取决于当前所在的楼层，还要看是否有人按下了这一层的按钮。在实际应用中，我们经常会使用这两种状态机的混合形式。

状态机的应用场景状态机在实际开发中有广泛的应用：
1. 游戏开发：控制角色动画、AI行为等2. 工作流管理：订单流转、审批流程等3. 协议实现：TCP协议状态管理4. UI交互：界面状态切换5. 业务流程：订单状态、支付流程等

使用状态机的优势
1. 代码结构清晰：避免了大量的if-else嵌套2. 易于维护：状态转换逻辑集中管理3. 业务逻辑清晰：状态和转换关系一目了然4. 扩展性好：易于添加新状态和转换规则

实践建议
1. 从简单开始：最初可以只实现基本的状态转换功能，随着需求的增加再逐步添加更多特性。
2. 注意并发安全：在多线程环境下，需要确保状态转换的原子性，可以使用锁或事务来保证。
3. 考虑可观察性：添加适当的监控和告警机制，及时发现异常的状态转换。
4. 文档化：维护清晰的状态转换图和文档，帮助团队成员理解业务流程。
5. 定期重构：随着业务规则的变化，及时调整状态机的实现，保持代码的清晰性。总结
"""


"""
1. 基础演示 ✅
2. 状态机钩子函数 ✅
3. 状态机的持久化 ✅
4. 状态定义清晰化 ✅
5. 状态转换规则可配置化 ✅
6. 异常处理 ✅
7. 状态机测试 ✅
8. 日志记录 ✅
9. 状态机组合
10. 状态机可视化 ✅
11. 状态机与业务规则集成
"""


class InvalidStateTransition(Exception):
    """非法状态转换异常"""
    pass


class OrderState(Enum):
    """订单状态枚举
    CREATED: 订单已创建,等待支付
    PAID: 订单已支付,等待发货
    SHIPPED: 订单已发货,等待签收
    DELIVERED: 订单已签收,交易完成
    CANCELLED: 订单已取消
    """
    CREATED = "created"  # 已创建，等待支付
    PAID = "paid"  # 已支付，等待发货
    SHIPPED = "shipped"  # 已发货，等待签收
    DELIVERED = "delivered"  # 已签收，交易完成
    CANCELLED = "cancelled"  # 已取消


class OrderStateMachine:
    """订单状态机
    在这个例子中，我们实现了一个简单的订单状态机，它管理订单从创建到交付的整个生命周期。状态机确保了订单状态只能按照预定义的规则进行转换，比如已发货的订单不能回退到已创建状态。
    """

    def __init__(self, state: Optional[OrderState] = None) -> None:
        """
        将状态转换规则抽取为配置,便于维护和修改
        """
        self.state_transitions: Dict[OrderState, Dict[OrderState, Callable]] = {
            OrderState.CREATED: {OrderState.PAID: self.pay_order, OrderState.CANCELLED: self.cancel_order},
            OrderState.PAID: {OrderState.SHIPPED: self.ship_order, OrderState.CANCELLED: self.cancel_and_refund},
            OrderState.SHIPPED: {OrderState.DELIVERED: self.complete_order},
            OrderState.DELIVERED: {},
            OrderState.CANCELLED: {}
        }
        self.current_state = state or OrderState.CREATED

    def pay_order(self):
        """模拟支付订单"""
        logger.info("订单支付成功")

    def ship_order(self):
        """模拟发货"""
        logger.info("订单已发货")

    def cancel_order(self):
        """取消订单"""
        logger.info("订单取消成功")

    def cancel_and_refund(self):
        """取消订单并退款"""
        logger.info("订单取消并退款成功")

    def complete_order(self):
        """订单完成"""
        logger.info("订单已完成")

    def before_transition(self, from_state: OrderState, to_state: OrderState):
        """状态机钩子函数
        在状态转换的过程中,我们经常需要在状态变化前后执行一些操作,比如日志记录、数据验证等。这时可以使用钩子函数:
        """
        print(f"准备从 {from_state.value} 转换到 {to_state.value}")
        #  可以在这里添加验证逻辑

    def after_transition(self, from_state: OrderState, to_state: OrderState):
        """状态机钩子函数
        在状态转换的过程中,我们经常需要在状态变化前后执行一些操作,比如日志记录、数据验证等。这时可以使用钩子函数:
        """
        print(f"已从 {from_state.value} 转换到 {to_state.value}")
        #  可以在这里记录日志或发送通知

    def transition_to(self, new_state: OrderState) -> bool:
        """状态转换"""
        try:
            if new_state not in self.state_transitions[self.current_state]:
                raise InvalidStateTransition(f"非法状态转换：{self.current_state.value} -> {new_state.value}")
            logger.info(f"状态转换：{self.current_state.value} -> {new_state.value}")
            # 执行钩子函数
            old_state = self.current_state
            self.before_transition(old_state, new_state)
            self.state_transitions[self.current_state][new_state]()
            self.current_state = new_state
            self.after_transition(old_state, new_state)
            # 钩子函数执行完毕
            return True
        except Exception as e:
            logger.error(f"状态转换失败：{str(e)}")
            return False

    def visualize(self, filename: str = "状态机流程图"):
        """状态机可视化"""
        import graphviz
        dot = graphviz.Digraph(comment="Order State Machine")
        for from_state, transitions in self.state_transitions.items():
            for to_state in transitions:
                dot.edge(from_state.value, to_state.value)
        dot.render(filename, format="png", cleanup=True)
        logger.info(f"状态机图已生成：{filename}.png")
        

class PersistentOrderStateMachine(OrderStateMachine):
    """
    持久化状态机
    在实际应用中,我们可能需要将状态机的状态持久化到数据库中
    """
    def __init__(self, order_id: str):
        super().__init__()
        self.order_id = order_id

    def load_state(self):
        # 从数据库加载状态
        state_value = db.get_order_state(self.order_id)
        self.current_state = OrderState(state_value)

    def save_state(self):
        # 保存状态到数据库
        db.save_order_state(self.order_id, self.current_state.value)

    def transition_to(self, new_state: OrderState) -> bool:
        if super().transition_to(new_state):
            self.save_state()
            return True
        return False


class TestOrderStateMachine(unittest.TestCase):
    """为状态机编写完整的单元测试非常重要"""
    def setUp(self):
        self.fsm = OrderStateMachine()

    def test_initial_state(self):
        self.assertEqual(self.fsm.current_state, OrderState.CREATED)

    def test_valid_transition(self):
        self.assertTrue(self.fsm.transition_to(OrderState.PAID))
        self.assertEqual(self.fsm.current_state, OrderState.PAID)

    def test_invalid_transition(self):
        self.fsm.transition_to(OrderState.PAID)
        self.assertFalse(self.fsm.transition_to(OrderState.CREATED))


def main_test():
    order = OrderStateMachine()

    # 初始状态
    logger.info(f"当前订单状态：{order.current_state.value}")

    # 状态转换
    order.transition_to(OrderState.PAID)
    order.transition_to(OrderState.SHIPPED)
    order.transition_to(OrderState.DELIVERED)

    # 非法状态转换
    order.transition_to(OrderState.CREATED)

    # 状态机可视化
    order.visualize()


# 测试代码
if __name__ == "__main__":
    # main_test()
    unittest.main()
