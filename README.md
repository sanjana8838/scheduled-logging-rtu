# scheduled-logging-rtu

## Overview

This Python script provides a scheduled task to read float values from a Modbus RTU energy meter and logs the data at regular intervals. The script uses the `pymodbus` library for Modbus communication and `apscheduler` for scheduling tasks.

## Requirements

- Python 3.x
- `pandas` library
- `pymodbus` library
- `apscheduler` library

Install the required libraries using:

```bash
pip install pandas pymodbus apscheduler
```

## Usage

1. **Configuration**

   Edit the script to set the Modbus RTU parameters, i.e., COM port and baud rate if different from the default.

   ```python
   def ModbusConnect(port="COM3", brate=9600):
   ```

2. **Modbus Connection**

   Initialize the Modbus connection in the script. 

   ```python
   client = ModbusSerialClient(baudrate=brate, port=port)
   ```

3. **Reading Float Values**

   Modify the `ReadRegister` function to match the register addresses of your energy meter or other device. The script currently reads float values from various registers, and you should adapt it based on your device's Modbus map.

   ```python
   p1lnv = client.read_input_registers(0, 2, slave=1)
   ploads['Phase 1 line to neutral volts'] = BinaryPayloadDecoder.fromRegisters(p1lnv.registers, byteorder=Endian.BIG).decode_32bit_float()
   ```

4. **Scheduling**

   Adjust the scheduling parameters based on your requirements. The script is currently set to read registers every 5 seconds.

   ```python
   intervalTrigger1 = IntervalTrigger(seconds=5)
   ```

5. **Run the Script**

   Execute the script using the following command:

   ```bash
   python your_script_name.py
   ```

## Output

The script logs the read data to a CSV file named `RTE_energymeter.csv` at the specified intervals.
