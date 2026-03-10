from pyspark.sql import SparkSession
from local_pyspark import try_dataframe

spark = SparkSession.builder.appName("example").master("local[*]").getOrCreate()
spark.sparkContext.setLogLevel("INFO")

df = try_dataframe(spark)
df.show()

spark.stop()
