import serial
import logging
import sys

logger = logging.getLogger()




class Moisture_logger():
    def __init__(self):
        """Init"""
        self._ser=serial.Serial()
        

        
    def start(self,port):
        """Start"""
        self._ser.port=port
        self._ser.baudrate=9600
        self._ser.open()
        
    def get_sample(self):
        """Get sample"""
        logger.info(self._ser.readline().strip())

def run():
    """Run"""
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler('log.txt', mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
        
    ml=Moisture_logger()
    logger.info("Starting...")
    ml.start(port="/dev/ttyUSB0")
    
if __name__=="__main__":
    run()