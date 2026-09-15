# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %run ../../config/parameters

# COMMAND ----------

# MAGIC %run ./ecommerce_orders_function

# COMMAND ----------

# Define o ambiente que será utilizado
dbutils.widgets.dropdown("env","hom",["hom", "prd"])
env = dbutils.widgets.get("env")

# COMMAND ----------

# Envia os dados da Bronze para a função de transformação
df_silver = transform_orders(df_bronze)


# COMMAND ----------

# Grava os dados transformados na tabela Silver
(
    df_silver
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(silver_table)
)