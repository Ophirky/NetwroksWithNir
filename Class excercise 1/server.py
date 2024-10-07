import socket as sok

MAX_PACKET = 1024
QUEUE_LEN = 1
IP = "0.0.0.0"
PORT = 5500

sock = sok.socket(sok.AF_INET, sok.SOCK_STREAM)

try:
    sock.bind((IP,PORT))
    sock.listen(QUEUE_LEN)
    client_socket, client_ip = sock.accept()

    try:
        request = client_socket.recv(MAX_PACKET).decode()
        print(f"server got: {request}")
        client_socket.send("MSG received".encode())

    except sok.error as err:
        print("ERROR: " + str(err))

    finally:
        client_socket.close()

except sok.error as err:
    print('ERROR: ' + str(err))

finally:
    sock.close()