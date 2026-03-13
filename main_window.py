from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QFrame
from PyQt6.QtCore import Qt


class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Circle Drawer")
        MainWindow.resize(800, 600)

        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.layout = QVBoxLayout(self.centralwidget)

        self.drawButton = QPushButton("Нарисовать окружность")
        self.layout.addWidget(self.drawButton)

        # Область рисования
        self.drawingArea = QFrame()
        self.drawingArea.setFrameShape(QFrame.Shape.StyledPanel)
        self.drawingArea.setFrameShadow(QFrame.Shadow.Raised)
        self.layout.addWidget(self.drawingArea)


class DrawingArea(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.circles = []

    def add_circle(self, x, y, diameter, color):
        self.circles.append((x, y, diameter, color))
        self.update()

    def paintEvent(self, event):
        from PyQt6.QtGui import QPainter

        painter = QPainter(self)

        for x, y, diameter, color in self.circles:
            painter.setPen(color)
            painter.setBrush(color)
            painter.drawEllipse(x, y, diameter, diameter)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.drawing_area = DrawingArea(self.drawingArea)
        self.drawing_area.setGeometry(self.drawingArea.geometry())
        self.drawing_area.setFrameShape(self.drawingArea.frameShape())
        self.drawing_area.setFrameShadow(self.drawingArea.frameShadow())
        self.layout.replaceWidget(self.drawingArea, self.drawing_area)

        self.drawingArea.hide()
        self.drawing_area.show()

        self.drawButton.clicked.connect(self.add_circle)

    def add_circle(self):
        import random
        from PyQt6.QtGui import QColor

        # Случайный диаметр
        diameter = random.randint(20, 100)

        # Случайный цвет
        color = QColor(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

        # Случайная позиция
        x = random.randint(0, self.drawing_area.width() - diameter)
        y = random.randint(0, self.drawing_area.height() - diameter)

        self.drawing_area.add_circle(x, y, diameter, color)