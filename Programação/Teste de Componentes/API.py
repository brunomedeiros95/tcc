import requests

cidade = input("Informe sua cidade: ")
estado = input ("Informe seu estado: ")

r = requests.get('https://apiadvisor.climatempo.com.br/api/v1/locale/city?name={}&state={}&country=BR&token=5a73402f3418fd8495970fecf8c38cdd'.format (cidade, estado))

print(r.json())