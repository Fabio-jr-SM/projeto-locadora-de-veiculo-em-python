import sqlite3 as sql

con = sql.connect("banco.db")
cur = con.cursor()


numero = input("Digite o numero: ")
conta = input("Digite a conta: ")

cur.execute(f"""
            insert into conta(numero,agencia,cliente_id)
            values('{numero}','{conta}',4)
            """)
con.commit()

res = cur.execute("select * from conta")
for id,numero,agencia,cliente_id in (res.fetchall()):
    print(id,numero,agencia,cliente_id)

con.close()
