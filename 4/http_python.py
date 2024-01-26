"""
    AUTHOR: Ophir Nevo Michrowski
    Date: 05/01/24
    DESCRIPTION: Simple http server using python
"""

# TODO: add logs to the entire file using the python logging package
# TODO: check for comments
import logging
import os
import re
import socket

QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 2
MAX_PACKET = 1024

DEFAULT_URL = "/"
REDIRECTION_DICTIONARY = {
    "/forbidden": "/forbidden",
    "/moved": "/index.html",
    "/error": "/error",
}

HTTP_VERSION = b"HTTP/1.1"
HEADER_SEPERATOR = b"\r\n"
LOCATION_HEADER = b"Location: %s"
CONTENT_TYPE_HEADER = b"Content-Type: %s"
CONTENT_LEN_HEADER = b"Content-Length: %d"

ERR_NUMBER_CONVERTION = "NAN"
ERR_BAD_REQUEST = "Bad Request"
ERR_INTERNAL_SERVER_ERROR = "Internal Server Error"

LOG_LEVEL = logging.DEBUG
LOG_DIR = r"Logs"
LOG_FILE = LOG_DIR + r"\server_log.log"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"

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


def get_query_params(http_request: str):
    """
    Extract the parameters from the http request
    :param http_request: the http request
    :return: dictionary of all the query parameters
    """
    return dict(x.split("=") for x in http_request.split("?", 1)[1].split("&"))


def get_request_body(http_request: bytes, client_socket: socket):
    """
    returns the body of the request
    :param http_request: http_request: the http request
    :return: bytes of the body
    """
    content_length = int(re.search(rb'Content-Length: (\d+)', http_request).group(1))
    body = b''
    while len(body) < content_length:
        chunk = client_socket.recv(MAX_PACKET)
        if not chunk:
            break
        body += chunk

    if len(body) < content_length:
        logging.error('Error: Incomplete request body received')

    return body

def calculate_next(number: bytes) -> str:
    """
    returns the following number to the number given
    :param number: the number to calc
    :return: string containing the following number
    """
    try:
        return str(int(number) + 1)
    except ValueError as err:
        logging.error(err)
        return ERR_NUMBER_CONVERTION


def handle_calculate_next(http_request: bytes):
    """
    handles the http according to the needed answer
    :param http_request:  the http request
    :return: returns the http response
    """
    param = get_query_params(http_request)
    error_code = 200
    if param == "NAN" or "num" not in param or calculate_next(param["num"]) == "NAN":
        logging.error(ERR_BAD_REQUEST)
        body = ""
        error_code = 400
    else:
        body = calculate_next(param["num"])

    return build_http(error_code=error_code, content_type=MIME_TYPES[".txt"], content_length=len(body), body=body.encode())


def calculate_area(width: bytes, height: bytes) -> str:
    """
    returns the following number to the number given
    :param height: the height of the triangle
    :param width: the width of the triangle
    :return: string with the area of the triangle
    """
    try:
        return str((float(width) * float(height))/2)
    except ValueError as err:
        logging.error(err)
        return ERR_NUMBER_CONVERTION


def handle_calculate_area(http_request: bytes):
    """
    handles the http according to the needed answer
    :param http_request:  the http request
    :return: returns the http response
    """
    param = get_query_params(http_request)
    error_code = 200
    if param == "NAN" or "width" not in param or "height" not in param or calculate_area(param["width"], param["height"]) == "NAN":
        logging.error(ERR_BAD_REQUEST)
        body = ""
        error_code = 400
    else:
        body = calculate_area(param["width"], param["height"])

    return build_http(error_code=error_code, content_type=MIME_TYPES[".txt"], content_length=len(body), body=body.encode())


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


def upload(http_request: bytes, resource: str, client_socket: socket):

    body = get_request_body(http_request, client_socket)
    file_name = get_query_params(resource)

    if "file-name" not in file_name:
        logging.error(ERR_BAD_REQUEST)
        return build_http(error_code=400, location="/index.html")

    if not os.path.isdir("upload"):
        os.makedirs("upload")

    try:
        with open("upload/" + file_name["file-name"], 'wb') as f:
            f.write(body)

        res = build_http()
    except Exception:
        res = build_http(error_code=500)
        logging.error(ERR_INTERNAL_SERVER_ERROR)

    return res


def upload_image(http_request: bytes):
    param = get_query_params(http_request)
    print(param)
    if "image-name" not in param:
        logging.error(ERR_BAD_REQUEST)
        return build_http(error_code=400, location="/index.html")
    print("upload\\" + param["image-name"])
    # if os.path.isfile("upload\\" + param["image-name"]):
    #     print("g")
    #     return build_http(error_code=404, location="/index.html")

    try:
        print("h")
        with open("upload/" + param["image-name"], 'rb') as f:
            read = f.read()
            return build_http(body=read, content_type=MIME_TYPES[os.path.splitext(param["image-name"])[1]], content_length=len(read))
    except Exception:
        print("f")
        logging.error(ERR_INTERNAL_SERVER_ERROR)
        return build_http(error_code=500)


def handle_client_request(resource, http_req, client_socket):
    """
    Check the required resource, generate proper HTTP response and send
    to client
    :param resource: the required resource
    :param client_socket: a socket for the communication with the client
    :return: None
    """

    http_header = b""
    if resource == '':
        uri = DEFAULT_URL
    else:
        uri = resource
    if http_req.startswith("POST"):
        if uri.startswith("/upload"):
            http_header = upload(http_req.encode(), uri, client_socket)
    elif http_req.startswith("GET"):
        if uri in REDIRECTION_DICTIONARY:
            match uri:
                case '/forbidden':
                    error_code = 403
                case '/moved':
                    error_code = 302
                case '/error':
                    error_code = 500
                case _:
                    error_code = 200
            file_data = get_file_data("/index.html")
            http_header = build_http(error_code=error_code, body=file_data, content_type=MIME_TYPES[".html"],
                                     content_length=len(file_data), location="/index.html")
        elif uri.startswith("/calculate-next"):
            http_header = handle_calculate_next(uri)
        elif uri.startswith("/calculate-area"):
            http_header = handle_calculate_area(uri)
        elif uri.startswith("/image"):
            http_header = upload_image(resource)
        else:
            # check if file exists
            filename = uri
            if filename == "/":
                filename = "/index.html"
            if not os.path.isfile("WEB-ROOT" + filename):
                print("WEB-ROOTS" + filename)
                http_header = build_http(error_code=404)
            else:
                # extract requested file type from URL (html, jpg etc)
                file_type = os.path.splitext(filename)[1]

                # generate proper HTTP header
                file_data = get_file_data(filename)
                http_header = build_http(body=file_data, content_type=MIME_TYPES[file_type], content_length=len(file_data))

    # send response
    client_socket.send(http_header)


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and
    the requested URL
    :param request: the request which was received from the client
    :return: a tuple of (True/False - depending if the request is valid,
    the requested resource )
    """
    # check if request starts with "GET"
    if request.startswith("GET") or request.startswith("POST"):
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
        client_request = client_socket.recv(MAX_PACKET).decode()
        while '\r\n\r\n' not in client_request:
            client_request += client_socket.recv(MAX_PACKET).decode()
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print(resource)
            print("Got a valid HTTP request")
            handle_client_request(resource, client_request, client_socket)
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
                client_socket.settimeout(SOCKET_TIMEOUT)
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
    demo_req = "WEB-ROOTS/calculate-next?num=2"

    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)

        # Log setup #
    logging.basicConfig(level=LOG_LEVEL, filename=LOG_FILE, format=LOG_FORMAT)

    # Asserts
    assert build_http(location="/index.html") == http_test_example, "build_http - not working"
    assert get_query_params(demo_req) == {"num": "2"}
    assert calculate_next(b"2") == "3"
    assert calculate_next(b"b") == ERR_NUMBER_CONVERTION

    # Call the main handler function
    main()
