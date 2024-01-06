"""
 HTTP Server Shell
 Author: Barak Gonen and Nir Dweck
 Purpose: Provide a basis for Ex. 4
 Note: The code is written in a simple way, without classes, log files or
 other utilities, for educational purpose
 Usage: Fill the missing functions and constants
"""


# TODO: import modules
import socket
import logging
import os
# TODO: set constants

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/server.log'

DEFAULT_URL = r"index.html"
FILES_TYPES = {
    "html": "text/html;charset=utf-8",
    "jpg": "image/jpeg",
    "css": "text/css",
    "js": "text/javascript; charset=UTF-8",
    "txt":"text/plain",
    "ico":"image/x-icon",
    "gif":"image/jpeg",
    "png":"image/png"
}
ERR_BAD_REQUEST = "400 BAD REQUEST"
ERR_PAGE_NOT_FOUND = "404 PAGE NOT FOUND"
QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 2

REDIRECTION_DICTIONARY = (
    "CSS/doremon.css",
    "imgs/abstract.jpg",
    "imgs/favicon.ico",
    "imgs/loading.gif",
    "js/box.js",
    "js/jquery.min.js",
    "js/submit.js",
    "uploads/",  # Added trailing slash to indicate a folder
    "index.html",
)


def get_file_data(file_name):
    """
    Get data from file
    :param file_name: the name of the file
    :return: the file data in a string
    """


def handle_client_request(resource, client_socket):
    """
    Check the required resource, generate proper HTTP response and send
    to client
    :param resource: the required resource
    :param client_socket: a socket for the communication with the client
    :return: None
    """
    """ """
    # TODO: add code that given a resource (URL and parameters) generates
    # the proper response
    if resource == '' or resource == '/':
        url = DEFAULT_URL
    else:
        url = resource

    # TODO: check if url had been redirected, not available or other error
    # code. For example:
    if url in REDIRECTION_DICTIONARY:
        pass
    else:
        return ERR_PAGE_NOT_FOUND

        # TODO: send 302 redirection response

    # TODO: extract requested file tupe from URL (html, jpg etc)
    file_type=
    if file_type == 'html':
        http_header = "" # TODO: generate proper HTTP header
    elif file_type == 'jpg':
        http_header =""  # TODO: generate proper jpg header
    # TODO: handle all other headers

    # TODO: read the data from the file
    data = get_file_data(filename)
    # http_header should be encoded before sended
    # data encoding depends on its content. text should be encoded, while files shouldn't
    http_response = http_header.encode() + data
    client_socket.send(http_response)


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and
    the requested URL
    :param request: the request which was received from the client
    :return: a tuple of (True/False - depending if the request is valid,
    the requested resource )
    """
    is_valid = True
    if request[0:4] != "GET ":
        is_valid = False

    url_start_index = 4
    url_end_index = request.find(" ", url_start_index)
    if url_end_index == -1:
        is_valid = False

    url = request[url_start_index:url_end_index]
    if url == "":
        is_valid = False

    print(url)
    if request[url_end_index + 1:url_end_index + 9] != "HTTP/1.1":
        is_valid = False

        #if request[9:13] != "\r\n":
        is_valid = False

    if not is_valid:
        url = ERR_BAD_REQUEST

    return (is_valid, url)


def handle_client(client_socket):
    """
    Handles client requests: verifies client's requests are legal HTTP, calls
    function to handle the requests
    :param client_socket: the socket for the communication with the client
    :return: None
    """
    print('Client connected')
    while True:
        # TODO: insert code that receives client request

        client_request = client_socket.recv(1024).decode()
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            logging.debug(resource)
            #handle_client_request(resource, client_socket)
        else:
            print('Error: Not a valid HTTP request')
            break
    #print('Closing connection')


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
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    # Call the main handler function
    #Http://127.0.0.1:80
    main()