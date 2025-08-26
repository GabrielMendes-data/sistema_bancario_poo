from abc import ABC, abstractmethod

def _calcula_digito(cpf_parcial: str) -> int:
    soma = 0
    for dig, peso in zip(cpf_parcial, range(len(cpf_parcial) + 1, 1, -1)):
        soma += int(dig) * peso
    d = 11 - (soma % 11)
    return 0 if d > 9 else d

def _so_digitos(cpf: str) -> str:
    return "".join(ch for ch in cpf if ch.isdigit())

def _valida_e_formata_cpf(cpf: str) -> str:
    # limpa e normaliza
    somente = _so_digitos(cpf)
    if not somente:
        raise ValueError("CPF inválido: vazio ou sem dígitos.")

    if len(somente) > 11:
        raise ValueError("CPF inválido: mais de 11 dígitos.")

    # mantém sua regra de preencher zeros à esquerda (igual ao seu código)
    cpf11 = f"{int(somente):011d}"

    # rejeita CPFs com todos os dígitos iguais (000..., 111..., etc.)
    if cpf11 == cpf11[0] * 11:
        raise ValueError("CPF inválido: todos os dígitos iguais.")

    # calcula DV
    d1 = _calcula_digito(cpf11[:9])
    d2 = _calcula_digito(cpf11[:9] + str(d1))
    if cpf11 != cpf11[:9] + str(d1) + str(d2):
        raise ValueError("CPF inválido: dígitos verificadores não conferem.")

    # retorna formatado
    return f"{cpf11[:3]}.{cpf11[3:6]}.{cpf11[6:9]}-{cpf11[9:]}"

class Conta:
    def __init__(self,cpf,agencia,conta,saldo):
        self._cpf = _valida_e_formata_cpf(cpf)
        self._agencia = agencia
        self._conta = conta
        self._saldo = saldo
        
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def conta(self):
        return self._conta
    
    @property
    def saldo(self):
        return self._saldo
    
    @saldo.setter
    def saldo(self,valor):
        if not isinstance(valor,(int,float)):
            raise ValueError('Precisa ser um número')
        self._saldo = valor

    def depositar(self,valor):
        if not isinstance(valor,(int,float)):
            raise ValueError('Precisa ser um número')
        
        self._saldo += valor
        self.detalhes()

    def detalhes(self):
        print(f'Agência: {self.agencia}', end=' ')
        print(f'Conta: {self.conta}', end=' ')
        print(f'Saldo: {self.saldo}')

    @abstractmethod # -> pode variar a utilização de acordo com outro objeto
    def sacar(self,valor):
        pass