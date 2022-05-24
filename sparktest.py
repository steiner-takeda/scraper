import findspark
findspark.init()
from pyspark.sql import SparkSession
spark = SparkSession.builder \
.master("yarn") \
.appName("Lunch_And_Lean") \
.getOrCreate()

test = spark.sparkContext.parallelize([1,2,3,4,5,6,7]).collect()
print(test)