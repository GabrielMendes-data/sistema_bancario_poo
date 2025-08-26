# 🏦 Sistema de Conta Bancária (POO em Python)

Este projeto demonstra a aplicação de **Programação Orientada a Objetos (POO)** em Python, criando uma classe `Conta` com:

- **Encapsulamento** de atributos (`cpf`, `agencia`, `conta`, `saldo`).
- **Validação de CPF** com cálculo de dígitos verificadores.
- **Propriedades (`@property`) e setters** para controle de acesso.
- **Métodos de negócio** (`depositar`, `sacar`).
- Uso de **classe abstrata** (`@abstractmethod`) para definir contratos obrigatórios.

---

## 🚀 Funcionalidades

- Criação de contas bancárias com CPF validado.
- Consulta de atributos (CPF, agência, número da conta, saldo).
- Depósitos com validação de valores.
- Método abstrato `sacar`, a ser implementado por subclasses (ex.: `ContaCorrente`, `ContaPoupanca`).
