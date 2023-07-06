## SSL Certificate Expiration Date(SSL 인증서 만료일)

#### SSL 인증서 도메인 리스트 파일 생성
```
vim domain_list.txt
```
```
www.google.com
www.daum.net
www.yahoo.com
```

#### 크론탭 설정
```
crontab -e
```
```
### domain check
00 10 1-7 * *	/bin/bash /app/script/SSL-Certificate-Verify/sslchecker.sh > /dev/null 2>&1
```
