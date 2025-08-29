import serial
import sys

# Adjust port to your Pico (check with mpremote connect list)
PORT = "/dev/cu.usbmodem1101"
BAUD = 115200

def main():
    with serial.Serial(PORT, BAUD, timeout=1) as ser:
        print("Connected to Pico. Type commands like 'setdac 12345' or 'readadc 0'.")
        print("Press Ctrl+C to quit.\n")

        while True:
            try:
                # Get user input
                cmd = input("-> ")
                if not cmd.strip():
                    continue

                # Send command to Pico
                ser.write((cmd + "\n").encode())

                # Read response(s)
                response = ser.readline().decode().strip()
                if response:
                    print("<- " + response)

            except KeyboardInterrupt:
                print("\nExiting.")
                break

if __name__ == "__main__":
    main()