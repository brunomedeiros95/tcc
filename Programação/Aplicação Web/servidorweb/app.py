#-------------------------------------------------------
# Programa: Irrigação Inteligente com Raspberry PI
# Curso:    Sistemas de Informação SI7P13/SI8P13.
# Autores:  Bruno Medeiros Justo Ferreira
#           Daniele da Silva Menezes
#           Leilton Pereira de Souza
#           Rodrigo Sanches de Oliveira
#-------------------------------------------------------

# Projeto Irrigação Inteligente

import RPi.GPIO as gpio
import time             
import busio
import board
from flask import Flask, render_template
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


rele = 16
gpio.setup(rele, gpio.OUT, initial= 4)

#Inicializa interface I2C / Configura ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
canal0 = AnalogIn(ads, ADS.P0)

gpio.setwarnings(False)

app = Flask(__name__)
#-------------------------------------------------------
@app.route('/') 
def index():
    
    umidade = (((canal0.value - 26490)/15490) *100 *-1)
    umidadeForm =("{}%".format(int(umidade)))
    
    gpio.setup(rele, 1)
    
    return render_template('web.html', umidade=umidade, umidadeForm=umidadeForm)
#-------------------------------------------------------
@app.route("/Inteligente")
def inteligente():
    
    umidade = (((canal0.value - 26490)/15490) *100 *-1) 
    umidadeForm =("{}%".format(int(umidade)))
   
    if (umidade <= 50): 
        gpio.setup(rele, 0)        
        print("Irrigando")
       
    elif (umidade >= 80):
        gpio.setup(rele, 1)
        print("Irrigação Desligada") 
    
    else:
        print("Monitorando...")  
       
    return render_template('web_inteligente.html', umidade=umidade, umidadeForm=umidadeForm)
#-------------------------------------------------------
@app.route('/Manual')
def manual():
    
    umidade = (((canal0.value - 26490)/15490) *100 *-1) 
    umidadeForm =("{}%".format(int(umidade)))
    
    return render_template('web_manual.html', umidade=umidade, umidadeForm=umidadeForm)
#-------------------------------------------------------
@app.route('/Manual/Ligar')
def ligarbomba():
    
    umidade = (((canal0.value - 26490)/15490) *100 *-1) 
    umidadeForm =("{}%".format(int(umidade)))
    gpio.setup(rele,0)
    
    return render_template('web_manual.html', umidade=umidade, umidadeForm=umidadeForm)
#-------------------------------------------------------
@app.route('/Manual/Parar')
def desligarbomba():
    
    gpio.setup(rele,1)
    umidade = (((canal0.value - 26490)/15490) *100 *-1) 
    umidadeForm =("{}%".format(int(umidade)))
    
    return render_template('web_manual.html', umidade=umidade, umidadeForm=umidadeForm)
#-------------------------------------------------------
if __name__=="__main__":

    app.run(debug=True, host='192.168.0.104')
#-------------------------------------------------------

