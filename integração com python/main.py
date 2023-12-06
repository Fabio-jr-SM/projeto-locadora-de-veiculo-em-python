import sqlite3
import datetime

def aparecer_tabela():
    con = sqlite3.connect('locadora.db')
    cur = con.cursor()

    mostrar_tabela = cur.execute('Select * from carros')

    print(" ".center(50), "LOCADORA DE VEÍCULOS\n")
    print("Código".ljust(14),
          "Marca".ljust(14),
          "Modelo".ljust(14),
          "Ano".ljust(14),
          "Cor".ljust(14),
          "Preço/Dia".ljust(14),
          "Disponível".ljust(14),
          )

    for id, marca, modelo, cor, quantidade, ano, preco_dia in mostrar_tabela:
        print(f"{id}".ljust(14),
              f"{marca}".ljust(14),
              f"{modelo}".ljust(14),
              f"{ano}".ljust(14),
              f"{cor}".ljust(14),
              f"{preco_dia}".ljust(14),
              f"{quantidade}".ljust(14),)

    con.commit()
    con.close()

def reservar_carro():

    codigo = int(input('Qual o código do carro:'))
    dias = int(input('Quantidade de dias de aluguel:'))
    OpcaoDois = input('\n(1) Confirmar contrato'
                      '\n(2) Mudar o veiculo'
                      '\n(3) Encerrar\n')

    if (OpcaoDois == '1'):
        pessoas_cadastradas = alugar_carro(codigo, dias)
        return pessoas_cadastradas
    elif (OpcaoDois == '2'):
        reservar_carro()
    elif (OpcaoDois == '3'):
        return None


def alugar_carro(codigo,dias):
    con = sqlite3.connect('locadora.db')
    cur = con.cursor()

    select_carros = cur.execute('SELECT * FROM carros')
    carros = select_carros.fetchall()

    print(carros[codigo-1])

    nome_completo = input('Nome completo: ')
    idade = int(input('Idade: '))

    if idade < 18:
        print("VOCÊ É MENOR DE IDADE!!!!!\n")
        alugar_carro(codigo, dias)

    if idade < 25:
        conta = (dias * carros[codigo-1][6]) + 30
    else:
        conta = dias * carros[codigo-1][6]

    cnh = input('CNH: ')
    cpf = input('CPF: ')

    now = datetime.datetime.now()

    now = datetime.datetime.now()
    data_atual = now.date().strftime('%d/%m/%Y')

    delta = datetime.timedelta(days=dias)
    data = now + delta
    formato = '%d/%m/%Y'
    data_entrega = data.strftime(formato)

    print(''.center(25), 'CONTRATO DE LOCAÇÃO\n')
    print('{} portador do CPF {} e da CNH {} \nestá alugando o veículo {}'.format(
        nome_completo, cpf, cnh, carros[codigo-1][0]))
    print('no período de {} dias, que ficará no valor de R${}'.format(dias, conta))
    print('e a devolução do veículo ficará para a data {}.\n'.format(data_entrega))
    print('-----ATENÇÃO: EM CASO DE ATRASO HAVERÁ COBRANÇA DE TAXA DE R$100,00 AO DIA-----')
    print('Locação com sucesso!\n')
    print('================================================================\n\n')

    con.execute('''
        INSERT INTO pessoa(nome, idade, cpf, cnh) VALUES (?, ?, ?, ?)
    ''', (nome_completo, idade, cpf, cnh))

    cur.execute('SELECT last_insert_rowid()')
    pessoa_id = cur.fetchone()[0]

    con.execute('''
        INSERT INTO aluga(data_alugada, data_devoluçao, preco_aluguel, id_carro, id_pessoa)
        VALUES (?, ?, ?, ?, ?)
    ''', (data_atual, data_entrega, conta, codigo, pessoa_id))

    new_quantity = carros[codigo-1][4] - 1
    con.execute('''
        UPDATE carros SET quantidade = ? WHERE id_carro = ?
    ''', (new_quantity, codigo))
    con.commit()

    con.commit()
    con.close()

    


def devolver_carro():
    con = sqlite3.connect('locadora.db')
    cur = con.cursor()
    
    cpf = int(input("Digite seu cpf: "))
    data = input("Digite a data de devolução (dd/mm/aaaa): ")
    
    cur.execute(f'''
        UPDATE aluga
        SET data_devoluçao = ?
        WHERE id_pessoa IN (SELECT id_pessoa FROM pessoa WHERE cpf = ?)
    ''', (data, cpf))
    
    new_quantity = carros[codigo-1][4] + 1
    con.execute('''
        UPDATE carros SET quantidade = ? WHERE id_carro = ?
    ''', (new_quantity, codigo))
    
    con.commit()
    con.close()


def menu():
    while True:
        aparecer_tabela()
        op = input(
            '\n(1) Reservar veiculo\n(2) Devolver veiculo\n(3) Finalizar\n')

        if op == '1':
            reservar_carro()
        elif op == '2':
            devolver_carro()
        elif op == '3':
            break


if __name__ == '__main__':
    menu()
