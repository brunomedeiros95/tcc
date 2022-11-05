#-------------------------------------------------------
# Programa: Irrigação Inteligente com Raspberry PI
# Curso:    Sistemas de Informação SI7P13/SI8P13.
# Autores:  Bruno Medeiros Justo Ferreira
#           Daniele da Silva Menezes
#           Leilton Pereira de Souza
#           Rodrigo Sanches de Oliveira
#-------------------------------------------------------

import RPi.GPIO as gpio
import time             
import busio
import board
from flask import Flask, render_template
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


rele = 16
gpio.setup(rele, gpio.OUT, initial= 1)

#Inicializa interface I2C / Configura ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
canal0 = AnalogIn(ads, ADS.P0)

gpio.setwarnings(False)

app = Flask(__name__)
#-------------------------------------------------------
@app.route('/') 
def index():
    
    gpio.setup(rele, 1)
    return render_template('index.html')
    
#-------------------------------------------------------
@app.route('/calibrar')
def calibrar():
    gpio.setup(rele, 1)
    print("Iniciar calibração")
    return render_template('calibrar.html')
#-------------------------------------------------------
@app.route('/calibrar1')
def calibrar1():

    global seco
    seco = (canal0.value)
    gpio.setup(rele, 1)
    print (seco)
    return render_template('calibrar1.html', seco=seco)
#-------------------------------------------------------
@app.route('/calibrar2')
def calibrar2():

    global molhado, umidade
    molhado = (canal0.value)
    umidade = (int(((canal0.value - seco)/(seco - molhado)) *100 *-1))
    gpio.setup(rele, 1)
    print (molhado)
    return render_template('calibrar2.html', molhado=molhado)
#-------------------------------------------------------
@app.route("/inteligente")
def inteligente():
   
    if (umidade <= 50) and (umidade > 0):
        gpio.setup(rele, 0)        
       
    elif (umidade >= 80) and (umidade < 100):
        gpio.setup(rele, 1)
    
    elif (umidade < 0):
        gpio.setup(rele, 0)
        umidade = 0
    
    elif (umidade > 100):
        gpio.setup(rele, 1)
        umidade = 100
    
    else:
        print("Monitorando...")  
       
    return render_template('inteligente.html', umidade=umidade)
#-------------------------------------------------------
@app.route('/manual')
def manual():

    gpio.setup(rele,1)
    return render_template('manual.html', umidade=umidade)
#-------------------------------------------------------
@app.route('/manual/ligar')
def ligarbomba():
    
    gpio.setup(rele,0)
    return render_template('manual.html', umidade=umidade)
#-------------------------------------------------------
@app.route('/manual/parar')
def desligarbomba():
    
    gpio.setup(rele,1) 
    return render_template('manual.html', umidade=umidade)
#-------------------------------------------------------
if __name__=="__main__":

    app.run(debug=True, host='192.168.0.108')
#-------------------------------------------------------

