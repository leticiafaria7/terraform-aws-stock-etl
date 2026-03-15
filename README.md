# Pipeline Batch | Ibovespa
*Tech Challenge da Fase 2 do curso de [pós-graduação em Engenharia de Machine Learning FIAP](https://postech.fiap.com.br/curso/machine-learning-engineering/)*

> 📽️ Vídeo com demonstração técnica do projeto - Em breve

## 🎯 Sobre o projeto
*O objetivo do projeto é construir um pipeline completo de dados para **extrair, processar, carregar e analisar** dados das ações que compõem o índice Ibovespa no momento de construção do projeto (março/2026).*

> ### AWS
A ideia é utilizar os serviços do ecossistema da AWS:
- S3: Data Lake que contém os buckets para armazenar os dados nas camadas raw e refined
- Glue: Para construir a ETL (extração dos dados, transformações para consistência e carregamento na camada refined)
- Lambda: Para configurar e executar o runtime dos códigos (horário e frequência de execução)
- Athena: Para analisar os dados obtidos

> ### Terraform
Para garantir que o processo de construção da infraestrurura não seja perdido, foi escolhido o uso do **Terraform** para a execução do projeto.

O Terraform é uma ferramenta de **IaC (Infraesturura como Código)**, que permite construir todo o processo de ETL na forma de código, desde o scraping até a disponibilização dos dados. Isto é vantajoso por 2 motivos:
- Permite documentação do processo
- Evita que as etapas executadas na AWS (caso fossem realizadas de forma low code, "arrastando caixinhas" ou preenchendo os campos dos formulários) sejam perdidas - evita retrabalhos
- Garante reprodutibilidade e melhoria contínua (possibilita refatoração do código e adição de novas funcionalidades)

> ### Conceitos | Mercado Financeiro
Uma etapa importante do projeto é o entendimento dos conceitos relacionados ao Mercado Financeiro. Isso permite que a disponibilização dos dados será feita de forma a atender as possíveis análises que utilizarão os dados disponibilizados. Abaixo, há um One Page que resume os principais conceitos:

![One Page | Mercado Financeiro](diagrams/one_page_bolsa.png)

Sabendo destes conceitos, temos a necessidade dos seguintes dados, disponibilizados pelas seguintes tabelas (que se relacionam a partir do Ticker (código) da ação):
- Fato (eventos): Tabela com os valores das ações que compõem o índice Ibovespa a cada hora do período analisado
- Dimensão (características): Tabela com as características de cada ação (nome da empresa, setor de atuação, tipo de ação, segmento da ação, % de participação na composição do índice)

## ⚙️ Funcionalidades

- Web Scraping dos dados do Ibovespa (etapa executada com frequência determinada no Lambda)
- Ingestão dos dados brutos, particionados por dia (no S3)
- Transformação dos dados (orquestrada no Glue)
  - Renomear colunas
  - Padronizar tipos das colunas
  - Agrupamentos numéricos, sumarização, contagem, soma
- Análise dos dados (no Athena)

## 📐 Arquitetura
> Em breve

## 📂 Estrutura do projeto
> Em breve

## ✅ Instruções para execução
> Em breve

## 🚀 Evolução do projeto
> Em breve
