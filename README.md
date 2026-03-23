# Pipeline ETL Batch | Ibovespa
*Tech Challenge da Fase 2 do curso de [pós-graduação em Engenharia de Machine Learning FIAP](https://postech.fiap.com.br/curso/machine-learning-engineering/)*

> 📽️ Vídeo com demonstração técnica do projeto - Em breve

## 🎯 Sobre o projeto
*O objetivo do projeto é construir um pipeline completo de dados para **extrair, processar, carregar e analisar** dados das ações que compõem o índice Ibovespa no momento de construção do projeto (março/2026).*

> ### AWS
O projeto foi provisionado utilizando os serviços do ecossistema da [Amazon Web Services - AWS](https://aws.amazon.com/pt/):
- **Amazon S3:** Data Lake que contém os buckets para armazenar os dados nas camadas raw e refined
- **AWS Glue:** Para construir a ETL (extração dos dados, transformações para consistência e carregamento na camada refined) - automatiza o processo de preparação e combinação dos dados
- **AWS Lambda:** Acionado pela carga no bucket do S3, chama o job de ETL no Glue
- **AWS Step Functions:** Para orquestrar as etapas do processo
- **AWS Glue Data Catalog**: Para catalogar os dados processados
- **Amazon Athena:** Para analisar os dados processados

> ### Terraform
Para garantir que o processo de construção da infraestrutura não seja perdido, foi escolhido o uso do **Terraform** para a execução do projeto.

O [Terraform](https://developer.hashicorp.com/terraform) é uma ferramenta de **IaC (Infraesturura como Código)**, que permite provisionar recursos de um pipeline de ETL em uma cloud, nesse caso, na AWS. Ele permite construir todo o processo de ETL na forma de código, desde o scraping até a disponibilização dos dados.

Algumas vantagens do uso do Terraform:
- Permite documentação do processo
- Evita que as etapas executadas na AWS (caso fossem realizadas de forma low code, "arrastando caixinhas" ou preenchendo os campos dos formulários) sejam perdidas - evita retrabalhos
- Garante reprodutibilidade e melhoria contínua (possibilita refatoração do código e adição de novas funcionalidades)

> ### Conceitos | Mercado Financeiro
Uma etapa importante do projeto é o entendimento dos conceitos relacionados ao Mercado Financeiro. Isso permite que a disponibilização dos dados será feita de forma a atender as possíveis análises que utilizarão os dados disponibilizados. Abaixo, há um One Page que resume os principais conceitos:

![One Page | Mercado Financeiro](diagrams/one_page_bolsa.png)

> ### Tabelas a serem ingestadas no processo de ETL

Sabendo destes conceitos, temos a necessidade dos seguintes dados, disponibilizados pelas seguintes tabelas (que se relacionam a partir do Ticker (código) da ação):
- **Dimensão (características):** Tabela com as características de cada ação (nome da empresa, setor de atuação, tipo de ação, segmento da ação, % de participação na composição do índice). Fontes de dados:
  - A lista atualizada de ativos do Ibovespa (que no projeto foi acessada em 08/03/2026) está disponível [neste link](https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-ibovespa-ibovespa-composicao-da-carteira.htm). A ideia será acompanhar os valores das ações que estão nesta lista.
  - A tabela de todas as empresas listadas na B3 com seus respectivos setores está disponível [neste link](https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/empresas-listadas.htm), opção "Busca por Setor de Atuação". Essa tabela será usada para enriquecer a tabela dimensão da lista de ativos que compõem o Ibovespa.

- **Fato (eventos):** Tabela com os valores das ações que compõem o índice Ibovespa a cada hora do período analisado. Os dados serão obtidos a partir do site do [Google Finance](https://www.google.com/finance/).

## ⚙️ Funcionalidades

- Processamento da tabela dimensão com as características dos ativos do Ibovespa (etapa executada na máquina local)
- **[Extract]** Web Scraping dos dados do Ibovespa (etapa executada na máquina local para evitar custos de processamento por hora na AWS)
- Rotina no **Apache Airflow** de execução do web scraping dos dados (a cada 1h entre 08:00 e 20:00 em dias úteis)
- Rotina no **Apache Airflow** para concatenar as tabelas do dia (1x por dia às 20:10 em dias úteis)
- Rotina no **GitHub Workflow** para ingestão diária da tabela .parquet (com os valores das ações extraídos no dia) em bucket do **Amazon S3**
- Criação de uma IAM Role para execução dos processos no **AWS Glue**
- **[Transform e Load]** Transformação e carregamento dos dados executada com **AWS Glue**
  - Renomear colunas
  - Criação de colunas auxiliares: dia da semana, abertura e fechamento do dia
  - Agrupamento e sumarização: contagem, min, max, média, mediana e desvio padrão por ação e dia
  - Cálculo do ganho ou perda % do dia
  - Valores mínimos e máximos da semana
- Catalogação dos dados no **AWS Glue Data Catalog**
- Orquestração dos serviços da AWS usando máquinas de estado criadas com **AWS Step Functions**
- Análise dos dados no **Amazon Athena**

## 📐 Arquitetura
> ⚠️ Ainda pode sofrer alterações

Obs.: As tags em vermelho são referentes aos 8 requisitos exigidos para completar o Tech Challenge

![Arquitetura](diagrams/arquitetura.png)

## 📂 Estrutura do projeto
> ⚙️ Em preenchimento
```
terraform-aws-stock-etl/
├── .github/
│   └── workflows/
│       └── upload_extracted_data.yaml
├── diagrams/
│   ├── plano_arquitetural.png
│   └── one_page_bolsa.png
├── extract_local/
│   ├── data/
│   │   ├── daily/ (tabelas .parquet diárias)
│   │   ├── raw/ (tabelas brutas para criar a tabela dimensão)
│   │   ├── refined/ (tabela dimensão pronta)
│   │   └── scraped/ (dados extraídos por hora)
│   └── src/
│       ├── airflow_daily.py
│       ├── airflow_hourly.py
│       ├── daily_concat_scraped_data.py
│       ├── process_dimension_table.py
│       └── web_scraping.py
├── infra_aws/
│   ├── s3/
│   │   └── main.tf
│   ├── iam/
│   │   └── main.tf
│   ├── glue/
│   │   ├── glue-job-extract.py
│   │   ├── glue-job-transform.py
│   │   ├── main.tf
│   │   └── variables.tf
│   ├── lambda/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── lambda_function.py
│   ├── stepfunctions/
│   │   ├── main.tf
│   │   └── variables.tf
│   └── prod/
│       ├── main.tf
│       ├── variables.tf
│       ├── terraform.tfvars
│       ├── backend.tf
│       └── providers.tf
├── tests/
├── README.md
└── requirements.txt
```

## ✅ Etapas de execução
> ⚙️ Em preenchimento

> ### 1. Processamento da tabela dimensão
- Download das tabelas disponíveis nos links da seção [Tabelas a serem ingestadas](#tabelas-a-serem-ingestadas-no-processo-de-etl)
  - Tabelas com os ativos no momento do projeto disponíveis em `extract_local/data/raw/`
- Pré-processamento e join para gerar a tabela dimensão
  - Módulo `extract_local/src/process_dimension_table.py`
  - Persiste tabela em `extract_local/data/refined/ativos_ibov.parquet`

> ### 2. Web scraping dos valores das ações
- Função para executar o scraping dos valores das ações → `extract_local/src/web_scraping.py`
- Dados por hora são persistidos em formato .csv em `extract_local/data/scraped/` (não sobe para repositório)
- Instalação do Apache Airflow (processo no Windows)
  - Download do Docker
  - Abrir o Docker e mantê-lo aberto durante a execução
  - Download do [`docker-compose.yaml`](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) do site do Airflow
  - Criar uma pasta `airflow`, colocar o `.yaml` baixado e criar um `.env` com o código `AIRFLOW_UID=50000`
  - Dentro dessa pasta, criar também as pastas `logs/`, `dags/` e `plugins/`
  - No terminal, navegar até a pasta e executar os comandos
    - `docker-compose up airflow-init`
    - `docker-compose up -d` (o `-d` é para rodar em background, e aí podemos fechar o terminal que o Airflow continua executando)
  - Enquanto o último comando roda no terminal, acessar no navegador `localhost:8080` e entrar com o login `airflow` e senha também `airflow`
- Configurar Airflow para executar a cada 1h entre 08:00 e 20:00 em dias úteis
- Configurar Airflow para concatenar as tabelas do dia (1x por dia às 20:10 em dias úteis) e persistir em .parquet

> ### 3. Etapas manuais na AWS
- Criação de uma conta na AWS
- Criação do usuário para usar as credenciais e criar a [IAM Role](#-sobre-a-iam-role)

> ### 4. Construção do pipeline ETL com Terraform (IaC) e GitHub Workflows
- [Instalação do terraform](https://developer.hashicorp.com/terraform/install) localmente
  - Download do .exe
  - Adicionar nas variáveis de ambiente da máquina para usar os comandos
- ...
- [Etapa manual] Fazer upload dos scripts dos jobs Glue no bucket S3
- Orquestrar pipeline com StepFunctions
- Workflow para subir as tabelas .parquet 1x por dia no bucket e acionar a lambda que chama o job de ETL no Glue

> *Em breve: Fluxo da state machine gerado pela orquestração no Step Functions*

Comandos do Terraform no terminal:
- `cd <PATH>` ir para a pasta do serviço a ser provisionado
  - `terraform init` → inicializa o terraform
  - `terraform plan` → mostra os recursos que serão provisionados
  - `terraform validate`→ valida o código
  - `terraform apply` → aplica o provisionamento dos recursos
  - `terraform destroy` → destroi os recursos provisionados naquele serviço

## 💡 Sobre a IAM Role
Não é possível usar uma conta root para provisionar recursos na AWS usando o terraform - é necessário criar um usuário com a conta root<br>

> ### 1. Criar manualmente (não precisa de chave de usuário de IAM Users)

- Entrar em IAM → Roles → Create role
- Etapa 1: Serviço da AWS, Use case: Glue
- Etapa 2: Selecionar permissões: AWSGlueServiceRole, AmazonS3FullAccess, CloudWatchLogsFullAccess
- Etapa 3: Nome role-glue-etl-ibov ou AWSGlueServiceRole-ibov-etl
- Create role



> ### 2. Criar usuário para utilizar chave de acesso em serviços de automação

*Necessário para conceder permissões para ferramentas como Terraform, AWS CLI, Scripts Python (usando a lib boto3), CI/CD com GitHub Actions, etc*

> Etapas para criar um usuário para usar credenciais na criação da Role:

- Console AWS → IAM → [menu esquerdo] Users → [botão laranja] Create user → definir nome → next → attach policies directly → selecionar AdministratorAccess → Next → Create user → Clicar no usuário criado → Security credentials (usar essas credenciais para provisionar recursos da AWS usando terraform) → Create access key → Other → Next → Create access key → Download .csv file

> Criando a role com Terraform:

No Windows: 
- colocar as credenciais em `C:\Users\SEU_USUARIO\.aws\credentials`
  ```
  aws_access_key_id = <access_key_id>
  aws_secret_access_key = <secret_access_key>
  ```

- criar o arquivo `C:\Users\SEU_USUARIO\.aws\config`
  ```
  region = us-east-1
  output = json
  ```

Ao executar os comandos, o terraform automaticamente lê o `.aws/credentials` e as variáveis de ambiente<br>

- No terminal: navegar até a pasta `iam/`
- Executar o comando `terraform init`
- `terraform plan` lista todos os recursos que estão declarados no main.tf da pasta `iam/`
- `terraform apply` para criar a IAM Role

No **GitHub Secrets**: Settings → Secrets → Actions → Configurar `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY`<br>

## 🚀 Evolução do projeto
> ⚙️ Em preenchimento
- Automação da geração da tabela dimensão dos ativos:
  - Adicionar etapa automatizada de atualização da composição da carteira do Ibovespa
  - Adicionar etapa automatizada de atualização da lista de empresas listadas na B3
- Esteira de CI/CD (Continuous Integration / Continuous Delivery) com GitHub Workflows para automatizar todo o processo de provisionamento dos recursos usando Terraform
- Processar o Web Scraping na AWS com EventBridge em vez de Airflow - Arquitetura alternativa abaixo:

![Arquitetura alternativa](diagrams/arquitetura_alternativa.png)