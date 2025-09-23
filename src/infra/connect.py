import requests
import pandas as pd

class ViaCep:

    def __init__(self, cep: str):
        self.cep = cep

    def url_conexao(self):
        url = f"https://viacep.com.br/ws/{self.cep}/json/"
        return url
    
    #funcao para fazer a requisicao
    def request(self):
        url = self.url_conexao()
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lança um erro para códigos de status HTTP 4xx/5xx
            return response.json()
        except requests.RequestException as e:
            print(f"Erro ao fazer a requisição: {e}")
            return {"erro": str(e)}
        
    def desempacotar_json(self):
        ...

#TODO: implementar forma de desempacotamento do json

#NOTE: validado dia 22/09 e funcionando

