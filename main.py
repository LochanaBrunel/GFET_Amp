from machine import Pin, I2C
import sys

# -----------------------------
# DAC80501 (I²C mode only)
# -----------------------------
i2c = I2C(0, scl=Pin(5), sda=Pin(4))
DAC_ADDR = 0x48
VREF = 3.3  # volts (tie DAC pin VREFIO to 3.3 V!)


def dac_write(voltage):
    print(f"[DEBUG] dac_write called with {voltage} V")
    if not (0.0 <= voltage <= VREF):
        raise ValueError(f"Voltage must be between 0 and {VREF} V")

    # Convert voltage to 16-bit DAC code
    code = int((voltage / VREF) * 65535)
    print(f"[DEBUG] code = {code}")

    # DAC80501 expects register 0x08 (DAC data)
    reg = 0x08
    high = (code >> 8) & 0xFF
    low = code & 0xFF
    buf = bytes([reg, high, low])
    print(f"[DEBUG] i2c buffer = {buf}")

    i2c.writeto(DAC_ADDR, buf)
    print("[DEBUG] I²C write done")

# -----------------------------
# Command loop
# -----------------------------
def command_loop():
    print("Pico firmware ready. Type 'start' to begin...")

    running = False
    while True:
        try:
            line = sys.stdin.readline().strip()
            if not line:
                continue

            parts = line.split()
            cmd = parts[0].lower()
            if cmd == "scan":
                print("I2C scan:", i2c.scan())
            # --- gating ---
            if not running:
                if cmd == "start":
                    running = True
                    print("System started. Ready for commands.")
                else:
                    print("Waiting for 'start' command...")
                continue

            # --- commands after start ---
            if cmd == "setdac" and len(parts) == 2:
                val = float(parts[1])
                dac_write(val)
                print(f"DAC set to {val:.3f} V")
            else:
                print(f"Unknown command: {line}")

        except Exception as e:
            print(f"Error: {e}")

command_loop()