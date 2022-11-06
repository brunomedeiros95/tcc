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
from flask import Flask, render_template, request, redirect
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
    return render_template('componentes.html')
    
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

    global molhado
    molhado = (canal0.value)
    gpio.setup(rele, 1)
    print (molhado)
    return render_template('calibrar2.html', molhado=molhado)
#-------------------------------------------------------
@app.route('/api', methods=['GET','POST'])
def api():

    if request.method == 'POST':
        req = request.form

        global cidade
        cidade = req['cidade']

        global estado
        estado = req['estado']

        print("Cidade: {} / Estado: {}" .format(cidade, estado))

        return redirect(request.url)
        
    return render_template('api.html')
#-------------------------------------------------------

#-------------------------------------------------------
@app.route("/inteligente")
def inteligente():
    
    umidade = (int(((canal0.value - seco)/(seco - molhado)) *100 *-1))
    status = ("Solo Úmido")
    if (umidade <= 50):
        status = ("Solo Seco")
        gpio.setup(rele, 0)        
        if (umidade < 0):
            umidade= 0
    
    elif (umidade >= 80):
        status = ("Solo Úmido")
        gpio.setup(rele, 1)
        if (umidade > 100):
            umidade = 100
       
    return render_template('inteligente.html', umidade=umidade, status=status)
#-------------------------------------------------------
@app.route('/manual')
def manual():
    
    umidade = (int(((canal0.value - seco)/(seco - molhado)) *100 *-1))
    gpio.setup(rele,1)
    status = ("Irrigação Desligada")

    return render_template('manual.html', umidade=umidade,status=status)
#-------------------------------------------------------
@app.route('/manual/ligar')
def ligarbomba():

    umidade = (int(((canal0.value - seco)/(seco - molhado)) *100 *-1))
    gpio.setup(rele,0)
    status = ("Irrigando")
    if (umidade < 0):
        umidade = 0
    
    elif (umidade > 100):
          umidade = 100

    return render_template('manual.html', umidade=umidade, status=status)
#-------------------------------------------------------
@app.route('/manual/parar')
def desligarbomba():

    umidade = (int(((canal0.value - seco)/(seco - molhado)) *100 *-1))
    gpio.setup(rele,1) 
    status = ("Irrigação Desligada")
    if (umidade < 0):
        umidade = 0
    
    elif (umidade > 100):
          umidade = 100

    return render_template('manual.html', umidade=umidade, status=status)
#-------------------------------------------------------
if __name__=="__main__":

    app.run(debug=True, host='192.168.0.103')
#-------------------------------------------------------

