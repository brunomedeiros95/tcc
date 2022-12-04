#-------------------------------------------------------
# Programa: Irrigação Inteligente com Raspberry PI
# Curso:    Sistemas de Informação SI7P13/SI8P13.
# Autores:  Bruno Medeiros Justo Ferreira
#           Daniele da Silva Menezes
#           Leilton Pereira de Souza
#           Rodrigo Sanches de Oliveira
#-------------------------------------------------------

import RPi.GPIO as gpio       
import busio
import board
import requests 
import time
from flask import Flask, render_template, redirect, request
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from datetime import datetime, timedelta
import time

#Inicializa interface I2C / Configura ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
canal0 = AnalogIn(ads, ADS.P0)

token = ("ecceaa6b7d3bbf475f371f4b4dc64d03")

rele = 16
gpio.setup(rele, gpio.OUT, initial= 1)
gpio.setwarnings(False)

app = Flask(__name__)
#-------------------------------------------------------
@app.route('/') 
def componentes():

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

    return render_template('calibrar1.html')
#-------------------------------------------------------
@app.route('/calibrar2')
def calibrar2():

    global molhado
    molhado = (canal0.value)
    gpio.setup(rele, 1)
    print (molhado)

    return render_template('calibrar2.html')
#-------------------------------------------------------
@app.route('/api', methods=['GET','POST'])
def api():

    if request.method == 'POST':
        req = request.form
       
        global cidade
        cidade = req['cidade']

        print("Cidade: {}" .format(cidade))
        erro = ""

        return redirect(request.url)
    
    try:
        link = ("https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&lang=pt_br").format(cidade,token)
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()
        descricao = requisicao_dic['weather'][0]['description']
        print(descricao)
        return render_template ("cidadeok.html")
    except:
        print('cidade não encontrada.')
        erro = "Cidade não encontrada, tente novamente"
    
    return render_template('api.html', erro=erro)
          
#-------------------------------------------------------
@app.route("/cidadeok")
def cidadeok():
    
    gpio.setup(rele,1) 

    return render_template ('cidadeok.html')
#-------------------------------------------------------
@app.route("/cidade_nao_encontrada")
def cidadenok():
    
    gpio.setup(rele,1) 

    return render_template ('cidadenok.html')
#-------------------------------------------------------
@app.route("/index")
def index():
    
    gpio.setup(rele,1) 

    return render_template ('index.html')
#-------------------------------------------------------
@app.route("/rq")
def rq():

    link = ("https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&lang=pt_br").format(cidade,token)
    requisicao = requests.get(link)
    requisicao_dic = requisicao.json()
    descricao = requisicao_dic['weather'][0]['description']
    print(descricao)
    
    gpio.setup(rele,1)

    global chuva
    chuva = "chuva"

    global chovendo
    if chuva in descricao: 
        chovendo = True
    else:
        chovendo = False

    return redirect("/inteligente")
#-------------------------------------------------------
@app.route("/inteligente")
def inteligente():
    global umidade 
    umidade = (int(((canal0.value - seco)/(seco - molhado)) *100 *-1))
    status = ("Verificando")
    stchuva = ("Previsão de Chuva em {}, não irrigar".format(cidade))
    
    if chovendo == False:
        stchuva = ("Sem chuva")

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
            return redirect('/verificacao')
    else:
        print (stchuva)
        stchuva = ("Chuva")
        gpio.setup(rele, 1)
        return redirect('/verificacao')

    return render_template('inteligente.html', umidade=umidade, status=status, stchuva=stchuva)
#-------------------------------------------------------
@app.route('/verificacao')
def iverificacao():
    
    gpio.setup(rele,1)
    dia= datetime.now()
    espera = timedelta (hours= + 6)
    total = (espera + dia)
    proxima_verificacao = total.strftime('%d/%m/%Y %H:%M')
    print (proxima_verificacao)
        
    return render_template('verificacao.html', proxima_verificacao=proxima_verificacao, umidade=umidade)
#-------------------------------------------------------
@app.route('/manual')
def manual():

    umidade = (int(((canal0.value - seco)/(seco - molhado)) *100 *-1))
    gpio.setup(rele,1)
    status = ("Irrigação Desligada")

    return render_template('manual.html', umidade=umidade, status=status)
#-------------------------------------------------------
@app.route('/manual/ligar')
def ligarbomba():

    umidade = (int(((canal0.value - seco)/(seco - molhado)) *100 *-1))
    status = ("Irrigando")
    gpio.setup(rele,0)

    if (umidade < 0):
        umidade = 0
    
    elif (umidade > 100):
          umidade = 100

    return render_template('manual.html', umidade=umidade, status=status)
#-------------------------------------------------------
@app.route('/manual/parar')
def desligarbomba():

    umidade = (int(((canal0.value - seco)/(seco - molhado)) *100 *-1))
    status = ("Irrigação Desligada")
    gpio.setup(rele,1) 
    
    if (umidade < 0):
        umidade = 0
    
    elif (umidade > 100):
          umidade = 100

    return render_template('manual.html', umidade=umidade, status=status)
#-------------------------------------------------------
if __name__=="__main__":

    app.run(debug=True, host='192.168.0.190')
#-------------------------------------------------------

