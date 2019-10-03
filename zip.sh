#!/usr/bin/env bash

cd package
zip -r9 ../terraform/lambda_function.zip * -x "bin/*" requirements.txt setup.cfg
cd ..
zip -g terraform/lambda_function.zip icon_node_monitor.py lambda_function.py

