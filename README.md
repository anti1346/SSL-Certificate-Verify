## SSL Certificate Expiration Date Checker(SSL 인증서 만료 날짜 검사기)

#### SSL 인증서 도메인 리스트 파일 생성
```
vim domain_list.txt
```
```
www.google.com
www.daum.net
www.yahoo.com
```

#### SSL 인증서 만료 날짜 검사기 실행
```
python ssl_certificate_expiration_date_checker_v2.py
```

#### 도커 컨테이너를 실행(웹 서버 실행)
```
bash docker_container_start.sh
```

#### 웹 브라우저
```
http://localhost:8080
```

#### 크론탭 설정
```
crontab -e
```
```
### domain check
00 10 1-5 * * /bin/bash /app/script/SSL-Certificate-Verify/ssl_certificate_expiration_date_checker_v2.py > /dev/null 2>&1
```

---
### sslinfo_v2.py 실행 방법
##### domains.txt 입력 파일과 result.html 출력 파일을 명령줄 인수로 전달할 수 있습니다.
```
python3 sslinfo_v2.py domains.txt result.html
````
