from abc import ABC, abstractmethod

class Conta(ABC):
    def __init__(self, agencia: str, numero: str, saldo=0):
        self._agencia = agencia
        self._numero = numero
        self._saldo = saldo

    @property
    def agencia(self):
        return self._agencia

    @property
    def numero(self):
        return self._numero

    @property
    def saldo(self):
        return self._saldo

    def depositar(self, valor: float):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("Depósito inválido.")
        self._saldo += valor

    @abstractmethod
    def sacar(self, valor: float):
        pass

class ContaCorrente(Conta):
    def __init__(self, agencia, numero, saldo=0, limite=0):
        super().__init__(agencia, numero, saldo)
        self._limite = limite

    @property
    def limite(self):
        return self._limite
    
    def sacar(self, valor:float):
        if not isinstance(valor,(int,float)) or valor <=0:
            raise ValueError('O valor precisa ser um número e maior que 0')
        
        if valor > self.saldo + self.limite:
            raise ValueError ('Saldo insuficiente')
        
        self._saldo -= valor

class ContaPoupanca(Conta):
    def __init__(self, agencia, numero, saldo=0):
        super().__init__(agencia, numero, saldo)
    
    def sacar(self, valor:float):
        if not isinstance(valor,(int,float)):
            raise ValueError('O valor precisa ser um número')
        
        if valor > self.saldo:
            raise ValueError ('Saldo insuficiente')
        
        self._saldo -= valor
