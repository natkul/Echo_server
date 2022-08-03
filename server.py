import argparse
import socket
from http import HTTPStatus

HOST = socket.gethostbyname(socket.gethostname())
FORMAT = "utf-8"


def start_server(port):
    try:
        with socket.create_server((HOST, port)) as server:
            print(f"Server is starting on {HOST}:{port}")
            server.listen()

            while True:
                conn, address = server.accept()
                data = conn.recv(1024).decode('utf-8').strip()

                for status in HTTPStatus:
                    if f"status={status.value}" in data.split()[1]:
                        status_value = status.value
                        status_phrase = status.phrase
                        break
                    else:
                        status_value = HTTPStatus.OK
                        status_phrase = HTTPStatus(HTTPStatus.OK).phrase

                response_headers = \
                    f'{data.split()[2]}' \
                    f'\n Content-Type: text/html; charset=utf-8 \r\n\r\n'.encode(FORMAT)
                conn.send(response_headers + f'Request Method: {data.split()[0]}'
                                             f'\nRequest Source: {HOST}, {port}'
                                             f'\nResponse Status: {status_value} {status_phrase}'
                                             f'\n{data[17:]}'.encode(FORMAT))
    except KeyboardInterrupt:
        conn.close()
        print('Server is down')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port',
                        action="store", dest="port", type=int,
                        required=True)
    given_args = parser.parse_args()
    port = given_args.port
    start_server(port)
