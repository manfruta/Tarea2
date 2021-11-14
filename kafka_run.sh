#!/bin/bash
source kafka_home.sh

$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties
