from utils.cliente_utils import Cliente
from utils.conta_utils import ContaCorrente
from utils.banco_utils import Banco

# 1. Criar o banco
banco = Banco("Banco Python")

# 2. Adicionar agência
banco.adicionar_agencia("0001")

# 3. Criar cliente
cliente = Cliente("João", "Silva", 30, "informar_cpf")  # CPF precisa ser válido

# 4. Criar conta corrente
conta = ContaCorrente("0001", "1234", saldo=500, limite=200)

# 5. Registrar cliente e conta no banco
banco.registrar_cliente(cliente)
banco.adicionar_conta(conta, cliente)

# 6. Fazer operações
try:
    banco.depositar(cliente.cpf, "0001", "1234", 300)
    print("Depósito realizado com sucesso.")
except Exception as e:
    print("Erro ao depositar:", e)

try:
    banco.sacar(cliente.cpf, "0001", "1234", 600)
    print("Saque realizado com sucesso.")
except Exception as e:
    print("Erro ao sacar:", e)

# 7. Verificar saldo final
print(f"Saldo final: {conta.saldo}")
