def so_digitos(cpf: str) -> str:
    # remove ., - e espaços, deixa só dígitos
    return "".join(ch for ch in str(cpf) if ch.isdigit())

def calcula_digito(cpf_parcial: str) -> int:
    # seu algoritmo: pesos decrescentes (len+1 ... 2)
    soma = 0
    for dig, peso in zip(cpf_parcial, range(len(cpf_parcial)+1, 1, -1)):
        soma += int(dig) * peso
    d = 11 - (soma % 11)
    return 0 if d > 9 else d

def valida_e_formata_cpf(cpf: str, formatar: bool = True) -> str:
    """
    - normaliza
    - rejeita tamanho != 11
    - rejeita todos dígitos iguais
    - confere dígitos verificadores
    - retorna formatado ou só dígitos
    """
    num = so_digitos(cpf)
    if len(num) != 11:
        raise ValueError("CPF inválido: precisa ter 11 dígitos")

    if num == num[0] * 11:
        raise ValueError("CPF inválido: todos os dígitos iguais")

    d1 = calcula_digito(num[:9])
    d2 = calcula_digito(num[:9] + str(d1))
    if num != (num[:9] + str(d1) + str(d2)):
        raise ValueError("CPF inválido: dígitos verificadores não conferem")

    if not formatar:
        return num

    return f"{num[:3]}.{num[3:6]}.{num[6:9]}-{num[9:]}"
