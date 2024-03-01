import sqlite3

conn = sqlite3.connect('sistema_financeiro.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origem_nome TEXT,
        destino_nome TEXT,
        tipo TEXT,
        valor REAL,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

class Conta:
    def __init__(self, nome, saldo=0.0):
        self.nome = nome
        self.saldo = saldo

    def registrar_transacoes(self, transacoes):
        cursor.executemany('''
            INSERT INTO transacoes (origem_nome, destino_nome, tipo, valor)
            VALUES (?, ?, ?, ?)
        ''', transacoes)
        conn.commit()

    def sacar(self, *valores):
        self.saldo -= sum(valores)
        transacoes = [(self.nome, None, 'SAQUE', valor) for valor in valores]
        self.registrar_transacoes(transacoes)

    def depositar(self, *valores):
        self.saldo += sum(valores)
        transacoes = [(self.nome, None, 'DEPOSITO', valor) for valor in valores]
        self.registrar_transacoes(transacoes)

    def transferir(self, destino, *valores):
        if self.saldo >= sum(valores):
            self.saldo -= sum(valores)
            destino.saldo += sum(valores)
            transacoes = [(self.nome, destino.nome, 'TRANSFERENCIA', valor) for valor in valores]
            self.registrar_transacoes(transacoes)
        else:
            print('ERRO: Saldo insuficiente')

    def pix_pagante(self, destino, *valores):
        if self.saldo >= sum(valores):
            self.saldo -= sum(valores)
            destino.saldo += sum(valores)
            transacoes = [(self.nome, destino.nome, 'PIX', valor) for valor in valores]
            self.registrar_transacoes(transacoes)
            print('Pix realizado com sucesso!')
        else:
            print('ERRO: Saldo insuficiente')

    def pix_recebedor():
        print('Pix recebido com sucesso')


    def consultar_saldo(self):
        return self.saldo

    def obter_historico_transacoes(self):
        cursor.execute('''
            SELECT * FROM transacoes WHERE origem_nome = ? OR destino_nome = ?
        ''', (self.nome, self.nome))
        transacoes = cursor.fetchall()
        for transacao in transacoes:
            print(transacao)


conta_wendell = Conta('Wendell')
conta_anna = Conta('Anna')

conta_anna.depositar(500, 300, 310)
conta_wendell.depositar(500)
conta_anna.pix_pagante(conta_wendell, 200)


conta_wendell.obter_historico_transacoes()  
conn.close()
