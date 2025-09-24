from src.domain.ValidacoesCadastro import FactoryValidacao

class CadastroCliente:
    def __init__(self, cpf_cnpj, nome_completo, data_nascimento, renda_mensal, cep, email, telefone):
        # Validações centralizadas
        if not FactoryValidacao.criar_validacao("cpf").executar_validacao(cpf_cnpj) \
           and not FactoryValidacao.criar_validacao("cnpj").executar_validacao(cpf_cnpj):
            raise ValueError("CPF/CNPJ inválido")

        if not FactoryValidacao.criar_validacao("data_nascimento").executar_validacao(data_nascimento):
            raise ValueError("Data de nascimento inválida")

        if not FactoryValidacao.criar_validacao("renda").executar_validacao(renda_mensal):
            raise ValueError("Renda inválida")

        if not FactoryValidacao.criar_validacao("cep").executar_validacao(cep):
            raise ValueError("CEP inválido")

        if not FactoryValidacao.criar_validacao("email").executar_validacao(email):
            raise ValueError("E-mail inválido")

        if not FactoryValidacao.criar_validacao("telefone").executar_validacao(telefone):
            raise ValueError("Telefone inválido")

        # Se tudo passar, atribui
        self._cpf_cnpj = cpf_cnpj
        self._nome_completo = nome_completo
        self._data_nascimento = data_nascimento
        self._renda_mensal = renda_mensal
        self._cep = cep
        self._email = email
        self._telefone = telefone