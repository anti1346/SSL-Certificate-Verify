#!/bin/bash

cd /sslchecker

python3 ssl_certificate_expiration_date_checker_v2.py

ln -s /sslchecker/result.html /var/www/html/index.html

nginx -g "daemon off;"
