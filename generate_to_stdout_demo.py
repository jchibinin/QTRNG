import spidev
import time
from datetime import datetime

class MCP3208:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 100000
        self.spi.mode = 2
    
    def read_channel(self, channel):
        if channel < 0 or channel > 7:
            return -1
        
        start_bit = 0x06    
        channel_bits = channel & 0x07  
    
        cmd = [
            start_bit,
            (channel_bits << 6),
            0
        ]
    
        adc = self.spi.xfer2(cmd)
    
        value = ((adc[1] & 0x0F) << 8) | adc[2]
        return value
    
    def read_channel_1(self, channel):
        cmd = [6 | (channel >> 2), (channel & 3) << 6, 0]
        adc = self.spi.xfer2(cmd)
        return ((adc[1] & 15) << 8) + adc[2]

adc = MCP3208()
bits_buffer = ""

try:
    start_time = time.time()
    samples = 0
    
    while True:
        ch0 = adc.read_channel_1(0)
        ch1 = adc.read_channel_1(1)
        
        # Add bit to buffer
        if ch1 > ch0:
            bits_buffer += "1"
        elif ch0 > ch1:
            bits_buffer += "0"
                    
        samples += 1
        
        
        if len(bits_buffer) >= 48:
            print(bits_buffer)
            bits_buffer = ""  
        

except KeyboardInterrupt:
    
    if bits_buffer:
        print(bits_buffer)
    elapsed = time.time() - start_time
    print("mean freq: " + str(samples/elapsed)) 