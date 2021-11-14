#!/bin/bash

source kafka_home.sh

$KAFKA_HOME/bin/kafka-topics.sh \
  --describe \
  --bootstrap-server localhost:9092 --topic event

