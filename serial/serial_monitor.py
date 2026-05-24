from __future__ import annotations

import argparse
import sys
import time

import serial
from serial.tools import list_ports


def print_ports():
    ports = list(list_ports.comports())
    if not ports:
        print("No serial ports found.")
        return

    print("Available ports:")
    for port in ports:
        print(f"  {port.device}  -  {port.description}")


def main():
    parser = argparse.ArgumentParser(description="ESP32 serial monitor")
    parser.add_argument("--port", type=str, default="COM6", help="Serial port (example: COM6 or /dev/ttyUSB0)")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate")
    parser.add_argument("--list", action="store_true", help="List available serial ports and exit")
    args = parser.parse_args()

    if args.list:
        print_ports()
        return

    try:
        with serial.Serial(args.port, args.baud, timeout=1) as ser:
            print(f"Connected to {args.port} at {args.baud} baud.")
            while True:
                line = ser.readline().decode(errors="ignore").strip()
                if line:
                    print(line)
                time.sleep(0.01)
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nSerial monitor stopped.")


if __name__ == "__main__":
    main()
    
    