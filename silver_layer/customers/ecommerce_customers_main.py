# Databricks notebook source
# Define o ambiente que será utilizado
dbutils.widgets.dropdown("env","hom",["hom", "prd"])
env = dbutils.widgets.get("env")

# COMMAND ----------

# MAGIC %run ../../config/parameters

# COMMAND ----------

# MAGIC %run ./ecommerce_customers_function

# COMMAND ----------

bronze_table = f"{catalog}.bronze.customers"
silver_table = f"{catalog}.{silver_schema}.ecommerce_customers"
df_bronze = spark.table(bronze_table) # Lendo os dados da Bronze
df_silver = transform_customers(df_bronze)

# COMMAND ----------

(
    df_silver
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(silver_table)
)