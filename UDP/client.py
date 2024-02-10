"""
    AUTHOR: Barak Gonen
    MODIFIED BY: Ophir Nevo Michrowski
    DESCRIPTION: Simple UDP client
"""
import socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
user_in = b''
while user_in != 'quit':
    user_in = input("Enter your message: ").encode()
    my_socket.sendto(user_in, ('127.0.0.1', 5500))
    (data, remote_address) = my_socket.recvfrom(1024)
    print('The server sent: ' + data.decode())

my_socket.close()