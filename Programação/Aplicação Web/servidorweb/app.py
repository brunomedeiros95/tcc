# Projeto Irrigação Inteligente

import RPi.GPIO as gpio
import time             
import busio, board
from flask import Flask, render_template

#Define o tipo de módulo usado, no caso, o ADS1115
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

gpio.setmode(gpio.BCM)

#Inicializa a interface I2C
i2c = busio.I2C(board.SCL, board.SDA)


#Cria o objeto ads
ads = ADS.ADS1115(i2c)

#Define a leitura da porta analogica 0 do módulo
canal0 = AnalogIn(ads, ADS.P0)

gpio.setwarnings(False)


gpio.setup(27, gpio.OUT, initial= 1)

#-------------------------------------------------------------------------
app = Flask(__name__)

@app.route('/')
def index():
    umidade = (((canal0.value - 26361)/14870) *100 *-1)
    umidadeForm =("{}%".format(int(umidade)))
    #gpio.output(27, 1)
    return render_template('web.html', umidade=umidade, umidadeForm=umidadeForm)

@app.route("/Inteligente")
def inteligente():
    umidade = (((canal0.value - 26361)/14870) *100 *-1)
    umidadeForm =("{}%".format(int(umidade)))
   
    if (umidade <= 50): 
        gpio.output(27, 0)        
        print("Irrigando")
    
    elif (umidade >= 80):
        gpio.output(27, 1)
        print("Irrigação Desligada") 
    
    else:
        print("Monitorando...")  
       
    return render_template('web_inteligente.html', umidade=umidade, umidadeForm=umidadeForm)

@app.route('/Manual')
def manual():
    umidade = (((canal0.value - 26361)/14870) *100 *-1)
    umidadeForm =("{}%".format(int(umidade)))
    return render_template('web_manual.html', umidade=umidade, umidadeForm=umidadeForm)

@app.route('/Manual/Ligar')
def ligarbomba():
    gpio.output(27,0)
    umidade = (((canal0.value - 26361)/14870) *100 *-1)
    umidadeForm =("{}%".format(int(umidade)))
    return render_template('web_manual.html', umidade=umidade, umidadeForm=umidadeForm)

@app.route('/Manual/Parar')
def desligarbomba():
    gpio.output(27,1)
    umidade = (((canal0.value - 26361)/14870) *100 *-1)
    umidadeForm =("{}%".format(int(umidade)))
    return render_template('web_manual.html', umidade=umidade, umidadeForm=umidadeForm)

if __name__=="__main__":

    app.run(debug=True, host='192.168.15.87')
#-------------------------------------------------------------------------

