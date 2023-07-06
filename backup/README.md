아래 sh 스크립트로 재작성하였습니다.

https://gist.github.com/stevenringo/2fe5000d8091f800aee4bb5ed1e800a6

<br>
#### 메일 정보 파일 생성

vim .mail_header

```
From: mail1234@mailserver.com
To: mail1234@mailserver.com
Subject: 도메인 만료일 안내
Content-Type: text/html
```

<br>
#### SSL 인증서 도메인 리스트 파일 생성

vim domain_list.txt

```
google.com
```

<br>
#### 크론탭 설정

crontab -e

```
### domain check
00 10 1-7 * *	/bin/bash /app/script/SSL-Certificate-Verify/sslchecker.sh > /dev/null 2>&1
