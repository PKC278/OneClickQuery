import sys
import time
import os
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPen, QPainter, QColor, QGuiApplication
from PyQt5.QtWidgets import QApplication, QWidget


class Screenshot(QWidget):
    # 初始化变量
    fullScreenImage = None
    captureImage = None
    isMousePressLeft = None
    beginPosition = None
    endPosition = None

    # 创建 QPainter 对象
    painter = QPainter()

    def __init__(self):
        super().__init__()
        self.initWindow()  # 初始化窗口
        self.captureFullScreen()  # 捕获全屏

    def initWindow(self):
        self.setCursor(Qt.CrossCursor)  # 设置光标
        # 产生无边框窗口，用户不能通过窗口系统移动或调整无边界窗口的大小
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowState(Qt.WindowFullScreen)  # 窗口全屏无边框
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

    def captureFullScreen(self):
        # 捕获当前屏幕，返回像素图
        self.fullScreenImage = QGuiApplication.primaryScreen().grabWindow(
            QApplication.desktop().winId()
        )

    def mousePressEvent(self, event):
        # 如果鼠标事件为左键，则记录起始鼠标光标相对于窗口的位置
        if event.button() == Qt.LeftButton:
            self.beginPosition = event.pos()
            self.isMousePressLeft = True

    def mouseMoveEvent(self, event):
        if self.isMousePressLeft is True:
            self.endPosition = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        self.endPosition = event.pos()
        self.isMousePressLeft = False
        self.saveImage()
        self.close()

    def paintBackgroundImage(self):
        # 填充颜色，黑色半透明
        fillColor = QColor(0, 0, 0, 0)
        # 加载显示捕获的图片到窗口
        self.painter.drawPixmap(0, 0, self.fullScreenImage)
        # 填充颜色到给定的矩形
        self.painter.fillRect(self.fullScreenImage.rect(), fillColor)

    def getRectangle(self, beginPoint, endPoint):
        # 计算矩形宽和高
        rectWidth = int(abs(beginPoint.x() - endPoint.x()))
        rectHeight = int(abs(beginPoint.y() - endPoint.y()))
        # 计算矩形左上角 x 和 y
        rectTopleftX = beginPoint.x() if beginPoint.x() < endPoint.x() else endPoint.x()
        rectTopleftY = beginPoint.y() if beginPoint.y() < endPoint.y() else endPoint.y()
        # 构造一个以（x，y）为左上角，给定宽度和高度的矩形
        pickRect = QRect(rectTopleftX, rectTopleftY, rectWidth, rectHeight)
        # 调试日志
        # logging.info('开始坐标：%s,%s', beginPoint.x(),beginPoint.y())
        # logging.info('结束坐标：%s,%s', endPoint.x(), endPoint.y())
        return pickRect

    def paintSelectBox(self):
        # 画笔颜色，蓝色
        penColor = QColor(211, 211, 211)  # 画笔颜色
        # 设置画笔属性，蓝色、2px大小、实线
        self.painter.setPen(QPen(penColor, 2, Qt.SolidLine))
        if self.isMousePressLeft is True:
            pickRect = self.getRectangle(
                self.beginPosition, self.endPosition
            )  # 获得要截图的矩形框
            self.captureImage = self.fullScreenImage.copy(pickRect)  # 捕获截图矩形框内的图片
            self.painter.drawPixmap(pickRect.topLeft(), self.captureImage)  # 填充截图的图片
            self.painter.drawRect(pickRect)  # 绘制矩形边框

    def paintEvent(self, event):
        self.painter.begin(self)  # 开始绘制
        self.paintBackgroundImage()  # 绘制背景
        self.paintSelectBox()  # 绘制选框
        self.painter.end()  # 结束绘制

    def saveImage(self):
        fileName = os.path.join(
            os.environ["TEMP"], time.strftime("Screenshot") + ".png"
        )
        if self.captureImage is not None:
            self.close()
            self.captureImage.save(fileName)
        else:
            self.close()

    def keyPressEvent(self, event):
        # 如果按下 ESC 键，则退出截图
        if event.key() == Qt.Key_Escape:
            self.close()

    def main():
        app = QApplication(sys.argv)
        windows = Screenshot()
        windows.show()
        app.exec_()


if __name__ == "__main__":
    # 调试日志
    # logger = logging.getLogger()
    # logger.setLevel(logging.DEBUG)
    # sh = logging.StreamHandler()
    # formatter = logging.Formatter('%(message)s')
    # sh.setFormatter(formatter)
    # logger.addHandler(sh)

    app = QApplication(sys.argv)  # 创建 QApplication 对象
    windows = Screenshot()  # 创建 Screenshot 对象
    windows.show()  # 显示窗口
    sys.exit(app.exec_())  # 进入主事件循环并等待直到 exit() 被调用
