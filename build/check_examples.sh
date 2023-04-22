#!/bin/bash

cd /examples/simple
python main.py runprocess &
sleep 2
curl -s http://localhost:8080/
if [[ $? != 0 ]]; then
    echo "simple example failed"
    exit 1
fi

cd /examples/advanced
python main.py runprocess &
sleep 2
curl -s http://localhost:8081/
if [[ $? != 0 ]]; then
    echo "advanced example failed"
    exit 1
fi