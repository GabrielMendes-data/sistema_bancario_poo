from abc import ABC, abstractmethod
from datetime import datetime


class Transacao:
    def __init__(self, tipo: str, valor: float, descricao: str = ""):
        self.tipo = tipo
        self.valor = valor
        self.data = datetime.now()
        self.descricao = descricao

    def __repr__(self):
        return f"{self.data:%d/%m/%Y %H:%M} - {self.tipo}: R$ {self.valor:.2f} ({self.descricao})"


class Conta(ABC):
    def __init__(self, cpf_cnpj: str, agencia: str, numero: str, saldo: float = 0.0, limite: float = 0.0):
        self._cpf_cnpj = cpf_cnpj
        self._agencia = agencia
        self._numero = numero
        self._saldo = saldo
        self._limite = limite
        self.transacoes = []

    @property
    def saldo(self):
        return self._saldo

    @property
    def limite(self):
        return self._limite

    def depositar(self, valor: float, descricao: str = "Depósito"):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("Depósito inválido.")
        self._saldo += valor
        self.transacoes.append(Transacao("depósito", valor, descricao))

    @abstractmethod
    def sacar(self, valor: float, descricao: str = "Saque"):
        pass

    @abstractmethod
    def transferir(self, destino, valor: float, descricao: str = "Transferência"):
        pass

    def extrato(self):
        return [repr(t) for t in self.transacoes]


class ContaCorrente(Conta):
    def sacar(self, valor: float, descricao: str = "Saque CC"):
        if valor <= 0:
            raise ValueError("Valor de saque inválido.")
        if valor > self._saldo + self._limite:
            raise ValueError("Saldo insuficiente.")
        self._saldo -= valor
        self.transacoes.append(Transacao("saque", -valor, descricao))

    def transferir(self, destino, valor: float, descricao: str = "Transferência CC"):
        if valor <= 0:
            raise ValueError("Valor de transferência inválido.")
        if valor > self._saldo + self._limite:
            raise ValueError("Saldo insuficiente para transferência.")
        self._saldo -= valor
        destino._saldo += valor
        self.transacoes.append(Transacao("transferência", -valor, descricao))
        destino.transacoes.append(Transacao("transferência", valor, f"De {self._numero}"))


class ContaPoupanca(Conta):
    def sacar(self, valor: float, descricao: str = "Saque Poupança"):
        if valor <= 0:
            raise ValueError("Valor de saque inválido.")
        if valor > self._saldo:
            raise ValueError("Saldo insuficiente (poupança não tem limite).")
        self._saldo -= valor
        self.transacoes.append(Transacao("saque", -valor, descricao))

    def transferir(self, destino, valor: float, descricao: str = "Transferência Poupança"):
        if valor <= 0:
            raise ValueError("Valor de transferência inválido.")
        if valor > self._saldo:
            raise ValueError("Saldo insuficiente para transferência (poupança não tem limite).")
        self._saldo -= valor
        destino._saldo += valor
        self.transacoes.append(Transacao("transferência", -valor, descricao))
        destino.transacoes.append(Transacao("transferência", valor, f"De {self._numero}"))

    def aplicar_juros(self, taxa: float):
        """Aplica rendimento sobre o saldo"""
        if taxa <= 0:
            raise ValueError("Taxa deve ser positiva")
        rendimento = self._saldo * taxa
        self._saldo += rendimento
        self.transacoes.append(Transacao("rendimento", rendimento, f"Juros {taxa*100:.2f}%"))
