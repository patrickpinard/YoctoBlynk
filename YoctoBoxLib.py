# Auteur    : Patrick Pinard
# Date      : 12.10.2020
# Objet     : gestion de senseur Yoctopuce pour température humidité et pression ainsi que relais et affichage
# Version   : 2.1 (amélioration de Object YoctoBox: Tmin, Tmax)

# -*- coding: utf-8 -*-

  
from yoctopuce.yocto_api import *
from yoctopuce.yocto_humidity import *
from yoctopuce.yocto_temperature import *
from yoctopuce.yocto_pressure import *
from yoctopuce.yocto_relay import *
from yoctopuce.yocto_lightsensor import *
from yoctopuce.yocto_display import *
import logging

logging = logging.getLogger()

class YoctoBox(object):

    """
    Classe definissant YoctoBox caracterisé par :
        - name : nom du boitier
        - IP   : adresse IP du module Wifi
        - Relay : module relais (4 ports 240V)
        - SensorTPH : module meteo (température, pression, humidité)
        - Display : module display OLED
    """

    def __init__(self, name, ip):
        """
        Constructeur de la classe YoctoBox.
        """
        logging.info("Construction de l'objet YoctoBox %s ", name)
        self.name = name     
        self.ip = ip     
        self.Tmin = 0
        self. Tmax = 0                               
        self.SensorTPH = YoctoSensorTPH(name, ip)                                                            
        self.Relay = YoctoRelay(name, ip)                                      
        self.Display = YoctoDisplay(name, ip)

    def __repr__(self):
        """
        Méthode permettant d'afficher les paramètres du YoctoBox complet
        """
        return "Paramètres du YoctoBox : {}\n   Température: {}\n   Pression   : {}\n   Humidité   : {}\n   Relai 1    : {}\n   Relai 2    : {}\n   Relai 3    : {}\n   Tmin       : {}\n   Tmax       : {}".format(self.name, self.SensorTPH.temperature,self.SensorTPH.pressure,self.SensorTPH.humidity, self.Relay.readState(1), self.Relay.readState(2),self.Relay.readState(3), self.Tmin, self.Tmax)
    

class YoctoSensorTPH(YoctoBox):

    """
    Classe definissant un senseur de température, pression et humidité caracterisé par :
        - name : nom du senseur
        - module : référence du module Yoctopuce
        - temp : température en degré celsius
        - pressure : pression atmosphérique en hectoPascal
        - humidity: humidité en pourcentage
    """

    def __init__(self, name , ip):
        """
        Constructeur de la classe Sensor.
        valeurs t, p, h  à zéro par défaut
        """
        logging.info("Connexion au YoctoBox wifi HUB...")
        self.name = name
        self.ip = ip
        errmsg = YRefParam()
        if YAPI.RegisterHub(self.ip, errmsg) != YAPI.SUCCESS:
           logging.warning("... Yoctopuce HUB indisponible....Veuillez contrôler la connexion wifi.")
        else:
            logging.info('Création du senseur TPH')  
            sensor = YHumidity.FirstHumidity()
            if sensor is None:
                logging.info('Pas de module METEO (T,H,P) connecté au Yoctopuce HUB')
                return
            else:
                m = sensor.get_module()
                self.target_sensor = m.get_serialNumber()
                logging.info('Senseur TPH créé avec succès')
                self.module = self.target_sensor                                        
                self.temperature = 0                                                             
                self.pressure = 0                                                
                self.humidity = 0

        return

    def __repr__(self):
        """
        Méthode permettant d'afficher les paramètres d'un senseur TPH
        """
        return "  Température : {}\n  Pression    : {}\n  Humidité    : {}\n".format(self.temperature,self.pressure,self.humidity)

    
    def read(self):
        """
        Méthode permettant de lire les valeurs du senseur t, p, h et enregistrement dans fichier log.
        """
        logging.info('Connexion au YoctoBox wifi HUB...')
        errmsg = YRefParam()
        if YAPI.RegisterHub(self.ip, errmsg) != YAPI.SUCCESS:
           logging.warning("... Yoctopuce HUB indisponible....Veuillez contrôler la connexion wifi.")
           return
        else:
            logging.info("Lecture du senseur TPH : ")
            humSensor = YHumidity.FindHumidity(self.target_sensor + '.humidity')
            pressSensor = YPressure.FindPressure(self.target_sensor + '.pressure')
            tempSensor = YTemperature.FindTemperature(self.target_sensor + '.temperature')
            self.temperature = tempSensor.get_currentValue()
            self.humidity = humSensor.get_currentValue()
            self.pressure = pressSensor.get_currentValue()
            logging.info('  Température (celsius)   : %s', self.temperature)
            logging.info('  Humidité    (pourcent)  : %s', self.humidity)
            logging.info('  Pression    (hPascal)   : %s', self.pressure)
        return

class YoctoRelay(YoctoBox):

    """
    Classe definissant un Module Relais caracterisé par :
        - name : nom du module Relai
        - module : référence du module Yoctopuce
        - num : numéro du relai (1,2,3,4)
        - state : état du relai (ON : True; OFF : False)
    """

    def __init__(self, name, ip):
        """
        Constructeur de la classe YoctoRelay pour module 4 relais.
        Etat de tous les relais forcés à OFF
        """
        logging.info('Connexion au YoctoBox wifi HUB...')
        self.name = name
        self.ip = ip
        errmsg = YRefParam()
        if YAPI.RegisterHub(self.ip, errmsg) != YAPI.SUCCESS:
            logging.warning("... Yoctopuce HUB indisponible....Veuillez contrôler la connexion wifi.")
        else:
            relay_module = YRelay.FirstRelay()
            if relay_module is None:
                logging.warning= ('Pas de module Relais connecté au YoctoBox :  %s', self.name)
                return
            else:
                n = relay_module.get_module()
                self.target_relay = n.get_serialNumber()
                logging.info("Module Relais %s créé avec succès sur YoctoBox '%s'", self.target_relay, name)
            
                self.relay1 = YRelay.FindRelay(self.target_relay + '.relay' + '1')
                self.relay2 = YRelay.FindRelay(self.target_relay + '.relay' + '2')
                self.relay3 = YRelay.FindRelay(self.target_relay + '.relay' + '3')
                self.relay4 = YRelay.FindRelay(self.target_relay + '.relay' + '4')
                
                self.relay1.set_output(YRelay.OUTPUT_OFF)
                self.relay2.set_output(YRelay.OUTPUT_OFF)
                self.relay3.set_output(YRelay.OUTPUT_OFF)
                self.relay4.set_output(YRelay.OUTPUT_OFF)  

                self.r = {1:'OFF',2:'OFF',3:'OFF',4:'OFF'}                                 
                
                logging.info('   Relai 1 configuré à OFF')
                logging.info('   Relai 2 configuré à OFF')
                logging.info('   Relai 3 configuré à OFF')
                logging.info('   Relai 4 configuré à OFF') 

        return

    def __repr__(self):
        """
        Méthode permettant d'afficher les paramètres d'un senseur
        """
        return "Relais 1: {}  2: {}  3: {}".format(self.r[1],self.r[2],self.r[3])

    
    def readState(self, number):
        """
        Méthode permettant de lire les états du relai -number et enregistrement dans fichier log.
        Retourne l'état du relai ON = True; OFF = False
        """
        
        errmsg = YRefParam()
        logging.info('Connexion au module Relais')
        if YAPI.RegisterHub(self.ip, errmsg) != YAPI.SUCCESS:
            logging.warning("... Yoctopuce HUB indisponible....Veuillez contrôler la connexion wifi.")
            return
        else:
            logging.info("Lecture du statut du relai : ")
            relay = YRelay.FindRelay(self.target_relay + '.relay' + str(number))
            relaystate = relay.get_state
            logging.info('  Module relais   : %s', self.target_relay)
            logging.info('  Numéro du relai : %s', number)
            if relaystate == YRelay.STATE_A:
                logging.info('  Etat (ON/OFF)   : %s ',self.r[number])
                return True
            else:
                logging.info('  Etat (ON/OFF)   : %s ', self.r[number])
                return False
        

    def setState(self, number, state):
        """
        Méthode permettant de changer l'état du relai -number et enregistrement dans fichier log.
        Paramètre state : True = ON; False = OFF
        """
        logging.info('Connexion au module Relais')
        errmsg = YRefParam()
        if YAPI.RegisterHub(self.ip, errmsg) != YAPI.SUCCESS:
            logging.warning("... Yoctopuce HUB indisponible....Veuillez contrôler la connexion wifi.")
            return
        else:
            logging.info("Changement d'état d'un relai ")
            relay = YRelay.FindRelay(self.target_relay + '.relay' + str(number))
            if relay.isOnline():
                if state :
                    relay.set_output(YRelay.OUTPUT_ON)
                    self.r[number] = 'ON'
                else:
                    relay.set_output(YRelay.OUTPUT_OFF)
                    self.r[number] = 'OFF'

                logging.info('  Module relais   : %s', self.target_relay)
                logging.info('  Numéro du relai : %s', number)
                logging.info('  Etat (ON/OFF)   : %s', self.r[number])

            else:
                logging.warning(' Attention !!!  Module Relais non connecté, contrôlez le wifi de la YoctoBox')        

        return


class YoctoDisplay(YoctoBox):

    """
    Classe definissant un display module Yoctopuce caracterisé par :
        - name : nom du display
        - text : affichage du texte sur display

    """

    def __init__(self, name, ip):
        """
        Constructeur de la classe Display.
        """ 
        logging.info('Connexion au YoctoBox wifi HUB...')
        self. name = name
        self.ip = ip
        errmsg = YRefParam()
        if YAPI.RegisterHub(self.ip, errmsg) != YAPI.SUCCESS:
            logging.warning("... Yoctopuce HUB indisponible....Veuillez contrôler la connexion wifi.")
            returns
        else:
            logging.info("Création du module Display sur YoctoBox '%s' ", self.name)  
            disp = YDisplay.FirstDisplay()
            if disp is None:
                logging.warning('Attention !!!  Module Display non connecté, contrôlez le wifi de la YoctoBox')
                return
            else: 
                self.d = disp.get_module()
                self.target_display = self.d.get_serialNumber()
                logging.info('Target Display : %s', self.target_display)

                #disp.resetAll()
                #w = disp.get_displayWidth()
                #h = disp.get_displayHeight()
            
                self.l0 = disp.get_displayLayer(0)
                self.l0.clear()
                text_ip = "ip : " + self.ip
                self.l0.drawText(30, 10, YDisplayLayer.ALIGN.CENTER_LEFT, "##############" )
                self.l0.drawText(30, 20, YDisplayLayer.ALIGN.CENTER_LEFT, "Bienvenue sur " )
                self.l0.drawText(30, 30, YDisplayLayer.ALIGN.CENTER_LEFT, "YoctoBox V2.1 " )
                self.l0.drawText(30, 40, YDisplayLayer.ALIGN.CENTER_LEFT, "Patrick Pinard")
                self.l0.drawText(30, 50, YDisplayLayer.ALIGN.CENTER_LEFT, " 12 oct. 2020 " ) 
                self.l0.drawText(30, 60, YDisplayLayer.ALIGN.CENTER_LEFT, text_ip )  
                self.l0.drawText(30, 70, YDisplayLayer.ALIGN.CENTER_LEFT, "##############" )                 
        return

    def __repr__(self):
        """
        Méthode permettant d'afficher les paramètres d'un senseur
        """
        return "  Texte sur Display : {}\n".format(self.text)

    
    def display(self, t,p,h,curr_time):
        """
        Méthode permettant d'afficher des valeurs sur le display et enregistrement dans fichier log.
        """
  
        logging.info('Connexion au module Display')
        errmsg = YRefParam()
        if YAPI.RegisterHub(self.ip, errmsg) != YAPI.SUCCESS:
            logging.warning("... Yoctopuce HUB indisponible....Veuillez contrôler la connexion wifi.")
            return
        else:
            logging.info('Affichage sur module Display...')            
            disp = YDisplay.FirstDisplay()
            if disp is None:
                logging.warning('Attention !!!  Module Display non connecté, contrôlez le wifi de la YoctoBox')
                return
            else: 
                self.d = disp.get_module()
                self.target_display = self.d.get_serialNumber()
                logging.info('Target Display : %s', self.target_display)

                #disp.resetAll()
                #w = disp.get_displayWidth()
                #h = disp.get_displayHeight()
            
                self.l0 = disp.get_displayLayer(0)
                self.l0.clear()
                self.l0.drawText(10, 10, YDisplayLayer.ALIGN.CENTER_LEFT, "Température (°C ) = " )
                self.l0.drawText(10, 20, YDisplayLayer.ALIGN.CENTER_LEFT, "Humidité    ( % ) = " )
                self.l0.drawText(10, 30, YDisplayLayer.ALIGN.CENTER_LEFT, "Pression    (hPa) = ")
                self.l0.drawText(60, 50, YDisplayLayer.ALIGN.CENTER, "Dernière mesure : ")
                self.l0.drawText(110, 10, self.l0.ALIGN.CENTER_RIGHT, str(t))
                self.l0.drawText(110, 20, self.l0.ALIGN.CENTER_RIGHT, str(h))
                self.l0.drawText(110, 30, self.l0.ALIGN.CENTER_RIGHT, str(p))
                self.l0.drawText(60, 60, self.l0.ALIGN.CENTER, str(curr_time))
                
                return
