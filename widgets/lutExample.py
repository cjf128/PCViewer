import sys
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
    QGraphicsEllipseItem, QLabel, QVBoxLayout, QWidget
)
from PySide6.QtGui import QPainterPath, QPixmap, QImage
from PySide6.QtCore import Qt

# ---------------- Transfer Function Logic ----------------
class TransferFunction:
    def __init__(self):
        self.points = [(0, 0), (255, 255)]

    def set_points(self, pts):
        self.points = sorted(pts, key=lambda x: x[0])

    def build_lut(self):
        lut = np.zeros(256, dtype=np.uint8)
        pts = self.points

        for i in range(len(pts) - 1):
            x0, y0 = pts[i]
            x1, y1 = pts[i + 1]

            for x in range(int(x0), int(x1) + 1):
                t = (x - x0) / (x1 - x0 + 1e-5)
                lut[x] = int(y0 + t * (y1 - y0))

        return lut

# ---------------- Control Point ----------------
class ControlPoint(QGraphicsEllipseItem):
    def __init__(self, x, y, parent):
        super().__init__(-5, -5, 10, 10)
        self.setPos(x, y)
        self.setBrush(Qt.GlobalColor.red)
        self.setFlag(self.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(self.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.parent = parent

    def itemChange(self, change, value):
        if change == self.GraphicsItemChange.ItemPositionChange:
            x = min(max(value.x(), 0), 255)
            y = min(max(value.y(), 0), 255)
            self.parent.update_curve()
            return super().itemChange(change, value)
        return super().itemChange(change, value)

# ---------------- Curve Editor ----------------
class TransferFunctionWidget(QGraphicsView):
    def __init__(self, callback=None):
        super().__init__()
        self.scene = QGraphicsScene(0, 0, 256, 256)
        self.setScene(self.scene)
        self.points = []
        self.callback = callback

        self.curve_item = self.scene.addPath(QPainterPath())

        self.add_point(0, 255)
        self.add_point(255, 0)

    def add_point(self, x, y):
        p = ControlPoint(x, y, self)
        self.scene.addItem(p)
        self.points.append(p)
        self.update_curve()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = self.mapToScene(event.pos())
            self.add_point(pos.x(), pos.y())
        super().mousePressEvent(event)

    def update_curve(self):
        pts = sorted(self.points, key=lambda p: p.pos().x())

        path = QPainterPath()
        if pts:
            path.moveTo(pts[0].pos())
            for p in pts[1:]:
                path.lineTo(p.pos())

        self.curve_item.setPath(path)

        if self.callback:
            coords = [(p.pos().x(), 255 - p.pos().y()) for p in pts]
            self.callback(coords)

# ---------------- Image Display ----------------
class ImageViewer(QLabel):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.setFixedSize(256, 256)
        self.update_image(np.arange(256, dtype=np.uint8))

    def update_image(self, lut):
        mapped = lut[self.image]
        h, w = mapped.shape
        qimg = QImage(mapped.data, w, h, w, QImage.Format.Format_Grayscale8)
        self.setPixmap(QPixmap.fromImage(qimg))

# ---------------- Main Window ----------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # fake image
        self.image = np.tile(np.arange(256, dtype=np.uint8), (256, 1))

        self.tf = TransferFunction()

        self.viewer = ImageViewer(self.image)
        self.editor = TransferFunctionWidget(self.on_tf_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.viewer)
        layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_tf_changed(self, points):
        self.tf.set_points(points)
        lut = self.tf.build_lut()
        self.viewer.update_image(lut)

# ---------------- Run ----------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
