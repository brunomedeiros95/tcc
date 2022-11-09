import requests

token = ("ecceaa6b7d3bbf475f371f4b4dc64d03")
cidade = ("carvão")

link = ("https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&lang=pt_br").format(cidade,token)

requisicao = requests.get(link)
requisicao_dic = requisicao.json()

descricao = requisicao_dic['weather'][0]['description']
print(descricao)

chuva = "chuva"

if chuva not in descricao:
    print("Ta tranquilo rapaziada!")
else:
    print("Ta chovendo rapaziada!")
