import threading
import serial
import math
import time

class SensorModule:
    def __init__(self, port=None, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.degree = 0
        self.lock = threading.Lock()
        self.running = True
        self.serial_connection = None
        self.thread = threading.Thread(target=self.read_serial_data, daemon=True)
        self.connect_serial()
        self.thread.start()

    def connect_serial(self):
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=0.2)
            print(f"Connected to {self.port} at {self.baudrate} baud.")
        except serial.SerialException as e:
            print(f"Failed to connect to {self.port}: {e}")
            self.running = False

    def read_serial_data(self):
        while self.running:
            if self.serial_connection and self.serial_connection.is_open:
                try:
                    # Read a line from the serial port
                    line = self.serial_connection.readline().decode('utf-8').strip()
                    if "X:" not in line or "," not in line:
                        continue
                    elif line:
                        try:
                            x = float(line.split("X:")[1].split(",")[0].strip())
                            y = float(line.split("Y:")[1].split(",")[0].strip())
                            # Calculate the heading (degree) using atan2
                            heading = math.atan2(y, x) * (180 / math.pi)
                            # Normalize the heading to 0-360 degrees
                            if heading < 0:
                                heading += 360
                            with self.lock:
                                self.degree = heading
                        except ValueError as e:
                            print(f"Error parsing X, Y, Z values: {e}")
                except (UnicodeDecodeError, serial.SerialException) as e:
                    print(f"Error reading serial data: {e}")
            else:
                print("Serial connection is not open.")
                time.sleep(1)

    def get_degree(self):
        with self.lock:
            return self.degree

    def stop(self):
        self.running = False
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
        self.thread.join()


# Create a global instance of the SensorModule
# sensor = SensorModule()

# def get_sensor_degree():
#     return sensor.get_degree()