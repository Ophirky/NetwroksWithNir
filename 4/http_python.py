# TODO: add logs to the entire file using the python logging package
# TODO: Fix page not loading when called from browser

import re
import socket
import os

QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 2


# TODO: define constants
DEFAULT_URL = "/"
REDIRECTION_DICTIONARY = {
    "forbidden": "/forbidden",
    "moved": "/index.html",
    "error": "/error",
}

HTTP_VERSION = b"HTTP/1.1"
HEADER_SEPERATOR = b"\r\n"
LOCATION_HEADER = b"Location: %s"
CONTENT_TYPE_HEADER = b"Content-Type: %s"
CONTENT_LEN_HEADER = b"Content-Length: %d"

ERROR_CODES = {
    200: b"OK",
    500: b"INTERNAL SERVER ERROR",
    302: b"MOVED TEMPORARILY",
    403: b"FORBIDDEN",
    404: b"NOT FOUND",
    400: b"BAD REQUEST"
}
MIME_TYPES = {
    ".html": "text/html;charset=utf-8",
    ".jpg": "image/jpeg",
    ".css": "text/css",
    ".js": "text/javascript; charset=UTF-8",
    ".txt": "text/plain",
    ".ico": "image/x-icon",
    ".gif": "image/jpeg",
    ".png": "image/png"
}


def get_file_data(file_name):
    """
    Get data from file
    :param file_name: the name of the file
    :return: the file data in a string
    """
    if file_name == "/":
        file_name = "/index.html"
    with open("WEB-ROOT" + file_name, "rb") as f:
        data = f.read()
    return data


def error_code_finder(error_code: int):
    """
    returns the error code and messge using the error code.
    :param error_code: the error code to be found
    :return: str the error code
    """
    if error_code in ERROR_CODES.keys():
        return str(error_code).encode() + b" " + ERROR_CODES[error_code]
    else:
        return "-1"


def build_http(error_code: int = 200, body=b"", **headers):
    """
    builds a http protocol msg
    :param body: the payload of the msg.
    :param error_code: the error code of the msg
    :param headers: all the headers that can be put in the msg [location, content-type, content-length]
    :return: msg to send to the client or -1 error code
    """
    if error_code_finder(error_code) != "-1":
        res = HTTP_VERSION + b" " + error_code_finder(error_code) + HEADER_SEPERATOR

        if "location" in headers.keys():
            res += LOCATION_HEADER % headers["location"].encode() + HEADER_SEPERATOR

        if "content_type" in headers.keys():
            res += CONTENT_TYPE_HEADER % headers["content_type"].encode() + HEADER_SEPERATOR

        if "content_length" in headers.keys():
            res += CONTENT_LEN_HEADER % headers["content_length"] + HEADER_SEPERATOR

        res += HEADER_SEPERATOR + body
    else:
        res = b"-1"

    return res


def handle_client_request(resource, client_socket):
    """
    Check the required resource, generate proper HTTP response and send
    to client
    :param resource: the required resource
    :param client_socket: a socket for the communication with the client
    :return: None
    """

    # TODO: insert the build_http function into the function.
    # TODO: use the MIME_TYPES constant with the calling of the build_http function

    if resource == '':
        uri = DEFAULT_URL
    else:
        uri = resource

    if uri in REDIRECTION_DICTIONARY:
        http_header = "HTTP/1.1 302 Found\r\nLocation: /index.html\r\n\r\n"
    else:
        # check if file exists
        filename = uri
        if filename == "/": filename = "/index.html"
        if not os.path.isfile("WEB-ROOT" + filename):
            print("WEB-ROOTS" + filename)
            http_header = "HTTP/1.1 404 Not Found\r\n\r\n"
        else:
            # extract requested file type from URL (html, jpg etc)
            file_type = os.path.splitext(filename)[1]

            # generate proper HTTP header
            if file_type == ".html":
                http_header = b"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: %d\r\n\r\n" % len(
                    get_file_data(filename)
                )
                file_data = get_file_data(filename)
                http_header = build_http(body=file_data, content_type=MIME_TYPES[".html"], content_length=len(file_data))
            elif file_type == ".jpg" or file_type == ".gif":
                http_header = b"HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nContent-Length: %d\r\n\r\n" % len(
                    get_file_data(filename)
                )
            elif file_type == ".css":
                http_header = b"HTTP/1.1 200 OK\r\nContent-Type: text/css\r\nContent-Length: %d\r\n\r\n" % len(
                    get_file_data(filename)
                )
            elif file_type == ".ico":
                http_header = b"HTTP/1.1 200 OK\r\nContent-Type: text/x-icon\r\nContent-Length: %d\r\n\r\n" % len(
                    get_file_data(filename)
                )
            elif file_type == ".txt":
                http_header = b"HTTP/1.1 200 OK\r\nContent-Type: text/css\r\nContent-Length: %d\r\n\r\n" % len(
                    get_file_data(filename)
                )
            elif file_type == ".png":
                http_header = b"HTTP/1.1 200 OK\r\nContent-Type: image/png\r\nContent-Length: %d\r\n\r\n" % len(
                    get_file_data(filename)
                )
            elif file_type == ".js":
                http_header = b"HTTP/1.1 200 OK\r\nContent-Type: text/javascript; charset=UTF-8\r\nContent-Length: %d\r\n\r\n" % len(
                    get_file_data(filename)
                )
            else:
                http_header = b"HTTP/1.1 400 Bad Request\r\n\r\n"

    # send response
    http_response = http_header
    print(http_response)
    client_socket.send(http_response)
    print("sent http resp")


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
    http_test_example = b"HTTP/1.1 200 OK\r\nLocation: /index.html\r\n\r\n"

    # Asserts
    # TODO: add asserts
    assert build_http(location="/index.html") == http_test_example, "build_http - not working"

    # Call the main handler function
    main()
