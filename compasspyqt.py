import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QTransform, QPainter
from PyQt5.QtCore import Qt, QTimer

class CompassApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Compass App')
        self.setGeometry(100, 100, 400, 400)

        # Set light blue background for the entire window
        self.setStyleSheet("background-color: lightblue;")

        # Main layout
        main_layout = QVBoxLayout()

        # Add a spacer above the compass image to center it vertically
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_top)

        # Horizontal layout to center the compass image horizontally
        h_layout = QHBoxLayout()

        # Add a spacer to the left of the compass image
        spacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_layout.addItem(spacer_left)

        # Compass display
        self.compass_display = QLabel(self)
        self.compass_display.setAlignment(Qt.AlignCenter)
        h_layout.addWidget(self.compass_display)

        # Add a spacer to the right of the compass image
        spacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_layout.addItem(spacer_right)

        # Add the horizontal layout to the main layout
        main_layout.addLayout(h_layout)

        # Label to display the current degree value
        self.degree_label = QLabel(self)
        self.degree_label.setAlignment(Qt.AlignCenter)
        self.degree_label.setStyleSheet("font-size: 20px; font-weight: bold;")  # Customize the font
        main_layout.addWidget(self.degree_label)

        # Add a spacer below the degree label to ensure it stays at the bottom
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_bottom)

        self.setLayout(main_layout)

        # Load the compass image (ensure it has a transparent background)
        self.compass_image = QPixmap("compass.png")  # Single image of the compass with transparency
        if self.compass_image.isNull():
            print("Error: Failed to load compass image.")
            sys.exit(1)

        # Resize the QLabel to match the size of the compass image
        self.compass_display.setFixedSize(self.compass_image.size())

        self.direction = 0  # Initial direction

        # Display the initial compass
        self.update_compass_display()

        # Set up a timer to update the compass direction automatically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_direction_automatically)
        self.timer.start(100)  # Update every 100 milliseconds (0.1 seconds)

    def update_direction_automatically(self):
        # Simulate a new direction value (e.g., from a sensor or data source)
        new_direction = random.uniform(0, 360)  # Random value between 0 and 360
        self.direction = new_direction

        # Update the degree label with the current direction
        self.degree_label.setText(f"Direction: {self.direction:.2f}°")

        # Update the compass display
        self.update_compass_display()

    def update_compass_display(self):
        # Create a pixmap to hold the rotated compass image
        pixmap = QPixmap(self.compass_image.size())
        pixmap.fill(Qt.transparent)  # Make the background transparent

        # Create a QPainter to draw on the pixmap
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)  # Enable antialiasing for smooth rotation

        # Calculate the center of the display area
        display_center = self.compass_image.rect().center()

        # Rotate the compass image around its center
        transform = QTransform()
        transform.translate(display_center.x(), display_center.y())  # Move to the center of the display
        transform.rotate(-self.direction)  # Rotate by the specified degree (negative for clockwise rotation)
        transform.translate(-self.compass_image.width() / 2, -self.compass_image.height() / 2)  # Move back to the image's top-left corner

        # Draw the rotated compass image
        painter.setTransform(transform)
        painter.drawPixmap(0, 0, self.compass_image)
        painter.end()

        # Display the final pixmap
        self.compass_display.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    compass_app = CompassApp()
    compass_app.show()
    sys.exit(app.exec_())