import serial
import logging
import sys
import time

logger = logging.getLogger("rh_logger")




class Moisture_logger():
    def __init__(self):
        """Init"""
        self._ser=serial.Serial()
        self.latestSample = {}

    def get_sample(self):
        """Get the latest sample"""
        return self.latestSample
        
    def start(self,port):
        """Start"""
        self._ser.port=port
        self._ser.baudrate=9600
        self._ser.timeout=0.1
        self._ser.open()
        self._sensorData = ""
        
    def read_from_sensor(self):
        """Get sample"""
        readFromSerialPort=self._ser.readall().decode("UTF8")
        self._sensorData += readFromSerialPort
        if self._sensorData[-2:] == "\r\n":
            elements=self._sensorData.split()
            if len(elements)>=3:
                #This should be correct data
                temp,humidity = float(elements[-3]), float(elements[-1])
                        
                self.latestSample={'time'    : time.time(),
                              'temp'    : temp,
                              'humidity': humidity}
                    
                logger.info("T:{}, RH:{}".format(temp, humidity))
                self._sensorData = ""
        

def run():
    """Run"""
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler('log.txt', mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
        
    ml=Moisture_logger()
    logger.info("Starting...")
    ml.start(port="/dev/ttyUSB0")
    ml.get_sample()
    
if __name__=="__main__":
    run()