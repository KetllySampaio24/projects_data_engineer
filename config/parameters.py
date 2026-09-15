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
        "volume_path": "/Volumes/ecommerce/default/bronze"
    },
    "prd": {
        "catalog": "ecommerce_prd",
        "volume_path": "/Volumes/ecommerce/default/bronze"
    }
}


# COMMAND ----------

config = ENV_CONFIG[env]

catalog = config["catalog"]
volume_path = config["volume_path"]

bronze_schema = "bronze"
silver_schema = "silver"
gold_schema = "gold"


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