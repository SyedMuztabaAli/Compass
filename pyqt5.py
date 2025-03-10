import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QComboBox
)
from PyQt5.QtGui import QPixmap, QTransform, QPainter
from PyQt5.QtCore import Qt, QTimer
from sensor_module import SensorModule, get_sensor_degree  # Import the sensor module

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class CompassApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Initialize the sensor module
        self.sensor = None

        # Set up a timer to update the compass direction automatically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_direction_from_sensor)
        self.timer.start(100)  # Update every 100 milliseconds

    def initUI(self):
        self.setWindowTitle('Compass App')
        self.setGeometry(100, 100, 400, 400)

        self.setStyleSheet("background-color: lightblue;")

        main_layout = QVBoxLayout()

        # Add a horizontal layout for the COM port selection
        com_layout = QHBoxLayout()

        # Dropdown for COM ports
        self.com_port_combo = QComboBox(self)
        self.com_port_combo.setStyleSheet("font-size: 30px;")  # Increase font size
        self.com_port_combo.setFixedSize(200, 40)  # Set a fixed size for the dropdown
        self.com_port_combo.addItem("COM Port")
        self.populate_com_ports()  # Populate available COM ports
        self.com_port_combo.currentIndexChanged.connect(self.connect_to_com_port)  # Auto-connect on selection
        com_layout.addWidget(self.com_port_combo)

        # Add the COM port dropdown to the top-left corner (0, 0)
        com_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        main_layout.addLayout(com_layout)

        # Add a spacer to push the compass display to the center
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_top)

        # Compass display layout
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
        self.degree_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(self.degree_label)

        # Add a spacer to push the compass display to the center
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_bottom)

        self.setLayout(main_layout)

        # Load compass images
        self.compass_circle = QPixmap(resource_path(os.path.join("images", "compass_circle.jpeg")))
        self.compass_needle = QPixmap(resource_path(os.path.join("images", "compass_needle.png")))

        if self.compass_circle.isNull() or self.compass_needle.isNull():
            print("Error: Failed to load compass images.")
            sys.exit(1)

        # Resize the compass images
        new_size1 = self.compass_circle.size() * 0.5
        new_size2 = self.compass_needle.size() * 1.1
        self.compass_circle = self.compass_circle.scaled(new_size1, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.compass_needle = self.compass_needle.scaled(new_size2, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.compass_display.setFixedSize(self.compass_circle.size())

        self.direction = 0  # Initial direction

        # Display the initial compass
        self.update_compass_display()

    def populate_com_ports(self):
        """Populate the COM port dropdown with available COM ports."""
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.com_port_combo.addItem(port.device)

    def connect_to_com_port(self):
        """Connect to the selected COM port."""
        selected_port = self.com_port_combo.currentText()
        if selected_port == "Select COM Port":
            print("Please select a valid COM port.")
            return

        try:
            # Initialize the sensor module with the selected COM port
            self.sensor = SensorModule(port=selected_port)
            print(f"Connected to {selected_port}")
        except Exception as e:
            print(f"Failed to connect to {selected_port}: {e}")

    def update_direction_from_sensor(self):
        """Update the compass direction based on sensor data."""
        if self.sensor:
            new_direction = get_sensor_degree()
            self.direction = new_direction
            self.degree_label.setText(f"Direction: {self.direction:.2f}°")
            self.update_compass_display()

    def update_compass_display(self):
        """Update the compass display with the current direction."""
        pixmap = QPixmap(self.compass_circle.size())
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.drawPixmap(0, 0, self.compass_circle)

        circle_center = self.compass_circle.rect().center()
        needle_center = self.compass_needle.rect().center()

        transform = QTransform()
        transform.translate(circle_center.x(), circle_center.y() - 2)
        transform.rotate(-self.direction)
        transform.translate(-needle_center.x(), -needle_center.y())

        painter.setTransform(transform)
        painter.drawPixmap(0, 0, self.compass_needle)
        painter.end()

        self.compass_display.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    compass_app = CompassApp()
    compass_app.show()
    sys.exit(app.exec_())