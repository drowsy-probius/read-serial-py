import sys
import time
import argparse

import serial


def hex_to_ascii(data: bytes):
    try:
        return data.decode("latin-1")
    except Exception:
        sys.stderr.write(f"[ERROR] {data.hex()}")
        return data.hex()


def decode_data(data: bytes):
    try:
        return data.decode("utf-8").strip()
    except UnicodeDecodeError:
        return hex_to_ascii(data)


def read_from_port(port, baudrate, output_file):
    while True:
        # run infinite loop
        ser = None
        try:
            ser = serial.Serial(
                port, baudrate, timeout=1, bytesize=8, parity="N", stopbits=1
            )
            sys.stderr.write(f"Connected to {port} at {baudrate} baudrate.\n\n")

            if output_file:
                with open(output_file, "a", encoding="utf8") as file:
                    while True:
                        if not ser.is_open:
                            break
                        data = decode_data(ser.read_until())
                        if data:
                            sys.stdout.write(f"{data}\n")
                            file.write(f"{data}\n")
                            file.flush()
                        time.sleep(0.001)
            else:
                while True:
                    if not ser.is_open:
                        break
                    data = decode_data(ser.read_until())
                    if data:
                        sys.stdout.write(f"{data}\n")
                    time.sleep(0.001)

        except serial.SerialException as e:
            sys.stderr.write(f"Error: {e}\n")
        except KeyboardInterrupt:
            sys.stderr.write("Program interrupted by user.\n")
            return
        finally:
            if ser and ser.is_open:
                ser.close()
                sys.stderr.write("Serial port closed.\n")

        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read from serial UART and save to a file."
    )
    parser.add_argument(
        "-p",
        "--port",
        type=str,
        help="The Bluetooth serial port (e.g., /dev/rfcomm0 or COM3)",
    )
    parser.add_argument(
        "-b",
        "--baudrate",
        type=int,
        help="The baud rate for the Bluetooth connection (e.g., 9600)",
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        default=None,
        help="The file to save the received data",
    )

    args = parser.parse_args()

    read_from_port(args.port, args.baudrate, args.output_file)
