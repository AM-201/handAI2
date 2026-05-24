
import serial
import time

class SerialMonitor:
    def __init__(self, port, baud_rate=115200, timeout=1):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = None

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            time.sleep(2) # Give some time for the serial connection to establish
            print(f"Connected to serial port {self.port} at {self.baud_rate} baud.")
        except serial.SerialException as e:
            print(f"Error connecting to serial port {self.port}: {e}")
            self.ser = None

    def read_line(self):
        if self.ser and self.ser.is_open:
            try:
                line = self.ser.readline().decode("utf-8").strip()
                return line
            except serial.SerialException as e:
                print(f"Error reading from serial port: {e}")
                return None
        return None

    def write_line(self, data):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(data.encode("utf-8") + b"\n")
                return True
            except serial.SerialException as e:
                print(f"Error writing to serial port: {e}")
                return False
        return False

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"Disconnected from serial port {self.port}.")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

if __name__ == '__main__':
    # This is a placeholder. Replace with your ESP32's serial port.
    # On Linux, it might be something like '/dev/ttyUSB0' or 'COM6'
    # On Windows, it would be 'COMx' (e.g., 'COM6')
    SERIAL_PORT = 'COM6' # <<<--- CHANGE THIS TO YOUR ESP32's SERIAL PORT

    try:
        with SerialMonitor(SERIAL_PORT) as monitor:
            if monitor.ser and monitor.ser.is_open:
                print("Serial monitor started. Reading data...")
                while True:
                    line = monitor.read_line()
                    if line:
                        print(f"Received from ESP32: {line}")
                    time.sleep(0.1)
            else:
                print("Could not open serial port. Check if ESP32 is connected and port is correct.")
    except KeyboardInterrupt:
        print("Serial Monitor stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
