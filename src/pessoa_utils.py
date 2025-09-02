from cpf_utils import valida_e_formata_cpf

class Pessoa:
    def __init__(self, nome: str, sobrenome: str, idade: int):

        #utilizar encapsulamento para guardar informações com '_'
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

    @property
    def cpf(self):
        return self._cpf