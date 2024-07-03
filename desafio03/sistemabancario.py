from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
import textwrap


class Cliente():
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def add_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class PessoaJuridica(Cliente):
    def __init__(self, nome, cnpj):
        self.nome = nome
        self.cnpj = cnpj

class Conta():
    def __init__(self, numero, cliente):
        self.agencia = "0001"
        self.numero = numero
        self.saldo = 0
        self.cliente = cliente
        self.historico = Historico()
    
    @classmethod
    def criar_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia

    @property   
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        if excedeu_saldo:
            print("Saldo insuficiente!")

        elif valor > 0:
            self.saldo -= valor
            print("Saque realizado com sucesso!")
            return True
        else:
            print("Valor inválido!")

        return False
    
    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print("Depósito realizado com sucesso!")
        else:
            print("Valor inválido!")
            return False
        return True
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=1000, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque".__name__]
        )
        excedeu_limite = numero_saques >= self.limite
        excedeu_saques = numero_saques >= self.saques

        if excedeu_limite:
            print("Limite de saques excedido!")
        
        elif excedeu_saques:
            print("Limite de saques diários excedido!")
        
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
              Agência:\t{self.agencia}
              Conta Corrente:\t\t{self.numero}
              Titular:\t{self.cliente.nome}
            """
    
#interface transacao
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.add_transacao(self)

class Saque(Transacao):    
    def __init__(self, valor):
        self.valor = valor
    
    @property
    def valor(self):
        return self._valor
    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.add_trasacao(self)

class Historico:
    def __init__(self):
        self.transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def add_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%s")
            }
        )

def menu():
    
    menu = """\n 
    ====== Bem-vindo(a) ao Banco Fast =======
    1. Depositar
    2. Sacar
    3. Extrato
    4. Nova Conta
    5. Listar Contas
    6. Novo Cliente
    7. Sair
    ->> Escolha uma opção:
    """   
    return int(input(textwrap.dedent(menu)))

def filtrar_cliente(clientes, cpf):
    clientes_existentes = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_existentes[0] if clientes_existentes else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui contas!")
        return
    
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(clientes, cpf)

    if not cliente:
        print("Cliente não encontrado!")
        return
    valor = float(input("Digite o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(clientes, cpf)

    if not cliente:
        print("Cliente não encontrado!")
        return
    valor = float(input("Digite o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def extrato(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(clientes, cpf)

    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\nExtrato da conta:")
    trasacoes = conta.historico.transacoes

    extrato = ""
    if not trasacoes:
        extrato = "Nenhuma transação realizada!"
    else:
        for transacao in trasacoes:
            extrato += f"""\
                Tipo: {transacao["tipo"]}
                Valor: R${transacao["valor"]}
                Data: {transacao["data"]}
                """
    print(extrato)
    print(f"\nSaldo atual: R${conta.saldo:.2f}")
    print("=====================================")

def listar_contas():
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def criar_conta_corrente(numero_conta, clientes, contas):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(clientes, cpf)

    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = ContaCorrente.criar_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

def validar_endereco(endereco):
    partes = endereco.split(" - ")
    if len(partes) != 3:
        return False
    logradouro_numero, bairro, cidade_estado = partes
    if ',' not in logradouro_numero or '/' not in cidade_estado:
        return False
    cidade, estado = cidade_estado.split('/')
    if len(estado.strip()) != 2:
        return False
    return True

def validar_data_nascimento(data_nascimento):
    if len(data_nascimento) != 8 or data_nascimento[2] != '/' or data_nascimento[5] != '/':
        return False
    return True

def novo_cliente(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(clientes, cpf)

    if cliente:
        print("Cliente já cadastrado!")
        return
    
    nome = input("Digite o nome do cliente: ")
    data_nascimento = input("Digite a data de nascimento do cliente: ")
    if not validar_data_nascimento(data_nascimento):
        print("Data de nascimento inválida!")
        return
    
    endereco = input("Digite o endereço do cliente:(logradouro, nro - bairro - cidade/sigla estado): ")
    if not validar_endereco(endereco):
        print("Endereço inválido!")
        return

    cliente = PessoaFisica(nome, cpf, data_nascimento)
    clientes.append(cliente)

    print("Cliente cadastrado com sucesso!")

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 1:
            depositar(clientes)
        
        elif opcao == 2:
            sacar(clientes)
        
        elif opcao == 3:
            extrato(contas)
        
        elif opcao == 4:
            numero_conta = len(contas) + 1
            criar_conta_corrente(numero_conta, clientes, contas)
        
        elif opcao == 5:
            listar_contas()
        
        elif opcao == 6:
            novo_cliente(contas)
        
        elif opcao == 7:
            print("Saindo...")
            break
        
        else:
            print("Opção inválida!")
        
main()