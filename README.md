# YoctoBox
# Modules Yoctopuce pilotés par APP Blynk sur IOS au travers d'une gateway Raspberry Pi 4

Ce projet consiste à créer une APP avec Blynk permettant de piloter à distance un boitier (YoctoBox) comprenant des relais, un affichage et une sonde de température, pression et humidité.

Il est constitué de modules Yoctopuce insérés dans un boitier permettant d'assurer une isolation électrique entre la partie 240V et les modules Yoctopuce. 

Comme Yoctopuce n'offre pas de compatibilité avec Blynk pour un contrôle complet, une gateway est utilisée au travers d'un Raspberry Pi 4 qui héberge le code Python permettant d'assurer les commandes au module YoctoBox. 

La YoctoBox intègre un relai pour un radiateur qui peut être enclenché et déclenché par un thermostat sur l'APP Blynk (pin V8 et V9). 

Utilisation de Yoctopuce Wifi avec yocto-display (display OLED de 128x32 pixels), yocto-maxipowerrelay (carte 4 relais 240V) et yocto-meteo (senseur de température, humidité et pression atmosphérique). Gateway au travers du Raspberry Pi 4 qui héberge le code python. Application Blynk sur SmartPhone IOS

# BLYNK 
Blynk est un service web d'Internet des Objets (IoT) permettant de créer des Application sous Android/IOS rapidement et très simplement. Il exisite une multitude de libraiaire dans les languages C, Python disponibles sur GitHub. 

![](images/YoctoBox-Blynk-APP.png)

https://www.yoctopuce.com

La définition des Virtual Pin est représentée sur l'image suivante : 


![](images/Yoctobox-Blynk-VPINs.png)

# LES MODULES Yoctopuce
4 modules Yoctopuce sont nécessaires pour ce boitier YoctoBox: 

# Module Wifi Yoctopuce
Le YoctoHub-Wireless-n est un module doté d'une connexion réseau sans fil (au standard 802.11b/g/n) permettant d'héberger 3 modules Yoctopuce pour y accéder à distance. Il peut être alimenté à l'aide d'un câble USB Micro-B et d'un simple chargeur de téléphone portable, ou d'une batterie 5V. 

![](images/YHUBWLN4.png)

https://www.yoctopuce.com

# Module Display Yoctopuce
Le Yocto-Display est un écran OLED de 128x32 pixels pilotable directement par USB. Il est doté d'un processeur embarqué permettant d'effectuer de manière autonome des opérations graphiques simples, d'afficher du texte avec diverses polices de caractères et même de jouer des animations pré-enregistrées. Son utilisation par USB, sans driver, en fait une solution idéale comme petit écran de contrôle pour des applications embarquées pilotées par un mini-PC tel que le Raspberry Pi. 

![](images/yoctodisplay.jpg)


# Module Relais Yoctopuce
le Yocto-MaxiPowerRelay comprend 5 relais qui supportent jusqu'à 250V et et 5 ampères. L'état de chaque relais est indiqué par une LED indépendante. 

![](images/yocto-maxipowerelay.jpg)

# Module Meteo Yoctopuce
Votre propre station météo USB: le module Yocto-Meteo permet d'effectuer des mesures instantanées de température, de pression et d'humidité via un port USB, ainsi que d'enregistrer des mesures en continu sur une mémoire flash intégrée et de les relire ultérieurement via USB. C'est le module idéal pour faire votre propre station météo et surveiller les conditions météorologiques dans votre jardin. 

![](images/yocto-meteo.jpg)


# Raspberry Pi 4
Le Raspberry Pi 4 n'a plus besoin d'être présenté...

![](images/raspberrypi.jpg)

La station Terminal Raspberry PI 4 : 

![](images/Raspberrypi-terminal.jpg)

# Schéma de connectivité Yoctopuce
Les modules Yoctopuces sont connectés entre eux par des câbles USB. 
ATTENTION au câblage 240V sur les relais. Il doit être fait selon les règles de l'art et isolé du boitier pour assurer une sécurité maximale.

![](images/schema.jpg)

# Montage de la YoctoBox
La YoctoBox est montée dans un boitier étanche et résistant pouvant accueillir l'ensemble des modules.

![](images/yoctobox1.jpg)

![](images/yoctobox2.jpg)

![](images/yoctobox3.jpg)

![](images/yoctobox4.jpg)

![](images/yoctobox5.jpg)

![](images/yoctobox6.jpg)


# Fichier de LOG
Un fichier de LOG permet de contrôler l'ensemble des actions et mesures faites sur le YoctoBox. Le LOG est disponible sur le Raspberry Pi sous le fichier YocotBox.log.

Exemple du LOG file : 

2020-10-09 11:26:11,944 - INFO - ########################################
2020-10-09 11:26:11,944 - INFO -   fichier de LOG : YoctoBox.log
2020-10-09 11:26:11,944 - INFO -   Patrick Pinard 2020 - YoctoBox V1
2020-10-09 11:26:11,945 - INFO -   Délai entre deux mesures (mn): 10
2020-10-09 11:26:11,945 - INFO - ########################################
2020-10-09 11:26:12,249 - INFO - Yoctopuce HUB connecté avec succès !
2020-10-09 11:26:12,250 - INFO - Création du senseur "YoctoBox Atelier"
2020-10-09 11:26:12,251 - INFO - Senseur cible identifié : METEOMK2-EB018
2020-10-09 11:26:12,251 - INFO - Création du module relais "YoctoBox relais 1 à 4"
2020-10-09 11:26:12,349 - INFO - Relais cible  : MXPWRRLY-EAA6E
2020-10-09 11:26:12,351 - INFO -    Relai 1 configuré à OFF
2020-10-09 11:26:12,351 - INFO -    Relai 2 configuré à OFF
2020-10-09 11:26:12,351 - INFO -    Relai 3 configuré à OFF
2020-10-09 11:26:12,351 - INFO -    Relai 4 configuré à OFF
2020-10-09 11:26:12,494 - INFO - Yoctopuce HUB connecté avec succès !
2020-10-09 11:26:12,495 - INFO - Création du display "YoctoBox Display"
2020-10-09 11:26:12,496 - INFO - Target Display : YD128X64-E4EB0
2020-10-09 11:26:39,399 - INFO - Changement d'état du relai
2020-10-09 11:26:39,461 - INFO -   Nom du senseur  : YoctoBox relais 1 à 4
2020-10-09 11:26:39,461 - INFO -   Module relais   : MXPWRRLY-EAA6E
2020-10-09 11:26:39,461 - INFO -   Numéro du relai : 3
2020-10-09 11:26:39,462 - INFO -   Etat (ON/OFF)   : ON
2020-10-09 11:26:40,200 - INFO - Changement d'état du relai
2020-10-09 11:26:40,235 - INFO -   Nom du senseur  : YoctoBox relais 1 à 4
2020-10-09 11:26:40,236 - INFO -   Module relais   : MXPWRRLY-EAA6E
2020-10-09 11:26:40,236 - INFO -   Numéro du relai : 3
2020-10-09 11:26:40,237 - INFO -   Etat (ON/OFF)   : OFF
2020-10-09 11:27:54,188 - INFO - Lecture du senseur TPH
2020-10-09 11:27:54,266 - INFO -   Nom du senseur          : YoctoBox Atelier
2020-10-09 11:27:54,267 - INFO -   Adresse IP              : 192.168.1.160
2020-10-09 11:27:54,267 - INFO -   Module du senseur       : METEOMK2-EB018
2020-10-09 11:27:54,268 - INFO -   Température (celsius)   : 14.82
2020-10-09 11:27:54,268 - INFO -   Humidité    (pourcent)  : 60.1
2020-10-09 11:27:54,269 - INFO -   Pression    (hPascal)   : 958.04
2020-10-09 11:27:54,290 - INFO - Prochaine mesure prévue à : 11:37:54
2020-10-09 11:27:54,336 - INFO - Nom du display    : YoctoBox Display
2020-10-09 11:27:54,337 - INFO - Module du display : YD128X64-E4EB0
2020-10-09 11:27:54,337 - INFO - ....Affichage des paramètres TPH
2020-10-09 11:27:54,341 - INFO - Demande manuelle de lecture des données du senseur TPH !
2020-10-09 11:27:57,759 - INFO - Lecture du senseur TPH
2020-10-09 11:27:57,812 - INFO -   Nom du senseur          : YoctoBox Atelier
2020-10-09 11:27:57,813 - INFO -   Adresse IP              : 192.168.1.160
2020-10-09 11:27:57,813 - INFO -   Module du senseur       : METEOMK2-EB018
2020-10-09 11:27:57,814 - INFO -   Température (celsius)   : 14.83
2020-10-09 11:27:57,814 - INFO -   Humidité    (pourcent)  : 60.4
2020-10-09 11:27:57,814 - INFO -   Pression    (hPascal)   : 958.05
2020-10-09 11:27:57,815 - INFO - Prochaine mesure prévue à : 11:37:57
2020-10-09 11:27:57,858 - INFO - Nom du display    : YoctoBox Display
2020-10-09 11:27:57,858 - INFO - Module du display : YD128X64-E4EB0
