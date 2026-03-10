from pyspark.sql import SparkSession, DataFrame


def try_dataframe(spark: SparkSession) -> DataFrame:
    data = [
        (1, "Alice", 34),
        (2, "Bob", 45),
        (3, "Carol", 29),
        (4, "Dave", 52),
    ]
    return spark.createDataFrame(data, schema=["id", "name", "age"])
