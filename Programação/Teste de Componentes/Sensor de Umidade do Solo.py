import board
import busio

#Define o tipo de módulo usado, no caso, o ADS1115
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

#Inicializa a interface I2C
i2c = busio.I2C(board.SCL, board.SDA)

#Cria o objeto ads
ads = ADS.ADS1115(i2c)

#Define a leitura da porta analogica 0 do módulo
canal0 = AnalogIn(ads, ADS.P0)

while True:
    #Formula para converter os valores analógicos de 0 a 100
    porcentagem = (((canal0.value - 26361)/14870) *100 *-1)
    
    #Formatação para imprimir a humidade de 0% a 100%
    resultado =("{}%".format(int(porcentagem)))
    print(resultado)