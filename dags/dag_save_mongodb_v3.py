from airflow import DAG
from airflow.operators.python import PythonOperator
from pymongo import MongoClient, errors
import pandas as pd
from datetime import datetime

# Task 1: Função para ler o CSV
def read_csv(**kwargs):
    try:
        csv_file = r'/opt/airflow/data/Checkpoint5e6profThiago.csv'
        data = pd.read_csv(csv_file)
        # Passa os dados como uma lista de dicionários via XCom
        kwargs['ti'].xcom_push(key='data', value=data.to_dict(orient='records'))
        print("Dados lidos com sucesso!")
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado. Detalhes: {e}")
    except pd.errors.EmptyDataError as e:
        print(f"Erro: O arquivo está vazio. Detalhes: {e}")
    except Exception as e:
        print(f"Erro ao ler o CSV. Detalhes: {e}")

# Task 2: Conectar ao MongoDB (sem retorno, apenas valida a conexão)
def connect_mongo():
    try:
        username = 'EnergyGuide'
        password = 'Backcast'
        client = MongoClient(f'mongodb://{username}:{password}@mongo:27017/', authSource='admin')
        db = client['checkpointThiago']
        db.list_collection_names()  # Verifica se a conexão está funcionando
        print("Conexão com MongoDB realizada com sucesso!")
    except errors.ConnectionError as e:
        print(f"Erro de conexão com o MongoDB. Detalhes: {e}")
    except errors.ConfigurationError as e:
        print(f"Erro de configuração do MongoDB. Detalhes: {e}")
    except Exception as e:
        print(f"Erro desconhecido ao conectar no MongoDB. Detalhes: {e}")

# Task 3: Inserir dados no MongoDB
def insert_data_to_mongo(**kwargs):
    try:
        # Recupera os dados lidos na task `read_csv`
        data_dict = kwargs['ti'].xcom_pull(task_ids='read_csv', key='data')
        if not data_dict:
            print("Nenhum dado para inserir.")
            return

        # Conexão com o MongoDB
        username = 'EnergyGuide'
        password = 'Backcast'
        client = MongoClient(f'mongodb://{username}:{password}@mongo:27017/', authSource='admin')
        db = client['checkpointThiago']
        collection = db['clientes']

        # Verifica e insere os dados
        records_to_insert = []
        for record in data_dict:
            if 'id' in record:
                existing_record = collection.find_one({'id': record['id']})
                if existing_record:
                    print(f"Registro com id {record['id']} já existe. Não será inserido.")
                else:
                    records_to_insert.append(record)
            else:
                print(f"Registro sem campo 'id': {record}")

        # Insere os novos registros
        if records_to_insert:
            collection.insert_many(records_to_insert)
            print(f"{len(records_to_insert)} novos registros inseridos com sucesso!")
        else:
            print("Nenhum novo registro para inserir.")

        # Validação da inserção
        count = collection.count_documents({})
        print(f"Total de documentos na coleção 'clientes': {count}")

    except errors.BulkWriteError as e:
        print(f"Erro ao inserir os dados no MongoDB. Detalhes: {e}")
    except Exception as e:
        print(f"Erro desconhecido ao inserir dados. Detalhes: {e}")

# Definindo a DAG e suas configurações
default_args = {
    'owner': 'user',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 17),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    'inserir_dados_mongodb',  # Nome da DAG
    default_args=default_args,
    description='DAG para inserir dados de CSV no MongoDB',
    schedule_interval=None,
    catchup=False,
) as dag:

    # Tarefa para ler o CSV
    read_csv_task = PythonOperator(
        task_id='read_csv',
        python_callable=read_csv,
        provide_context=True
    )

    # Tarefa para conectar ao MongoDB
    connect_mongo_task = PythonOperator(
        task_id='connect_mongo',
        python_callable=connect_mongo
    )

    # Tarefa para inserir os dados no MongoDB
    insert_data_task = PythonOperator(
        task_id='insert_data_to_mongo',
        python_callable=insert_data_to_mongo,
        provide_context=True
    )

    # Definindo a sequência de execução das tarefas
    read_csv_task >> connect_mongo_task >> insert_data_task
