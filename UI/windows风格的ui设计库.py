import tkinter as tk
import pywinstyles


class PyWindowStylesDemo:
    """
    使用 py-window-styles 创建 Windows 11 风格的 Python UI 示例。
    """
    def __init__(self, theme="dark", custom_theme=None):
        """
        初始化窗口及主题设置。
        
        :param theme: 预构建的主题名称，如 "dark", "light", "default"。
        :param custom_theme: 自定义主题字典，包括颜色、字体和图标。
        """
        self.tk = tk
        self.pywinstyles = pywinstyles
        self.root = tk.Tk()
        
        if custom_theme:
            self.apply_custom_theme(custom_theme)
        else:
            self.apply_built_in_theme(theme)

    def apply_built_in_theme(self, theme):
        """
        应用预构建主题。

        :param theme: 预构建的主题名称。
        """
        self.pywinstyles.apply_style(self.root, theme)

    def apply_custom_theme(self, custom_theme):
        """
        应用自定义主题。

        :param custom_theme: 包含主题设置的字典。
        """
        self.pywinstyles.apply_theme(self.root, custom_theme)

    def add_label(self, text):
        """
        向窗口添加标签。

        :param text: 标签文本内容。
        """
        label = self.tk.Label(self.root, text=text)
        label.pack()

    def run(self):
        """
        运行窗口。
        """
        self.root.mainloop()

# 示例代码
if __name__ == "__main__":
    # 使用预构建主题
    demo = PyWindowStylesDemo(theme="dark")
    demo.add_label("Hello, World!")
    demo.run()

    # 使用自定义主题
    custom_theme = {
        "background_color": "#222",
        "foreground_color": "#fff",
        "font": ("Arial", 12),
        "icon": "path/to/icon.ico"
    }
    custom_demo = PyWindowStylesDemo(custom_theme=custom_theme)
    custom_demo.add_label("Welcome to Custom Theme!")
    custom_demo.run()
