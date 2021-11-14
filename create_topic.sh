#!/bin/bash

source kafka_home.sh

$KAFKA_HOME/bin/kafka-topics.sh --create \
    --bootstrap-server localhost:9092 \
    --replication-factor 1 \
    --partitions 1 \
    --config retention.ms=259200000 \
    --topic event


