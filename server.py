"""
 HTTP Server
 Author: Daniel Ben-Bassat
 Purpose: Ex. 4- HTTP server
"""
import socket
import logging
import os

# CONSTANTS
LOG_FORMAT = '%(levelname)s | %(asctime)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/server.log'


QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 2

ERR_BAD_REQUEST = b'HTTP/1.1 400 BAD REQUEST\r\n'
ERR_PAGE_NOT_FOUND = b'HTTP/1.1 404 Not Found\r\n'

FORBIDDEN_URL = "/forbidden"
FORBIDDEN_RESPONSE = b'HTTP/1.1 403 Forbidden\r\n'
ERROR_500_URL = "/error"
ERR0R_500_RESPONSE = b'HTTP/1.1 500 INTERNAL SERVER ERROR\r\n'


DEFAULT_URL = r"/index.html"
WEBROOT = r"C:/work/cyber/p4/webroot"


FILES_TYPES = {
    "html": "text/html;charset=utf-8",
    "jpg": "image/jpeg",
    "css": "text/css",
    "js": "text/javascript; charset=UTF-8",
    "txt": "text/plain",
    "ico": "image/x-icon",
    "gif": "image/jpeg",
    "png": "image/png"}

REDIRECTION_DICTIONARY = {"/move": "/"}


def get_file_data(file_name):
    """
    Get data from file
    :param file_name: the name of the file
    :return: the file data in bites
    """
    try:
        with open(file_name, 'rb') as file:
            data = file.read()
    except FileNotFoundError:
        data = ERR_PAGE_NOT_FOUND
    return data


def handle_client_request(resource, client_socket):
    """
    Check the required resource, generate proper HTTP response and send
    to client
    :param resource: the required resource
    :param client_socket: a socket for the communication with the client
    :return: None
    """
    if resource in REDIRECTION_DICTIONARY:
        # if resource in REDIRECTION_DICTIONARY send 302 redirection response
        response = b'HTTP/1.1 302 Found\r\n'
        response += b'Location: ' + REDIRECTION_DICTIONARY[resource].encode() + b'\r\n\r\n'
        client_socket.sendall(response)
        logging.debug(response)
        return
    if resource == FORBIDDEN_URL:
        # SEND FORBIDDEN 403 RESPONSE
        client_socket.send(FORBIDDEN_RESPONSE)
        return
    if resource == ERROR_500_URL:
        # SEND ERROR 500 RESPONSE
        client_socket.send(ERR0R_500_RESPONSE)
        return

    if resource == '/' or resource == '':
        url = DEFAULT_URL
    elif os.path.exists(WEBROOT + resource):
        # check if file in webroot
        url = resource
    else:
        # send 404 not found
        client_socket.send(ERR_PAGE_NOT_FOUND)
        logging.debug(ERR_PAGE_NOT_FOUND)
        return

    # find type and make content type header
    url_list = url.split(".")
    file_type = url_list[-1]
    content_type = b'Content-Type: ' + FILES_TYPES[file_type].encode() + b'\r\n'

    # read the data from the file and make content length header
    filename = WEBROOT + url
    data = get_file_data(filename)
    if data != ERR_PAGE_NOT_FOUND:
        content_length = b'Content-Length: ' + str(len(data)).encode() + b'\r\n\r\n'

        http_header = b"HTTP/1.1 200 OK\r\n" + content_type + content_length
        http_response = http_header + data
        client_socket.send(http_response)
        logging.debug(http_header)
        return
    else:
        # send 404 file not found
        client_socket.send(data)
        return


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and
    the requested URL
    :param request: the request which was received from the client
    :return: a tuple of (True/False - depending if the request is valid,
    the requested resource )
    """
    is_valid = True
    try:
        if request[0:4] != "GET ":
            is_valid = False

        url_start_index = 4
        url_end_index = request.find(" ", url_start_index)
        if url_end_index == -1:
            is_valid = False

        url = request[url_start_index:url_end_index]

        if request[url_end_index + 1:url_end_index + 9] != "HTTP/1.1":
            is_valid = False

        if request[url_end_index + 9:url_end_index + 11] != "\r\n":
            is_valid = False

    except IndexError:
        is_valid = False

    finally:
        if not is_valid:
            url = ERR_BAD_REQUEST
        return is_valid, url


def handle_client(client_socket):
    """
    Handles client requests: verifies client's requests are legal HTTP, calls
    function to handle the requests
    :param client_socket: the socket for the communication with the client
    :return: None
    """
    print('Client connected')
    while True:
        try:
            client_request = client_socket.recv(1)
            while True:
                if b'\r\n\r\n' in client_request or client_request == b'':
                    break
                client_request += client_socket.recv(1)
            client_request = client_request.decode()

            valid_http, resource = validate_http_request(client_request)
            if valid_http:
                print(resource)
                logging.debug('Got a valid HTTP request')
                logging.debug("url: " + resource)
                handle_client_request(resource, client_socket)
            else:
                # send 400 bad request
                client_socket.send(resource)
                logging.debug('Error: Not a valid HTTP request')
                break
        except socket.error as err:
            print('received socket exception - ' + str(err))
            break
    print('Closing connection')


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
    assert isinstance(DEFAULT_URL, str)
    assert isinstance(WEBROOT, str), "WEBROOT should be a string"
    assert isinstance(PORT, int)
    assert isinstance(IP, str)
    assert isinstance(REDIRECTION_DICTIONARY, dict)
    assert isinstance(FILES_TYPES, dict)
    assert isinstance(ERR_PAGE_NOT_FOUND, bytes)
    assert isinstance(ERR_BAD_REQUEST, bytes)
    assert isinstance(FORBIDDEN_RESPONSE, bytes)
    assert isinstance(ERR0R_500_RESPONSE, bytes)

    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)
    main()
