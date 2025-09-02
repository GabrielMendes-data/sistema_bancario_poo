from utils.cpf_utils import valida_e_formata_cpf
from utils.conta_utils import Conta

class Pessoa:
    def __init__(self, nome: str, sobrenome: str, idade: int):

        self._nome = nome
        self._sobrenome = sobrenome
        self._idade = idade
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def sobrenome(self):
        return self._sobrenome
    
    @property
    def idade(self):
        return self._idade
    
class Cliente(Pessoa):
    def __init__(self, nome: str, sobrenome: str, idade :int, cpf: str):
        super().__init__(nome, sobrenome, idade)

        self._cpf = valida_e_formata_cpf(cpf,formatar=True)
        self._contas = []

    @property
    def cpf(self):
        return self._cpf
    
    @property
    def contas(self):
        return self._contas
    
    def adicionar_conta(self,conta):
        if not isinstance(conta,Conta):
            raise TypeError('Só é possível adicionar objetos do tipo conta')
        self._contas.append(conta)