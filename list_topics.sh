#!/bin/bash
source kafka_home.sh
$KAFKA_HOME/bin/kafka-topics.sh --list \
  --bootstrap-server localhost:9092