# Pico DAC/ADC Control via Serial

This project lets you control a **DAC80501 (16-bit DAC)** and **MCP3202 (12-bit ADC)** connected to a Raspberry Pi Pico using a simple serial command interface.

A Python script on your PC (`PC_control.py`) sends commands over USB, while the Pico firmware (`main.py`) interprets them and talks to the DAC and ADC via SPI.

---

## Features

- Control a **DAC80501** DAC (set 16-bit values 0–65535).
- Read from a **MCP3202** ADC (12-bit, channels 0 or 1).
- Send simple commands from your PC via USB serial:
  - `setdac <value>`
  - `readadc <channel>`

---

## Hardware Setup

- **Microcontroller**: Raspberry Pi Pico / Pico 2
- **Peripherals**:
  - DAC80501 (SPI DAC)
  - MCP3202 (SPI ADC)

### Pin Connections (as used in `main.py`)

| Pico Pin | Function   | Connected Device          |
|----------|------------|---------------------------|
| GP2      | SPI0 SCK   | DAC80501 & MCP3202 SCK    |
| GP3      | SPI0 MOSI  | DAC80501 & MCP3202 DIN    |
| GP4      | SPI0 MISO  | MCP3202 DOUT              |
| GP5      | CS DAC     | DAC80501 CS               |
| GP6      | CS ADC     | MCP3202 CS                |

---

## Software Setup

### On Your PC

1. Install Python 3.
2. Install required Python package:
   ```bash
   pip install pyserial
   ```
3. Connect the Pico via USB.
4. Find the Pico’s serial port:
   ```bash
   mpremote connect list
   ```
   Example: `/dev/cu.usbmodem1101` (macOS/Linux) or `COM3` (Windows).
5. Edit `PC_control.py` and set the correct `PORT`.

### On the Pico

1. Flash MicroPython firmware to the Pico.
2. Copy `main.py` to the Pico:
   ```bash
   mpremote cp main.py :main.py
   ```
3. Reset the Pico. It will now wait for serial commands from your PC.

---

## Usage

Start the PC control script:

```bash
python PC_control.py
```

You should see:

```
Connected to Pico. Type commands like 'setdac 12345' or 'readadc 0'.
Press Ctrl+C to quit.
```

### Example Interaction

```
-> setdac 30000
<- DAC set to 30000

-> readadc 0
<- ADC0 = 1523

-> readadc 1
<- ADC1 = 2047
```

---

## Command Reference

| Command           | Arguments  | Description                          |
|-------------------|------------|--------------------------------------|
| `setdac <value>`  | `0–65535`  | Sets DAC80501 output voltage.        |
| `readadc [ch]`    | `0` or `1` | Reads 12-bit ADC value from MCP3202. |

---

## Notes

- DAC80501 output range depends on its reference voltage wiring.
- MCP3202 measures relative to its own reference (Vref).
- PC script uses a 1s timeout when waiting for responses.
- Invalid commands return an error message but don’t stop the loop.

---

## Troubleshooting

- **No output from PC script** → Check that `PORT` is correct.
- **Permission denied (Linux/Mac)** → Add your user to the `dialout` group or run with `sudo`.
- **Unexpected ADC values** → Verify wiring, reference voltages, and grounding.

---
