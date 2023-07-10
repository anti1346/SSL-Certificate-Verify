#!/bin/bash

cd /sslchecker

python3 sslinfo.py domains.txt result.html

ln -s /sslchecker/result.html /var/www/html/index.html

nginx -g "daemon off;"
