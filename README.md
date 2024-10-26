# AIRFLOW_CHECKPOINT

### Integrantes

TURMA: 1TSCPG

- RM: 557897 | Állex Augusto de Souza Brandão
- RM: 555560 | Diego Augusto Oliveira Rocha
- RM: 554677 | Giovana Cintra Nogueira
- RM: 558060 | Tiago Aiala de Lima

### INSTRUÇÕES

Necessário ter o docker desktop
(necessário manter o docker desktop aberto no processo)

Faça o Donwload da pasta

É necessário que a pasta AIRFLOW_CHECKPOINT esteja dento do D:
(o nome da pasta deve permanecer o mesmo)

Ou seja tem que estar assim:
D:\AIRFLOW_CHECKPOINT

Caso queira alterar o diretório onde irá rodar abra o "docker-compose.yml"

Na linha 23, altere o diretório de acordo com o que deseja

Por exemplo alterar o "D:/AIRFLOW_CHECKPOINT:/opt/airflow/data" por
"C:/AIRFLOW_CHECKPOINT:/opt/airflow/data"

### PARTE 1:

Abrir o cmd ou o PowerShell no diretório onde estão os arquivos

```cmd
docker ps
docker-compose up airflow-init
docker-compose down
docker-compose up --build
```

RODE TODOS ESTES COMANDOS, UM APÓS O TERMINO DO OUTRO
(Atenção, não feche o cmd ou PowerShell)

Depois de rodar aguarde 5 minutos para começar a PARTE 2

### PARTE 2:

Abra este link no navegador: http://localhost:8080/home (usuario: airflow, senha: airflow)

A DAG estará na página inicial, em "Actions" na interface da página inicial
Clique em "Trigger DAG" (o botão de play)

### PARTE 3:

Abra outro cmd ou o PowerShell no diretório onde estão os arquivos

Para inicializar o MongoDB com o usuário e senha:

```cmd
docker exec -it airflow_checkpoint-mongo-1 mongosh -u EnergyGuide -p Backcast --authenticationDatabase admin
```

Verificação dos dados:

- Para verificar os bancos de dados existentes:

  ```cmd
  show dbs
  ```

- Para entrar no banco de dados:

  ```cmd
  use checkpointThiago
  ```

- Mostrar as coleções existentes:

  ```cmd
  show collections
  ```

- Mostrar os dados da coleção "clientes":
  ```cmd
  db.clientes.find().pretty()
  ```
