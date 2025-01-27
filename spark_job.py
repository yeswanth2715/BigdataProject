from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder.appName("FindHighestAndLowestSalaries").getOrCreate()

# Load the dataset from HDFS
data = spark.read.csv("/home/datasrc/bigDataTask/retailstore_large.csv", header=False, inferSchema=True)

# Rename columns for better readability (assuming the salary is in the third column)
data = data.withColumnRenamed("_c2", "Salary")

# Calculate the highest and lowest salaries
highest_salary = data.agg({"Salary": "max"}).collect()[0][0]
lowest_salary = data.agg({"Salary": "min"}).collect()[0][0]

# Print the results
print(f"Highest Salary: {highest_salary}")
print(f"Lowest Salary: {lowest_salary}")

# Stop the Spark session
spark.stop()