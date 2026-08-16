from pyspark.sql.types import *
from pyspark.sql.functions import *

#ADLS configuration 
spark.conf.set(
  "fs.azure.account.key.hospadbstorageaccount.dfs.core.windows.net",
  dbutils.secrets.get(scope="hospitalanalyticsvaultscope", key="storge-account-connection")
)

#Define bronze and silver path
bronze_path = "abfss://bronze@hospadbstorageaccount.dfs.core.windows.net/patient_data"
silver_path = "abfss://silver@hospadbstorageaccount.dfs.core.windows.net/patient_data"

#read from bronze
bronze_df = (
    spark.readStream
    .format("delta")
    .load(bronze_path)
)

#Define Schema
schema = StructType([
    StructField("patient_id", StringType()),
    StructField("gender", StringType()),
    StructField("age", IntegerType()),
    StructField("department", StringType()),
    StructField("admission_time", StringType()),
    StructField("discharge_time", StringType()),
    StructField("bed_id", IntegerType()),
    StructField("hospital_id", IntegerType())
])

#Parse it to dataframe
parsed_df = bronze_df.withColumn("data",from_json(col("raw_json"),schema)).select("data.*")

#convert type to Timestamp
clean_df = parsed_df.withColumn("admission_time", to_timestamp("admission_time"))
clean_df = clean_df.withColumn("discharge_time", to_timestamp("discharge_time"))

#invalid admission_times
clean_df = clean_df.withColumn("admission_time",
                               when(
                                   col("admission_time").isNull() | (col("admission_time") > current_timestamp()),
                                   current_timestamp())
                               .otherwise(col("admission_time")))


#Handle Invalid Age
clean_df = clean_df.withColumn("age",
                               when(col("age")>100,floor(rand()*90+1).cast("int"))
                               .otherwise(col("age"))
                               )

#schema evolution
expected_cols = ["patient_id", "gender", "age", "department", "admission_time", "discharge_time", "bed_id", "hospital_id"]

for col_name in expected_cols:
    if col_name not in clean_df.columns:
        clean_df = clean_df.withColumn(col_name, lit(None))

# Write stream to silver
(
    clean_df
    .writeStream
    .format("delta")
    .outputMode("append")
    .option("mergeSchema", "true")
    .option("checkpointLocation", f"{silver_path}/_checkpoints/patient_flow")
    .start(silver_path)
)

#verifying silver path
df = spark.read.format("delta").load(silver_path)
display(df)