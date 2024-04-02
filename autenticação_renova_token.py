import requests
import json
import schedule
import time
from colorama import Fore, Style, init

init()

with open('config.json', 'r') as file:
    config_data = json.load(file)

def autenticar(codigoAcesso, codigoUg):
    url = config_data['urlBase'] + '/autenticacao/login'
    headers = {
        'codigoAcesso': codigoAcesso,
        'senha': '123456'
    }
    params = {
        'codigoUg': codigoUg,
        'descricaoEmpresaTI': 'teste',
        'descritivoSoftware': 'teste'
    }

    try:
        response = requests.post(url, headers=headers, params=params)
        response.raise_for_status()

        token = response.json()['chave']
        print(Fore.GREEN + "Login realizado com sucesso!")
        config_data['codigoAcesso'] = codigoAcesso
        config_data['codigoUg'] = codigoUg

        msg = "Autenticação realizada com sucesso"
        #montarLogEnvioRemessa(msg, "")
        return token
    except requests.exceptions.RequestException as e:
        try:
            msg = "Erro ao autenticar: "
            #montarLogEnvioRemessa(msg, e.response.json())
            return
        except json.JSONDecodeError:
            msg = "Erro ao autenticar: "
            #montarLogEnvioRemessa(msg, e)
            return
Style.RESET_ALL
codigoAcesso = input('Código acesso: ')
codigoUg = input('Código UG: ')
token = autenticar(codigoAcesso, codigoUg)
config_data['headers']['AUTH_TOKEN'] = token

with open('config.json', 'w') as file:
    json.dump(config_data, file)
            
def obter_novo_token():
    global config_data
    codigoAcesso = config_data['codigoAcesso']
    codigoUg = config_data['codigoUg']
    token = autenticar(codigoAcesso, codigoUg)
    config_data['headers']['AUTH_TOKEN'] = token
    with open('config.json', 'w') as file:
        json.dump(config_data, file)

def main():
    global config_data
    with open('config.json', 'r') as file:
        config_data = json.load(file)

    # Agendar a obtenção de novo token a cada 5 horas
    schedule.every(5).hours.do(obter_novo_token)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()