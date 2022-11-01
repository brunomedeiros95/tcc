#-------------------------------------------------------
# Programa: Calibrar Sensor de Umidade
# Esse código tem como objetivo calibrar de forma automática
# o sensor de umidade
#-------------------------------------------------------

import board
import busio
import time

#Define o tipo de módulo usado, no caso, o ADS1115
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

#Inicializa a interface I2C
i2c = busio.I2C(board.SCL, board.SDA)

#Cria o objeto ads
ads = ADS.ADS1115(i2c)

#Define a leitura da porta analogica 0 do módulo
canal0 = AnalogIn(ads, ADS.P0)

#-------------------------------------------------------

print ("CALIBRAÇÃO DO SENSOR DE UMIDADE:")
time.sleep (2)

#-------------------------------------------------------

print ("Para iniciar a calibração do sensor, ele precisa estar seco!","\n")
time.sleep (1)
pergunta1 = input ("O sensor está seco? Digite S ou N para continuar: ",)

if pergunta1 == ("s"):
    seco = (canal0.value)
else:
    secar= input ("Então após secar o sensor digite ok para continuar: ")
    seco = (canal0.value)


print ("Valor 1 definido com sucesso", "\n")
time.sleep (2)

#-------------------------------------------------------

print ("Agora afunde o sensor em um copo água até a altura limite", "\n")
pergunta2 = input ("Com o sensor na água digite ok para continuar: ")
molhado = (canal0.value)

time.sleep (2)
print ("Valor 2 definido com sucesso","\n","\n")
time.sleep (2)
print ("SENSOR DE UMIDADE CALIBRADO COM SUCESSO","\n")

#-------------------------------------------------------
  
while True:
    #Formula para converter os valores analógicos de 0 a 100
    porcentagem = (((canal0.value - seco)/(seco - molhado)) *100 *-1)
   
    if porcentagem <=(0):
        print("0%")
        time.sleep (1)

    elif porcentagem >=(100):
        print("100%")
        time.sleep (1)

    else:
        resultado =("{}%".format(int(porcentagem)))
        print(resultado)
        time.sleep (1)

        
