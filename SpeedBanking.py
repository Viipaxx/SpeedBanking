from time import sleep
from os import system
import mysql.connector
from mysql.connector import Error

def conectar():

    try:
        global con
        con = mysql.connector.connect(host='localhost', database='speedbanking', user='root', password='')

    except Error as erro:
        print('Erro ao conectar!')

# Inicio
def inicio():

    system('cls')
    print('-' * 60)
    print(' ' * 17 + '\033[32mBEM VINDO AO SPEED BANKING\033[m')
    print('-' * 60)
    print('(1) - Abrir Conta')
    print('(2) - Acessar Conta')
    print('(3) - Sair')
    alt = int(input('Escolha uma opção: '))
    system('cls')
    if alt == 1:
        abrir_conta()
    elif alt == 2:
        acessar_conta()
    elif alt == 3:
        sair_banco()
    else:
        sem_opcao()

# Abrir conta
def abrir_conta():

    try:
        conectar()
        system('cls')
        cursor = con.cursor()
        nome = str(input('Digite o seu primeiro nome: '))
        sobrenome = str(input('Digite o seu sobrenome: '))
        senha = str(input('Digite a sua senha: '))
        confirmar_senha = str(input('Confirme a sua senha: '))
        tentativa = 0
        while confirmar_senha != senha and tentativa < 3:
            confirmar_senha = str(input('Senha incorreta! Tente novamente: '))
            tentativa += 1
            if tentativa == 3:
                print('\n\033[31mErro! Muitas tentativas, tente mais tarde!\033[m')
                input("Aperte 'Enter' para sair!")
                inicio()
            else:
                continue

        cod_trans = input('Digite o seu código de transação: (5 dígitos) ')
        while len(cod_trans) != 5:
            cod_trans = input('5 dígitos: ')
        cod = 'SELECT * FROM dados'
        cursor.execute(cod)
        linhas = cursor.fetchall()

        for linha in linhas:
            while cod_trans == linha[4]:
                cod_trans = str(input('Código já usado, escolha outro! '))


        print('\033[32mConta criada com sucesso!\033[m')
        abrir_conta = "INSERT INTO dados VALUES (default, '" + nome + "', '" + sobrenome + "', '" + senha + "', '" + cod_trans + "', default, default, default);"
        cursor.execute(abrir_conta)
        con.commit()

        num_conta = 'SELECT * FROM dados'
        cursor.execute(num_conta)
        contas = cursor.fetchall()

        for conta in contas:
            if conta[4] == cod_trans:
                print('O número da sua conta é:', conta[0])

    except Error as e:
        print('Erro!', e)

    finally:
        if (con.is_connected()):
            cursor.close()
            con.close()
    input("Aperte 'Enter' para prosseguir!")
    inicio()

# Acessar conta
def acessar_conta():

    try:
        conectar()
        cursor = con.cursor()

        login_acesso = int(input('Insira seu número da conta: '))

        consulta = 'SELECT * FROM dados'
        cursor.execute(consulta)
        linhas = cursor.fetchall()

        for linha in linhas:
            if login_acesso == linha[0]:
                system('cls')
                senha = str(input(f'Bem-vindo Sr(a).{linha[1]} \nInsira a sua senha: '))
                if senha == linha[3]:
                    conta_acessada(login_acesso)
                else:
                    tentativa = 0
                    while senha != linha[3] and tentativa < 3:
                        senha = str(input('Senha incorreta \nDigite sua senha: '))
                        tentativa += 1
                    if tentativa == 3:
                        inicio()
                    else:
                        conta_acessada(login_acesso)

        print('Número incorreto!')
        acessar_conta()

    except Error as e:
        print('Erro!', e)

    finally:
        if (con.is_connected()):
            cursor.close()
            con.close()

# Dentro da conta
def conta_acessada(id):

    try:
        conectar()
        system('cls')
        num_conta = str(id)
        cursor = con.cursor()
        conta = 'SELECT * FROM dados WHERE num_conta = ' + num_conta
        cursor.execute(conta)
        linhas = cursor.fetchone()
        print('-' * 50)
        print(' ' * 10 + f'\033[32mBem Vindo a Sua Conta Sr(a).{linhas[1]}\033[m')
        print(' ' * 10 + f'\033[97mSeu saldo atual: R$ {linhas[5]:.2f}\033[m')
        print('-' * 50)
        print('(1) - Sacar')
        print('(2) - Depositar')
        print('(3) - Empréstimo')
        print('(4) - Transferir')
        print('(5) - Fechar Conta')
        print('(6) - Voltar')
        alt1 = int(input('Escolha uma opção: '))
        system('cls')
        if alt1 == 1:
            sacar(id)
        elif alt1 == 2:
            depositar(id)
        elif alt1 == 3:
            emprestimo(id)
        elif alt1 == 4:
            transferencia(id)
        elif alt1 == 5:
            fechar_conta(id)
        elif alt1 == 6:
            voltar()
        else:
            conta_acessada()

    except Error as e:
        print('Erro!', e)

    finally:
        if(con.is_connected()):
            cursor.close()
            con.close()

# Sacar
def sacar(id):

    try:
        conectar()
        system('cls')
        cursor = con.cursor()
        num_conta = str(id)
        saldo = 'SELECT * FROM dados WHERE num_conta = ' + num_conta
        cursor.execute(saldo)
        linhas = cursor.fetchone()

        print(f'O seu saldo é de R$ {linhas[5]}')
        sacar = float(input('Quanto deseja sacar: R$ '))
        saldo_atual = float(linhas[5])

        if saldo_atual < sacar:
            print('Erro! Valor de saque indisponível!')
            input("Aperte 'Enter' para prosseguir!")
            conta_acessada(id)
        else:
            print(f'Você acabou de sacar R$ {sacar}')
            saldo_atual = saldo_atual - sacar
            print(f'Você ficou com um saldo de R$ {saldo_atual}')

            atualizacao = f'UPDATE dados SET saldo = {saldo_atual} WHERE num_conta = {num_conta}'
            cursor.execute(atualizacao)
            con.commit()

            input("Aperte 'Enter' para prosseguir!")
            conta_acessada(id)

    except Error as e:
        print('Erro ao sacar!', e)

    finally:
        if (con.is_connected()):
            cursor.close()
            con.close()

# Depositar
def depositar(id):

    try:
        conectar()
        system('cls')
        cursor = con.cursor()
        num_conta = str(id)
        consulta = f'SELECT * FROM dados WHERE num_conta = {num_conta}'
        cursor.execute(consulta)
        linhas = cursor.fetchone()

        print(f'O seu saldo é de R$ {linhas[5]}')
        deposito = float(input('Digite o valor que você quer depositar: R$ '))
        while deposito < 0:
            deposito = float(input('Digite um valor acima de 0: R$ '))

        saldo = float(linhas[5])
        saldo_atual = saldo + deposito
        atualizacao = f'UPDATE dados SET saldo = {saldo_atual} WHERE num_conta = {num_conta}'
        cursor.execute(atualizacao)
        print(f'\nVocê acabou de fazer um depósito de R$ {deposito} \nSeu saldo atual é de R$ {saldo_atual}')
        con.commit()

        input("Aperte 'Enter' para prosseguir!")
        conta_acessada(id)

    except Error as e:
        print('Erro ao depositar!', e)

    finally:
        if (con.is_connected()):
            cursor.close()
            con.close()

# Empréstimo
def emprestimo(id):

    print('Opção disponível em breve!')
    input('Aperte "Enter" para voltar!')
    system('cls')
    conta_acessada(id)

# Transferência
def transferencia(id):

    try:
        conectar()
        system('cls')
        cursor = con.cursor()
        num_conta = str(id)

        consulta = f'SELECT * FROM dados WHERE num_conta = {num_conta}'
        
        cursor.execute(consulta)
        
        linhas = cursor.fetchone()
        
        print(f'O seu saldo atual é de R$ {linhas[5]}')

        trans = str(input('Digite o código de transferência do usuário: '))
        
        while trans == linhas[4]:
        
            trans = str(input('Você não pode transferir para você mesmo! Digite outro código: '))

        consulta = f'SELECT * FROM dados WHERE cod_trans = {trans}'
        
        system('cls')
        cursor.execute(consulta)

        linhas = cursor.fetchone()
        print(f'Tranferência para Sr(a).{linhas[1]}')
        transacao = float(input('Digite o valor que deseja transferir: R$ '))
        consulta_saldo = f'SELECT * FROM dados WHERE num_conta = {num_conta}'
        cursor.execute(consulta_saldo)
        conta = cursor.fetchone()
        if conta[5] >= transacao:
            saldo = float(linhas[5])
            novo_saldo = transacao + saldo
            saldo_atual = float(conta[5]) - transacao
            print(f'Transferência realizada com sucesso! \nSeu saldo atual é de R$ {saldo_atual}')
            atualizacao1 = f'UPDATE dados SET saldo = {novo_saldo} WHERE cod_trans = {trans}'
            cursor.execute(atualizacao1)
            con.commit()
            atualizacao2 = f'UPDATE dados SET saldo = {saldo_atual} WHERE num_conta = {num_conta}'
            cursor.execute(atualizacao2)
            con.commit()

        else:
            print('Erro! Saldo insuficiente!')
            input("Aperte 'Enter' para prosseguir!")
            conta_acessada(id)

    except Error as e:
        print('Erro ao transferir!', e)

    finally:
        if (con.is_connected()):
            cursor.close()
            con.close()
    input("Aperte 'Enter' para prosseguir!")
    conta_acessada(id)

# Fechar conta
def fechar_conta(id):

    try:
        conectar()
        system('cls')
        cursor = con.cursor()
        num_conta = str(id)
        consulta = f'SELECT * FROM dados WHERE num_conta = {num_conta}'
        cursor.execute(consulta)
        linha = cursor.fetchone()
        saldo = float(linha[5])
        if saldo > 0:
            print('A conta ainda está com dinheiro... Retire para poder fechar a conta!')
            input("Aperte 'Enter' para prosseguir!")
            conta_acessada(id)
        elif saldo < 0:
            print('A conta está com débito... Realize o pagamento para poder fechar a conta!')
            input("Aperte 'Enter' para prosseguir!")
            conta_acessada(id)
        else:
            deletar_conta = f'DELETE FROM dados WHERE num_conta = {num_conta}'
            cursor.execute(deletar_conta)
            con.commit()
            print('Conta fechada com sucesso!')
            input("Aperte 'Enter' para prosseguir!")
            inicio()

    except Error as e:
        print('Erro ao fechar a conta!', e)

    finally:
        if (con.is_connected()):
            cursor.close()
            con.close()

# Voltar
def voltar():

    for c in range(0, 1, 1):
        print('\033[36mSaindo!\033[m')
        sleep(1)
        print('\033[32m•\033[m')
        sleep(1)
        print('\033[33m••\033[m')
        sleep(1)
        print('\033[31m•••\033[m')
        sleep(1)
        input('Aperte "Enter" para sair!')
        system('cls')
        inicio()

# Sem Opção
def sem_opcao():

    print('Não temos essa opção! Tente novamente!')
    input('Aperte "Enter" para sair!')
    system('cls')
    inicio()

# Sair do Banco
def sair_banco():

        for c in range(0, 1, 1):
            print('\033[36mSaindo!\033[m')
            sleep(1)
            print('\033[32m•\033[m')
            sleep(1)
            print('\033[33m••\033[m')
            sleep(1)
            print('\033[31m•••\033[m')
            sleep(1)
            system('cls')
        print('-' * 40)
        print(' ' * 12 + '\033[32mFIM DO PROGRAMA!\033[m')
        print('-' * 40)
        input("Aperte 'Enter' para sair!")
        exit()

# Começar o programa
inicio()
