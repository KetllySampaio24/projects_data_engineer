# Databricks notebook source
# MAGIC %run ../../config/parameters
# MAGIC

# COMMAND ----------

# Define o ambiente que será utilizado
dbutils.widgets.dropdown("env","hom",["hom", "prd"])
env = dbutils.widgets.get("env")

# COMMAND ----------

spark.sql(f"""
CREATE TABLE IF NOT EXISTS {catalog}.{silver_schema}.ecommerce_customers (

    ecommerce_customer_id    STRING    COMMENT 'ID único do Cliente cadastrado',
    customer_id              STRING    COMMENT 'ID único do Cliente.',
    name                     STRING    COMMENT 'Nome do Cliente',
    email                    STRING    COMMENT 'E-mail do Cliente.',
    phone                    STRING       COMMENT 'Telefone do Cliente.',
    created_at               DATE      COMMENT 'Data da criação do cadastro',
    birth_date               DATE      COMMENT 'Data de nascimento do Cliente.'

)
USING DELTA
COMMENT 'Tabela de cadastro dos Clientes da camada Silver'
""")