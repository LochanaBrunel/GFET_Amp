# Pico DAC/ADC Control via Serial

This project lets you control a **DAC80501 (16-bit DAC, I²C mode)** and a **MCP3202 (12-bit ADC, SPI mode)** connected to a Raspberry Pi Pico (or Pico 2).
You interact through a simple serial command interface: a Python script on your PC (`PC_control.py`) sends commands over USB, while the Pico firmware (`main.py`) interprets them and talks to the DAC (I²C) and ADC (SPI).

---

## Features

* **DAC80501 (I²C, 16-bit)**

  * Set output voltage with commands like `setdac 1.23`
  * Internal or external reference selectable (`intref` / `extref`)
* **MCP3202 (SPI, 12-bit)**

  * Read analog inputs on channels 0 or 1 via `readadc <channel>`

---

## Hardware Setup

### Components

* Raspberry Pi Pico or Pico 2 (3.3 V I/O)
* DAC80501 (16-bit DAC, configured for I²C mode)
* MCP3202 (12-bit SPI ADC)

### DAC80501 Wiring (I²C mode)

| DAC80501 Pin                                            | Connected To     | Notes                                           |
| ------------------------------------------------------- | ---------------- | ----------------------------------------------- |
| 1 VDD                                                   | Pico 3V3         | Power supply (3.3 V)                            |
| 2 VOUT                                                  | Measure with DMM | DAC analog output                               |
| 3 RSTSEL                                                | GND              | Power-up at 0 V output                          |
| 4 AGND                                                  | Pico GND         | Analog ground                                   |
| 5 SPI2C                                                 | 3V3 (HIGH)       | I²C mode selected                               |
| 6 SCL                                                   | Pico GP5         | I²C clock                                       |
| 7 SYNC/A0                                               | GND              | I²C address = `0x48`                            |
| 8 SDA                                                   | Pico GP4         | I²C data                                        |
| 10 VREFIO                                               | **⚠ Important**  | Internal ref: leave floating, add 150 nF to GND |
| External ref: tie to 3.3 V via ≥1 kΩ, add 150 nF to GND |                  |                                                 |

### MCP3202 Wiring (SPI mode)

| MCP3202 Pin | Connected To         |
| ----------- | -------------------- |
| VDD         | Pico 3V3             |
| VREF        | Pico 3V3             |
| AGND/DGND   | Pico GND             |
| CS          | Pico GP6             |
| DIN         | Pico GP3 (SPI0 MOSI) |
| DOUT        | Pico GP4 (SPI0 MISO) |
| SCK         | Pico GP2 (SPI0 SCK)  |

---

## Software Setup

### On Your PC

1. Install Python 3.
2. Install dependency:

   ```bash
   pip install pyserial
   ```
3. Connect the Pico via USB.
4. Find its serial port:

   ```bash
   mpremote connect list
   ```

   Example: `/dev/cu.usbmodem1101` (macOS/Linux) or `COM3` (Windows).
5. Edit `PC_control.py` and set `PORT`.

### On the Pico

1. Flash MicroPython firmware.
2. Copy firmware:

   ```bash
   mpremote cp main.py :main.py
   ```
3. Reset the Pico. It will listen for serial commands.

---

## Usage

Run the PC control script:

```bash
python PC_control.py
```

Example session:

```text
-> intref
<- Internal reference enabled.

-> setdac 1.23
<- DAC output set to 1.23 V

-> readadc 0
<- ADC0 = 1523
```

---

## Commands

| Command          | Arguments         | Description                               |
| ---------------- | ----------------- | ----------------------------------------- |
| `setdac <volts>` | float (e.g. 1.23) | Set DAC output voltage                    |
| `intref`         | none              | Enable internal 2.5 V reference (default) |
| `extref`         | none              | Disable internal ref, use external VREFIO |
| `readadc <ch>`   | `0` or `1`        | Read MCP3202 ADC channel                  |

---

## Notes

* **DAC Reference**: Choose one configuration:

  * **Internal ref (2.5 V)**: leave VREFIO floating, add 150 nF to GND.
  * **External ref (3.3 V)**: tie VREFIO to 3.3 V via ≥1 kΩ, add 150 nF to GND, and run `extref` on boot.
* **Address**: With A0=0, I²C address = `0x48`.
* **ADC Range**: MCP3202 reads 0–3.3 V (since Vref=3.3 V).

---

## Troubleshooting

* **DAC stuck at 0 V** → Likely VREFIO not wired/decoupled properly, or internal ref not enabled.
* **Have to type `setdac` repeatedly** → Caused by I²C hanging due to reference misconfig; fix by running `intref`/`extref` first.
* **No serial output** → Check `PORT` setting in `PC_control.py`.
* **Permission denied** → Add your user to `dialout` group (Linux) or run with `sudo`.
