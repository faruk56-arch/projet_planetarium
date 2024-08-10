from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StringType, FloatType, IntegerType, StructField
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline

# Creer la session Spark
spark = SparkSession.builder \
    .appName("PlanetDiscoveryProcessor") \
    .config("spark.master", "local[*]") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .enableHiveSupport() \
    .getOrCreate()

# Schema pour les donnees JSON
schema = StructType([
    StructField("Name", StringType(), True),
    StructField("Num_Moons", IntegerType(), True),
    StructField("Minerals", IntegerType(), True),
    StructField("Gravity", FloatType(), True),
    StructField("Sunlight_Hours", FloatType(), True),
    StructField("Temperature", FloatType(), True),
    StructField("Rotation_Time", FloatType(), True),
    StructField("Water_Presence", IntegerType(), True),
    StructField("Colonisable", IntegerType(), True)
])

# Lecture des donnees de Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "topic_1") \
    .load()

# Convertir les valeurs des messages Kafka en JSON et les transformer en DataFrame
df = df.selectExpr("CAST(value AS STRING)", "timestamp") \
    .select(from_json(col("value"), schema).alias("data"), col("timestamp")) \
    .select("data.*", "timestamp")

# Ajouter un watermark base sur le champ temporel
df_with_watermark = df.withWatermark("timestamp", "10 minutes")

# 1. Calcul de la moyenne de la gravite des planetes par fenetre de temps
average_gravity = df_with_watermark \
    .groupBy(window(col("timestamp"), "10 minutes")) \
    .avg("Gravity") \
    .alias("average_gravity")

average_gravity_query = average_gravity.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "/user/spark/average_gravity") \
    .option("checkpointLocation", "/user/spark/average_gravity_checkpoint") \
    .start()

# 2. Distribution du nombre de lunes des planetes par fenetre de temps
moon_distribution = df_with_watermark \
    .groupBy(window(col("timestamp"), "10 minutes"), col("Num_Moons")) \
    .count() \
    .alias("moon_distribution")

moon_distribution_query = moon_distribution.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "/user/spark/moon_distribution") \
    .option("checkpointLocation", "/user/spark/moon_distribution_checkpoint") \
    .start()

# 3. Analyse des correlations entre les caracteristiques des planetes
corr_gravity_water = df_with_watermark.stat.corr("Gravity", "Water_Presence")
corr_temperature_water = df_with_watermark.stat.corr("Temperature", "Water_Presence")
print(f"Correlation entre la gravite et la presence d'eau : {corr_gravity_water}")
print(f"Correlation entre la temperature et la presence d'eau : {corr_temperature_water}")

# 4. Clustering des planetes selon leurs caracteristiques avec K-Means
assembler = VectorAssembler(inputCols=["Gravity", "Temperature", "Rotation_Time"], outputCol="features")
feature_df = assembler.transform(df_with_watermark)

kmeans = KMeans().setK(3).setSeed(1)
model = kmeans.fit(feature_df)

predictions = model.transform(feature_df)

# Affichage des clusters dans la console
cluster_console = predictions.select("Name", "prediction").writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# 5. Prediction de la colonisabilite des planetes avec une regression logistique
indexer = StringIndexer(inputCol="Colonisable", outputCol="label")
assembler = VectorAssembler(inputCols=["Gravity", "Temperature", "Rotation_Time", "Water_Presence"], outputCol="features")

lr = LogisticRegression(maxIter=10)
pipeline = Pipeline(stages=[indexer, assembler, lr])

model = pipeline.fit(df_with_watermark)
predictions = model.transform(df_with_watermark)

# Affichage des predictions dans la console
prediction_console = predictions.select("Name", "prediction").writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# 6. Stockage des resultats dans Hive
spark.sql("CREATE DATABASE IF NOT EXISTS planetarium")
spark.sql("USE planetarium")

average_gravity_query_hive = average_gravity.writeStream \
    .outputMode("append") \
    .format("hive") \
    .option("path", "/user/hive/warehouse/planetarium.db/average_gravity") \
    .option("checkpointLocation", "/user/spark/average_gravity_hive_checkpoint") \
    .start()

moon_distribution_query_hive = moon_distribution.writeStream \
    .outputMode("append") \
    .format("hive") \
    .option("path", "/user/hive/warehouse/planetarium.db/moon_distribution") \
    .option("checkpointLocation", "/user/spark/moon_distribution_hive_checkpoint") \
    .start()

# Attendre la fin du stream
average_gravity_query.awaitTermination()
moon_distribution_query.awaitTermination()
cluster_console.awaitTermination()
prediction_console.awaitTermination()
average_gravity_query_hive.awaitTermination()
moon_distribution_query_hive.awaitTermination()
