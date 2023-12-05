import sqlite3


def valor_aluguel():
    ent = input(int('Digite o valor do aluguel do carros: '))
    ent1 = input(int('Digite a quantidade de dias que deseja: '))
    aluguel = ent * ent1
    return aluguel


def aparecer_tabela():
    con = sqlite3.connect()
    cur = con.cursor()
    mostrar_tabela = cur.execute('Select * from Exemplo')
    return mostrar_tabela.fetchall()


def alugar_carro():
    con = sqlite3.connect()
    cur = con.cursor()
    alugar = cur.execute(
        'update <tabela> set <coluna>=<valor> where <condição>')
    return alugar.fetchone()


def devolver_carro():
    con = sqlite3.connect()
    cur = con.cursor()
    devolver = cur.execute(
        'update <tabela> set <coluna>=<valor> where <condição>')
    return devolver.fetchone()


def menu():
    while True:
        aparecer_tabela()
        op = input(
            '\n(1) Reservar veiculo\n(2) Devolver veiculo\n(3) Finalizar\n')

        if op == '1':
            alugar_carro()
        elif op == '2':
            devolver_carro()
        elif op == '3':
            break


if __name__ == 'main':
    menu()
