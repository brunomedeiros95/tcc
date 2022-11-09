#-------------------------------------------------------
# Programa: Módulo Relé
# Esse código tem como objetivo testar o funcionamento 
# do relé de forma isolada.
#-------------------------------------------------------

import RPi.GPIO as gpio
import time

rele = 16

gpio.setmode(gpio.BCM)
gpio.setup(rele, gpio.OUT, initial= 0)
gpio.setwarnings(False)

print ("***Teste de Funcionamento do Relé***")


