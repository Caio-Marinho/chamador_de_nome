from pytz import timezone  # Importa o módulo para manipulação de fusos horários
from datetime import datetime, timezone as tmz  # Importa datetime e renomeia timezone para tmz
from Configuration.mysql_connection import \
    Connection  # Importa a classe Connection para conexão com o banco de dados MySQL


class Paciente:
    """
    Representa um paciente no sistema hospitalar, com informações como nome, sintomas,
    prioridade e horário de chegada. Inclui métodos para gerenciar o armazenamento
    no banco de dados e a ordenação dos pacientes para atendimento.
    """

    # Define configurações iniciais da classe
    fuso = timezone('America/Fortaleza')  # Define o fuso horário de Fortaleza
    chamada = False  # Flag para indicar se há um paciente em chamada
    lista_paciente = []  # Lista temporária de pacientes recuperados do banco
    date = datetime.today().strftime('%Y-%m-%d')  # Data atual no formato YYYY-MM-DD

    def __init__(self, nome: str, sintomas: str, prioridade: int):
        """
        Inicializa um novo objeto Paciente.

        Args:
            nome (str): Nome do paciente.
            sintomas (str): Descrição dos sintomas do paciente.
            prioridade (int): Nível de prioridade do paciente (1 a n).
        """
        self.__nome = nome
        self.__sintomas = sintomas
        self.__prioridade = prioridade
        # Define hora de chegada com ajuste para o fuso horário
        self.__hora_chegada = datetime.now(tmz.utc).astimezone(self.fuso).strftime('%H:%M:%S')
        self.__data = datetime.today().strftime('%Y-%m-%d')

    def __call__(self) -> None:
        """
        Adiciona o paciente ao banco de dados ao chamar a instância.
        """
        self.adicionar_banco()

    def __lt__(self, outro: 'Paciente') -> bool:
        """
        Compara dois pacientes com base na prioridade e hora de chegada,
        para organizar a ordem de atendimento.

        Args: outro (Paciente): Outro paciente para comparação.

        Returns:
            bool: True se o paciente atual tiver maior prioridade ou chegou antes.
        """
        if self.__prioridade == outro.__prioridade:
            return self.__hora_chegada < outro.__hora_chegada
        return self.__prioridade < outro.__prioridade

    def __str__(self) -> str:
        """
        Retorna uma representação em string do paciente.

        Returns:
            str: representação em string do paciente.
        """
        return f"Paciente: {self.nome()}, Prioridade: {self.prioridade()}, Sintomas: {self.sintomas()}"

    def nome(self) -> str:
        """
        Retorna o nome do paciente.

        Returns:
            str: Nome do paciente.
        """
        return self.__nome

    def sintomas(self) -> str:
        """
        Retorna os sintomas do paciente.

        Returns:
            str: Sintomas do paciente.
        """
        return self.__sintomas

    def prioridade(self) -> int:
        """
        Retorna a prioridade do paciente.

        Returns:
            int: Nível de prioridade do paciente.
        """
        return self.__prioridade

    def data(self) -> str:
        """
        Retorna a data de chegada do paciente.

        Returns:
            str: Data de chegada no formato YYYY-MM-DD.
        """
        return self.__data

    def hora(self) -> str:
        """
        Retorna a hora de chegada do paciente.

        Returns:
            str: hora de chegada no formato HH:MM:SS.
        """
        return self.__hora_chegada

    def adicionar_banco(self) -> None:
        """
        Adiciona o paciente ao banco de dados no sistema hospitalar.
        """
        conn = Connection()  # Estabelece a conexão com o banco
        cursor = conn.cursor
        # Executa comando SQL para inserir dados do paciente
        cursor.execute("USE hospital;")
        sql = "INSERT INTO paciente (nome, sintoma, prioridade, hora, data) VALUES (%s, %s, %s, %s, %s);"
        values = (self.nome(), self.sintomas(), self.prioridade(), self.hora(), self.data())
        cursor.execute(sql, values)
        conn.commit()  # Confirma a transação no banco de dados
        cursor.close()  # Fecha o cursor
        conn.close()  # Fecha a conexão

    @classmethod
    def recuperar_pacientes(cls) -> list:
        """
        Recupera todos os pacientes registrados no banco de dados para a data atual.

        Returns:
            list: Lista de tuplas contendo os dados dos pacientes recuperados.
        """
        try:
            conn = Connection()
            cursor = conn.cursor
            # Recupera dados dos pacientes para a data atual
            cursor.execute("USE hospital;")
            cursor.execute(f"SELECT * FROM paciente WHERE data = '{cls.date}'")
            return cursor.fetchall()  # Retorna a lista de pacientes
        except Exception as erro:
            print(f"Falha na conexão : {erro}")

    @classmethod
    def proximo_paciente(cls) -> 'Paciente' | None:
        """
        Retorna o próximo paciente a ser atendido com base na prioridade.

        Returns:
            Paciente | None: Próximo paciente a ser atendido ou None se a fila estiver vazia.
        """
        if not cls.chamada:
            pacientes = cls.recuperar_pacientes()  # Obtém pacientes da data atual
            if not pacientes:  # Verifica se a lista está vazia
                print("Não há pacientes na fila.")
                return None

            # Converte tuplas em objetos Paciente para manipulação
            pacientes_objetos = [cls(nome=paciente[1], sintomas=paciente[2], prioridade=paciente[3])
                                 for paciente in pacientes]
            pacientes_objetos.sort()  # Ordena por prioridade e hora de chegada
            cls.lista_paciente = pacientes_objetos.copy()  # Armazena lista ordenada
            cls.chamada = True

        if cls.lista_paciente:
            return cls.lista_paciente.pop(0)  # Retorna o próximo paciente
        else:
            print("Não há pacientes na fila.")
            return None
