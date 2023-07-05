import ssl
import socket

def get_ssl_info(domain):
    # Get the socket object for the domain
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((domain, 443))

    # Get the SSL object for the socket
    ssl_obj = ssl.wrap_socket(sock)

    # Get the certificate from the SSL object
    cert = ssl_obj.getpeercert()

    # Get the start date, expiration date, and remaining days for the certificate
    start_date = cert['notBefore']
    expiration_date = cert['notAfter']
    remaining_days = (expiration_date - start_date).days

    # Get the registry authority for the certificate
    reg_authority = cert['subjectAltName'][1]['dNSName']

    return domain, ip, start_date, expiration_date, remaining_days, reg_authority

if __name__ == '__main__':
    # Get the domain name from the user
    domain = input('Enter the domain name: ')

    # Get the SSL information for the domain
    ssl_info = get_ssl_info(domain)

    # Print the SSL information
    print('Domain: {}'.format(ssl_info[0]))
    print('IP: {}'.format(ssl_info[1]))
    print('Start date: {}'.format(ssl_info[2]))
    print('Expiration date: {}'.format(ssl_info[3]))
    print('Remaining days: {}'.format(ssl_info[4]))
    print('Registry authority: {}'.format(ssl_info[5]))
