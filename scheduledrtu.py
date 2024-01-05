import pandas as pd
from pymodbus.client import ModbusTcpClient
from pymodbus.client import ModbusSerialClient
import time
import logging
import schedule
import ctypes
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

from apscheduler.schedulers.background import BackgroundScheduler, BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
from datetime import datetime

ploads = {
    "TIMESTAMP":0,
    "Phase 1 line to neutral volts":0,
    "Phase 2 line to neutral volts":0,
    "Phase 3 line to neutral volts":0,
    "Phase 1 current":0,
    "Phase 2 current":0,
    "Phase 3 current":0,
    "Phase 1 active power W":0,
    "Phase 2 active power W":0,
    "Phase 3 active power W":0,
    "Total Import kWh" :0,
    "Total Export kWh" :0
}

df = pd.DataFrame(ploads, index=[0])

def ModbusConnect(port="COM3", brate=9600):
    global client 
    client = ModbusSerialClient(baudrate=brate, port=port)
    connect = client.connect()

    builder = BinaryPayloadBuilder(byteorder=Endian.BIG)    
    builder.add_32bit_float(77.77)
    
ModbusConnect()


def ReadRegister():

    timestamp1 = int(time.time())

    timestamp2 = str(datetime.now())
    print(timestamp2)
    ploads['TIMESTAMP'] = timestamp2
    
    p1lnv = client.read_input_registers(0, 2, slave=1)
  #BinaryPayloaddecoder needed to decode float value from modbus register readd
    ploads['Phase 1 line to neutral volts'] = BinaryPayloadDecoder.fromRegisters(p1lnv.registers, byteorder=Endian.BIG).decode_32bit_float()

    p2lnv = client.read_input_registers(2, 2, slave=1)
    ploads['Phase 2 line to neutral volts'] = BinaryPayloadDecoder.fromRegisters(p2lnv.registers, byteorder=Endian.BIG).decode_32bit_float()
    
    p3lnv = client.read_input_registers(4, 2, slave=1)
    ploads['Phase 3 line to neutral volts'] = BinaryPayloadDecoder.fromRegisters(p3lnv.registers, byteorder=Endian.BIG).decode_32bit_float()

    p1c = client.read_input_registers(6, 2, slave=1)
    ploads['Phase 1 current'] = BinaryPayloadDecoder.fromRegisters(p1c.registers, byteorder=Endian.BIG).decode_32bit_float()
    
    p2c = client.read_input_registers(8, 2, slave=1)
    ploads['Phase 2 current'] = BinaryPayloadDecoder.fromRegisters(p2c.registers, byteorder=Endian.BIG).decode_32bit_float()
    
    p3c = client.read_input_registers(10, 2, slave=1)
    ploads['Phase 3 current'] = BinaryPayloadDecoder.fromRegisters(p3c.registers, byteorder=Endian.BIG).decode_32bit_float()
    
    p1p = client.read_input_registers(12, 2, slave=1)
    ploads['Phase 1 active power W'] = BinaryPayloadDecoder.fromRegisters(p1p.registers, byteorder=Endian.BIG).decode_32bit_float()
    
    p2p = client.read_input_registers(14, 2, slave=1)
    ploads['Phase 2 active power W'] = BinaryPayloadDecoder.fromRegisters(p2p.registers, byteorder=Endian.BIG).decode_32bit_float()
    
    p3p = client.read_input_registers(16, 2, slave=1)
    ploads['Phase 3 active power W'] = BinaryPayloadDecoder.fromRegisters(p3p.registers, byteorder=Endian.BIG).decode_32bit_float()

    totalim = client.read_input_registers(72, 2, slave=1)
    ploads['Total Import kWh'] = BinaryPayloadDecoder.fromRegisters(totalim.registers, byteorder=Endian.BIG).decode_32bit_float()
    
    totalex = client.read_input_registers(76, 2, slave=1)
    ploads['Total Export kWh'] = BinaryPayloadDecoder.fromRegisters(totalex.registers, byteorder=Endian.BIG).decode_32bit_float()
    
    global df
  #Adding column name to dataframe
    df.loc[-1] = [ploads['TIMESTAMP'],  ploads["Phase 1 line to neutral volts"], ploads['Phase 2 line to neutral volts'], ploads['Phase 2 line to neutral volts'], ploads['Phase 1 current'], ploads['Phase 2 current'], ploads['Phase 3 current'], ploads['Phase 1 active power W'], ploads['Phase 2 active power W'], ploads['Phase 3 active power W'], ploads["Total Import kWh"], ploads["Total Export kWh"]]  # adding a row
    df.index = df.index + 1  
  #Sort by index
    df = df.sort_index(ascending=False)  
    save_csv()
    
def save_csv():
    df.to_csv("RTE_energymeter.csv")

if __name__== "__main__":
    executors = {'default': ThreadPoolExecutor(20)}
    scheduler = BackgroundScheduler ( executors = executors, job_defaults={'max_instances':2})
  #Interval definition
    intervalTrigger1= IntervalTrigger(seconds=5)
    scheduler.add_job(ReadRegister, intervalTrigger1)
    scheduler.start()
    
