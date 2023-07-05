#!/bin/bash

docker run -d -p 8080:80 -v $(pwd)/result.html:/usr/share/nginx/html/index.html nginx

echo -e "\nhttp://localhost:8080\n"