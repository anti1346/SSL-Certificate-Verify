#!/bin/bash

### Linux
docker run -d -p 8080:80 -v $(pwd)/result.html:/usr/share/nginx/html/index.html nginx

### 원도우
# docker run -d -p 8080:80 -v ${PWD}/result.html:/usr/share/nginx/html/index.html nginx

echo -e "\nhttp://localhost:8080\n"