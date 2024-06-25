# sp-budget-data-integration
Integração de dados de orçamento do estado de São Paulo.

## Dependências

- Docker.
- Docker compose.
- Python.
- Acesso a ambiente Linux (alguma distro, wsl, etc).

## Contexto

Essa integração consiste em 2 módulos:

- *etl-engine*: engine genérica responsável pelo processamento dos dados, a lógica está disponível nas pastas ingestion (ingestões dos arquivos .csv) e app (transformação e modelagem).
- *airflow*: software de orquestração de pipelines de dados. Para essa integração, foi desenvolvida uma dag que executa a engine de processamento conteinerizada.

A integração gera 3 tabelas no BigQuery:

- *sp_budget.raw_gdvdespesasexcel*: dados brutos do arquivo gdvdespesasexcel.csv;
- *sp_budget.raw_gdvreceitasexcel*: dados brutos do arquivo gdvreceitasexcel.csv;
- *sp_budget.app_sp_budget*: dados tratados a partir da integração das outras tabelas.

## Subindo o ambiente

Esses são os passos para executar a integração:

1) Na raiz do projeto, executar o comando *sudo docker build -t etl-engine .* para realizar o build da imagem da engine de integração;
2) Executar o comando *sudo chmod 666 /var/run/docker.sock* para permitir que o Aiflow consiga enxergar os containeres na máquina host (essa liberação de permissão é temporária, retornará a permissão padrão após reset da máquina);
3) Adicionar ao diretório */gcloud* o arquivo json da service account com o nome *service_account_json.json* (verificar se essa conta de serviço tem as permissões necessárias no BigQuery);
4) No BigQuery, criar o dataset *sp_budget*, que irá armazenar as tabelas da integração;
5) No diretório *airflow*, executar os seguintes comandos:
   a) *sudo docker compose up airflow-init* -> inicialização dos metadados da aplicação;
   b) *docker compose up -d* -> inicialização da aplicação;

## Execução da Integração

1) Acessar *http://localhost:8080/*;
2) Login: airflow / Senha: airflow;
3) Selecionar a dag *sp_budget_pipeline*;
4) Selecionar *Trigger dag*.

## Saídas

As respostas para as perguntas e evidências de execuções de queries estão disponíveis no diretório *misc/*.