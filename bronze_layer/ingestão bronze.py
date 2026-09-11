# Databricks notebook source
dbutils.widgets.dropdown("env", "hom", ["hom", "prd"], "Ambiente")
env = dbutils.widgets.get("env")

# COMMAND ----------

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
bronze_schema = "bronze"
 
print(f"Catalog:      {catalog}")
print(f"Schema:       {bronze_schema}")
print(f"Volume path:  {volume_path}")

# COMMAND ----------

spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{bronze_schema}")

# COMMAND ----------

from pyspark.sql import functions as F
 
TABLES = [
    "categories",
    "customers",
    "addresses",
    "products",
    "orders",
    "order_items",
    "payments",
    "reviews",
]

# COMMAND ----------


def ingest_table(table_name: str) -> None:
    file_path = f"{volume_path}/{table_name}.csv"
    target_table = f"{catalog}.{bronze_schema}.{table_name}"
 
    print(f"Lendo {file_path} ...")
    df = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(file_path)
    )
 
    df_with_metadata = (
        df.withColumn("_ingestion_timestamp", F.current_timestamp())
        .withColumn("_source_file", F.col("_metadata.file_path"))
        .withColumn("_env", F.lit(env))
    )
 
    row_count = df_with_metadata.count()
 
    (
        df_with_metadata.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(target_table)
    )
 
    print(f"  -> {target_table}: {row_count} linhas gravadas\n")
 

# COMMAND ----------


def ingest_table(table_name: str) -> None:
    file_path = f"{volume_path}/{table_name}.csv"
    target_table = f"{catalog}.{bronze_schema}.{table_name}"
 
    print(f"Lendo {file_path} ...")
    df = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(file_path)
    )
 
    df_with_metadata = (
        df.withColumn("_ingestion_timestamp", F.current_timestamp())
        .withColumn("_source_file", F.col("_metadata.file_path"))
        .withColumn("_env", F.lit(env))
    )
 
    row_count = df_with_metadata.count()
 
    (
        df_with_metadata.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(target_table)
    )
 
    print(f"  -> {target_table}: {row_count} linhas gravadas\n")
 

# COMMAND ----------

results = []
 
for table in TABLES:
    try:
        ingest_table(table)
        results.append((table, "sucesso"))
    except Exception as e:
        print(f"  ERRO ao ingerir {table}: {e}\n")
        results.append((table, f"falha: {e}"))

# COMMAND ----------

summary_df = spark.createDataFrame(results, ["tabela", "status"])
display(summary_df)

# COMMAND ----------

for table in TABLES:
    target_table = f"{catalog}.{bronze_schema}.{table}"
    try:
        count = spark.table(target_table).count()
        print(f"{target_table}: {count} linhas")
    except Exception as e:
        print(f"{target_table}: não foi possível ler ({e})")