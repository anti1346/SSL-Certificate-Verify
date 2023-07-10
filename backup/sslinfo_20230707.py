import ssl
import socket
from datetime import datetime

def get_ssl_info(domain):
    try:
        # 도메인에 대한 소켓 객체 가져오기
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((domain, 443))

        # 소켓 객체를 SSL 컨텍스트로 감싸기
        context = ssl.create_default_context()
        context.check_hostname = False  # 호스트 이름 검증 비활성화
        ssl_sock = context.wrap_socket(sock, server_hostname=domain)

        # SSL 객체에서 인증서 가져오기
        cert = ssl_sock.getpeercert()

        # 인증서의 시작일, 만료일 및 남은 일 수 가져오기
        start_date = datetime.strptime(cert['notBefore'], "%b %d %H:%M:%S %Y %Z").strftime("%Y-%m-%d")
        expiration_date = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z").strftime("%Y-%m-%d")
        remaining_days = (datetime.strptime(expiration_date, "%Y-%m-%d") - datetime.now()).days

        # 등록행자(Registrar) 가져오기
        registrar = ""
        issuer = dict(x[0] for x in cert['issuer'])
        if 'organizationName' in issuer:
            registrar = issuer['organizationName']

        # 도메인의 IP 주소 가져오기
        ip = socket.gethostbyname(domain)

        return domain, ip, start_date, expiration_date, int(remaining_days), registrar
    except (socket.timeout, ssl.SSLCertVerificationError):
        return domain, "N/A", "N/A", "N/A", "N/A", "N/A"

if __name__ == '__main__':
    # 파일에서 도메인 이름 가져오기
    with open('domains.txt', 'r') as f:
        domains = f.readlines()

    table_rows = []

    # 각 도메인에 대한 SSL 정보 가져오기
    for domain in domains:
        ssl_info = get_ssl_info(domain.strip())

        # SSL 정보를 테이블 행에 추가하기
        table_rows.append(ssl_info)

    # "N/A" 값을 처리하여 남은 일 수(`remaining_days`)를 기준으로 테이블 행 정렬하기 (오름차순)
    table_rows.sort(key=lambda x: x[4] if isinstance(x[4], int) else float('inf'))

    # HTML 테이블 생성하기
    html_table = "<html>"
    html_table += "<head>"
    html_table += "<meta charset='utf-8'>"
    html_table += "<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>"
    html_table += "<style>"
    html_table += "table {"
    html_table += "width: 80%;"
    html_table += "border-top: 1px solid #444444;"
    html_table += "border-collapse: collapse;"
    html_table += "font-family: Monaco;"
    html_table += "font-size:90%;"
    html_table += "}"
    html_table += "th, td {"
    html_table += "border-bottom: 1px solid #444444;"
    html_table += "padding: 10px;"
    html_table += "text-align: center;"
    html_table += "}"
    html_table += "th {"
    html_table += "background-color: #e3f2fd;"
    html_table += "}"
    html_table += "td {"
    html_table += "background-color: #FFFFFF;"
    html_table += "}"
    html_table += "</style>"
    html_table += "</head>"
    html_table += "<body>"
    html_table += "<h1>SSL Certificate Expiration Date</h1>"
    html_table += "<table style='border-collapse: collapse; border: 1px solid black;'>\n"
    html_table += "<tr>"
    html_table += "<th style='border: 1px solid black;'>Domain</th>"
    html_table += "<th style='border: 1px solid black;'>IP Addresses</th>"
    html_table += "<th style='border: 1px solid black; text-align: center;'>Start Date</th>"
    html_table += "<th style='border: 1px solid black; text-align: center;'>Expiration Date</th>"
    html_table += "<th style='border: 1px solid black; text-align: center;'>Remaining Days</th>"
    html_table += "<th style='border: 1px solid black;'>Registrar</th>"
    html_table += "</tr>\n"

    for row in table_rows:
        html_table += "<tr>"
        for i, cell in enumerate(row):
            # 특정 열에 가운데 정렬 적용하기
            if i in [2, 3, 4]:
                html_table += f"<td style='border: 1px solid black; text-align: center;'>{cell}</td>"
            else:
                html_table += f"<td style='border: 1px solid black;'>{cell}</td>"
        html_table += "</tr>\n"

    html_table += "</table>"
    html_table += "</body>"
    html_table += "</html>"

    # HTML 테이블을 result.html 파일에 저장하기
    with open('result.html', 'w') as file:
        file.write(html_table)

    print("SSL 정보가 result.html 파일에 저장되었습니다.")
    

### SSL 인증서 만료일 조회
# echo "" | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -startdate -enddate