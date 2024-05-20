import logging
from pyspark.sql import SparkSession
from pyspark.sql.streaming import Trigger
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, LongType

logging.basicConfig(level=logging.INFO,format='%(asctime)s:%(funcName)s:%(levelname)s:%(message)s')
logger = logging.getLogger("spark_structured_streaming")

aws_access_key_id = 'YOUR_ACCESS_KEY_ID'
aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
s3_bucket_path = 's3a://streaming-bucket-1/parquet_files/'
checkpoint_location = 's3a://streaming-bucket-1/checkpoints/'

def create_spark_session():
    try:
        spark = SparkSession.builder\
            .appName("StructuredNetworkWordCount")\
            .config("spark.driver.host", "spark-master")\
            .config("spark.driver.port", "7077")\
            .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.1,org.apache.hadoop:hadoop-client:2.10.2")\
            .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2")\
            .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
            .config("spark.hadoop.fs.s3a.connection.maximum", 100)\
            .config("spark.hadoop.fs.s3a.fast.upload", "true")\
            .config("spark.hadoop.fs.s3a.path.style.access", "true")\
            .config("spark.hadoop.fs.s3a.impl.disable.cache", "true")\
            .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id)\
            .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key)\
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")\
            .getOrCreate()
        spark.sparkContext.setLogLevel("ERROR")
        logger.info('Spark session initialized successfully')
        return spark
    except Exception as e:
        logger.error(f"Spark session initialization failed. Error: {e}")

def connect_spark_with_kafka(spark):
    dict_schema = StructType([
        StructField("timestamp", LongType()),
        StructField("message", StringType()),
        StructField("iss_position", StructType([
            StructField("longitude", StringType()),
            StructField("latitude", StringType())]))])
    df = spark.readStream.format("kafka")\
        .option("kafka.bootstrap.servers", "kafka:9092")\
        .option("subscribe", "project_topic")\
        .option("startingOffsets", "earliest").load()
    parsed_df = df.selectExpr("CAST(value AS STRING)")\
                .select(from_json("value", dict_schema)\
                .alias("data")).select("data.*")
    result_df = parsed_df.withColumn("longitude", col("iss_position.longitude"))\
                .withColumn("latitude", col("iss_position.latitude"))\
                .drop("iss_position")
    return result_df

def start_streaming(result_df):
    logger.info("Initiating streaming process...")
    stream_query = result_df.writeStream\
                    .format("parquet")\
                    .outputMode("append")\
                    .option("path", s3_bucket_path)\
                    .trigger(Trigger.ProcessingTime("5 seconds"))
                    .option("checkpointLocation", checkpoint_location)\
                    .start()
    stream_query.awaitTermination()

def main():
    spark = create_spark_session()
    result_df = connect_spark_with_kafka(spark)
    start_streaming(result_df)

if __name__ == '__main__':
    main()
