#!/bin/bash

source kafka_home.sh

$KAFKA_HOME/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic event --from-beginning --max-messages 100