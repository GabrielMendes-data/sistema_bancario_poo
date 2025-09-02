# 🏦 Sistema Bancário em Python (POO)

Este projeto implementa um sistema bancário simples utilizando **Programação Orientada a Objetos (POO)** em Python.

## 📚 Estrutura de Classes

- **Pessoa**: representa uma pessoa com nome, sobrenome e idade.
- **Cliente**: herda de Pessoa, possui CPF validado e pode ter várias contas.
- **Conta (abstrata)**: possui agência, número e saldo.
  - **ContaCorrente**: herda de Conta, possui limite de crédito.
  - **ContaPoupanca**: herda de Conta.
- **Banco**: gerencia clientes, contas e agências, além de autenticar operações.

## 🚀 Funcionalidades

- Cadastro de clientes com validação de CPF.
- Criação de contas correntes e poupança.
- Depósitos e saques com autenticação.
- Validação de agência, cliente e conta antes das operações.

## 🛠️ Como Executar

1. Instale o Python 3.11 ou superior.
2. Execute o arquivo principal:

   ```sh
   python src/main.py
   ```

3. O sistema irá criar um banco, cadastrar um cliente, abrir uma conta corrente e realizar operações de depósito e saque.

## 📁 Estrutura de Pastas

```
src/
  main.py
  utils/
    banco_utils.py
    cliente_utils.py
    conta_utils.py
    cpf_utils.py
```

## 📌 Observações

- O CPF é validado conforme regras oficiais.
- O sistema utiliza encapsulamento e propriedades.
- Métodos abstratos garantem implementação específica para cada tipo de conta.
