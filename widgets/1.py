import sys
from app.mode import VIEWERMode, VIEWMode

import numpy as np
from PySide6.QtCore import QPoint, QRect, Qt, Signal
from PySide6.QtGui import QColor, QPen, QTransform, QFont
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsEllipseItem,
    QGraphicsPixmapItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
)


class ImageViewer(QGraphicsView):
    Sam_Signal = Signal(np.ndarray)
    Mode_Signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.point_list = []
        self.input_box = []
        self.parent = parent

        self.mode = VIEWERMode.NORMAL
        self.view_mode = VIEWMode.CROSS

        self.show_crosshair = False
        self.cross_show = False

        self.spacing = (1, 1, 1)

        self.pixmap_item = QGraphicsPixmapItem()
        self.rect_item = QGraphicsRectItem()
        self.ellipse_item = QGraphicsEllipseItem()

        self.start_point = QPoint()
        self.end_point = QPoint()
        self.last_mouse_position = QPoint()

        self.radius = 0
        self.ellipse_pos = [0, 0]
        self.position = [0, 0, 0]   
        self.config()

    def config(self):
        self.setMouseTracking(True)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def load_image(self, pixmap, radius):
        global scale_x, scale_y
        self.scene.clear()
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.radius = 2*radius
        self.ellipse_item = QGraphicsEllipseItem(QRect(self.ellipse_pos[0], self.ellipse_pos[1], self.radius+1, self.radius+1))
        if self.mode in (VIEWERMode.PAINT, VIEWERMode.ERASER):
            self.ellipse_item.setVisible(True)
        else:
            self.ellipse_item.setVisible(False)

        pen = QPen(Qt.blue)
        pen.setWidth(0.5)     
        self.ellipse_item.setPen(pen)

        transform = QTransform()
        transform.rotate(180)

        match self.view_mode:
            case VIEWMode.CROSS:
                scale_x, scale_y = -self.spacing[0], -self.spacing[1]
            case VIEWMode.SAGITTAL:
                scale_x, scale_y = -self.spacing[1], self.spacing[2]
            case VIEWMode.CORONAL:
                scale_x, scale_y = -self.spacing[0], self.spacing[2]
            case _:
                raise ValueError(f"Unsupported view mode: {self.view_mode}")

        transform.scale(scale_x, scale_y)
        
        self.pixmap_item.setTransform(transform)
        self.ellipse_item.setTransform(transform)

        self.scene.addItem(self.pixmap_item)
        self.scene.addItem(self.ellipse_item)

        self.rect_item = None
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.pixmap_item != None:
            if event.button() == Qt.LeftButton:
                self.last_mouse_position = event.pos()
                self.scene_pos = self.mapToScene(event.pos())
                self.point = self.pixmap_item.mapFromScene(self.scene_pos).toPoint()
                self.point_list = [self.point.x(), self.point.y()]
                self.ellipse_pos = [self.point.x() - self.radius/2, self.point.y()- self.radius/2]

                if self.mode == VIEWERMode.AIM:
                    self.position[0] = event.pos().x()
                    self.position[1] = event.pos().y()
                    self.update()
    
                if self.mode == VIEWERMode.SAM:
                    self.setCursor(Qt.CrossCursor)
                    self.start_point = self.pixmap_item.mapFromScene(self.scene_pos).toPoint()
                    self.end_point = self.start_point
                    self.rect_item = QGraphicsRectItem(QRect(self.start_point, self.end_point))
                    scale = self.transform().m11()
                    if scale < 1:
                        pen_size = 2
                    elif scale < 2:
                        pen_size = 1
                    else:
                        pen_size = 0.5
                    self.rect_item.setPen(QPen(QColor('blue'), pen_size))
                    self.rect_item.setTransform(self.pixmap_item.transform())
                    self.scene.addItem(self.rect_item)

                if self.mode == VIEWERMode.PAINT:
                    self.draw_state = 1

                if self.mode == VIEWERMode.ERASER:
                    self.draw_state = 0

            if event.button() == Qt.MiddleButton:
                self.mode = VIEWERMode.MOVE

            if event.button() == Qt.RightButton:
                self.mode = VIEWERMode.ZOOM

        event.ignore()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.pixmap_item != None:
            self.delta = event.pos() - self.last_mouse_position
            self.last_mouse_position = event.pos()
            self.scene_pos = self.mapToScene(event.pos())
            self.point = self.pixmap_item.mapFromScene(self.scene_pos).toPoint()
            self.point_list = [self.point.x(), self.point.y()]
            self.ellipse_pos = [self.point.x() - self.radius/2, self.point.y()- self.radius/2]

            if self.mode == VIEWERMode.AIM and event.buttons() & Qt.LeftButton:
                self.position[0] = event.pos().x()
                self.position[1] = event.pos().y()
                self.update()

            if self.mode == VIEWERMode.MOVE and (event.buttons() & Qt.LeftButton or event.buttons() & Qt.MiddleButton):
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - self.delta.x())
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() - self.delta.y())

            if self.mode == VIEWERMode.SAM and event.buttons() & Qt.LeftButton:
                self.end_point = self.pixmap_item.mapFromScene(self.scene_pos).toPoint()
                if self.rect_item:
                    self.rect_item.setRect(QRect(self.start_point, self.end_point).normalized())
                    self.input_box = np.array([self.start_point.x(), self.start_point.y(),
                                            self.end_point.x(), self.end_point.y()])
            
            if self.mode == VIEWERMode.PAINT or self.mode == VIEWERMode.ERASER:
                if self.ellipse_item:
                    self.ellipse_item.setVisible(True)
                    self.ellipse_item.setRect(QRect(self.ellipse_pos[0], self.ellipse_pos[1], self.radius+1, self.radius+1))
                
            if self.mode == VIEWERMode.ZOOM and event.buttons() & Qt.RightButton:
                scale_factor = 1.0 + (self.delta.y() / 100.0)
                scale_factor = max(0.2, min(2, scale_factor))

                self.scale(scale_factor, scale_factor)

        event.ignore()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.pixmap_item != None:
            if event.button() == Qt.LeftButton:
                if self.mode == VIEWERMode.SAM and np.any(self.input_box):
                    self.setCursor(Qt.ArrowCursor)
                    self.Sam_Signal.emit(self.input_box)
                    self.mode = VIEWERMode.NORMAL
            else:
                self.Mode_Signal.emit() # 取消操作，检查当前状态，为的是跟无按键即可进行的鼠标事件分开来，例如缩放和调窗

        event.ignore()
    
    def wheelEvent(self, event):
        angle = event.angleDelta()
        if event.modifiers() == Qt.ControlModifier:
            if self.mode == VIEWERMode.PAINT or self.mode == VIEWERMode.ERASER:
                if angle.y() > 0 and self.radius < 15:
                    self.radius += 2
                elif angle.y() < 0 and self.radius > 2:
                    self.radius -= 2

        event.ignore()
    
    def enterEvent(self, event):
        # 鼠标进入控件时隐藏指针
        if self.mode == VIEWERMode.PAINT or self.mode == VIEWERMode.ERASER:
            self.setCursor(Qt.BlankCursor)
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        # 鼠标离开控件时恢复默认指针
        self.unsetCursor()
        super().leaveEvent(event)
        
    def drawForeground(self, painter, rect):
        super().drawForeground(painter, rect)
        if not self.show_crosshair:
            return

        # 1. 保存当前变换
        painter.save()

        # 2. 重置变换（不受 scale/translate 影响）
        painter.resetTransform()

        # 3. 获取视口尺寸
        center_x = self.position[0]
        center_y = self.position[1]

        if self.view_mode == VIEWMode.CROSS:
            axe = ["R", "L", "A", "P"]
            color = ["red", "blue"]
        elif self.view_mode == VIEWMode.SAGITTAL:
            axe = ["A", "P", "S", "I"]
            color = ["green", "red"]
        elif self.view_mode == VIEWMode.CORONAL:
            axe = ["R", "L", "S", "I"]
            color = ["green", "blue"]

        # 4. 绘制十字线（设备坐标，不受缩放影响）
        if self.cross_show:
            penx = QPen(QColor(color[0]), 1, Qt.DashLine)
            peny = QPen(QColor(color[1]), 1, Qt.DashLine)
            painter.setPen(penx)
            painter.drawLine(center_x, 20, center_x, self.viewport().height() - 20)
            painter.setPen(peny)
            painter.drawLine(20, center_y, self.viewport().width() - 20, center_y)


        # 5. 绘制方向标签（设备坐标）
        font = QFont("Arial", 10)
        painter.setFont(font)
        painter.setPen(Qt.yellow)
        margin = 10
        painter.drawText(margin, self.viewport().height() // 2 - 5, axe[0])
        painter.drawText(self.viewport().width() - margin - 10, self.viewport().height() // 2 - 5, axe[1])
        painter.drawText(self.viewport().width() // 2 - 5, margin + 10, axe[2])
        painter.drawText(self.viewport().width() // 2 - 5, self.viewport().height() - margin, axe[3])

        # 6. 恢复原始坐标系统
        painter.restore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec_())
