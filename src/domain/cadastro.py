class CadastroCliente:

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