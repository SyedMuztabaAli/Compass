import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QComboBox
)
from PyQt5.QtGui import QPixmap, QTransform, QPainter
from PyQt5.QtCore import Qt, QTimer
from sensor_module import SensorModule  # Import the sensor module

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class CompassApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.sensor = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_direction_from_sensor)
        self.timer.start(100)

    def initUI(self):
        self.setWindowTitle('Compass App')
        self.setGeometry(100, 100, 400, 400)
        self.setStyleSheet("background-color: black;")

        main_layout = QVBoxLayout()

        # COM port dropdown
        com_layout = QHBoxLayout()
        self.com_port_combo = QComboBox(self)
        self.com_port_combo.setStyleSheet("font-size: 30px;")
        self.com_port_combo.setFixedSize(200, 40)
        self.com_port_combo.addItem("COM Port")
        self.populate_com_ports()
        self.com_port_combo.currentIndexChanged.connect(self.connect_to_com_port)
        com_layout.addWidget(self.com_port_combo)
        com_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        main_layout.addLayout(com_layout)

        # Spacer (top)
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_top)

        # Compass display
        h_layout = QHBoxLayout()
        spacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_layout.addItem(spacer_left)

        self.compass_display = QLabel(self)
        self.compass_display.setAlignment(Qt.AlignCenter)
        h_layout.addWidget(self.compass_display)

        spacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_layout.addItem(spacer_right)
        main_layout.addLayout(h_layout)

        # Degree label
        self.degree_label = QLabel(self)
        self.degree_label.setAlignment(Qt.AlignCenter)
        self.degree_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        main_layout.addWidget(self.degree_label)

        # Spacer (bottom)
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_bottom)

        self.setLayout(main_layout)

        # Load images
        self.compass_circle = QPixmap(resource_path(os.path.join("images", "compass_circle.png")))
        self.compass_needle = QPixmap(resource_path(os.path.join("images", "compass_needle.png")))

        if self.compass_circle.isNull() or self.compass_needle.isNull():
            print("Error: Failed to load compass images.")
            sys.exit(1)

        # Resize images
        new_size1 = self.compass_circle.size()
        new_size2 = self.compass_needle.size()*0.8
        self.compass_circle = self.compass_circle.scaled(new_size1, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.compass_needle = self.compass_needle.scaled(new_size2, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.compass_display.setFixedSize(self.compass_circle.size())

        # Combine images into one base image
        self.combined_compass = QPixmap(self.compass_circle.size())
        self.combined_compass.fill(Qt.transparent)

        painter = QPainter(self.combined_compass)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, self.compass_circle)

        circle_center = self.compass_circle.rect().center()
        needle_offset = self.compass_needle.rect().center()
        needle_x = circle_center.x() - needle_offset.x()
        needle_y = circle_center.y() - needle_offset.y()
        painter.drawPixmap(needle_x, needle_y, self.compass_needle)
        painter.end()

        self.direction = 0
        self.update_compass_display()

    def populate_com_ports(self):
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.com_port_combo.addItem(port.device)

    def connect_to_com_port(self):
        selected_port = self.com_port_combo.currentText()
        if selected_port == "COM Port":
            print("Please select a valid COM port.")
            return
        try:
            if self.sensor:
                self.sensor.stop()
            self.sensor = SensorModule(port=selected_port)
            print(f"Connected to {selected_port}")
        except Exception as e:
            print(f"Failed to connect to {selected_port}: {e}")

    def update_direction_from_sensor(self):
        if self.sensor:
            new_direction = self.sensor.get_degree()
            self.direction = new_direction
            self.degree_label.setText(f"Direction: {self.direction:.2f}°")
            self.update_compass_display()

    def update_compass_display(self):
        rotated_pixmap = QPixmap(self.combined_compass.size())
        rotated_pixmap.fill(Qt.transparent)

        painter = QPainter(rotated_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        center = self.combined_compass.rect().center()

        transform = QTransform()
        transform.translate(center.x(), center.y())
        transform.rotate(-self.direction)
        transform.translate(-center.x(), -center.y())

        painter.setTransform(transform)
        painter.drawPixmap(0, 0, self.combined_compass)
        painter.end()

        self.compass_display.setPixmap(rotated_pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    compass_app = CompassApp()
    compass_app.show()
    sys.exit(app.exec_())
