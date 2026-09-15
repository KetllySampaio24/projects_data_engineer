# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %run ../../config/parameters

# COMMAND ----------

# Define o ambiente que será utilizado
dbutils.widgets.dropdown("env","hom",["hom", "prd"])
env = dbutils.widgets.get("env")

# COMMAND ----------

silver_schema = "silver"

spark.sql(f"""
    CREATE SCHEMA IF NOT EXISTS {catalog}.{silver_schema}
    COMMENT 'Schema da camada Silver do e-commerce'
""")

# COMMAND ----------

spark.sql(f"""
    CREATE TABLE IF NOT EXISTS {catalog}.silver.ecommerce_orders (
        order_id                STRING        COMMENT 'ID único do pedido.',
        customer_id             STRING        COMMENT 'ID único do cliente.',
        shipping_address_id     STRING        COMMENT 'ID único do endereço de envio.',
        order_date               DATE          COMMENT 'Data em que o pedido foi realizado.',
        status                   STRING        COMMENT 'Status do pedido: Concluído, Enviado, Cancelado e Em Processamento.',
        total_amount             DECIMAL(10,2) COMMENT 'Valor total do pedido.'
    )
    USING DELTA
    COMMENT 'Tabela de pedidos de e-commerce da camada Silver'
""")