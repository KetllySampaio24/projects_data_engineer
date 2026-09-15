# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
from pyspark.sql.functions import (col, concat_ws, trim, when)

# COMMAND ----------

def transform_customers(df):

    df_silver = (
        df
        .withColumn(
            "ecommerce_customer_id",
            generate_hash(
                "customer_id",
                "birth_date"
            )
        )
        .withColumn(
            "customer_id",
            col("customer_id").cast("string")
        )
        .withColumn(
            "name",
            concat_ws(
                " ",
                col("first_name"),
                col("last_name")
            )
        )
        .withColumn(
            "email",
            col("email").cast("string")
        )
        .withColumn(
            "phone",
            col("phone").cast("string")
        )
        .withColumn(
            "created_at",
            to_date(col("signup_date"))
        )
        .withColumn(
            "birth_date",
            to_date(col("birth_date"))
        )
        .select(
            "ecommerce_customer_id",
            "customer_id",
            "name",
            "email",
            "phone",
            "created_at",
            "birth_date"
        )
    )

    return df_silver