import socket as sock

IP = "192.168.68.100"
PORT = 5555
MAX_PACKET = 1024

socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

try: 
    socket.connect((IP, PORT))

    socket.send(input("Enter your name: ").encode())

    print(socket.recv(MAX_PACKET).decode())

except sock.error as err: print(f"ERROR!! {err}")

finally: socket.close()