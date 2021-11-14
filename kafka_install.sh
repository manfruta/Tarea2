#!/bin/bash

source kafka_home.sh

mkdir -p $KAFKA_HOME

wget https://downloads.apache.org/kafka/2.8.0/kafka_2.13-2.8.0.tgz -P $KAFKA_HOME

tar -xzf $KAFKA_HOME/kafka_2.13-2.8.0.tgz
