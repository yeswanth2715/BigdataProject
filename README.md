# BigdataProject with Docker Desktop
Run the following command in my terminal to pull the Hadoop Docker image:
````bash
docker pull suhotayan/hadoop-spark-pig-hive:2.9.2 
````
Step 1: Create container
Execute the following command in the same terminal window where you pulled the image:
````bash
docker run -it --name myhadoop \
    -p 9000:9000 -p 2122:2122 -p 50070:50070 \
    -p 50010:50010 -p 50075:50075 -p 50020:50020 \
    -p 50090:50090 -p 8040:8040 -p 8042:8042 \
    -p 8080:8080 -p 8081:8081 -p 10000:10000 \
    -p 9083:9083 suhotayan/hadoop-spark-pig-hive:2.9.2 bash
````
Use in administrator as the above ports wont be available
````bash

net stop winnat
hdfs namenode -format
nano ~/.bashrc

export HADOOP_HOME=/usr/local/hadoop
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
source ~/.bashrc

````

Step 2: Prepare the Dataset
Download and unzip the  retail store dataset on your local machine.

Step 3: Copy the Dataset to Docker

For eg container ID 422b17bd68e240f6c4c30c5554527269411314c5d6454696d596925d24b14969 and run to root and from root to hdfs
Copy the File to the Docker Container: Use the docker cp command to copy the file into the container.

````
docker cp "D:\Chrome Downloads\retailstore_large\retailstore_large.csv" myhadoop:/root/
ls /root/
````

Step 4: Upload the Dataset to HDFS
Create a directory in HDFS: I created first with home/datasrc and then proceeded with bigdatatask and added the file into the hdfs
````bash
hadoop fs -mkdir -p /home/datasrc/bigDataTask
hadoop fs -put /root/retailstore_large.csv /home/datasrc/bigDataTask

````
Upload the file to HDFS:

````bash

hadoop fs -put retailstore_large.csv /home/datasrc/bigDataTask
````
Verify the uploaded file:
````bash
hadoop fs -ls /home/datasrc/bigDataTask
````
File Validation
````
Check the Number of Blocks
````bash
hadoop fsck /home/datasrc/bigDataTask
````

Create a directory, for instance, /home/scripts
````
mkdir -p /home/scripts
````
and navigate to this directory using cd /home/scripts command. Create the Mapper **touch mapper.py** and Reducer **touch reducer.py** and change their permission:
````bash
chmod +x mapper.py
chmod +x reducer.py

````bash

````bash
chmod 777 mapper.py reducer.py
````
Open mapper in nano editor:
````bash
nano mapper.py
````
Implemented a sample MapReduce job to analyze the dataset. This job calculates the minimum and maximum salaries from the dataset. The following Python scripts were used: and add the following code:
````bash
#!/usr/bin/env python
import sys
import csv

for line in sys.stdin:
    try:
        reader = csv.reader([line])
        for row in reader:
            salary = row[2]  # Assuming column 2 contains the salary
            if salary:
                print(f"{salary}")
    except Exception as e:
        sys.stderr.write(f"Error processing line: {line} - {str(e)}\n")
        continue

````
````bash
nano reducer.py
````
and added the below code:
````
#!/usr/bin/env python
import sys

highest_salary = float('-inf')
lowest_salary = float('inf')

for line in sys.stdin:
    try:
        salary = float(line.strip())
        highest_salary = max(highest_salary, salary)
        lowest_salary = min(lowest_salary, salary)
    except ValueError:
        sys.stderr.write(f"Skipping invalid salary: {line}\n")
        continue

print(f"Highest Salary: {highest_salary}")
print(f"Lowest Salary: {lowest_salary}")
````
Press ctrl+x, type Y and press enter to close nano.

verify the mapper and reducer in home scripts
````
ls -l /home/scripts
````

Submited the MapReduce Job to YARN
````
hadoop jar /usr/local/hadoop-2.9.2/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar \
    -D mapreduce.job.name="FindHighestAndLowestSalaries" \
    -input /home/datasrc/bigDataTask/retailstore_large.csv \
    -output /home/dataout \
    -mapper "python3 /home/scripts/mapper.py" \
    -reducer "python3 /home/scripts/reducer.py"
````
Submited the MapReduce Job to YARN to see the job running time
````
time hadoop jar /usr/local/hadoop-2.9.2/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar -D mapreduce.job.name="FindHighestAndLowestSalaries" -input /home/datasrc/bigDataTask/retailstore_large.csv -output /home/dataout -mapper "python3 /home/scripts/mapper.py" -reducer "python3 /home/scripts/reducer.py"

````
View the Results
````
hadoop fs -cat /home/dataout/part-00000
````
Important

I tested my scripts mapper.py and reducer.py locally before i submit it to the YARN, and ensure that it works as expected.
````
cat /home/datasrc/bigDataTask/retailstore_large.csv | python3 /home/scripts/mapper.py
````
and
````
cat /home/datasrc/bigDataTask/retailstore_large.csv | python3 /home/scripts/reducer.py
````
To view the output of reducer, better to use below syntax
````
echo -e "35000\n37000\n39000\n17600" | python3 /home/scripts/reducer.py
````

Next i proceeded with Spark job e.g displaying data, filtering based on salary, and calculating average salary by country

Created python file
````
touch spark_job.py
````
To make it executable, i used chmod
````
chmod +x spark_job.py
````
entered the code with nano
````
nano spark_job.py
````
add this code
````
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
````

Run the job with time function
````
time spark-submit spark_job.py
````
















