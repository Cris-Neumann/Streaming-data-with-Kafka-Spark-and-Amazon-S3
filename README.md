<h1 align="center"> Streaming data en tiempo real con Apache Kafka, Spark y Amazon S3 </h1>

## Índice

- [Resumen del proyecto](#Resumen-del-proyecto)
- [Arquitectura empleada](#Arquitectura-empleada)

## Resumen del proyecto
Este proyecto de stremaing data en tiempo real consume data desde la API pública "Open Notify", desde la página web http://open-notify.org/, que transmite información sobre la posición de la estación espacial internacional cada 5 segundos, y dichos datos son transmitidos usando la tecnología de mensajería Apache Kafka, el cual canaliza mensajes hacia Apache Spark para ser procesados, modificado sus formatos y posteriormente almacenados en Amazon S3.

## Arquitectura empleada
El esquema general del modo en que se relacionan las partes del sistema es el siguiente:
<br/><br/>

![streaming_data_kafka_spark_S3](https://github.com/Cris-Neumann/Streaming-data-with-Kafka-Spark-and-Amazon-S3/assets/99703152/6ac753d1-a994-4223-b315-69f56adcbf1c)
