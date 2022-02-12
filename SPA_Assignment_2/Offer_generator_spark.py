######
#kafka console consumer to validate pushed events
#kafka-console-consumer.bat --topic pizzario_customer_offers_spark --bootstrap-server localhost:9092
######

from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
import pyspark.sql.functions as F
from pyspark.sql.types import IntegerType, StringType, ArrayType, StructType, StructField
from time import sleep
from json import dumps
from kafka import KafkaProducer

@F.udf(returnType=StringType())
def send_to_kafka(message):
    my_producer = KafkaProducer(
        bootstrap_servers = ['localhost:9092'],
        value_serializer = lambda x:dumps(x).encode('utf-8')
    )

    my_producer.send('pizzario_customer_offers_spark', value=message)
    return "sent"


Pizzario_outlets_coordinates = [('O1', 10, 15), ('O2', 25, 51) ]
@F.udf(returnType=ArrayType(StructType([StructField('outlet', StringType()), StructField('distance', IntegerType())])))
def nearest_outlets(coordinates):
    nearest_outlets = []
    for o in Pizzario_outlets_coordinates:
        distance_from_pizzario = abs(o[1] - coordinates[0]) + abs(o[2] - coordinates[1])
        if distance_from_pizzario < 30:
            nearest_outlets.append((o[0],distance_from_pizzario))
    return nearest_outlets


spark = SparkSession.builder.appName("reader-support").enableHiveSupport().getOrCreate()
sc = spark.sparkContext
sc.setLogLevel("error")

customer_segments = spark.read.option("header", "true").csv("cluster_results.csv")
offers = spark.read.json("Segments_and_offers.json")


incoming_customers = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "pizzario_customer_visit") \
    .load()

incoming_customers = incoming_customers.withColumn("parsed_message", F.from_json(F.col("value").cast("string"), 'customerid INT, coordinates Array<INT>'))
incoming_customers = incoming_customers.withColumn("customer_id", F.col("parsed_message.customerid"))
incoming_customers = incoming_customers.withColumn("nearest_outlets", nearest_outlets(F.col("parsed_message.coordinates")))

incoming_customers = incoming_customers\
    .join(customer_segments.select("customer_id","segment"), "customer_id", "left")
incoming_customers = incoming_customers.join(offers.select("segment","offer"), "segment", "left")

incoming_customers = incoming_customers.withColumn("senttoKafka",send_to_kafka(F.to_json(F.struct(incoming_customers.columns))))

query = incoming_customers \
.writeStream \
    .format("console") \
    .start()
query.awaitTermination()

