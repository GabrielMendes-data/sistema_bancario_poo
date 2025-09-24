from datetime import date, datetime
from math import isclose

def add_months(orig_date: date, months: int) -> date:
    """Adiciona 'months' meses a orig_date tratando fim de mês."""
    year = orig_date.year + (orig_date.month - 1 + months) // 12
    month = (orig_date.month - 1 + months) % 12 + 1
    # dias por mês (considera ano bissexto)
    mdays = [31,
             29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28,
             31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day = min(orig_date.day, mdays[month - 1])
    return date(year, month, day)

class Emprestimo:
    """
    Empréstimo com tabela PRICE, registro de pagamentos e integração com contas.
    A taxa_juros é por período (ex.: mensal). taxa_juros pode ser 0.0.
    """
    def __init__(self, cliente, valor: float, taxa_juros: float, parcelas: int, data_contratacao: date = None):
        if valor <= 0:
            raise ValueError("Valor do empréstimo deve ser positivo.")
        if taxa_juros is None or taxa_juros < 0:
            raise ValueError("Taxa de juros deve ser >= 0.")
        if parcelas <= 0:
            raise ValueError("Número de parcelas deve ser positivo.")

        self.cliente = cliente
        self.valor = float(valor)
        self.taxa_juros = float(taxa_juros)
        self.parcelas = int(parcelas)
        self.data_contratacao = data_contratacao or date.today()
        self.parcelas_pagas = 0
        self.status = "ativo"          # ativo | quitado | atrasado
        self.desembolsado = False
        self.pagamentos = []          # lista de dicts: {"data": date, "valor": float, "parcela": int}
        # gerar tabela de amortização no construtor
        self.tabela = self._gerar_tabela_amortizacao()

    def calcular_valor_parcela(self) -> float:
        """Retorna o valor fixo da parcela (PMT). Se taxa==0, parcela = valor / n"""
        i = self.taxa_juros
        n = self.parcelas
        if isclose(i, 0.0):
            pmt = self.valor / n
        else:
            pmt = self.valor * (i * (1 + i) ** n) / ((1 + i) ** n - 1)
        return round(pmt, 2)

    def _gerar_tabela_amortizacao(self):
        pmt = self.calcular_valor_parcela()
        saldo = self.valor
        tabela = []
        for k in range(1, self.parcelas + 1):
            juros = round(saldo * self.taxa_juros, 2)
            amortizacao = round(pmt - juros, 2)
            # corrige última parcela para ajustar arredondamentos
            if k == self.parcelas:
                amortizacao = round(saldo, 2)
                parcela_total = round(amortizacao + juros, 2)
            else:
                parcela_total = pmt
            vencimento = add_months(self.data_contratacao, k)
            saldo_apos = round(saldo - amortizacao, 2)
            tabela.append({
                "parcela": k,
                "vencimento": vencimento,
                "juros": juros,
                "amortizacao": amortizacao,
                "parcela_total": parcela_total,
                "saldo_devedor_apos": saldo_apos
            })
            saldo = saldo_apos
        return tabela

    def desembolsar(self, conta):
        """Desembolsa o principal para a conta informada. Só uma vez."""
        if self.desembolsado:
            raise ValueError("Empréstimo já desembolsado.")
        # usa método depositar da Conta (assume assinatura depositar(valor, descricao=...))
        conta.depositar(self.valor, descricao="Desembolso empréstimo")
        self.desembolsado = True

    def pagar_parcela(self, data_pagamento: date = None, valor: float = None):
        """
        Registra um pagamento (sem movimentação em conta). Útil para testes ou pagamentos externos.
        Se 'valor' for None, usa o valor da parcela prevista.
        """
        if self.status != "ativo":
            raise ValueError("Empréstimo não está ativo.")
        data_pagamento = data_pagamento or date.today()
        parcela_no = self.parcelas_pagas + 1
        pmt = self.calcular_valor_parcela()
        valor_recebido = float(valor) if valor is not None else pmt
        self.pagamentos.append({"data": data_pagamento, "valor": round(valor_recebido, 2), "parcela": parcela_no})
        self.parcelas_pagas += 1
        if self.parcelas_pagas >= self.parcelas:
            self.status = "quitado"

    def pagar_parcela_via_conta(self, conta, data_pagamento: date = None):
        """
        Tenta debitar a parcela do cliente a partir da conta informada e registra o pagamento.
        Conta deve implementar sacar(valor, descricao=...).
        """
        if not self.desembolsado:
            raise ValueError("Empréstimo não desembolsado — nada a pagar da conta.")
        if self.status != "ativo":
            raise ValueError("Empréstimo não está ativo.")
        pmt = self.calcular_valor_parcela()
        # tenta sacar na conta; pode lançar ValueError se saldo insuficiente
        conta.sacar(pmt, descricao=f"Pagamento parcela empréstimo {getattr(self.cliente, '_cpf_cnpj', '')}")
        # registra pagamento
        self.pagar_parcela(data_pagamento=data_pagamento, valor=pmt)

    def verificar_atraso(self, data_referencia: date = None):
        """
        Verifica se já deveriam ter sido pagas x parcelas até data_referencia.
        Considera dia do mês da contratação: se dia de referência < dia de contratação, conta um mês a menos.
        """
        data_referencia = data_referencia or date.today()
        meses_passados = (data_referencia.year - self.data_contratacao.year) * 12 + (data_referencia.month - self.data_contratacao.month)
        if data_referencia.day < self.data_contratacao.day:
            meses_passados -= 1
        # número de parcelas que deveriam ter sido pagas até agora:
        parcelas_devidas = max(0, min(self.parcelas, meses_passados))
        if self.parcelas_pagas < parcelas_devidas and self.status == "ativo":
            self.status = "atrasado"
        return self.status

    def saldo_devedor_atual(self) -> float:
        """Calcula saldo devedor atual com base em tabela e parcelas pagas (apenas aproximação pela tabela)."""
        if self.parcelas_pagas >= self.parcelas:
            return 0.0
        # se tabela foi gerada, pega saldo_devedor_apos da parcela paga mais recente
        if self.parcelas_pagas == 0:
            # saldo inicial
            return round(self.valor, 2)
        else:
            idx = min(self.parcelas_pagas, len(self.tabela)) - 1
            return round(self.tabela[idx]["saldo_devedor_apos"], 2)

    def __repr__(self):
        return f"<Empréstimo R${self.valor:.2f} parcelas={self.parcelas} juros={self.taxa_juros*100:.2f}% status={self.status}>"
    
#TODO: deixar mais simples
