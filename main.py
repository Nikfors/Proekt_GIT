import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QFrame
from PyQt6.QtGui import QPainter, QColor
from PyQt6.uic import loadUi


class DrawingArea(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.circles = []

    def add_circle(self, x, y, diameter):
        self.circles.append((x, y, diameter))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(255, 255, 0))
        painter.setBrush(QColor(255, 255, 0))

        for x, y, diameter in self.circles:
            painter.drawEllipse(x, y, diameter, diameter)


class CircleDrawer(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI.ui', self)

        self.original_drawing_area = self.drawingArea

        self.drawing_area = DrawingArea(self.original_drawing_area)

        self.drawing_area.setGeometry(self.original_drawing_area.geometry())
        self.drawing_area.setFrameShape(self.original_drawing_area.frameShape())
        self.drawing_area.setFrameShadow(self.original_drawing_area.frameShadow())

        layout = self.centralWidget().layout()
        layout.replaceWidget(self.original_drawing_area, self.drawing_area)

        self.original_drawing_area.hide()
        self.drawing_area.show()

        self.drawButton.clicked.connect(self.add_circle)

    def add_circle(self):
        diameter = random.randint(20, 100)
        x = random.randint(0, self.drawing_area.width() - diameter)
        y = random.randint(0, self.drawing_area.height() - diameter)
        self.drawing_area.add_circle(x, y, diameter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CircleDrawer()
    window.show()
    sys.exit(app.exec())