
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QTransform, QPainter
from PyQt5.QtCore import Qt, QTimer
from sensor_module import get_sensor_degree  # Replace with actual sensor module


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QTransform, QPainter
from PyQt5.QtCore import Qt, QTimer
from sensor_module import get_sensor_degree  # Replace with actual sensor module


class CompassApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Set up a timer to update the compass direction automatically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_direction_from_sensor)
        self.timer.start(100)  # Update every 100 milliseconds

    def initUI(self):
        self.setWindowTitle('Compass App')
        self.setGeometry(100, 100, 400, 400)

        self.setStyleSheet("background-color: lightblue;")

        main_layout = QVBoxLayout()

        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_top)

        h_layout = QHBoxLayout()

        spacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_layout.addItem(spacer_left)

        self.compass_display = QLabel(self)
        self.compass_display.setAlignment(Qt.AlignCenter)
        h_layout.addWidget(self.compass_display)

        spacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_layout.addItem(spacer_right)

        main_layout.addLayout(h_layout)


        self.degree_label = QLabel(self)
        self.degree_label.setAlignment(Qt.AlignCenter)
        self.degree_label.setStyleSheet("font-size: 20px; font-weight: bold;")  # Customize the font
        main_layout.addWidget(self.degree_label)


        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_bottom)

        self.setLayout(main_layout)

        self.compass_circle = QPixmap("images/compass_circle.jpeg")
        self.compass_needle = QPixmap("images/compass_needle.png")

        if self.compass_circle.isNull() or self.compass_needle.isNull():
            print("Error: Failed to load compass images.")
            sys.exit(1)

        # Resize the compass circle to make it smaller
        new_size1 = self.compass_circle.size() * 0.5
        new_size2 = self.compass_needle.size() * 1.1# Reduce size to 50% of the original
        self.compass_circle = self.compass_circle.scaled(new_size1, Qt.KeepAspectRatio, Qt.SmoothTransformation)


        self.compass_needle = self.compass_needle.scaled(new_size2, Qt.KeepAspectRatio, Qt.SmoothTransformation)


        self.compass_display.setFixedSize(self.compass_circle.size())

        self.direction = 0  # Initial direction

        # Display the initial compass
        self.update_compass_display()

    def update_direction_from_sensor(self):

        new_direction = get_sensor_degree()

        # Update the direction
        self.direction = new_direction

        # Update the degree label with the current direction
        self.degree_label.setText(f"Direction: {self.direction:.2f}°")

        # Update the compass display
        self.update_compass_display()

    def update_compass_display(self):

        # Create a pixmap to hold the combined compass image
        pixmap = QPixmap(self.compass_circle.size())
        # Make the background transparent
        pixmap.fill(Qt.transparent)

        # Create a QPainter to draw on the pixmap
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.drawPixmap(0, 0, self.compass_circle)

        #display_center = self.compass_circle.rect().center()
        circle_center = self.compass_circle.rect().center()
        needle_center = self.compass_needle.rect().center()

        transform = QTransform()
        transform.translate(circle_center.x(), circle_center.y()-2)
        #transform.translate(display_center.x(), display_center.y())
        transform.rotate(-self.direction)
        transform.translate(-needle_center.x(), -needle_center.y())
        #transform.translate(-self.compass_needle.width() / 2, -self.compass_needle.height() / 2)

        painter.setTransform(transform)
        painter.drawPixmap(0, 0, self.compass_needle)
        painter.end()

        self.compass_display.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    compass_app = CompassApp()
    compass_app.show()
    sys.exit(app.exec_())