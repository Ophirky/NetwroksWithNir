# TO DO: import modules
import socket
import os

# TO DO: set constants
QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 2


# TO DO: define constants
DEFAULT_URL = "/"
REDIRECTION_DICTIONARY = {
    "forbidden": "/forbidden",
    "moved": "/index.html",
    "error": "/error",
}


def get_file_data(file_name):
    """
    Get data from file
    :param file_name: the name of the file
    :return: the file data in a string
    """
    with open("WEB-ROOT" + file_name, "rb") as f:
        data = f.read()
    return data


def handle_client_request(resource, client_socket):
    """
    Check the required resource, generate proper HTTP response and send
    to client
    :param resource: the required resource
    :param client_socket: a socket for the communication with the client
    :return: None
    """

    if resource == '':
        uri = DEFAULT_URL
    else:
        uri = resource

    if uri in REDIRECTION_DICTIONARY:
        http_header = "HTTP/1.1 302 Found\r\nLocation: /index.html\r\n\r\n"
    else:
        # check if file exists
        filename = uri
        if not os.path.isfile(filename):
            http_header = "HTTP/1.1 404 Not Found\r\n\r\n"
        else:
            # extract requested file type from URL (html, jpg etc)
            file_type = os.path.splitext(filename)[1]

            # generate proper HTTP header
            if file_type == ".html":
                http_header = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: %d\r\n\r\n" % len(
                    get_file_data(filename)
                )
            elif file_type == ".jpg":
                filename = "/imgs" + filename
                http_header = "HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nContent-Length: %d\r\n\r\n" % len(
                    get_file_data(filename)
                )
            else:
                http_header = "HTTP/1.1 400 Bad Request\r\n\r\n"

    # send response
    http_response = http_header.encode() + get_file_data(filename)
    client_socket.send(http_response)


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and
    the requested URL
    :param request: the request which was received from the client
    :return: a tuple of (True/False - depending if the request is valid,
    the requested resource )
    """
    # check if request starts with "GET"
    if request.startswith("GET"):
        # get resource from request
        resource = request.split(" ")[1]

        # check if resource is valid
        if resource.startswith("/"):
            return True, resource
        else:
            return False, ""
    else:
        return False, ""


def handle_client(client_socket):
    """
    Handles client requests: verifies client's requests are legal HTTP, calls
    function to handle the requests
    :param client_socket: the socket for the communication with the client
    :return: None
    """
    print("Client connected")
    while True:
        client_request = client_socket.recv(1024).decode()
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print("Got a valid HTTP request")
            handle_client_request(resource, client_socket)
        else:
            print("Error: Not a valid HTTP request")
            break
    print("Closing connection")
    client_socket.close()  # Close the socket after handling the client


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print("Listening for connections on port %d" % PORT)

        while True:
            client_socket, client_address = server_socket.accept()
            try:
                print('New connection received')
                # client_socket.settimeout(SOCKET_TIMEOUT)
                handle_client(client_socket)
            except socket.error as err:
                print('received socket exception - ' + str(err))
            finally:
                client_socket.close()
    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    # Call the main handler function
    main()
