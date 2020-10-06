# Auteur    : Patrick Pinard
# Date      : 14.08.2020
# Objet     : gestion de senseur Yoctopuce pour température humidité et pression ainsi que relais et affichage
# Version   : 1
# -*- coding: utf-8 -*-

  
from yoctopuce.yocto_api import *
from yoctopuce.yocto_humidity import *
from yoctopuce.yocto_temperature import *
from yoctopuce.yocto_pressure import *
from yoctopuce.yocto_relay import *
from yoctopuce.yocto_lightsensor import *
from yoctopuce.yocto_display import *
import logging

target_sensor = ''
target_relay = ''
target_display = ''

YOCTO_IP_ADDRESS        = "192.168.1.160"

logging.basicConfig(filename='YoctoBox.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('------- {  fichier log du YoctoBox } ----------')
logging.info('Yoctopuce IP address : %s', YOCTO_IP_ADDRESS)

class YoctoSensorTPH:

    """
    Classe definissant un senseur de température, pression et humidité caracterisé par :
        - name : nom du senseur
        - module : référence du module Yoctopuce
        - temp : température en degré celsius
        - pressure : pression atmosphérique en hectoPascal
        - humidity: humidité en pourcentage

    """

    def __init__(self, name):
        """
        Constructeur de la classe Sensor.
        valeurs t, p, h  à zéro par défaut
        """
        global target_sensor

        errmsg = YRefParam()
        # Setup the API to use local Yoctopuce Wireless Hub
        if YAPI.RegisterHub(YOCTO_IP_ADDRESS, errmsg) != YAPI.SUCCESS:
            sys.exit("... Yoctopuce HUB init error....")
        else:
            logging.info('Yoctopuce HUB connecté avec succès !')

        logging.info('Création du senseur "%s"', name)  
        # setup Yoctopuce meteo sensor module
        sensor = YHumidity.FirstHumidity()
        if sensor is None:
            msg = 'Pas de module METEO (T,H,P) connecté au Yoctopuce HUB'
            sys.exit(msg)
        m = sensor.get_module()
        target_sensor = m.get_serialNumber()
        logging.info('Senseur cible identifié : %s', target_sensor)
        
        self.name = name     
        self.module = target_sensor                                        
        self.temperature = 0                                                             
        self.pressure = 0                                                
        self.humidity = 0
        self.ip = YOCTO_IP_ADDRESS 

        return

    def __repr__(self):
        """
        Méthode permettant d'afficher les paramètres d'un senseur
        """
        return "\n  Senseur     : {}\n  IP address  : {}\n  Température : {}\n  Pression    : {}\n  Humidité    : {}\n".format(self.name,self.ip, self.temperature,self.pressure,self.humidity)

    
    def read(self):
        """
        Méthode permettant de lire les valeurs du senseur t, p, h et enregistrement dans fichier log.
        """
        global target_sensor
        logging.info("Lecture du senseur TPH")
        humSensor = YHumidity.FindHumidity(target_sensor + '.humidity')
        pressSensor = YPressure.FindPressure(target_sensor + '.pressure')
        tempSensor = YTemperature.FindTemperature(target_sensor + '.temperature')
        self.temperature = tempSensor.get_currentValue()
        self.humidity = humSensor.get_currentValue()
        self.pressure = pressSensor.get_currentValue()
        logging.info('  Nom du senseur          : %s', self.name)
        logging.info('  Module du senseur       : %s', self.module)
        logging.info('  Température (celsius)   : %s', self.temperature)
        logging.info('  Humidité    (pourcent)  : %s', self.humidity)
        logging.info('  Pression    (hPascal)   : %s', self.pressure)
        logging.info("Fin de lecture du senseur TPH")
        return

class YoctoRelay:

    """
    Classe definissant un Module Relais caracterisé par :
        - name : nom du module Relai
        - module : référence du module Yoctopuce
        - num : numéro du relai (1,2,3,4)
        - state : état du relai (ON : True; OFF : False)

    """

    def __init__(self, name):
        """
        Constructeur de la classe YoctoRelay pour module 4 relais Yoctoupce.
        Etat de tous les relais forcés à OFF
        """
        global target_relay

        logging.info('Création du module relais "%s"', name)  
        errmsg = YRefParam()
        # Setup the API to use local Yoctopuce Wireless Hub
        if YAPI.RegisterHub(YOCTO_IP_ADDRESS, errmsg) != YAPI.SUCCESS:
            sys.exit("... Yoctopuce HUB initialisation ERROR....")
        relay_module = YRelay.FirstRelay()
        if relay_module is None:
            msg = 'Pas de module RELAY connecté au YoctoBox'
            sys.exit(msg)
        n = relay_module.get_module()
        target_relay = n.get_serialNumber()
        logging.info('Relais cible  : %s', target_relay)
       
        self.relay1 = YRelay.FindRelay(target_relay + '.relay' + '1')
        self.relay2 = YRelay.FindRelay(target_relay + '.relay' + '2')
        self.relay3 = YRelay.FindRelay(target_relay + '.relay' + '3')
        self.relay4 = YRelay.FindRelay(target_relay + '.relay' + '4')
        
        self.relay1.set_output(YRelay.OUTPUT_OFF)
        self.relay2.set_output(YRelay.OUTPUT_OFF)
        self.relay3.set_output(YRelay.OUTPUT_OFF)
        self.relay4.set_output(YRelay.OUTPUT_OFF)

        self.name = name     
        self.module = target_relay                                        
                
        logging.info('   Relai 1 configuré à OFF')
        logging.info('   Relai 2 configuré à OFF')
        logging.info('   Relai 3 configuré à OFF')
        logging.info('   Relai 4 configuré à OFF') 

        return

    def __repr__(self):
        """
        Méthode permettant d'afficher les paramètres d'un senseur
        """
        return "\n  Relais : {}\n  1 : {}\n  2    : {}\n  3    : {}\n 4    : {}\n".format(self.name,self.relay1,self.relay2,self.relay3, self.relay4)

    
    def readState(self, number):
        """
        Méthode permettant de lire les états du relai -number et enregistrement dans fichier log.
        Retourne l'état du relai ON = True; OFF = False
        """
        global target_relay
        logging.info("Lecture du relai")
        relay = YRelay.FindRelay(target_relay + '.relay' + str(number))
        relaystate = relay.get_state
        logging.info('  Nom du senseur  : %s', self.name)
        logging.info('  Module relais   : %s', self.module)
        logging.info('  Numéro du relai : %s', number)
        if relaystate == YRelay.STATE_A:
            logging.info(' Etat (ON/OFF)    : ON')
            return True
        else:
            logging.info(' Etat (ON/OFF)    : OFF')
            return False
        

    def setState(self, number, state):
        """
        Méthode permettant de changer l'état du relai -number et enregistrement dans fichier log.
        Paramètre state : True = ON; False = OFF
        """
        global target_relay
        logging.info("Changement d'état du relai")
        relay = YRelay.FindRelay(target_relay + '.relay' + str(number))
        if not (relay.isOnline()):
            logging.info('Relai non connecté') 
        if relay.isOnline():
            if state :
                relay.set_output(YRelay.OUTPUT_ON)
                relaystate = 'ON'
            else:
                relay.set_output(YRelay.OUTPUT_OFF)
                relaystate = 'OFF'
        else:
            logging.info('Relai non connecté') 

        logging.info('  Nom du senseur  : %s', self.name)
        logging.info('  Module relais   : %s', self.module)
        logging.info('  Numéro du relai : %s', number)
        logging.info('  Etat (ON/OFF)   : %s', relaystate)
        

        return
