import serial

PORT = "/dev/cu.usbmodem101"  # adjust for your Pico
BAUD = 115200

def main():
    with serial.Serial(PORT, BAUD, timeout=1) as ser:
        print("Connected to Pico. Type 'start' first, then 'setdac <V>' or 'readadc <ch>'.")
        print("Press Ctrl+C to quit.\n")

        # Read any startup message
        startup = ser.readline().decode().strip()
        if startup:
            print("<- " + startup)

        while True:
            try:
                cmd = input("-> ")
                if not cmd.strip():
                    continue

                ser.write((cmd + "\n").encode())

                response = ser.readline().decode().strip()
                if response:
                    print("<- " + response)

            except KeyboardInterrupt:
                print("\nExiting.")
                break

if __name__ == "__main__":
    main()