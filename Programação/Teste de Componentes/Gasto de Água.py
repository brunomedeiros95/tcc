import RPi.GPIO as gpio
import time

rele = 16

gpio.setmode(gpio.BCM)
gpio.setup(rele, gpio.OUT, initial= 1)
gpio.setwarnings(False)

#CALIBRAÇÃO (INÍCIO)

print ("Calibração da Quantidade de Água Irrigada")
gpio.setup(rele, 1)
print ("Encha o copo de medição até a marcação de 100ml")

input("Coloque o copo na entrada da bomba de irrigação, pressione ENTER quando estiver pronto")

input("Ao digitar iniciar a bomba de irrigação será ligada, quando esgotar a água do copo pressione ENTER para parar ")
tempo_inicial = (time.time()) # em segundos
gpio.setup(rele, 0)

input("Pressione ENTER se a água do copo foi esgotada: ")
tempo_final = (time.time()) # em segundos
gpio.setup(rele, 1)

#Print do tempo que demorou para rodar a parte específica do código
tempo_total = (tempo_final - tempo_inicial)

print (tempo_total, "segundos")


ml_segundo = (100 / tempo_total)

#CALIBRAÇÃO (FIM)

# TESTE

input ("Pressione ENTER para ligar a irrigação")
tempo_inicial = (time.time())
gpio.setup(rele, 0)

input ("Pressione ENTER para parar a irrigação")
tempo_final = (time.time())
gpio.setup(rele, 1)

tempo_total = (tempo_final - tempo_inicial)

gasto_litros = ((ml_segundo * tempo_total)/1000)

print ("O total gasto com água foi de {:.2f} litros".format (gasto_litros))