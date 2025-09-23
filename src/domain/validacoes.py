from abc import ABC, abstractmethod

class IValidacao(ABC):

    @abstractmethod
    def executar_validacao(self, cpf_cnpj: str) -> bool:
        pass


class ValidarCPF(IValidacao):

    def executar_validacao(self, cpf_cnpj: str) -> bool:
        numero = ''.join(filter(str.isdigit, cpf_cnpj))

        if len(numero) != 11:
            return False

        # Verifica se todos os dígitos são iguais (ex: 111.111.111-11)
        if numero == numero[0] * 11:
            return False

        for i in range(9, 11):
            soma = sum(int(numero[num]) * ((i+1) - num) for num in range(i))
            digito = ((soma * 10) % 11) % 10
            if digito != int(numero[i]):
                return False
        return True


class ValidarCNPJ(IValidacao):

    def executar_validacao(self, cpf_cnpj: str) -> bool:
        numero = ''.join(filter(str.isdigit, cpf_cnpj))

        if len(numero) != 14:
            return False

        # Verifica se todos os dígitos são iguais
        if numero == numero[0] * 14:
            return False

        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        pesos2 = [6] + pesos1

        for i, pesos in enumerate([pesos1, pesos2], start=12):
            soma = sum(int(numero[num]) * pesos[num] for num in range(i))
            digito = 11 - (soma % 11)
            digito = 0 if digito >= 10 else digito
            if digito != int(numero[i]):
                return False
        return True


class FactoryValidacao:

    @staticmethod
    def criar_validacao(cpf_cnpj: str) -> IValidacao:
        numero = ''.join(filter(str.isdigit, cpf_cnpj))

        if len(numero) == 11:
            return ValidarCPF()
        elif len(numero) == 14:
            return ValidarCNPJ()
        else:
            raise ValueError("CPF ou CNPJ inválido")
        
#NOTE: validado dia 22/09 e funcionando