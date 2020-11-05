import blynklib
import blynktimer
import moisture_logger
import logging
import sys
import time

logger = logging.getLogger()

# import blynklib_mp as blynklib # micropython import

BLYNK_AUTH = 'riJfOIo0uTbyVPzvm8WgeV8KwpiESfAn' #insert your Auth Token here
# base lib init
blynk = blynklib.Blynk(BLYNK_AUTH)

timer = blynktimer.Timer()

t0 = time.time()

# 
# @blynk.handle_event('read V3')
# def read_virtual_pin_handler3(pin):
#     logger.debug("read pin %s" % (pin))
#     sample=ml.get_sample()
#     if sample != {}:
#         #self.blynk.virtual_write(pin, sample['temp'])
#     # send value to Virtual Pin and store it in Blynk Cloud 
#         blynk.virtual_write(pin, sample['temp'])
# 
# @blynk.handle_event('read V4')
# def read_virtual_pin_handler4(pin):
#     logger.debug("read pin %s" % (pin))
#     sample=ml.get_sample()
#     if sample != {}:
#         #self.blynk.virtual_write(pin, sample['temp'])
#     # send value to Virtual Pin and store it in Blynk Cloud 
#         blynk.virtual_write(pin, sample['humidity'])
#     
# Code below: register two timers for different pins with different intervals
# run_once flag allows to run timers once or periodically
@timer.register(vpin_num=3, interval=5, run_once=False)
@timer.register(vpin_num=4, interval=5, run_once=False)
def write_to_virtual_pin(vpin_num=1):
    if vpin_num in [3,4]:
        sample=ml.get_sample()
        if sample != {}:
            if vpin_num == 3:
                blynk.virtual_write(vpin_num, sample['temp'])
            elif vpin_num == 4:
                blynk.virtual_write(vpin_num, sample['humidity'])

@timer.register(vpin_num=5, interval=10, run_once=False)
@timer.register(vpin_num=6, interval=10, run_once=False)
def write_uptime(vpin_num=1):
    """Write the uptime to a virtual pin"""
    last_restart = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t0))
    uptime = time.strftime("%H:%M:%S",time.localtime(time.time()-t0))
    if vpin_num==5:
        blynk.virtual_write(vpin_num, last_restart)
    elif vpin_num==6:
        blynk.virtual_write(vpin_num, uptime)
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
     


def run():
    """Run"""
    formatter = logging.Formatter(fmt='%(asctime)s %(name)-9s %(levelname)-8s %(message)s',
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
        timer.run()
        ml.read_from_sensor()
    
if __name__ == "__main__":
    run()
