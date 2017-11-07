#! /bin/bash

apache2ctl start
service memcached restart
watch ls
