import requests
from pandas import json_normalize

class ViaCep:

    def __init__(self, cep: str):
        self.cep = cep

    def url_conexao(self):
        url = f"https://viacep.com.br/ws/{self.cep}/json/"
        return url

    def executar_conexao(self):
        url = self.url_conexao()
        try:
            data = requests.get(url)
            return data.json()  # transforma em dicionário
        except Exception:
            raise ValueError("CEP inválido")
        
    def desempacotar_json(self):
        ...
