"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 11/4/2023
    DESCRIPTION: simple remote command line client.
"""

# Imports #
import socket as sock

# Constants #
IP = "127.0.0.1"
PORT = 5500
MAX_PACKET = 1024


# Client code #
def main():
    socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

    try:
        socket.connect((IP, PORT))
        print(socket.recv(MAX_PACKET).decode())

        while True:
            # Getting user input #
            user_in = input("Enter a command: ")

            # Validating input #
            if len(user_in) > 4 or len(user_in) < 4:
                print("Invalid input")
                continue

            socket.send(user_in.encode())

            server_ans = socket.recv(MAX_PACKET).decode()

            print(server_ans)
            if server_ans == 'Disconnecting...':
                break

    except sock.error:
        pass

    finally:
        socket.close()


if __name__ == '__main__':
    main()
