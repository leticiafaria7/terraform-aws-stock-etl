import sys
import logging
import boto3
from datetime import datetime
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame

# =========================
# CONFIG
# =========================
args = getResolvedOptions(sys.argv, ['RAW_PATH', 'REFINED_PATH'])

RAW_PATH = args['RAW_PATH']
REFINED_PATH = args['REFINED_PATH']

DATABASE = "db_refined"
TABLE = "ativos_ibov_fp"

# =========================
# LOGGING
# =========================
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# =========================
# CONTEXT
# =========================
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

s3 = boto3.client('s3')

def get_processed_dates():
    try:
        path = REFINED_PATH.replace("s3://", "")
        bucket, prefix = path.split("/", 1)

        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

        datas = set()
        if "Contents" in response:
            for obj in response["Contents"]:
                key = obj["Key"]
                if "data=" in key:
                    data = key.split("data=")[1].split("/")[0]
                    datas.add(data)

        return datas

    except Exception as e:
        logger.error(f"Erro ao listar datas processadas: {e}")
        return set()

try:
    logger.info("Lendo dados RAW...")

    # lê todas as tabelas parquet dessa pasta e já concatena
    df = spark.read.parquet(RAW_PATH)
    logger.info(df.printSchema())

    df = df.select("date", "codigo", "price")

    df = df.withColumnRenamed("date", "data_hora") \
           .withColumnRenamed("codigo", "ticker")

    df = df.withColumn("data_hora", to_timestamp("data_hora"))
    df = df.withColumn("data", to_date("data_hora"))
    df = df.withColumn("weekday", date_format("data", "EEEE"))

    # =========================
    # FILTRAR DIAS JÁ PROCESSADOS
    # =========================
    processed_dates = get_processed_dates()

    if processed_dates:
        logger.info(f"Datas já processadas: {processed_dates}")
        df = df.filter(~col("data").isin(list(processed_dates)))

    if df.limit(1).count() == 0:
        logger.info("Nenhum dado novo para processar.")
        sys.exit(0)

    # =========================
    # ABERTURA / FECHAMENTO
    # =========================
    window_asc = Window.partitionBy("ticker", "data").orderBy("data_hora")
    window_desc = Window.partitionBy("ticker", "data").orderBy(col("data_hora").desc())

    abertura = df.withColumn("rn", row_number().over(window_asc)) \
                 .filter(col("rn") == 1) \
                 .select("ticker", "data", col("price").alias("abertura_dia"))

    fechamento = df.withColumn("rn", row_number().over(window_desc)) \
                   .filter(col("rn") == 1) \
                   .select("ticker", "data", col("price").alias("fechamento_dia"))

    # =========================
    # AGREGAÇÃO
    # =========================
    df_summary = df.groupBy("ticker", "data", "weekday").agg(
        count("data_hora").alias("qtd_leituras_dia"),
        min("price").alias("price_min"),
        max("price").alias("price_max"),
        avg("price").alias("price_mean"),
        expr("percentile(price, 0.5)").alias("price_median"),
        stddev("price").alias("price_std")
    )

    # =========================
    # JOIN + VARIAÇÃO
    # =========================
    df_summary = df_summary.join(abertura, ["ticker", "data"], "left") \
                           .join(fechamento, ["ticker", "data"], "left")

    df_summary = df_summary.withColumn(
        "variacao_dia",
        round((col("fechamento_dia") - col("abertura_dia")) * 100 / col("abertura_dia"), 2)
    )

    # =========================
    # SEMANA
    # =========================
    window_week = Window.partitionBy("ticker", "weekday").orderBy("data")

    df_summary = df_summary.withColumn("n_semana", row_number().over(window_week))

    df_summary = df_summary.withColumn(
        "valor_min_semana",
        min("price_min").over(Window.partitionBy("ticker", "n_semana"))
    ).withColumn(
        "valor_max_semana",
        max("price_max").over(Window.partitionBy("ticker", "n_semana"))
    )

    # =========================
    # WRITE + DATA CATALOG
    # =========================
    logger.info("Salvando dados refinados e atualizando Data Catalog...")

    dyf = DynamicFrame.fromDF(df_summary, glueContext, "dyf")

    glueContext.write_dynamic_frame.from_options(
        frame=dyf,
        connection_type="s3",
        connection_options={
            "path": REFINED_PATH,
            "partitionKeys": ["data"]
        },
        format="parquet"
    )

    glueContext.write_dynamic_frame.from_catalog(
        frame=dyf,
        database=DATABASE,
        table_name=TABLE,
        additional_options={
            "enableUpdateCatalog": True,
            "partitionKeys": ["data"]
        }
    )
    
    spark.sql(f"MSCK REPAIR TABLE {DATABASE}.{TABLE}")

    logger.info("Job finalizado com sucesso!")

except Exception as e:
    logger.error(f"Erro no job: {str(e)}")
    raise