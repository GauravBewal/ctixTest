#!/bin/bash
export PYTHONPATH=`pwd`
rm -f temp.txt
python3 config/process_config.py
a=`cat temp.txt`
#while read line || [ -n "$line" ]; do python3 -u $line; done < config/testplans/$a
while read -r line; do [[ "$line" =~ ^#.*$ ]] && continue; python3 -u $line; done < config/testplans/$a