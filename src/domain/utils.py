class ValidarDocumento:
    def __init__(self, cpf_cnpj: str):
        # remove caracteres não numéricos
        self.numero = ''.join(filter(str.isdigit, cpf_cnpj))

    def _validar_cpf(self):
        # regra simplificada para explicar a ideia:
        # - não pode ter todos os dígitos iguais
        if self.numero == self.numero[0] * 11:
            return False

        # cálculo dos 2 dígitos verificadores
        for i in range(9, 11):
            soma = sum(int(self.numero[num]) * ((i+1) - num) for num in range(i))
            digito = ((soma * 10) % 11) % 10
            if digito != int(self.numero[i]):
                return False
        return True

    def _validar_cnpj(self):
        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        pesos2 = [6] + pesos1

        for i, pesos in enumerate([pesos1, pesos2], start=12):
            soma = sum(int(self.numero[num]) * pesos[num] for num in range(i))
            digito = 11 - (soma % 11)
            digito = 0 if digito >= 10 else digito
            if digito != int(self.numero[i]):
                return False
        return True

    def executar_validacao(self):
        if len(self.numero) == 11:
            return self._validar_cpf()
        elif len(self.numero) == 14:
            return self._validar_cnpj()
        else:
            raise ValueError("CPF/CNPJ inválido")


