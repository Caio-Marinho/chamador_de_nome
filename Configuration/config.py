class Configuracion:
    def __init__(self):
        """
        Inicializa a classe Configuracion com as configurações padrão.

        As configurações padrão incluem as credenciais para acessar um banco de dados MySQL.
        """
        # Configurações para acessar o banco de dados
        self.config: dict = {
            'MySQL': {
                'user': 'USUARIO',  # Usuário do banco de dados MySQL
                'password': 'SENHA',  # Senha do banco de dados MySQL
                'host': 'HOST',  # Host do banco de dados MySQL
                'port': 'PORTA'  # Porta de conexão do banco de dados MySQL
            }
        }