#!/bin/bash

python main.py migrate;
python main.py update;

echo $@
exec $@
