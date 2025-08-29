from machine import Pin, SPI
import sys

# SPI setup
spi = SPI(0, baudrate=1000000, polarity=0, phase=1, sck=Pin(2), mosi=Pin(3), miso=Pin(4))

# Chip Selects
cs_dac = Pin(5, Pin.OUT, value=1)   # DAC80501
cs_adc = Pin(6, Pin.OUT, value=1)   # MCP3202

# -----------------------------
# DAC80501
# -----------------------------
def dac_write(value):
    """Write 16-bit value to DAC80501."""
    if not (0 <= value <= 65535):
        raise ValueError("DAC value must be 0–65535")

    cmd = 0x08  # Write to DAC register
    high = (value >> 8) & 0xFF
    low = value & 0xFF
    buf = bytes([cmd, high, low])

    cs_dac.value(0)
    spi.write(buf)
    cs_dac.value(1)

# -----------------------------
# MCP3202
# -----------------------------
def adc_read(channel=0):
    if channel not in (0, 1):
        raise ValueError("Channel must be 0 or 1")

    start_bit = 0b00000110
    config = channel << 6   # channel select

    # Prepare command: 3 bytes
    buf = bytearray([start_bit, config, 0x00])
    resp = bytearray(3)

    cs_adc.value(0)
    spi.write_readinto(buf, resp)
    cs_adc.value(1)

    # resp now has 3 bytes from ADC
    # Extract 12-bit ADC value
    value = ((resp[1] & 0x0F) << 8) | resp[2]
    return value

# -----------------------------
# Command loop over USB serial
# -----------------------------
def command_loop():
    while True:
        try:
            line = sys.stdin.readline().strip()
            if not line:
                continue

            parts = line.split()
            cmd = parts[0].lower()

            if cmd == "setdac" and len(parts) == 2:
                val = int(parts[1])
                dac_write(val)
                print(f"DAC set to {val}")

            elif cmd == "readadc":
                ch = int(parts[1]) if len(parts) > 1 else 0
                val = adc_read(ch)
                print(f"ADC{ch} = {val}")

            else:
                print(f"Unknown command: {line}")

        except Exception as e:
            print(f"Error: {e}")
            # continue running loop instead of crashing

command_loop()
