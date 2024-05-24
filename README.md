<h1 align="center"> Streaming de datos en tiempo real con Apache Kafka, Spark y Amazon S3 </h1>

## Índice

- [Resumen del proyecto](#Resumen-del-proyecto)
- [¿Qué es Apache Kafka?](#qué-es-apache-kafka)
- [Arquitectura empleada](#Arquitectura-empleada)
- [Instalaciones adicionales](#Instalaciones-adicionales)

## Resumen del proyecto
Este proyecto de streaming de datos en tiempo real consume información desde la API pública "Open Notify" (http://open-notify.org/), que envía la posición de la estación espacial internacional cada 5 segundos, y dichos datos son transmitidos usando la tecnología de mensajería Apache Kafka (productor de mensajes), cuyos mensajes se pueden monitorear en tiempo real en la WEB UI Kafdrop (http://localhost:9000/), para posteriormente canalizarlos hacia Apache Spark (consumidor de mensajes) para ser procesados, cambiando la estructura de los archivos json anidados de origen, y posteriormente almacenados en la nube de AWS, utilizando el servicio Amazon Simple Storage Service (Amazon S3). La implementación de Apache Kafka y Spark se realizó con la tecnología de contenedores Docker y Docker Compose.

## ¿Qué es Apache Kafka?
Apache Kafka es una plataforma de procesamiento de flujos de datos distribuida y de código abierto, y se utiliza principalmente para construir pipelines de datos en tiempo real y aplicaciones de streaming de datos, como por ejemplo: monitoreo en tiempo real, análisis de logs, procesamiento de eventos, etc.

## Arquitectura empleada
El esquema general del modo en que se relacionan las partes del sistema es el siguiente:
<br/><br/>

![streaming_data_kafka_spark_S3](https://github.com/Cris-Neumann/Streaming-data-with-Kafka-Spark-and-Amazon-S3/assets/99703152/6ac753d1-a994-4223-b315-69f56adcbf1c)

## Instalaciones adicionales
Se necesitan básicamente 4 instalaciones previas para ejecutar este streaming de datos:
  1. Instalación de Docker y Docker Compose en servidor a utilizar.
  2. Crear un tópico en la WEB UI Kafdrop (o en la terminal) llamado 'project_topic', el cual funciona como intermediario de mensajes entre la API y Spark.
  3. En Amazon S3 se debe crear un bucket llamado 'streaming-bucket-1', que cuente con una carpeta en su interior llamada 'parquet_files' y otra 'checkpoints', para los 
     archivos parquet generados en el streaming y los checkpoints de respaldo en S3, respectivamente. Además, se debe poseer una access key id de AWS y una
     secret access key de AWS, para poder ingresar a la nube de Amazon Web Services. Puede instalar una versión de prueba de AWS: https://aws.amazon.com/es/free/start-your-free-trial/
  5. Al activar el productor de datos (Kafka), el consumidor (Spark) debe ejecutarse con el siguiente script:
```
     spark-submit\
      --master spark://spark-master:7077\
      --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.hadoop:hadoop-aws:3.3.1\
      --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem\
      --conf spark.hadoop.fs.s3a.access.key=YOUR_ACCESS_KEY_ID\
      --conf spark.hadoop.fs.s3a.secret.key=YOUR_SECRET_ACCESS_KEY\
      /opt/spark_scripts/spark_consumer.py
```
