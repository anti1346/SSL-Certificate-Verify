import ssl
import socket
import dns.resolver
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

        # 도메인의 IP 주소 가져오기
        ip = socket.gethostbyname(domain)

        # 도메인의 IP 주소 가져오기 (DNS 쿼리 사용)
        resolver = dns.resolver.Resolver()
        ip_addresses = [result.address for result in resolver.resolve(domain, 'A')]

        # 등록행자(Registrar) 가져오기
        registrar = ""
        issuer = dict(x[0] for x in cert['issuer'])
        if 'organizationName' in issuer:
            registrar = issuer['organizationName']

        return domain, ip, start_date, expiration_date, int(remaining_days), ip_addresses, registrar
    except (socket.timeout, ssl.SSLCertVerificationError):
        return domain, [], "N/A", "N/A", "N/A", "N/A"

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
    html_table = """
        <html>
        <head>
        <meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
        <style>
        table {
            width: 70%;
            border-top: 1px solid #444444;
            border-collapse: collapse;
            font-family: Monaco;
            font-size: 80%;
        }
        th, td {
            border-bottom: 1px solid #444444;
            padding: 10px;
            text-align: center;
        }
        th {
            background-color: #e3f2fd;
        }
        td {
            background-color: #FFFFFF;
        }
        </style>
        </head>
        <body>
        <h1>SSL Certificate Expiration Date(SSL 인증서 만료일)</h1>
        <table>
        <tr>
        <th>Domain</th>
        <th>IP</th>
        <th>Start Date</th>
        <th>Expiration Date</th>
        <th>Remaining Days</th>
        <th>IP Addresses</th>
        <th>Registrar</th>
        </tr>
        """

    for row in table_rows:
        domain, ip, start_date, expiration_date, remaining_days, ip_addresses, registrar = row
        ip_addresses_str = ", ".join(ip_addresses) if ip_addresses else "N/A"
        html_table += f"<tr><td>{domain}</td><td>{ip}</td><td>{start_date}</td><td>{expiration_date}</td><td>{remaining_days}</td><td>{ip_addresses_str}</td><td>{registrar}</td></tr>"

    html_table += "</table></body></html>"

    # HTML 테이블을 result.html 파일에 저장하기
    with open('result.html', 'w') as file:
        file.write(html_table)

    print("SSL 정보가 result.html 파일에 저장되었습니다.")

