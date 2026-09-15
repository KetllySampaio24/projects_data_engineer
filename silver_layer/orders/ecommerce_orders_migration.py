# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
dbutils.widgets.dropdown("env", "hom", ["hom", "prd"], "Ambiente")
env = dbutils.widgets.get("env")
 
ENV_CONFIG = {
    "hom": {
        "catalog": "ecommerce_hom",
        "volume_path": "/Volumes/ecommerce/default/bronze",
    },
    "prd": {
        "catalog": "ecommerce_prd",
        "volume_path": "/Volumes/ecommerce/default/bronze",
    },
}
 
config = ENV_CONFIG[env]
catalog = config["catalog"]
volume_path = config["volume_path"]
silver_schema = "silver"

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
