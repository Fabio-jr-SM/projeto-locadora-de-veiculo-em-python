import json   '''importando a biblioteca JSON pois Ele usa uma sintaxe leve e minimalista, tornando-o rápido de ser processado
 esta biblioteca nos fornece uma maneira fácil de obter informações do sistema operacional com apenas uma linha de código.'''
import os
 '''utilizado para ter uma forma rapida e simples de acessar datas dentre outros'''
import datetime


def exibir_tabela_carros(carros):
    '''Função para exibir a tabela de seleção dos veiculos'''

    print(" ".center(50), "LOCADORA DE VEÍCULOS\n")
    print("Código".ljust(14),
          "Marca".ljust(14),
          "Modelo".ljust(14),
          "Ano".ljust(14),
          "Cor".ljust(14),
          "Preço/Dia".ljust(14),
          "Disponível".ljust(14),
          "Placa")

    '''Loop para que exiba uma tabela de informação dos veiculos disponivel.'''
    for codigo, lista in carros.items():
        '''Exibe as informações do arquivo carros.Json em um formato tabelado'''
        print(f"{codigo}".ljust(14),
              f"{lista[0]}".ljust(14),
              f"{lista[1]}".ljust(14),
              f"{lista[2]}".ljust(14),
              f"{lista[3]}".ljust(14),
              f"{lista[4]}".ljust(14),
              f"{lista[5]}".ljust(14),
              f"{lista[6]:<15}")


def carregar_arquivo_carros():
    ''''''Função utilizada para abrir o arquivo Json no codigo e utilizar no corpo do codigo''''''

    with open('carros.json', 'r') as f:
        texto = f.read()
        abrir_carros = json.loads(texto)
    return abrir_carros


def carregar_arquivo_pessoas_cadastradas():
    '''Função utilizada para carregar o arquivo json de pessoas cadastradas
        para ser utilizado na devolução do carro'''

    with open('pessoas_cadastradas.json', 'r') as f:
        texto = f.read()
        pessoas_cadastradas = json.loads(texto)
    return pessoas_cadastradas  '''pessoas_cadastradas é uma lista dentro do arquivo json e
    sera usada para adicionar pessoa ao nosso "banco de dados"'''


def escrever_json_carros(carros):
    '''Função para adicionar um carro como disponivel no estoque quando ele for devolvido.
    uma outra forma de explicar é para Reescrever/atualizar o arquivo "carros.json", abrindo no modo write
    podendo escrever ou retirar informações.'''

    with open('carros.json', 'w') as f:
        '''o arquivo carros é um arquivo.json que tem uma lista dentro
        que adiciona ou remove carros do nosso banco de dados'''
        f.write(json.dumps(carros))


def escrever_json_pessoas_cadastradas(pessoas_cadastradas):
    '''Função para Reescrever/atualizar o arquivo "pessoas_cadastradas" abrindo o
    arquivo no modo "write" podendo escrever ou retirar informações.'''

    with open('pessoas_cadastradas.json', 'w') as f:
        f.write(json.dumps(pessoas_cadastradas))


def reservar_carro(carros):
    '''função para utilizar quando a pessoa for alugar que ja foi
    reservado anteriormente recebendo qual modelo de carro e
    quantos dias a pessoa vai ficar com o carro,
    reservar um carro pelo codigo.
    ou retornar ao inicio'''

    codigo = input('Qual o código do carro:')
    dias = int(input('Quantidade de dias de aluguel:'))
    OpcaoDois = input('\n(1) Confirmar contrato'
                      '\n(2) Mudar o veiculo'
                      '\n(3) Encerrar\n')

    if (OpcaoDois == '1'):
        pessoas_cadastradas = alugar_carro(carros, codigo, dias)
        return pessoas_cadastradas
    elif (OpcaoDois == '2'):
        reservar_carro(carros)
    elif (OpcaoDois == '3'):
        return None


def alugar_carro(carros, codigo, dias):
    '''esta função é utilizada para pegar as informações do pessoa e se ela for
    maior de idade iremos alugar um carro para ela, vamos perguntar qual o carro, codigo e dias ela vai pegar
    pedimos a CNH e cpf ambos sendo testada para verificar se tem mais de 11 numeros
    vemos os dias que ela vai alugar para o contrato e avisamos a multa de atraso e outras informações'''

    nome_completo = input('Nome completo: ')
    idade = int(input('Idade: '))
    if idade < 18:
        print("VOCÊ É MENOR DE IDADE!!!!!\n")
        alugar_carro(carros, codigo, dias)
    if idade < 25:
        '''faz a conta para a cobrança do cliente'''
        conta = (dias * carros[codigo][4]) + 30
    else:
        conta = dias * carros[codigo][4]

    cnh = input('CNH:')
    while len(cnh) < 11:
        print('CNH invalido!\n')
        cnh = input('CNH:')

    cpf = input('CPF:')
    while len(cpf) < 11:
        print('CPF invalido!\n')
        cpf = input('CPF:')

    now = datetime.datetime.now()
    delta = datetime.timedelta(days=dias)
    data = now + delta
    formato = '%d/%m/%Y'
    data_entrega = data.strftime(formato)
    print(''.center(25), 'CONTRATO DE LOCAÇÃO\n')
    print('{} portador do CPF {} e da CNH {} \nestá alugando o veiculo {}'.format(
        nome_completo, cpf, cnh, carros[codigo][0]))
    print('no periodo de {} dias ,que ficará no valor de R${}'.format(dias, conta))
    print('e a devolução do veiculo ficará para a data {}.\n'.format(data_entrega))
    print('-----ATENCAO: EM CASO DE ATRASO HAVERA COBRANÇA DE TAXA DE 100R$ AO DIA-----')
    print('Locação com sucesso!\n')
    print('================================================================\n\n')

    carros[codigo][5] -= 1
    escrever_json_carros(carros)

    pessoas_cadastradas = criar_escrever_arquivo_pessoas_cadastradas(
        nome_completo, idade, cpf, cnh, codigo, dias, conta, data_entrega)
    return pessoas_cadastradas


def criar_escrever_arquivo_pessoas_cadastradas(nome, idade, cpf, cnh, codigo, dias, conta, data_entrega):
    '''utilizado para verificar a pessoa e a data de entrega abrindo no modo edição e salvando'''

    pessoas_cadastradas = {}

    while True:
        if os.path.exists('pessoas_cadastradas.json'):
            with open('pessoas_cadastradas.json', 'r') as f:
                texto = f.read()
                pessoas_cadastradas = json.loads(texto)

        pessoas_cadastradas[cpf] = [nome, idade, dias,
                                    conta, codigo, cnh, conta, data_entrega]
        with open('pessoas_cadastradas.json', 'w') as f:
            f.write(json.dumps(pessoas_cadastradas))
        return pessoas_cadastradas


def devolver_carro(carros, pessoas_cadastradas):
    '''Função usado para verificar com o cpf qual carro foi alugado e verifica se a data esta correta caso nao esteja
    aplica uma multa de R$ 100,00 no valor total por dia atrasdo'''

    cpf_pessoa = input('Digite seu CPF: ')
    dia_entregue = input('Dia de entrega (dd/mm/YYYY): ')

    '''entra na lista procura a pessoa e verifica se o dia que ela entregou esta correto e se estiver diferente é aplicado a multa'''
    if dia_entregue != pessoas_cadastradas[cpf_pessoa][7]:
        dia_entregue = datetime.datetime.strptime(dia_entregue, '%d/%m/%Y')
        data_entregue = datetime.datetime.strptime(
            pessoas_cadastradas[cpf_pessoa][7], '%d/%m/%Y')

        atraso = dia_entregue - data_entregue
        valor = atraso.days * 100
        print('Pague uma multa no valor de R$: ', valor)

    if cpf_pessoa in pessoas_cadastradas.keys():
        '''retira o nome da pessoa que alugou o carro e devolve o carro para o estoque inicial'''
        carros[pessoas_cadastradas[cpf_pessoa][4]][5] += 1
        del pessoas_cadastradas[cpf_pessoa]

        escrever_json_carros(carros)
        escrever_json_pessoas_cadastradas(pessoas_cadastradas)

        print('Devolvido com sucesso')


def menu():
    '''menu utilizado para correr o codigo e ser utilizado'''
    carros = carregar_arquivo_carros()
    while True:
        exibir_tabela_carros(carros)
        op = input(
            '\n(1) Reservar veiculo\n'
            '(2) Devolver veiculo\n'
            '(3) Finalizar\n')

        if (op == '1'):
            pessoas_cadastradas = reservar_carro(carros)
        elif (op == '2'):
            pessoas_cadastradas = carregar_arquivo_pessoas_cadastradas()
            devolver_carro(carros, pessoas_cadastradas)
        elif (op == '3'):
            break


if __name__ == '__main__':
    menu()
