import base64
import ssl
import socket
import json
import sys
import os
import getpass
from pathlib import Path

"""
Корнеев Михаил, КН-203 (ИЕНиМ-280208)
"""

USR_NAME = ''   # 'testingIProtocols@yandex.ru'
PSWD = ''       # '11_02&?'
RCPT = ''       # 'someone@example.com'

help_args = {'--help', '-h', '-help'}
help_message = """
Script to send emails from your registered [yandex.ru] account using SMTP Protocol directly
    +-------------------------------------------------------------------------------+
    |                    USAGE: python3 smtp_mail.py -i                             |
    |                 HELP: smtp_mail.py [--help, -h, -help]                        |
    |            current server: smtp.yandex.ru :: current port: 465                |
    +-------------------------------------------------------------------------------+
"""

if len(sys.argv) != 2:
    print(help_message)
    sys.exit()
if sys.argv[1] in help_args or sys.argv[1] != '-i':
    print(help_message)
    sys.exit(0)
if sys.argv[1] == '-i':
    print('Enter your user name: ')
    user_name = input()
    USR_NAME += user_name
    password = getpass.getpass('Password: ')
    PSWD += password
    recipient = input('Enter recipient address: ')
    RCPT += recipient
    subject = input('Subject: ')
    message = input('Enter your message here: ')
# print(user_name)
# print(password)
# print(recipient)
# print(message)
    paths_to_attachments = input('Enter path(s) to attachment(s) separated by whitespace: ')
    if paths_to_attachments != '':
        attached = True
        attachments = paths_to_attachments.split(' ')
    else:
        attached = False
# print(attachments)


def read_pict(item):
    """ Prepares attachments to be sent over SMTP Protocol"""
    filename = Path(item)
    try:
        with open(filename, 'rb') as pict:
            return base64.b64encode(pict.read()).decode(), filename.name
    except OSError as e:
        print('File not found! Error: ', e)


def create_msg():
    """Creates message"""
    head = ''
    head += 'From: ' + USR_NAME + '\n'
    head += 'To: ' + RCPT + '\n'
    head += 'Subject: ' + '=?utf-8?B?' + base64.b64encode(subject.encode()).decode() + '?=' + '\n'
    head += 'MIME-Version: 1.0' + '\n'
    boundary = 'bound-bound123456'
    head += 'Content-Type: multipart/mixed; boundary="' + boundary + '"' + '\n'
    head += '\n'

    body = ''
    body += '--' + boundary + '\n'
    body += 'Content-Transfer-Encoding: 7bit' + '\n'
    body += 'Content-Type: text/plain' + '\n' + '\n'
    body += message + '\n'

    if attached:
        try:
            for item in attachments:
                body += '--' + boundary + '\n'
                body += f'Content-Disposition: attachment; filename="{read_pict(item)[1]}"' \
                        f'\nContent-Transfer-Encoding: base64' \
                        f'\nContent-Type: image/png; name="{read_pict(item)[1]}"' + '\n' + '\n'
                body += read_pict(item)[0] + '\n'
        except TypeError as exc:
            print('Error occurred: ', str(exc))

    body += '--' + boundary + '--' + '\n'
    body += '.' + '\n'

    return head + body


def request(socket_, request):
    socket_.send((request + '\n').encode())
    received_data = socket_.recv(65535).decode()
    return received_data


host_address = 'smtp.yandex.ru'
port = 465


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    try:
        client.connect((host_address, port))
    except socket.gaierror as ex:
        print('Error occurred: ' + str(ex))
    client = ssl.wrap_socket(client)
    try:
        print(client.recv(1024))
        print(request(client, f'EHLO {USR_NAME}'))

        base64login = base64.b64encode(USR_NAME.encode()).decode()
        base64pswd = base64.b64encode(PSWD.encode()).decode()

        print(request(client, 'AUTH LOGIN'))
        print(request(client, base64login))
        print(request(client, base64pswd))

        print(request(client, 'MAIL FROM: ' + USR_NAME))
        print(request(client, 'RCPT TO: ' + RCPT))
        print(request(client, 'DATA'))
        print(request(client, create_msg()))

    except (ssl.SSLError, OSError) as ex:
        print('Errors occurred:' + str(ex))
