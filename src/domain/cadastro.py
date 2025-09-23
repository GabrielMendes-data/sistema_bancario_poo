class CadastroCliente:

    def __init__(self, 
                 cpf_cnpj: str, 
                 nome_completo: str, 
                 data_nascimento: str,
                 renda_mensal: float,
                 cep: str,
                 email: str,
                 telefone: str):
        self._cpf_cnpj = cpf_cnpj
        self._nome_completo = nome_completo
        self._data_nascimento = data_nascimento
        self._renda_mensal = renda_mensal
        self._cep = cep
        self._email = email
        self._telefone = telefone

    @property
    def cpf_cnpj(self):
        return self._cpf_cnpj
    
    @property
    def nome_completo(self):
        return self._nome_completo  
    
    @property
    def data_nascimento(self):
        return self._data_nascimento  
    
    @property
    def renda_mensal(self):
        return self._renda_mensal  
    
    @property
    def cep(self):
        return self._cep  
    
    @property
    def email(self):
        return self._email  
    
    @property
    def telefone(self):
        return self._telefone  
    
    @nome_completo.setter
    def nome_completo(self, novo_nome: str):
        self._nome_completo = novo_nome

    @renda_mensal.setter
    def renda_mensal(self, nova_renda: float):
        self._renda_mensal = nova_renda

    @cep.setter
    def cep(self, novo_cep: str):
        self._cep = novo_cep

    @email.setter
    def email(self, novo_email: str):
        self._email = novo_email

    @telefone.setter
    def telefone(self, novo_telefone: str):
        self._telefone = novo_telefone

    

    cpf,cnpj
    nome
    data_nascimento
    data_abertura_conta
    renda_mensal
    cep
    email
    telefone

    Validações:

CPF/CNPJ válidos (dígitos verificadores, formato).

Data de nascimento compatível com maioridade (≥ 16 anos).

Data de abertura da conta ≤ hoje.

Renda_mensal ≥ 0.

CEP validado via API dos Correios ou IBGE → enriquecido com cidade, estado, região.

E-mail em formato válido e único.

Telefone válido no padrão internacional (+55 para Brasil).