def mostrar_menu():
    menu = """
    ========== MENU ==========
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [c] Cadastrar Usuário
    [k] Cadastrar Conta
    [q] Sair
    ==========================
    => """
    return input(menu)

usuarios_cadastrados = []  # Lista para armazenar os usuários cadastrados

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

def cadastrar_usuario():
    global usuarios_cadastrados
    nome = input("Informe seu nome: ")
    cpf = input("Informe somente os números do CPF: ")
    while len(cpf) != 11:
    #verifica se tem 11 números no cpf
        print("CPF inválido. O CPF deve conter 11 dígitos.")
        cpf = input("Informe somente os números do CPF: ")
    
    # Verifica se o CPF já está cadastrado
    for usuario in usuarios_cadastrados:
        if usuario['cpf'] == cpf:
            print("Usuário com este CPF já cadastrado.")
            return False  # Encerra a função sem cadastrar o usuário
    
    endereco = input("Informe seu endereço (Logradouro, número - bairro - cidade/sigla do estado): ")
    while not validar_endereco(endereco):
        print("Formato de endereço inválido. Por favor, siga o formato: Logradouro, número - bairro - cidade/sigla do estado")
        endereco = input("Informe seu endereço (Logradouro, número - bairro - cidade/sigla do estado): ")

    data_nascimento = input("Informe sua data de nascimento, A data deve seguir o formato dd/mm/aaaa.")
    # Verifica se a data de nascimento está no formato correto dd/mm/aaaa
    while len(data_nascimento) != 8 or data_nascimento[2] != '/' or data_nascimento[5] != '/':
        print("Data de nascimento inválida. A data deve seguir o formato dd/mm/aaaa.")
        data_nascimento = input("Informe sua data de nascimento: ")


    telefone = input("Informe seu telefone. Deve estar no formato (DDD) números: ")
    while len(telefone) < 11 or telefone[0] != '(' or telefone[3] != ')' or not telefone[4:].isnumeric():
        print("Telefone inválido. O telefone deve estar no formato (DDD) números.")
        telefone = input("Informe seu telefone: ")

    
    # dicionário com as informações do usuário e adiciona à lista de cadastrados
    usuario = {
        'nome': nome,
        'cpf': cpf,
        'endereco': endereco,
        'data_nascimento': data_nascimento,
        'telefone': telefone
    }
    usuarios_cadastrados.append(usuario)
    return True  

contas_cadastradas = []  # Lista global para armazenar as contas

def cadastrar_conta(cpf):
    for usuario in usuarios_cadastrados:
        if cpf not in usuario['cpf']:
            print("Usuário não cadastrado. Por favor, realize o cadastro antes de criar uma conta.")
            return None
    global contas_cadastradas
    agencia = "001"
    # O número da conta é o tamanho atual da lista + 1, garantindo sequencialidade
    numero = str(len(contas_cadastradas) + 1)
    conta = {
        'agencia': agencia,
        'numero': numero,
        'usuario': cpf
    }
    contas_cadastradas.append(conta)
    print(f"Conta cadastrada com sucesso! Número da conta: {numero}, Agência: {agencia}, Usuário: {cpf}")
    return conta


def depositar(saldo, extrato):
    cpf = input("Informe o CPF do usuário: ")
    for usuario in usuarios_cadastrados:
        if cpf not in usuario['cpf']:
            print("Usuário não cadastrado. Por favor, realize o cadastro antes de tentar.")
            return None
    c = input("Informe o número da conta: ")
    for conta in contas_cadastradas:
        if conta not in c['numero']:
            print("Conta não cadastrada. Por favor, realize o cadastro antes de tentar.")
            return None

    valor = float(input("Informe o valor do depósito: "))
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(saldo, extrato, numero_saques, LIMITE_SAQUES, limite):
    valor = float(input("Informe o valor do saque: "))
    
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3

    while True:
        opcao = mostrar_menu()
        if opcao == "d":
            saldo, extrato = depositar(saldo, extrato)
        elif opcao == "s":
            saldo, extrato, numero_saques = sacar(saldo, extrato, numero_saques, LIMITE_SAQUES, limite)
        elif opcao == "e":
            exibir_extrato(saldo, extrato)
        elif opcao == "q":
            print("Obrigado, Volte sempre!")
            break
        elif opcao == "c":
           c = cadastrar_usuario()
           if c: 
                print("Usuário cadastrado com sucesso!")
        elif opcao == "k":
            cpf = input("Informe o CPF do usuário: ")
            conta = cadastrar_conta(cpf)
            for usuario in usuarios_cadastrados:
                if usuario['cpf'] == cpf:
                    usuario['conta'] = conta
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
