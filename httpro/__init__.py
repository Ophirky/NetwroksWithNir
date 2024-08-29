"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 15/03/24
    DESCRIPTION: HTTP protocol package. Includes (http_ophir parser and formatter, http_ophir request builder)
"""

import http_ophir.constants as consts
import http_ophir.http_parser
import http_ophir.http_message


def http_auto_tests() -> None:
    """
    Function that contains all the auto_checks for the http_ophir package
    :return: None
    """
    http_parser.auto_test_http_parser()
    http_message.auto_test_http_message()

    # is_valid_request auto tests #
    request: bytes = b"GET /index.html HTTP/1.1\r\nHost: 192.168.37.45\r\n\r\n"
    request_invalid: bytes = b"GET /index.html HTTP/1.1\r\nHost:192.168.37.45\r\n\r\n"
    assert is_valid_request(request)["valid"], is_valid_request(request)["reason"]
    assert not is_valid_request(request_invalid)["valid"]


def is_valid_request(request: bytes) -> dict[bool, str] or dict[bool]:
    """
    Checks if a http_ophir request is valid.
    :param request: the request to validate.
    :return dict[bool, string]: {"valid": True/False, "reason":"reason"}
    """
    # Making sure that the argument is correct #
    if not isinstance(request, bytes):
        return {"valid": False, "reason": "request data type must be bytes"}

    # Split the request into lines #
    lines = request.decode('utf-8').split('\r\n')

    # Check if there's at least one line (the request line) and a blank line separating headers and body #
    if len(lines) < 2 or b'\r\n\r\n' not in request:
        return {"valid": False, "reason": "At least one line (the request line) and a blank line separating headers "
                                          "and body are needed."}

    # Check the request line for the correct number of elements and separators #
    request_line_parts = lines[0].split(' ')
    if len(request_line_parts) < 3:
        return {"valid": False, "reason": "Incorrect number of elements or separators."}

    # Ensure method, path, and HTTP version are correctly separated #
    method, path, version = request_line_parts[0], request_line_parts[1], request_line_parts[-1]
    if method.encode() not in consts.REQUEST_TYPES.values():
        return {"valid": False, "reason": f"{method} is not a real method in http_ophir."}

    # Check if the request has a http_ophir version #
    if not method or not path or not version.startswith('HTTP/'):
        return {"valid": False, "reason": "Request must have http_ophir version."}

    # Check headers for correct formatting
    is_host_header = False
    for header in lines[1:-2]:  # Ignoring the request line and the last two elements (the last header and the body)
        if ': ' not in header:
            return {"valid": False, "reason": f"{header} header does not contain colon-space separator."}
        if "Host" in header:
            is_host_header = True  # Mandatory host header is in the request

    # Check if the request has mandatory host header #
    if not is_host_header:
        return {"valid": False, "reason": "Host header is mandatory."}

    # Return true if the request is valid #
    return {"valid": True}
