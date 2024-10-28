from Configuration.mysql_connection import Connection  # Importa a classe Connection para conexão com o banco MySQL
from pessoas.pessoa import Paciente  # Importa a classe Paciente

# Inicialização e criação de banco e tabela para armazenar dados dos pacientes
try:
    conn = Connection()  # Estabelece a conexão com o banco de dados
    cursor = conn.cursor
    # Cria o banco de dados 'hospital' caso não exista
    cursor.execute("CREATE DATABASE IF NOT EXISTS hospital;")
    cursor.execute("USE hospital;")
    # Cria a tabela 'paciente' caso não exista, com campos para id, nome, sintoma, prioridade, hora e data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paciente (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            sintoma VARCHAR(255) NOT NULL,
            prioridade INT NOT NULL,
            hora TIME NOT NULL,
            data DATE NOT NULL
        );
    """)

    # Instâncias de Paciente são criadas e adicionadas a uma lista
    lista_pacientes = [
        Paciente("João", "Dor no peito", 1),  # Adiciona paciente João
        Paciente("Maria", "Febre alta", 2),   # Adiciona paciente Maria
        Paciente("Ana", "Dor de cabeça leve", 3),  # Adiciona paciente Ana
        Paciente("Carlos", "Fratura exposta", 1),  # Adiciona paciente Carlos
        Paciente("Caio", "Febre alta", 2)   # Adiciona paciente Caio
    ]
    # Adiciona todos os pacientes da lista ao banco de dados
    for paciente in lista_pacientes:
        paciente()  # Executa o método __call__, que adiciona o paciente ao banco

    """paciente = Paciente.proximo_paciente()
    print(f"Chamando {paciente.nome()} para atendimento (Prioridade: {paciente.prioridade()})")
    paciente = Paciente.proximo_paciente()
    print(f"Chamando {paciente.nome()} para atendimento (Prioridade: {paciente.prioridade()})")"""

    # Chama pacientes para atendimento conforme a prioridade e a hora de chegada
    while True:
        proximo = Paciente.proximo_paciente()
        if not proximo:  # Se não houver mais pacientes na lista
            print("Não há mais pacientes na lista.")
            break
        print(f"Chamando {proximo.nome()} para atendimento (Prioridade: {proximo.prioridade()})")

# Tratamento de exceções que possam ocorrer ao conectar ao banco ou executar comandos SQL
except Exception as erro:
    print(f"Ocorreu um erro: {erro}")
