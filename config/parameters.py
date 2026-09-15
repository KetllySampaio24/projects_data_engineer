# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# Ambiente atual da execução
dbutils.widgets.dropdown(
    "env",
    "hom",
    ["hom", "prd"],
    "Ambiente"
)

env = dbutils.widgets.get("env")

# COMMAND ----------

ENV_CONFIG = {
    "hom": {
        "catalog": "ecommerce_hom",
        "bronze_schema": "bronze",
        "silver_schema": "silver",
        "gold_schema": "gold",
        "volume_path": "/Volumes/ecommerce/default/bronze"
    },

    "prd": {
        "catalog": "ecommerce_prd",
        "bronze_schema": "bronze",
        "silver_schema": "silver",
        "gold_schema": "gold",
        "volume_path": "/Volumes/ecommerce/default/bronze"
    }
}

# COMMAND ----------

config = ENV_CONFIG[env]

# COMMAND ----------

catalog = config["catalog"]

bronze_schema = config["bronze_schema"]
silver_schema = config["silver_schema"]
gold_schema = config["gold_schema"]

volume_path = config["volume_path"]

# COMMAND ----------

# MAGIC %md
# MAGIC # HASH

# COMMAND ----------

from pyspark.sql.functions import (col, concat_ws, hash, hex, to_date, trim, when, pmod, lpad, lit)

# COMMAND ----------

def generate_hash(*columns):

    hash_value = hash(
        concat_ws(
            "||",
            *[col(column) for column in columns]
        )
    )

    return lpad(
        hex(
            pmod(
                hash_value.cast("long"),
                lit(4294967296)
            )
        ),
        8,
        "0"
    )