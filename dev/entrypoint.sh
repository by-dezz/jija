#!/bin/bash

python main.py migrate;
python main.py update;

#pip install /jija_orm/jija-orm-0.0.1.tar.gz

echo $@
exec $@
