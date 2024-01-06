import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor


class TooltipListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 获取屏幕尺寸并设置窗口位置和大小
        global screen
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        width_ratio = 1 / 7
        height_ratio = 1 / 4
        width = screen.width() * width_ratio
        global height
        height = screen.height() * height_ratio
        # 将窗口向左移动10%的屏幕宽度
        self.setGeometry(
            screen.width() - width - screen.width() * 0.01,
            (screen.height() - height) // 2,
            width,
            height,
        )
        self.installEventFilter(self)  # 安装事件过滤器

    def add_item_with_tooltip(self, text):
        item = QtWidgets.QListWidgetItem()
        self.addItem(item)
        # 设置项目的底色
        if self.count() % 2 == 0:
            item.setBackground(QBrush(QColor(240, 240, 240)))  # 浅灰色
        else:
            item.setBackground(QBrush(QColor(255, 255, 255)))  # 白色

        item.setSizeHint(QtCore.QSize(0, height / 5))  # 设置项目的大小
        lines = text.split("\n")  # 将文本分割为多行
        label_text = "\n".join(lines[:2])  # 只取前两行
        label = QtWidgets.QLabel(label_text)
        self.setItemWidget(item, label)  # 为项目设置自定义的小部件
        item.setToolTip(text)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.WindowDeactivate:
            self.close()  # 修改为退出程序
        return super().eventFilter(obj, event)

    def exit_app(self):
        sys.exit()  # 添加一个方法来退出程序

    def mousePressEvent(self, event):
        # 无论鼠标点击哪里，都直接关闭窗口
        self.close()

    def keyPressEvent(self, event):
        # 如果按下 ESC 键，则退出
        if event.key() == Qt.Key_Escape:
            self.close()

    def wheelEvent(self, event):
        pass

    def main(final_data):
        # 创建应用和窗口
        app = QtWidgets.QApplication(sys.argv)
        window = TooltipListWidget()

        # 添加数据到窗口
        for item in final_data:
            window.add_item_with_tooltip(item)
        # 显示窗口
        window.show()
        window.setFocus()
        window.raise_()
        window.activateWindow()
        # 运行应用
        app.exec_()


if __name__ == "__main__":
    # 创建应用和窗口
    app = QtWidgets.QApplication(sys.argv)
    window = TooltipListWidget()
    # 示例数据
    data = [
        "测试1\n测试2",
        "测试1\n测试2",
        "测试1\n测试2",
        "测试1\n测试2",
        "测试1\n测试2",
    ]
    # 添加数据到窗口
    for item in data:
        window.add_item_with_tooltip(item)
    # 显示窗口
    window.show()
    window.setFocus()
    window.raise_()
    window.activateWindow()
    # 运行应用
    sys.exit(app.exec_())
