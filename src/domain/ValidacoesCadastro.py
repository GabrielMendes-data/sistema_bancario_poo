# src/domain/validacoes.py
from abc import ABC, abstractmethod
from datetime import date, datetime
import re
import requests
from functools import lru_cache
from typing import Optional, Union


# ---------- Interface ----------
class IValidacao(ABC):
    @abstractmethod
    def executar_validacao(self, valor) -> bool:
        """Retorna True se válido, False caso contrário."""
        pass


# ---------- CPF ----------
class ValidarCPF(IValidacao):
    def executar_validacao(self, cpf: Union[str, int]) -> bool:
        if cpf is None:
            return False
        try:
            numero = ''.join(filter(str.isdigit, str(cpf)))
        except Exception:
            return False
        if len(numero) != 11 or numero == numero[0] * 11:
            return False
        for i in range(9, 11):
            soma = sum(int(numero[num]) * ((i + 1) - num) for num in range(i))
            digito = ((soma * 10) % 11) % 10
            if digito != int(numero[i]):
                return False
        return True


# ---------- CNPJ ----------
class ValidarCNPJ(IValidacao):
    def executar_validacao(self, cnpj: Union[str, int]) -> bool:
        if cnpj is None:
            return False
        try:
            numero = ''.join(filter(str.isdigit, str(cnpj)))
        except Exception:
            return False
        if len(numero) != 14 or numero == numero[0] * 14:
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


# ---------- Data de nascimento ----------
def _calculate_age(birth_date: date, ref: date) -> int:
    """Calcula idade precisa em anos a partir de birth_date até ref."""
    years = ref.year - birth_date.year
    if (ref.month, ref.day) < (birth_date.month, birth_date.day):
        years -= 1
    return years


class ValidarDataNascimento(IValidacao):
    def executar_validacao(self, data: Union[str, date, datetime]) -> bool:
        if data is None:
            return False
        try:
            if isinstance(data, (date, datetime)):
                nascimento = data.date() if isinstance(data, datetime) else data
            else:
                # aceita 'YYYY-MM-DD' preferencialmente
                nascimento = datetime.strptime(str(data), "%Y-%m-%d").date()
            idade = _calculate_age(nascimento, date.today())
            return idade >= 16
        except Exception:
            return False


# ---------- Renda ----------
class ValidarRenda(IValidacao):
    def executar_validacao(self, renda: Union[float, int]) -> bool:
        try:
            return float(renda) >= 0
        except Exception:
            return False


# ---------- CEP via ViaCep (com cache e timeout) ----------
@lru_cache(maxsize=1024)
def _fetch_viacep_cached(cep_num: str, timeout: float = 2.0) -> Optional[dict]:
    """Busca o resultado do ViaCep e cacheia por CEP."""
    try:
        r = requests.get(f"https://viacep.com.br/ws/{cep_num}/json/", timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


class ValidarCEP(IValidacao):
    def __init__(self, use_network: bool = True):
        """
        If use_network is False, the validator will only check format (8 digits) and won't call ViaCEP.
        Useful for tests / bulk generation where network calls are undesirable.
        """
        self.use_network = use_network

    def executar_validacao(self, cep: Union[str, int]) -> bool:
        if cep is None:
            return False
        try:
            cep_num = ''.join(filter(str.isdigit, str(cep)))
        except Exception:
            return False
        if len(cep_num) != 8:
            return False
        if not self.use_network:
            # only basic format validation
            return True
        dados = _fetch_viacep_cached(cep_num)
        if not dados:
            return False
        return "erro" not in dados


# ---------- E-mail ----------
class ValidarEmail(IValidacao):
    EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def executar_validacao(self, email: Union[str, None]) -> bool:
        if email is None:
            return False
        try:
            return bool(self.EMAIL_REGEX.match(str(email)))
        except Exception:
            return False


# ---------- Telefone ----------
class ValidarTelefone(IValidacao):
    """
    Valida telefone no formato +55DD9XXXXXXXX (11 ou 12 dígitos após +):
    aceita +55DD9XXXXXXXX (13 chars) ou +55DDXXXXXXXX (12 chars) dependendo do número.
    """
    PHONE_REGEX = re.compile(r"^\+55\d{10,11}$")

    def executar_validacao(self, telefone: Union[str, int, None]) -> bool:
        if telefone is None:
            return False
        s = str(telefone).strip()
        return bool(self.PHONE_REGEX.match(s))


# ---------- Factory ----------
class FactoryValidacao:
    @staticmethod
    def criar_validacao(tipo: str, **kwargs) -> IValidacao:
        """
        cria_validacao('cep', use_network=False) -> instancia ValidarCEP com network desligada.
        """
        tipo = tipo.lower()
        tipos = {
            "cpf": ValidarCPF(),
            "cnpj": ValidarCNPJ(),
            "data_nascimento": ValidarDataNascimento(),
            "renda": ValidarRenda(),
            "cep": ValidarCEP(**kwargs),
            "email": ValidarEmail(),
            "telefone": ValidarTelefone()
        }
        if tipo not in tipos:
            raise ValueError(f"Tipo de validação não suportado: {tipo}")
        return tipos[tipo]

if __name__ == "__main__":
    teste = _fetch_viacep_cached('32341310',30)
    print(teste)