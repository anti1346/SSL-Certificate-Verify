import requests
from datetime import datetime
import socket

def get_ssl_certificate(domain):
    url = f"https://api.certspotter.com/v1/issuances?domain={domain}&expand=dns_names"
    response = requests.get(url)
    data = response.json()
    return data

def get_remaining_days(expiration_date):
    current_date = datetime.now()
    remaining_days = (expiration_date - current_date).days
    return remaining_days

def get_domain_ip(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return None

def generate_html_table(rows):
    html_table = "<table>\n"
    html_table += "<tr><th>Domain</th><th>SSL Start Date</th><th>SSL Expiration Date</th><th>SSL Remaining Days</th><th>SSL Registrar</th><th>Domain IP</th></tr>\n"

    for row in rows:
        html_table += "<tr>"
        for cell in row:
            html_table += f"<td>{cell}</td>"
        html_table += "</tr>\n"

    html_table += "</table>"
    return html_table

if __name__ == '__main__':
    file_path = 'domain_list.txt'  # 도메인 목록이 포함된 파일 경로

    with open(file_path, 'r') as file:
        domains = file.readlines()
        domains = [domain.strip() for domain in domains]

    table_rows = []

    for domain in domains:
        data = get_ssl_certificate(domain)
        if data and isinstance(data, list) and len(data) > 0 and 'leaf_cert' in data[0]:
            certificates = data[0]['leaf_cert']
            start_date = certificates.get('not_before', 'N/A')
            expiration_date = certificates.get('not_after', 'N/A')
            remaining_days = 'N/A'
            if start_date != 'N/A' and expiration_date != 'N/A':
                expiration_datetime = datetime.strptime(expiration_date, "%Y-%m-%dT%H:%M:%S")
                remaining_days = get_remaining_days(expiration_datetime)
            registrar = certificates['issuer'].get('registered_name', 'N/A')
            ip_address = get_domain_ip(domain)

            row = [domain, start_date, expiration_date, remaining_days, registrar, ip_address]
            table_rows.append(row)
        else:
            row = [domain, "N/A", "N/A", "N/A", "N/A", "N/A"]
            table_rows.append(row)

    html_table = generate_html_table(table_rows)

    with open("result.html", "w") as output_file:
        output_file.write(html_table)

    print("Output saved to result.html.")
