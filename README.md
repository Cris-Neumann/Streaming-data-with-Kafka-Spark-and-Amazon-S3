<h1 align="center"> Streaming data en tiempo real con Apache Kafka, Spark y Amazon S3 </h1>

## Índice

- [Resumen del proyecto](#Resumen-del-proyecto)
- [Arquitectura empleada](#Arquitectura-empleada)
- [Instalaciones adicionales](#Instalaciones-adicionales)

## Resumen del proyecto
Este proyecto de streaming data en tiempo real consume información desde la API pública "Open Notify", desde la página web http://open-notify.org/, que transmite la posición de la estación espacial internacional cada 5 segundos, y dichos datos son transmitidos usando la tecnología de mensajería Apache Kafka, el cual canaliza mensajes hacia Apache Spark para ser procesados, modificado sus formatos y posteriormente almacenados en la nube de AWS, utilizando el servicio Amazon Simple Storage Service (Amazon S3) y guardando la data en formato parquet.

## Arquitectura empleada
El esquema general del modo en que se relacionan las partes del sistema es el siguiente:
<br/><br/>

![streaming_data_kafka_spark_S3](https://github.com/Cris-Neumann/Streaming-data-with-Kafka-Spark-and-Amazon-S3/assets/99703152/6ac753d1-a994-4223-b315-69f56adcbf1c)

## Instalaciones adicionales
Adicional a las librerías detallas en archivo requirements.txt, es necesario instalar el conector ODBC (Open Database Connectivity) para SQL Server: ODBC Driver 18: https://acortar.link/lsyUnp.
