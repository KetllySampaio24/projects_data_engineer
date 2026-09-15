# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
from pyspark.sql.functions import (col, to_date, trim, when)

# COMMAND ----------

def transform_orders(df):

    df_silver = (
        df
        .withColumn(
            "order_id",
            generate_hash(
                "order_id",
                "customer_id",
                "order_date",
                "shipping_address_id"
            )
        )
        .withColumn(
            "customer_id",
            col("customer_id").cast("string")
        )
        .withColumn(
            "shipping_address_id",
            col("shipping_address_id").cast("string")
        )
        .withColumn(
            "order_date",
            to_date(col("order_date"))
        )
        .withColumn(
            "status",
            when(trim(col("status")) == "processing", "Em Processamento")
            .when(trim(col("status")) == "completed", "Concluído")
            .when(trim(col("status")) == "shipped", "Enviado")
            .when(trim(col("status")) == "recusad", "Recusado")
            .otherwise("Status Desconhecido")
        )
        .withColumn(
            "total_amount",
            col("total_amount").cast("decimal(10,2)")
        )
        .select(
            "order_id",
            "customer_id",
            "shipping_address_id",
            "order_date",
            "status",
            "total_amount"
        )
    )

    return df_silver