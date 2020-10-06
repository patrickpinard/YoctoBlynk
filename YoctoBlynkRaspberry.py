# Auteur    : Patrick Pinard
# Date      : 4.10.2020
# Objet     : interface Yoctopuce et Blynk sous IOS 


import logging
import blynklib
import time
import os
from YoctoBoxLib import YoctoSensorTPH, YoctoRelay

delay = 900  #Temps en secondes entre deux lectures des senseurs
global Tmin
global Tmax
path = "/home/pi/YoctoBlynk"

# tune console logging


BLYNK_AUTH = 'blynk key'
blynk = blynklib.Blynk(BLYNK_AUTH)

logging.basicConfig(filename='YoctoBox.log', filemode='wa', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Logging depuis YoctoBlynkRaspberry.py')
logging.info('Délai entre deux mesures (mn): %s', int(delay/60))

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

# refresh
@blynk.handle_event('write V4')
def write_virtual_pin_handler(pin, value):
    send_TPH()
    logging.info('Demande manuelle de lecture des données')
    return

# TPH V5, V6, V7

def send_TPH():
    global Meteo
    Meteo.read()
    blynk.virtual_write(5,Meteo.temperature) 
    blynk.virtual_write(6,Meteo.humidity) 
    blynk.virtual_write(7,Meteo.pressure) 
    if Meteo.temperature < 20:
        blynk.notify("Température basse : < 20°C !")
        logging.info('Température basse : < 20°C !')
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

# Date et Heure de la dernière mesure

@blynk.handle_event('write V10')
def write_virtual_pin_handler(pin, value):
    now = time.strftime("%H:%M:%S")
    blynk.virtual_write(10,str(now)) 
    return    

# Prochaine mesure

@blynk.handle_event('write V11')
def write_virtual_pin_handler(pin, value):
    
    return    

if __name__ == '__main__':
    Meteo = YoctoSensorTPH('YoctoBox Atelier')
    Relay = YoctoRelay('YoctoBox relais 1 à 4')
    start_time = time.time()  
    Tmin = 5
    Tmax = 15
  
try:
    while blynk.connect:
        blynk.run()
        interval = int(time.time() - start_time )
        if (interval > delay):
            send_TPH()   
            start_time = time.time()  
            now = time.strftime("%H:%M:%S")
            blynk.virtual_write(10,str(now))  
            blynk.virtual_write(11,delay) 
            if int(Meteo.temperature) < Tmin:
                Relay.setState(1,True)
                logging.info('Radiateur enclenché par termostat')
            if int(Meteo.temperature) > Tmax:
                Relay.setState(1,False)
                logging.info('Radiateur déclenché par termostat')
                
    
except KeyboardInterrupt:
    
    blynk.disconnect()
    logging.info('Programme terminé')
