# BigdataProject
Run the following command in my terminal to pull the Hadoop Docker image:
```bash
docker pull suhotayan/hadoop-spark-pig-hive:2.9.2

Execute this Docker command in the same window where you have pulled the image:

docker run -it --name myhadoop -p 9000:9000 -p 2122:2122 -p 50070:50070 -p 50010:50010 -p 50075:50075 -p 50020:50020 -p 50090:50090 -p 8088:8088 -p 8030:8030 -p 8031:8031 -p 8032:8032 -p 8033:8033 -p 8040:8040 -p 8042:8042 -p 8080:8080 -p 8081:8081 -p 10000:10000 -p 9083:9083 suhothayan/hadoop-spark-pig-hive:2.9.2 bash
Troubleshooting

Error: ...Ports are not available on Windows

Fix: Open a Terminal (must be run as administrator) and execute net stop winnat command

Error: The container name "/myhadoop" is already in use

Fix: Remove the container using Docker Desktop and re-run the docker run... command.











