import time
import argparse

import serial


def decode_data(data: bytes):
    try:
        return data.decode("utf-8").strip()
    except UnicodeDecodeError:
        return data.hex()


def read_from_port(port, baudrate, output_file):
    while True:
        # run infinite loop
        ser = None
        try:
            ser = serial.Serial(
                port, baudrate, timeout=1, bytesize=8, parity="N", stopbits=1
            )
            print(f"Connected to {port} at {baudrate} baudrate.")
            print()

            if output_file:
                with open(output_file, "a", encoding="utf8") as file:
                    while True:
                        if ser.closed:
                            break
                        data = decode_data(ser.read_until(size=1000))
                        if data:
                            print(data)
                            file.write(data)
                            file.flush()
                        time.sleep(0.001)
            else:
                while True:
                    if ser.closed:
                        break

                    data = decode_data(ser.read_until(size=1000))
                    if data:
                        print(data)
                    time.sleep(0.001)

        except serial.SerialException as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("Program interrupted by user.")
            return
        finally:
            if ser and ser.is_open:
                ser.close()
                print("Serial port closed.")

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
