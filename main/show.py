import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt


class TooltipListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 获取屏幕尺寸并设置窗口位置和大小
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.setGeometry(screen.width() - 450, (screen.height() - 600) // 2, 400, 600)

        self.installEventFilter(self)  # 安装事件过滤器

        # 添加关闭按钮
        self.close_button = QtWidgets.QPushButton("关闭", self)
        self.close_button.clicked.connect(self.close)  # 修改为退出程序
        self.close_button.move(335, -5)  # 将按钮移动到右上角
        self.close_button.setFixedHeight(50)  # 设置按钮的高度
        self.close_button.setFixedWidth(70)  # 设置按钮的宽度
        self.close_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")

    def add_item_with_tooltip(self, text):
        item = QtWidgets.QListWidgetItem()
        self.addItem(item)
        item.setSizeHint(QtCore.QSize(0, 65))  # 设置项目的大小
        lines = text.split("\n")  # 将文本分割为多行
        label_text = "\n".join(lines[:2])  # 只取前两行
        label = QtWidgets.QLabel(label_text)
        self.setItemWidget(item, label)  # 为项目设置自定义的小部件
        item.setToolTip(text)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.WindowDeactivate:
            self.close()  # 修改为退出程序
        return super().eventFilter(obj, event)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def exit_app(self):
        sys.exit()  # 添加一个方法来退出程序

    def keyPressEvent(self, event):
        # 如果按下 ESC 键，则退出截图
        if event.key() == Qt.Key_Escape:
            self.close()

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
    data = ["这是一个很\n长的文本，需要用工具提示来完整显示。", "另一个文本示例。"]

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
