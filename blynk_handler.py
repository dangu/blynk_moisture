import blynklib
import moisture_logger
import logging
import sys

logger = logging.getLogger()

# import blynklib_mp as blynklib # micropython import

BLYNK_AUTH = 'riJfOIo0uTbyVPzvm8WgeV8KwpiESfAn' #insert your Auth Token here
# base lib init
blynk = blynklib.Blynk(BLYNK_AUTH)
 
# advanced options of lib init
# from __future__ import print_function
# blynk = blynklib.Blynk(BLYNK_AUTH, server='blynk-cloud.com', port=80, ssl_cert=None,
#                        heartbeat=10, rcv_buffer=1024, log=print)

# Lib init with SSL socket connection
# blynk = blynklib.Blynk(BLYNK_AUTH, port=443, ssl_cert='<path to local blynk server certificate>')
# current blynk-cloud.com certificate stored in project as 
# https://github.com/blynkkk/lib-python/blob/master/certificate/blynk-cloud.com.crt
# Note! ssl feature supported only by cPython

    
    # you can define if needed any other pin
    # example: blynk.virtual_write(24, sensor_data)
        
    # you can perform actions if value reaches a threshold (e.g. some critical value)
#     if sensor_data >= critilcal_data_value
#         
#         blynk.set_property(pin, 'color', '#FF0000') # set red color for the widget UI element 
#         blynk.notify('Warning critical value') # send push notification to Blynk App 
#         blynk.email(<youremail@email.com>, 'Email Subject', 'Email Body') # send email to specified address

class BlynkPublisher:
    blynk = blynklib.Blynk(BLYNK_AUTH)
    blynk.run()

    def write_event_handler(self, pin, val):
        print("write to pin %s value %s" % (pin,val))

    def read_event_handler(self, pin):
        print("read pin %s" % (pin))

    def other(self,pin,val):
        self.blynk.virtual_write(pin, val)

@blynk.handle_event('write V*')
def write_virtual_pin_handler(pin, val):
    BlynkPublisher().write_event_handler(pin, val)

@blynk.handle_event('read V*')
def read_virtual_pin_handler(pin):
    BlynkPublisher().read_event_handler(pin)
    
class BlynkHandler:
    """Blynk handler class"""
    def __init__(self):
        """Init"""
        self.data1=11
           
    # register handler for Virtual Pin V22 reading by Blynk App.
    # when a widget in Blynk App asks Virtual Pin data from server within given configurable interval (1,2,5,10 sec etc) 
    # server automatically sends notification about read virtual pin event to hardware
    # this notification captured by current handler 
    @blynk.handle_event('read V22')
    def read_virtual_pin_handler(self,pin):
        
        # your code goes here
        # ...
        # Example: get sensor value, perform calculations, etc
        critilcal_data_value = '<YourThresholdSensorValue>'
            
        # send value to Virtual Pin and store it in Blynk Cloud 
        blynk.virtual_write(pin, self.data1)
        self.data1 += 1


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
        
    ml=moisture_logger.Moisture_logger()
    logger.info("Starting...")
    ml.start(port="/dev/ttyUSB0")
            
    while True:
        blynk.run()
#         ml.get_sample()
    
if __name__ == "__main__":
    run()
