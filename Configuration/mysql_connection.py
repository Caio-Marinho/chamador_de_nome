import mysql.connector  # Importa o conector MySQL
from Configuration.config import Configuracion  # Importa a classe Configuracion do módulo Configuration


class Connection(Configuracion):
    def __init__(self):
        """
        Inicializa a classe Connection com a conexão ao banco de dados MySQL.

        Esta classe herda as configurações da classe Configuracion para acessar o banco de dados.
        """
        Configuracion.__init__(self)  # Inicializa as configurações da classe pai
        try:
            self.conn = mysql.connector.connect(**self.config['MySQL'])  # Estabelece a conexão com o banco de dados
            # MySQL
            self.cursor = self.conn.cursor()
        except Exception as erro:
            print(f"Falha de conexão, tipo de erro: {erro}")  # Trata exceções de conexão
            exit(1)

    def connection(self):
        """
        Retorna a conexão ativa com o banco de dados.
        """
        return self.conn

    def cursor(self):
        """
        Retorna o cursor para executar consultas no banco de dados.
        """
        return self.cursor

    def commit(self):
        """
        Realiza o commit das transações no banco de dados.
        """
        return self.conn.commit()

    def fetchone(self):
        """
        Retorna a próxima linha do resultado da consulta.
        """
        return self.cursor.fetchone()

    def fetchall(self):
        """
        Retorna todas as linhas do resultado da consulta.
        """
        return self.cursor.fetchall()

    def execute(self):
        """
        Executa uma consulta SQL no banco de dados.
        """
        return self.cursor.execute()

    def close(self):
        """
        Fecha a conexão com o banco de dados.
        """
        pass
