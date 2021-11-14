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

# La instalacion de Python version 3.8.10

```
sudo apt install python3.8.10
```
```
sudo apt-get -y install python3-pip
```
```
sudo pip3 install kafka-python
```



# La instalacion de Flask para la Api


```
pip3 install flask
```



# Instancia

Se destaca que se tiene que estar dentro del archivo kafka_home.sh, por consiguiente se levantan los servicios de Zookeeper, donde se ejecuta el archivo Zookeeper_run y se corre con el siguiente comando:
```
zsh zookeeper_run.sh
```
Posterior a lo anterior en otra terminal, se tiene que ejecutrar el archivo kafka_run.sh, el cual se corre con el siguiente comando:

```
zsh kafka_run.sh
```
Al tener el kafka activado, ocuparemos el archivo archivo create_topics.sh para los topicos de las ordenes y daily summary, el cual se corre con:

```
zsh create_topics.sh
```
Se ocupa el archivo list_topic.sh para validar que los topicos se crearon de forma correcta, se corre con:
```
zsh list_topic.sh
```

