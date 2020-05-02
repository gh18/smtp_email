import base64
import ssl
import socket
import json


def request(socket_, request):
    socket_.send((request + '\n').encode())
    received_data = socket_.recv(65535).decode()
    return received_data


host_address = 'smtp.yandex.ru'
port = 465
user_name = 'testingIProtocols@yandex.ru'
password = '11_02&?'

with open('config.JSON') as config:
    data = json.load(config)
    data_parsed = ''
    for k in data.keys():
        data_parsed += ''.join(k)
        data_parsed += ''.join(data[k])
        data_parsed += ''.join('\n')
# print(data_parsed)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    try:
        client.connect((host_address, port))
    except socket.gaierror as ex:
        print('Error occurred: ' + str(ex))
    client = ssl.wrap_socket(client)
    try:
        print(client.recv(1024))
        print(request(client, f'EHLO {user_name}'))
    # except OSError as ex:
    #     print('Error occurred:' + str(ex))

        base64login = base64.b64encode(user_name.encode()).decode()
        base64pswd = base64.b64encode(password.encode()).decode()

    # try:
        print(request(client, 'AUTH LOGIN'))
        print(request(client, base64login))
        print(request(client, base64pswd))

        print(request(client, 'MAIL FROM:testingIProtocols@yandex.ru'))
        print(request(client, 'RCPT TO:random.urls@gmail.com'))
        print(request(client, 'DATA'))
    # except (ssl.SSLError, OSError) as ex:
    #     print('Authentication failed:' + str(ex))

        with open('msg.txt') as file:
            msg = data_parsed + '\r\n' + file.read() + '\n.\n'
            print(msg)
            # try:
            print(request(client, msg))
            # except OSError as ex:
            #     print('Error occurred:' + str(ex))
    except (ssl.SSLError, OSError) as ex:
        print('Errors occurred:' + str(ex))

# TODO: connection errors -> +
#       MIME attachments
