import blynklib
import moisture_logger
import logging
import sys

logger = logging.getLogger()

# import blynklib_mp as blynklib # micropython import

BLYNK_AUTH = 'riJfOIo0uTbyVPzvm8WgeV8KwpiESfAn' #insert your Auth Token here
# base lib init
blynk = blynklib.Blynk(BLYNK_AUTH)
 

@blynk.handle_event('read V3')
def read_virtual_pin_handler3(pin):
    logger.debug("read pin %s" % (pin))
    sample=ml.get_sample()
    if sample != {}:
        #self.blynk.virtual_write(pin, sample['temp'])
    # send value to Virtual Pin and store it in Blynk Cloud 
        blynk.virtual_write(pin, sample['temp'])

@blynk.handle_event('read V4')
def read_virtual_pin_handler4(pin):
    logger.debug("read pin %s" % (pin))
    sample=ml.get_sample()
    if sample != {}:
        #self.blynk.virtual_write(pin, sample['temp'])
    # send value to Virtual Pin and store it in Blynk Cloud 
        blynk.virtual_write(pin, sample['humidity'])
    


# class BlynkPublisher:
# 
#     def write_event_handler(self, pin, val):
#         logger.debug("write to pin %s value %s" % (pin,val))
# 
#     def read_event_handler(self, pin):
#         logger.debug("read pin %s" % (pin))
#         if pin in [3,4]:
#             sample=ml.get_sample()
#             if sample != {}:
#                 if pin == 3:
#                     blynk.virtual_write(pin, sample['temp'])
#                 elif pin == 4:
#                     blynk.virtual_write(pin, sample['humidity'])
# 
# @blynk.handle_event('write V*')
# def write_virtual_pin_handler(pin, val):
#     BlynkPublisher().write_event_handler(pin, val)
#  
# @blynk.handle_event('read V*')
# def read_virtual_pin_handler(pin):
#     BlynkPublisher().read_event_handler(pin)
     

#     
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
                   
        # send value to Virtual Pin and store it in Blynk Cloud 
        blynk.virtual_write(pin, self.data1)
        self.data1 += 1


def run():
    """Run"""
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler('log.txt', mode='a')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
        
    global ml
    ml=moisture_logger.Moisture_logger()
    logger.info("Starting...")
    ml.start(port="/dev/ttyUSB0")
    
            
    while True:
        blynk.run()
        ml.read_from_sensor()
    
if __name__ == "__main__":
    run()
