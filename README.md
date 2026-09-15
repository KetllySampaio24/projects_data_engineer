# 🛠️ Projects Data Engineer

Repositório de estudo e prática em **Engenharia de Dados**, criado para
aplicar e aprimorar conhecimentos em tratamento de dados, modelagem,
arquitetura de dados e boas práticas de mercado — usando um cenário
realista de e-commerce como base.

## 🎯 Objetivo do projeto

Este repositório documenta a construção de um pipeline de dados completo,
do dado bruto até métricas de negócio prontas para consumo, com foco em:

- **Modelagem de dados** (relacional/transacional e dimensional)
- **Tratamento e qualidade de dados** (Data Quality)
- **Arquitetura Medallion** (Bronze → Silver → Gold)
- **Boas práticas de engenharia**: separação de ambientes (hom/prd),
  documentação de tabelas/colunas, uso combinado de SQL e PySpark,
  versionamento com Git/GitHub e organização de código em notebooks

O dataset utilizado é **sintético** (gerado artificialmente), simulando
um sistema transacional (OLTP) de e-commerce.

## 🏗️ Arquitetura

```
Dados brutos (CSV)
       │
       ▼
   🥉 BRONZE   → cópia fiel do dado de origem, sem transformação
       │           + metadados de rastreabilidade (ingestion_timestamp,
       │             source_file, ambiente)
       ▼
   🥈 SILVER   → dados limpos e validados (tipos corretos, sem
       │           duplicados, regras de negócio verificadas)
       ▼
   🥇 GOLD     → tabelas analíticas prontas para consumo
                  (métricas de negócio, agregações)
```

Cada camada é organizada por **ambiente** (`hom` e `prd`), usando catalogs
separados no Unity Catalog (`ecommerce_hom` e `ecommerce_prd`), simulando
como isso funciona em um cenário real de produção.

## 🚧 Status do projeto

- [x] Camada Bronze (ingestão com seleção de ambiente hom/prd)
- [x] Camada Silver (limpeza e validação de dados)
- [ ] Camada Gold (métricas de negócio)

## 📐 Resumo das tabelas do transacional (origem)

O conjunto de dados simula o transacional de um e-commerce, com **8
tabelas relacionadas entre si**:

| Tabela         | O que representa                                                        | Relaciona-se com               |
|----------------|--------------------------------------------------------------------------|---------------------------------|
| `categories`   | Categorias de produtos (ex: Eletrônicos, Moda Feminina)                 | `products`                      |
| `customers`    | Clientes cadastrados (nome, e-mail, data de cadastro, etc.)              | `addresses`, `orders`, `reviews`|
| `addresses`    | Endereços de entrega/cobrança dos clientes (um cliente pode ter mais de um) | `customers`, `orders`        |
| `products`     | Catálogo de produtos (nome, preço, custo, estoque)                       | `categories`, `order_items`, `reviews` |
| `orders`       | Pedidos realizados pelos clientes (data, status, valor total)            | `customers`, `addresses`, `order_items`, `payments`, `reviews` |
| `order_items`  | Itens de cada pedido (produto, quantidade, desconto, valor da linha)     | `orders`, `products`            |
| `payments`     | Pagamentos associados a cada pedido (método, status, possíveis reprocessos) | `orders`                      |
| `reviews`      | Avaliações de produtos feitas pelos clientes após a compra               | `customers`, `products`, `orders` |


## 📁 Estrutura do repositório

```
projects_data_engineer/
├── bronze_layer/
│   └── 01_bronze_ingestion.py     # Notebook de ingestão (env: hom/prd)
├── silver_layer/                  # (em construção)
├── gold_layer/                    # (em construção)
└── README.md
```

## 🧰 Stack utilizada

- **Databricks** (Unity Catalog, Volumes, Delta Lake)
- **PySpark** + **SQL** (Spark SQL, combinando as duas abordagens)
- **Python** (geração do dataset sintético com Faker)
- **Git/GitHub** (versionamento, branches por feature, Pull Requests)

## 📝 Notas

- Este é um projeto de estudo com fins de portfólio — os dados são
  100% fictícios.
- O objetivo é simular, o mais próximo possível, o dia a dia de um
  Engenheiro de Dados Júnior: ingestão, transformação, validação e
  entrega de dados confiáveis para o negócio.
