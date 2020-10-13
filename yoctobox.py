# Auteur    : Patrick Pinard
# Date      : 12.10.2020
# Objet     : interface Yoctopuce et Blynk avec APP IOS 
# Version   : 2.1  (amélioration de Object YocotBox)
# -*- coding: utf-8 -*-


import logging
import blynklib
import time
from datetime import datetime, timedelta
import os
from YoctoBoxLib import YoctoBox 

global delay
delay = 600  # temps en sec entre deux lectures des senseurs
global YoctoBox

PATH = "/home/pi/yoctoblynk"
YOCTO_IP = '192.168.1.160'
YOCTO_NAME = 'Atelier'
BLYNK_AUTH = 'rcB91tMoGqFLKR7vZ1ePrDIqn0izH59W'

blynk = blynklib.Blynk(BLYNK_AUTH)

logging.basicConfig(filename='yoctobox.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('YoctoBOX - v2.1 ')
logging.info('Patrick Pinard - oct. 2020')
logging.info('Délai entre deux mesures (mn): %s', int(delay/60))
logging.info('Adresse IP :  %s', YOCTO_IP)

# relai 1
@blynk.handle_event('write V1')
def write_virtual_pin_handler(pin, value):
    
    if str(value[0]) == "1":
        YoctoBox.Relay.setState(1,True)    
    else:
        YoctoBox.Relay.setState(1,False)     
    return
    
# relai 2
@blynk.handle_event('write V2')
def write_virtual_pin_handler(pin, value):
    
    if str(value[0]) == "1":
        YoctoBox.Relay.setState(2,True)  
    else:
        YoctoBox.Relay.setState(2,False)
    return

# relai 3
@blynk.handle_event('write V3')
def write_virtual_pin_handler(pin, value):
    
    if str(value[0]) == "1":
        YoctoBox.Relay.setState(3,True)
    else:
        YoctoBox.Relay.setState(3,False)  
    return

# refresh
@blynk.handle_event('write V4')
def write_virtual_pin_handler(pin, value):
    if str(value[0]) == "1":
        logging.info('Lecture manuelle des données du senseur TPH')   
        send_TPH()  
    return

# TPH V5, V6, V7
def send_TPH():
    global YoctoBox
    YoctoBox.SensorTPH.read()
    blynk.virtual_write(5,YoctoBox.SensorTPH.temperature) 
    blynk.virtual_write(6,YoctoBox.SensorTPH.humidity) 
    blynk.virtual_write(7,YoctoBox.SensorTPH.pressure) 
    now = time.strftime("%H:%M:%S")
    blynk.virtual_write(10,now)
    next = next_time()
    blynk.virtual_write(12,next)
    YoctoBox.Display.display(YoctoBox.SensorTPH.temperature,YoctoBox.SensorTPH.pressure,YoctoBox.SensorTPH.humidity,now)
    if int(YoctoBox.SensorTPH.temperature) < YoctoBox.Tmin:
        YoctoBox.Relay.setState(1,True)
        blynk.virtual_write(1,1)
        logging.info('Radiateur enclenché (ON) par thermostat car T : %s plus petite que Tmin : %s', YoctoBox.SensorTPH.temperature, Tmin)
    if int(YoctoBox.SensorTPH.temperature) > YoctoBox.Tmax:
        YoctoBox.Relay.setState(1,False)
        blynk.virtual_write(1,0)
        logging.info('Radiateur déclenché (OFF) par thermostat car T : %s plus grande que Tmax : %s', YoctoBox.SensorTPH.temperature, Tmax)
    logging.info("Relais 1: %s  2: %s  3 : %s",YoctoBox.Relay.r[1], YoctoBox.Relay.r[2],YoctoBox.Relay.r[3])
    terminal.write(YoctoBox)
    return

def next_time():
    departure_time = time.strftime("%H:%M:%S")
    delaystr = "00:10:00"
    departure_time_obj = datetime.strptime(departure_time, '%H:%M:%S')
    delay_obj = datetime.strptime(delaystr, '%H:%M:%S') 
    next = departure_time_obj + timedelta(hours=delay_obj.hour, minutes=delay_obj.minute, seconds=delay_obj.second)
    logging.info('Prochaine mesure prévue à : %s', next.strftime("%H:%M:%S"))
    return next.strftime("%H:%M:%S")

# Tmin
@blynk.handle_event('write V9')
def write_virtual_pin_handler(pin, value):
    YoctoBox.Tmin = int(value[0])
    logging.info('Changement de Tmin : %s ', YoctoBox.Tmin)
    return

# Tmax
@blynk.handle_event('write V8')
def write_virtual_pin_handler(pin, value):
    YoctoBox.Tmax = int(value[0])
    logging.info('Changement de Tmax : %s ', YoctoBox.Tmax)
    return    

# Next mesure
@blynk.handle_event('write V12')
def write_virtual_pin_handler(pin, value):
    
    return    

# Terminal
@blynk.handle_event('write V0')
def write_virtual_pin_handler(pin, value):
    blynk.virtual_write(0,YoctoBox)
    return    

if __name__ == '__main__':
    YoctoBox = YoctoBox(YOCTO_NAME, YOCTO_IP)
    start_time = time.time()  
    YoctoBox.Tmin = 5
    YoctoBox.Tmax = 15
    
try:
    while blynk.connect:
        blynk.run()
        interval = int(time.time() - start_time ) 
        blynk.virtual_write(11,delay/60) 
        if (interval > delay):
            send_TPH()   
            start_time = time.time() 
    
except KeyboardInterrupt:
    blynk.disconnect()
    logging.info('Programme YoctoBox terminé')
