from pyspark.sql.functions import *

# Azure Event Hub Configuration
event_hub_namespace = "adb-eventhub-ns.servicebus.windows.net"
event_hub_name = "hospital-adb-eventhub"
event_hub_conn_str = dbutils.secrets.get(scope="hospitalanalyticsvaultscope", key="eventhub-connection")

kafka_options = {
    'kafka.bootstrap.servers': f"{event_hub_namespace}:9093",
    'subscribe': event_hub_name,
    'kafka.security.protocol': 'SASL_SSL',
    'kafka.sasl.mechanism': 'PLAIN',
    'kafka.sasl.jaas.config': f'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username="$ConnectionString" password="{event_hub_conn_str}";',
    'startingOffsets': 'latest',
    'failOnDataLoss': 'false'
}

# Read raw streaming data from Event Hub via Kafka-compatible endpoint
raw_df = (spark.readStream
          .format("kafka")
          .options(**kafka_options)
          .load()
          )

#Cast data to json
json_df = raw_df.selectExpr("CAST(value AS STRING) as raw_json")

#ADLS configuration 
spark.conf.set(
  "fs.azure.account.key.hospadbstorageaccount.dfs.core.windows.net",
  dbutils.secrets.get(scope="hospitalanalyticsvaultscope", key="storge-account-connection")
)

bronze_path = "abfss://bronze@hospadbstorageaccount.dfs.core.windows.net/patient_data"

# Write stream to bronze
(
    json_df
    .writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", f"{bronze_path}/_checkpoints/patient_flow")
    .start(bronze_path)
)
# Verifying data rather than from azure containers
spark.conf.set(
    "fs.azure.account.key.hospadbstorageaccount.dfs.core.windows.net",
    dbutils.secrets.get(scope="hospitalanalyticsvaultscope", key="storge-account-connection")
)

df = spark.read.format("delta").load("abfss://bronze@hospadbstorageaccount.dfs.core.windows.net/patient_data")
display(df)gi