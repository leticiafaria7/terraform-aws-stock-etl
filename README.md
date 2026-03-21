# Pipeline Batch | Ibovespa
*Tech Challenge da Fase 2 do curso de [pós-graduação em Engenharia de Machine Learning FIAP](https://postech.fiap.com.br/curso/machine-learning-engineering/)*

> 📽️ Vídeo com demonstração técnica do projeto - Em breve

## 🎯 Sobre o projeto
*O objetivo do projeto é construir um pipeline completo de dados para **extrair, processar, carregar e analisar** dados das ações que compõem o índice Ibovespa no momento de construção do projeto (março/2026).*

> ### AWS
O projeto foi provisionado utilizando os serviços do ecossistema da [Amazon Web Services - AWS](https://aws.amazon.com/pt/):
- **S3:** Data Lake que contém os buckets para armazenar os dados nas camadas raw e refined
- **Glue:** Para construir a ETL (extração dos dados, transformações para consistência e carregamento na camada refined) - automatiza o processo de preparação e combinação dos dados
- **Lambda:** Para configurar e executar o runtime dos códigos (horário e frequência de execução)
- **Eventbrigde:** Para definir a frequência e horários de execução das etapas
- **Athena:** Para analisar os dados obtidos

> ### Terraform
Para garantir que o processo de construção da infraestrutura não seja perdido, foi escolhido o uso do **Terraform** para a execução do projeto.

O [Terraform](https://developer.hashicorp.com/terraform) é uma ferramenta de **IaC (Infraesturura como Código)**, que permite provisionar recursos de um pipeline de ETL em uma cloud, nesse caso, na AWS. Portanto, ele permite construir todo o processo de ETL na forma de código, desde o scraping até a disponibilização dos dados.<br>Algumas vantagens do uso do Terraform:
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

- Web Scraping dos dados do Ibovespa (etapa executada com frequência determinada no Lambda)
- Configuração de horário e frequência de execução da rotina de ETL (com Eventbridge)
- Ingestão dos dados brutos, particionados por dia (no S3)
- Transformação dos dados (orquestrada no Glue)
  - Renomear colunas
  - Padronizar tipos das colunas
  - Agrupamentos numéricos, sumarização, contagem, soma
- Orquestração dos serviços da AWS usando máquinas de estado (Step Functions)
- Análise dos dados (no Athena)

## 📐 Arquitetura
> Em breve

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
│   │   ├── daily/
│   │   ├── raw/
│   │   ├── refined/
│   │   └── scraped/
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

> ### 1. Testes locais da ETL das tabelas a serem ingestadas
- Download das tabelas disponíveis nos links da seção [Tabelas a serem ingestadas](#tabelas-a-serem-ingestadas-no-processo-de-etl)
  - Tabelas com os ativos no momento do projeto disponíveis em `local_tests/raw/`
- Pré-processamento e join para gerar a tabela dimensão
  - Notebook `local_tests/tratar_lista_empresas.ipynb`
  - Persiste tabela em `local_tests/refined/ativos_ibov.xlsx`
- Função para executar o scraping dos valores das ações → `local_tests/main.py`
- Notebook para testes dos dados obtidos → `local_tests/testes_scraped_data.ipynb`

> ### 2. Etapas manuais na AWS
- Criação de uma conta na AWS
- Criação do usuário para usar as credenciais e criar a [IAM Role](#-sobre-a-iam-role)

> ### 3. Construção do pipeline ETL com Terraform (IaC)
- [Instalação do terraform](https://developer.hashicorp.com/terraform/install) localmente
  - Download do .exe
  - Adicionar nas variáveis de ambiente da máquina para usar os comandos
- ...
- Orquestrar pipeline com StepFunctions
- Esteira de CI/CD (Continuous Integration / Continuous Delivery) com GitHub Workflows
  - CI valida o código - `terraform validate`
  - CD faz o deploy - `terraform apply`

Comandos do Terraform no terminal:
- `cd <PATH>` ir para a pasta do serviço a ser provisionado
  - `terraform init` → inicializa o terraform
  - `terraform plan` → mostra os recursos que serão provisionados
  - `terraform apply` → aplica o provisionamento dos recursos
  - `terraform destroy` → destroi os recursos provisionados naquele serviço

## 💡 Sobre a IAM Role
Não é possível usar uma conta root para provisionar recursos na AWS usando o terraform - é necessário criar um usuário com a conta root<br>

**Etapas para criar um usuário para usar credenciais na criação da Role em `infra/modules/iam/main.tf`:**<br>Console AWS → IAM → [menu esquerdo] Users → [botão laranja] Create user → definir nome → next → attach policies directly → selecionar AdministratorAccess → Next → Create user → Clicar no usuário criado → Security credentials (usar essas credenciais para provisionar recursos da AWS usando terraform) → Create access key → Other → Next → Create access key → Download .csv file

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

Para criar a role:
- No terminal: navegar até a pasta `iam/`
- Executar o comando `terraform init`
- `terraform plan` lista todos os recursos que estão declarados no main.tf da pasta `iam/`

No **GitHub Secrets**: Settings → Secrets → Actions → Configurar `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY`<br>


## 🚀 Evolução do projeto
> ⚙️ Em preenchimento
- Adicionar etapa automatizada de atualização da composição da carteira do Ibovespa
- Adicionar etapa automatizada de atualização da lista de empresas listadas na B3
