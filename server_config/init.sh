#! /bin/bash

service stunnel4 start
dev_appserver.py --port 80 --host 0.0.0.0 --datastore_consistency_policy consistent --storage_path /logs/picbit /app/src 2> /logs/picbit.log
