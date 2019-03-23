import socket
import sys

LOCALHOST = socket.gethostname()  # Get local machine name
DEFAULT_PORT = 12345  # Reserve a port for your service.
DEFAULT_BINARY_FILE_PATH: str = 'C:/Users/paulr/PycharmProjects/Conda_project/geo/__pycache__/geo.cpython-37.pyc'


def run_server(host=LOCALHOST, port=DEFAULT_PORT):
    try:
        s = socket.socket()  # Create a socket object
        s.bind((host, port))  # Bind to the port
        print(f'Server run on host={host} port={port}')

        s.listen(5)  # Now wait for client connection.

        while True:
            c, addr = s.accept()  # Establish connection with client.
            print(f'Got connection from: {addr}')

            i_batch: int = 1

            with open('temp_data.bin', 'wb') as f:
                data = c.recv(1024)
                while data:
                    print(f'Receiving batch of data #{i_batch}')
                    f.write(data)
                    i_batch += 1
                    data = c.recv(1024)

                f.close()
                print('Done Receiving')
                c.send(b'The data has been received successfully')
                c.close()  # Close the connection

    except KeyboardInterrupt:
        print('Exit')
        sys.exit(0)


def run_client(host=LOCALHOST, port=DEFAULT_PORT):
    s = socket.socket()  # Create a socket object
    s.connect((host, port))
    print(f'Connect to server with host={host} port={port}')

    i_batch: int = 1

    with open(DEFAULT_BINARY_FILE_PATH, 'rb') as f:
        data = f.read(1024)
        while data:
            print(f'Sending batch of data #{i_batch}')
            s.send(data)
            i_batch += 1
            data = f.read(1024)
        f.close()
        print('The data has been sent successfully')
        s.close()  # Close the socket when done


if __name__ == '__main__':
    cli_args = sys.argv
    if len(cli_args) > 1:
        cmd: str = cli_args[1]

        if cmd == 'run_server':
            run_server()

        elif cmd == 'run_client':
            run_client()

        else:
            print(f'Unexpected argument: {cmd}\nAvailable args: [run_server, run_client]')
