#! /bin/bash

service stunnel4 start
dev_appserver.py --port 80 --host 0.0.0.0 /app/src 2> /logs/picbit.log
