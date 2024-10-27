class Configuracion:
    def __init__(self):
        """
        Inicializa a classe Configuracion com as configurações padrão.

        As configurações padrão incluem as credenciais para acessar um banco de dados MySQL.
        """
        # Configurações para acessar o banco de dados
        self.config: dict = {
            'MySQL': {
                'user': 'Usuario',  # Usuário do banco de dados MySQL
                'password': 'Senha',  # Senha do banco de dados MySQL
                'host': 'HOST_DE_ACESSO',  # Host do banco de dados MySQL
                'port': 'PORTA_DE_ACESSO'  # Porta de conexão do banco de dados MySQL
            }
        }