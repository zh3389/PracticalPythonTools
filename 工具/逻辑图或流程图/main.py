from enum import Enum
from typing import Dict, List, Optional


# 定义订单状态
class OrderState(Enum):
    """订单状态枚举类"""
    file = "文件解析"
    extract = "PDF Word文件内容提取"
    lda = "文档纯文本主题建模识别"
    llm_video = "视频大模型"
    llm_img = "图像大模型"
    ocr = "OCR识别"
    llm_speech = "语音识别"
    form = "表格识别"
    structured = "结构化数据"
    llm_text = "文本大模型"
    result = "识别结果或分类结果"


class OrderStateMachine:
    """订单状态机
    负责管理订单在不同状态之间的转换
    """
    def __init__(self) -> None:
        # 初始化状态转换规则
        self.state_transitions: Dict[OrderState, List[OrderState]] = {
            OrderState.file: [OrderState.extract],
            OrderState.extract: [OrderState.lda, OrderState.llm_video, OrderState.llm_img, OrderState.llm_speech, OrderState.form, OrderState.structured],
            OrderState.lda: [OrderState.form, OrderState.llm_text],
            OrderState.llm_video: [OrderState.llm_img],
            OrderState.llm_img: [OrderState.llm_text, OrderState.ocr],
            OrderState.ocr: [OrderState.llm_text],
            OrderState.llm_speech: [OrderState.llm_text],
            OrderState.form: [OrderState.llm_text],
            OrderState.structured: [OrderState.llm_text],
            OrderState.llm_text: [OrderState.result],
            OrderState.result: []
        }
        self.current_state: OrderState = OrderState.extract

    def generate_graph(self):
        """生成状态机的图形表示"""
        import graphviz
        dot = graphviz.Digraph()
        for from_state, transitions in self.state_transitions.items():
            for to_state in transitions:
                dot.edge(from_state.value, to_state.value)
        # 显示图像
        dot.render(filename='vis', format='png', cleanup=True)  # 保存并渲染为 PNG 图片
        # dot.view()  # 调用默认查看器打开图像
        return dot


order = OrderStateMachine()
order.generate_graph()
