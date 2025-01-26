# BigdataProject
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
# Use in administrator as the above ports wont be available
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
My container ID 422b17bd68e240f6c4c30c5554527269411314c5d6454696d596925d24b14969 and run to root and from root to hdfs
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

Finding Highest and Lowest Review Scores
Create a directory, for instance, /home/scripts and navigate to this directory using cd /home/scripts command. Create the Mapper touch mapper.py and Reducer touch reducer.py and change their permission:
````bash
chmod 777 mapper.py reducer.py
````
Open mapper in nano editor:
````bash
nano mapper.py
````
and add the following code:
````bash
#!/usr/bin/env python
import sys
import csv
for line in sys.stdin:
    try:
        reader = csv.reader([line])
        for row in reader:
            review_score = row[6]

            if review_score:
                print('{0}'.format(review_score))
    except Exception as e:
        sys.stderr.write("Error processing line: {0} - {1}\n".format(line, str(e)))
        continue
````
````bash
nano reducer.py
````
and added the below code:
````
#!/usr/bin/env python
import sys
highest_score = float('-inf')
lowest_score = float('inf')
for line in sys.stdin:
    line = line.strip()
    try:
        score = float(line)
        if score > highest_score:
            highest_score = score
        if score < lowest_score:
            lowest_score = score
    except ValueError:

        sys.stderr.write("Skipping invalid score: {0}\n".format(line))
        continue

print('Highest Score: {0}'.format(highest_score))
print('Lowest Score: {0}'.format(lowest_score))
Press ctrl+x, type Y and press enter to close nano.
````
After adding the codes to local scripts we need to make sure the input file is also added to the home scripts
````
hadoop fs -get /home/datasrc/bigDataTask/Books_rating.csv /home/scripts/
````

Submited the MapReduce Job to YARN
````
hadoop jar /usr/local/hadoop-2.9.2/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar \
    -D mapreduce.job.name="FindHighestAndLowestReviewScores" \
    -input /home/datasrc/bigDataTask/Books_rating.csv \
    -output /home/dataout \
    -mapper /home/scripts/mapper.py \
    -reducer /home/scripts/reducer.py \
````
Submited the MapReduce Job to YARN to see the job running time
````
time hadoop jar /usr/local/hadoop-2.9.2/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar \
    -D mapreduce.job.name="FindHighestAndLowestReviewScores" \
    -input /home/datasrc/bigDataTask/Books_rating.csv/Books_rating.csv \
    -output /home/dataout \
    -mapper /home/scripts/mapper.py \
    -reducer /home/scripts/reducer.py
````


View the Results
````
hadoop fs -cat /home/dataout/part-00000
````
Important

I tested my scripts mapper.py and reducer.py locally before i submit it to the YARN, and ensure that it works as expected.
````
cat /home/datasrc/bigDataTask/Books_rating.csv | python /home/scripts/mapper.py
and

cat /home/datasrc/bigDataTask/Books_rating.csv | python /home/scripts/reducer.py
````














