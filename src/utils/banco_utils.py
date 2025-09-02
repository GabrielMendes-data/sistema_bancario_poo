class Banco:
    def __init__(self, nome:str):
        self._nome = nome
        self._agencias = set()
        self._clientes = {}
        self._contas = {}

    def adicionar_agencia(self, agencia: str):
        self._agencias.add(agencia)
    
    def registrar_cliente(self, cliente):

        if cliente.cpf in self._clientes:
            raise ValueError("Cliente já registrado")

        self._clientes[cliente.cpf] = cliente
    
    def adicionar_conta(self, conta, cliente):
        chave = (conta.agencia,conta.numero)

        if conta.agencia not in self._agencias:
            raise ValueError('Agência inválida')

        self._contas[chave] = conta
        cliente.adicionar_conta(conta)
    
    def autenticar(self, cpf: str, agencia: str, numero: str) -> bool:
        #verifica se cliente existe
        if cpf not in self._clientes:
            return False
        
        #Verifica se agência é válida
        if agencia not in self._agencias:
            return False
        
        #Verifica se a conta está registrada
        chave = (agencia,numero)

        if chave not in self._contas:
            return False
        
        #Verifica se a conta pertence ao cliente
        cliente = self._clientes[cpf]
        conta = self._contas[chave]

        if conta not in cliente.contas:
            return False
        
        #Todos os testes passaram
        return True
    
    def sacar(self, cpf: str, agencia: str, numero: str, valor: float):
        if not isinstance(valor,(int,float)) or valor <= 0:
            raise ValueError('Valor inválido para operação')
        
        if not self.autenticar(cpf, agencia, numero):
            raise PermissionError("Autenticação falhou. Saque não autorizado.")
        
        conta = self._contas[(agencia, numero)]
        conta.sacar(valor)  # Isso vai usar a regra da conta (corrente ou poupança)

    def depositar(self, cpf: str, agencia: str, numero: str, valor: float):
        if not isinstance(valor,(int,float)) or valor <= 0:
            raise ValueError('Valor inválido para operação')
        
        if not self.autenticar(cpf, agencia, numero):
            raise PermissionError("Autenticação falhou. Depósito não autorizado.")
        
        conta = self._contas[(agencia, numero)]
        conta.depositar(valor)
