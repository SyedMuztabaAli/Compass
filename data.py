import serial
import random
import time

# Configure the serial port
com_port = 'COM1'  # Replace with your COM port
baud_rate = 9600  # Set the baud rate (match the device's configuration)
timeout = 5  # Timeout for reading (in seconds)

try:
    # Open the serial port
    ser = serial.Serial(com_port, baud_rate, timeout=timeout)
    print(f"Connected to {com_port} at {baud_rate} baud.")

    # Data to send

    # Send data
    while True:
        x = random.uniform(0.0, 360.0)
        y = random.uniform(0.0, 360.0)
        z = random.uniform(0.0, 360.0)

        data_to_send = f"X:{x}, Y:{y}, Z:{z}\n"  # \r\n for a new line (if needed)
        ser.write(data_to_send.encode())  # Encode string to bytes
        print(f"Sent: {data_to_send}")
        time.sleep(1)

    # Close the serial port
    ser.close()
    print("Serial port closed.")

except serial.SerialException as e:
    print(f"Error: {e}")