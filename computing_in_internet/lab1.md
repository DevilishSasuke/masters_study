# Лабораторная работа 1. Сводка по технологиям больших данных. Анализ существующих решений, техноблоги

## a) Технологии по компонентам архитектуры больших данных для платформ и облачных сервисов

| Компонент архитектуры            | Hadoop Ecosystem                            | AWS                                                  | Google Cloud                                                         | Microsoft Azure                                                 | Yandex Cloud                                                 |
|:-------------------------------- |:-------------------------------------------:|:----------------------------------------------------:|:--------------------------------------------------------------------:|:---------------------------------------------------------------:|:------------------------------------------------------------:|
| **Object Storage**               | HDFS                                        | S3                                                   | Storage                                                              | Blob Storage                                                    | YOS                                                          |
| **Message queue**                | Kafka                                       | SQS                                                  | Pub/Sub                                                              | Service Bus                                                     | YMQ                                                          |
| **Data ingestion**               | Flume                                       | Kinesis                                              | Dataflow                                                             | Data Factory                                                    | Data Transfer                                                |
| **Compute engine**               | Spark                                       | EC2                                                  | GCE                                                                  | Virtual Machines                                                | Compute Cloud                                                |
| **SQL engine / MPP DB**          | Hive                                        | RDS                                                  | Cloud SQL                                                            | Synapse Analytics                                               | YDB                                                          |
| **Orchestration**                | Oozie                                       | Step Functions                                       | Composer                                                             | Kubernetes Service                                              | Kubernetees                                                  |
| **Ссылки на архитектуру систем** | [Apache Hadoop](https://hadoop.apache.org/) | [AWS Solutins](https://aws.amazon.com/ru/solutions/) | [Cloud solutions](https://cloud.google.com/solutions/data-analytics) | [Azure Solutions](https://azure.microsoft.com/en-us/solutions/) | [Y Arch](https://yandex.cloud/ru/docs/overview/architecture) |

## б) Архитектура и технологии крупной it-компании - Ozon

* **Object storage:** HDFS [1]

* **Message queue:** Kafka [1]

* **Data ingestion:** data-bus[3]

* **Compute engine:** Spark [2]

* **SQL engine:** ClickHouse [1]

* **Orchestration:** Airflow [1]

Источники:

1. [Профиль OzonTech с Хабра](https://habr.com/ru/companies/ozontech/profile/)

2. [Статья от OzonTech на Хабре](https://habr.com/ru/companies/ozontech/articles/692860/)

3. [Статья с упоминанием проекта](https://habr.com/ru/companies/ozontech/articles/749328/)
