#! /bin/bash

echo "export HTTP_PATH=%{HTTP_PATH}" >> /etc/environment
apache2ctl start
service memcached restart
watch ls
