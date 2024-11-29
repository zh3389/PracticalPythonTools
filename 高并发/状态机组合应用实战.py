from enum import Enum
from typing import Dict, List
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 定义订单状态枚举
class OrderState(Enum):
    """订单状态枚举"""
    CREATED = "created"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# 定义支付状态枚举
class PaymentState(Enum):
    """支付状态枚举"""
    UNPAID = "unpaid"
    PAID = "paid"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


# 定义状态转换异常
class InvalidStateTransition(Exception):
    pass


# 基础状态机类
class BaseStateMachine:
    def __init__(self, initial_state: Enum, state_transitions: Dict[Enum, List[Enum]]):
        self.current_state = initial_state
        self.state_transitions = state_transitions

    def can_transition_to(self, new_state: Enum) -> bool:
        """检查是否可以进行状态转换"""
        return new_state in self.state_transitions[self.current_state]

    def before_transition(self, from_state: Enum, to_state: Enum):
        """状态转换前操作"""
        logger.info(f"准备从 {from_state.value} 转换到 {to_state.value}")

    def after_transition(self, from_state: Enum, to_state: Enum):
        """状态转换后操作"""
        logger.info(f"已从 {from_state.value} 转换到 {to_state.value}")

    def transition_to(self, new_state: Enum) -> bool:
        """执行状态转换"""
        try:
            if not self.can_transition_to(new_state):
                raise InvalidStateTransition(
                    f"不允许从 {self.current_state.value} 转换到 {new_state.value}"
                )
            old_state = self.current_state
            self.before_transition(old_state, new_state)
            self.current_state = new_state
            self.after_transition(old_state, new_state)
            return True
        except Exception as e:
            logger.error(f"状态转换失败: {str(e)}")
            return False


# 支付状态机
class PaymentStateMachine(BaseStateMachine):
    def __init__(self):
        super().__init__(initial_state=PaymentState.UNPAID,
                         state_transitions={PaymentState.UNPAID: [PaymentState.PAID, PaymentState.CANCELLED],
                                            PaymentState.PAID: [PaymentState.REFUNDED],
                                            PaymentState.CANCELLED: [],
                                            PaymentState.REFUNDED: [],
                                            },
                         )


# 订单状态机
class OrderStateMachine(BaseStateMachine):
    def __init__(self):
        super().__init__(initial_state=OrderState.CREATED,
                         state_transitions={OrderState.CREATED: [OrderState.PAID, OrderState.CANCELLED],
                                            OrderState.PAID: [OrderState.SHIPPED, OrderState.CANCELLED],
                                            OrderState.SHIPPED: [OrderState.DELIVERED],
                                            OrderState.DELIVERED: [],
                                            OrderState.CANCELLED: [],
                                            },
                         )

    def _check_inventory(self) -> bool:
        """检查库存"""
        logger.info("检查库存...")
        # 模拟库存检查逻辑
        return True

    def _check_payment(self) -> bool:
        """检查支付状态"""
        logger.info("检查支付状态...")
        # 模拟支付检查逻辑
        return True

    def can_transition_to(self, new_state: Enum) -> bool:
        """重写状态转换规则，集成业务逻辑"""
        if new_state == OrderState.SHIPPED:
            if not self._check_inventory() or not self._check_payment():
                return False
        return super().can_transition_to(new_state)


# 订单组合类
class Order:
    """
    订单处理演示
    """
    def __init__(self, order_id: str):
        """
        初始化订单实例
        :param order_id: 订单ID
        """
        self.order_id = order_id
        self.order_fsm = OrderStateMachine()  # 订单状态机
        self.payment_fsm = PaymentStateMachine()  # 支付状态机

    def process_order(self):
        """订单处理演示"""
        self.order_fsm.transition_to(OrderState.PAID)
        self.order_fsm.transition_to(OrderState.SHIPPED)
        self.order_fsm.transition_to(OrderState.DELIVERED)


if __name__ == "__main__":
    # 示例运行
    order = Order(order_id="12345")
    order.process_order()
