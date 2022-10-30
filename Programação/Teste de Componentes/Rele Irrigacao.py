#-------------------------------------------------------
# Programa: Módulo Relé
# Esse código tem como objetivo testar o funcionamento 
# do relé de forma isolada.
#-------------------------------------------------------

import RPi.GPIO as gpio
import time

rele = 16

gpio.setmode(gpio.BCM)
gpio.setup(rele, gpio.OUT, initial= 1)
gpio.setwarnings(False)

print ("***Teste de Funcionamento do Relé***")

for i in range (3): # Irá ligar/desligar o relé 3 vezes.
    
    gpio.setup(rele, 0)
    print ("Relé Ativado")
    time.sleep(2)

    gpio.setup(rele, 1)
    print ("Relé Desativado")
    time.sleep(2)

gpio.cleanup ()
