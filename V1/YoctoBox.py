# Auteur    : Patrick Pinard
# Date      : 4.10.2020
# Objet     : interface Yoctopuce et Blynk avec APP IOS 
# Version   : 1.0
# -*- coding: utf-8 -*-

#   Clavier MAC :      
#  {} = "alt/option" + "(" ou ")"
#  [] = "alt/option" + "5" ou "6"
#   ~  = "alt/option" + n    
#   \  = Alt + Maj + / 


import logging
import blynklib
import time
from datetime import datetime, timedelta
import os
from YoctoBoxLib import YoctoSensorTPH, YoctoRelay,YoctoDisplay

global delay
delay = 600  # temps en sec entre deux lectures des senseurs
global Tmin
global Tmax
path = "/home/pi/YoctoBlynßk"

BLYNK_AUTH = 'clé blynk'
blynk = blynklib.Blynk(BLYNK_AUTH)

logging.basicConfig(filename='YoctoBox.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('########################################')
logging.info('  fichier de LOG : YoctoBox.log')
logging.info('  Patrick Pinard 2020 - YoctoBox V1')
logging.info('  Délai entre deux mesures (mn): %s', int(delay/60))
logging.info('########################################')

# relai 1
@blynk.handle_event('write V1')
def write_virtual_pin_handler(pin, value):
    if str(value[0]) == "1":
        Relay.setState(1,True)     
    else:
        Relay.setState(1,False)   
    return
    
# relai 2
@blynk.handle_event('write V2')
def write_virtual_pin_handler(pin, value):
    if str(value[0]) == "1":
        Relay.setState(2,True)
    else:
        Relay.setState(2,False)
    return

# relai 3
@blynk.handle_event('write V3')
def write_virtual_pin_handler(pin, value):
    if str(value[0]) == "1":
        Relay.setState(3,True)
    else:
        Relay.setState(3,False)
    return

def next_time():
    departure_time = time.strftime("%H:%M:%S")
    delaystr = "00:10:00"
    departure_time_obj = datetime.strptime(departure_time, '%H:%M:%S')
    delay_obj = datetime.strptime(delaystr, '%H:%M:%S') 
    next_time = departure_time_obj + timedelta(hours=delay_obj.hour, minutes=delay_obj.minute, seconds=delay_obj.second)
    next_time = next_time.strftime("%H:%M:%S")
    logging.info('Prochaine mesure prévue à : %s', next_time)
    return next_time

# refresh
@blynk.handle_event('write V4')
def write_virtual_pin_handler(pin, value):
    if str(value[0]) == "1":
        send_TPH()   
        logging.info('Demande manuelle de lecture des données du senseur TPH !')       
    return

# TPH V5, V6, V7
def send_TPH():
    global Meteo, Display
    Meteo.read()
    blynk.virtual_write(5,Meteo.temperature) 
    blynk.virtual_write(6,Meteo.humidity) 
    blynk.virtual_write(7,Meteo.pressure) 
    now = time.strftime("%H:%M:%S")
    blynk.virtual_write(10,now)
    if int(Meteo.temperature) < Tmin:
        Relay.setState(1,True)
        blynk.virtual_write(1,1)
        logging.info('Radiateur enclenché (ON) par thermostat')
    if int(Meteo.temperature) > Tmax:
        Relay.setState(1,False)
        blynk.virtual_write(1,0)
        logging.info('Radiateur déclenché (OFF) par thermostat')
    if Meteo.temperature <= Tmin:
        logging.info('Température basse : <= %s °C !', Tmin)
    blynk.virtual_write(12,next_time())
    Display.display(Meteo.temperature,Meteo.pressure,Meteo.humidity,now)
    return

# Tmin
@blynk.handle_event('write V9')
def write_virtual_pin_handler(pin, value):
    global Tmin, Tmax  
    Tmin = int(value[0])
    logging.info('Changement de Tmin : %s ', Tmin)
    return

# Tmax
@blynk.handle_event('write V8')
def write_virtual_pin_handler(pin, value):
    global Tmin, Tmax  
    Tmax = int(value[0])
    logging.info('Changement de Tmax : %s ', Tmax)
    return    


if __name__ == '__main__':
    Meteo = YoctoSensorTPH('YoctoBox Atelier')
    Relay = YoctoRelay('YoctoBox relais 1 à 4')
    Display = YoctoDisplay('YoctoBox Display')
    start_time = time.time()  
    Tmin = 5
    Tmax = 15
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
