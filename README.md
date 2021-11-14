# Tarea 2

En esta tarea se estudiran conceptos relacionados al curso Sistemas distribuidos, implementando un sistema de streaming de eventos distribuidos usando Apache Kafka.

Integrantes: Diego Venegas, Andres Daille, Marcelo Luengo.


# La instalacion de Kafka
Cear carpeta para trabajar:
```
mkdir KAFKA_HOME
```
Dentro de la carpeta creada:
```
wget https://downloads.apache.org/kafka/2.8.1/kafka_2.13-2.8.1.tgz 
```

```
tar -xzf kafka_2.13-2.8.1.tgz 
```

Se destaca que se tiene que estar dentro del archivo kafka_home.sh, por consiguiente se levantan los servicios de Zookeeper, donde se ejecuta el archivo Zookeeper_run y se corre con el siguiente comando:
```
zsh zookeeper_run.sh
```

