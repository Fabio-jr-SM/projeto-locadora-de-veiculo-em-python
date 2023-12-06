import sqlite3
import datetime

'''Imprimir estoque de carros'''
def aparecer_tabela():
    '''Faz a conexão com o banco de dados'''
    con = sqlite3.connect('locadora.db')
    cur = con.cursor()

    '''Seleciona todas as informações da tabela carros'''
    mostrar_tabela = cur.execute('SELECT * FROM carros')

    print(" ".center(50), "LOCADORA DE VEÍCULOS\n")
    print("Código".ljust(8),
          "Marca".ljust(10),
          "Modelo".ljust(12),
          "Cor".ljust(8),
          "Disponivel".ljust(10),
          "Ano".ljust(12),
          "Preço/Dia".ljust(10),
        )

    for id, marca, modelo, ano, cor, preco_dia, quantidade in mostrar_tabela:
        print(f"{id}".ljust(8),
              f"{marca}".ljust(10),
              f"{modelo}".ljust(12),
              f"{ano}".ljust(8),
              f"{cor}".ljust(10),
              f"{preco_dia}".ljust(12),
              f"{quantidade}".ljust(10), 
            )

    '''Fecha o banco de dados'''
    con.close()

'''Alugar um carro fazendo um isert into na tabela pessoa'''
def alugar_carro():
    '''Faz a conexão com o banco de dados'''
    con = sqlite3.connect('locadora.db')
    cur = con.cursor()

    '''Solicita ao usuário o codigo do carro e os dias de aluguel'''
    codigo = int(input('Digite o código do carro que deseja alugar: '))
    dias = int(input('Digite a quantidade de dias que deseja alugar: '))

    '''Seleciona todas as informações da tabela carros'''
    select_carros = cur.execute('SELECT * FROM carros')
    carros = select_carros.fetchall()

    if codigo < 1 or codigo > len(carros):
        print("Código de carro inválido.")
        con.close()
        return

    '''Imprime o carro selecionado pelo usuario'''
    print(f"\nCarro desejado: {carros[codigo - 1]}\n")

    '''Solicita ao usuario dados basicos com validações não rigososas (Nome,Idade, Cnh, CPF)'''
    nome_completo = input('Nome completo: ')
    idade = int(input('Idade: '))

    if idade < 18:
        print("VOCÊ É MENOR DE IDADE!!!!!\n")
        con.close()
        return

    if idade < 25:
        conta = (dias * carros[codigo - 1][6]) + 30
    else:
        conta = dias * carros[codigo - 1][6]

    cnh = input('CNH: ')
    cpf = input('CPF: ')


    '''O datetime armazena a data atual para adicionar na tabela aluga'''
    now = datetime.datetime.now()
    data_atual = now.date().strftime('%d/%m/%Y')

    '''Calculo da data de devolução'''
    delta = datetime.timedelta(days=dias)
    data = now + delta
    formato = '%d/%m/%Y'
    data_entrega = data.strftime(formato)

    '''Imprimindo o contrato de locação'''
    print(''.center(25), 'CONTRATO DE LOCAÇÃO\n')
    print('{} portador do CPF {} e da CNH {} \nestá alugando o veículo {}'.format(
        nome_completo, cpf, cnh, carros[codigo - 1][0]))
    print('no período de {} dias, que ficará no valor de R${}'.format(dias, conta))
    print('e a devolução do veículo ficará para a data {}.\n'.format(data_entrega))
    print('-----ATENÇÃO: EM CASO DE ATRASO HAVERÁ COBRANÇA DE TAXA DE R$100,00 AO DIA-----')
    print('Locação com sucesso!\n')
    print('================================================================\n\n')

    '''Insere a nova pessoa cadastrada na tabela pessoa'''
    con.execute('''
        INSERT INTO pessoa(nome, idade, cpf, cnh) VALUES (?, ?, ?, ?)
    ''', (nome_completo, idade, cpf, cnh))

    '''o comando last_insert_rowid():
        recuperar o valor da chave primária (ou identificador único) 
        gerado automaticamente durante a última operação de inserção em 
        uma tabela'''
    pessoa_id = con.execute('SELECT last_insert_rowid()').fetchone()[0]

    '''Insere os dados de locação na tabela de relacionamento aluga'''
    con.execute('''
        INSERT INTO aluga (data_alugada, data_devoluçao, preco_aluguel, id_carro, id_pessoa)
        VALUES (?, ?, ?, ?, ?)
    ''', (data_atual, data_entrega, conta, codigo, pessoa_id))

    '''Atualiza a tabela carros descrementando um carro a menos no id escolhido pelo usuario'''
    con.execute('''
        UPDATE carros SET quantidade = quantidade-1 WHERE id_carro = ?
    ''', (codigo,))

    '''Confirmar as alterações (commit)'''
    con.commit()
    con.close()

'''Devolver um carro de acordo com o CPF da pessoa'''
def devolver_carro():
    con = sqlite3.connect('locadora.db')
    cur = con.cursor()
    '''select_carros = cur.execute('SELECT * FROM carros')
    carros = select_carros.fetchall()'''
        
    codigo = int(input('Digite o código do carro: '))
    data_devolução = input('Digite a data de devolução (dd/mm/aaaa): ')

    '''Atualizando a tabela carros adicionando a unidade devolvida'''
    cur.execute('''
            UPDATE carros SET quantidade = quantidade+1 WHERE id_carro = ?
        ''', (codigo,))


    '''Atualizando a data de devolução na tabela aluga'''
    cur.execute('''
            UPDATE aluga SET data_devoluçao = ? WHERE id_carro = ?
        ''', (data_devolução,codigo))
    con.commit()
    con.close()

'''Menu de interação com o usuario'''
def menu():
    while True:
        aparecer_tabela()
        op = input('\n(1) Reservar veiculo\n(2) Devolver veiculo\n(3) Finalizar\n')

        if op == '1':
            alugar_carro()
        elif op == '2':
            devolver_carro()
        elif op == '3':
            break


if __name__ == '__main__':
    menu()
