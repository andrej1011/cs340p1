import sys
import socket
import re

def simpleserver(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', int(port)))

    server.listen(6)

    while True:
        client, addr = server.accept()
        #KLIJENTOV UPIT
        rqst = client.recv(2048).decode()
        response_code=0
        path = ''
        match = re.search(r'GET (.*) (.*)',rqst)
        if match:
            path =match.group(1)
        else:
            response_code = 400
        #TRAZIMO FAJL
        print(path)
        try:
            fin = open('files'+path)
            content = fin.read()
            fin.close()
            response_code = 200
        except FileNotFoundError:
            response_code = 404
        if not (path.endswith(('.htm','.html'))):
            response_code = 403
        #ODGOVOR KLIJENTU
        header = 'HTTP/1.0 '
        body = ''
        if(response_code==200):
            header += '200 OK'
            body = content
        elif(response_code==404):
            header += '404 Not Found'
            body = "<html><body><h1>404 Not Found</h1><p>Localhost on ANDREJ'S MACHINE</p></body></html>"
        elif (response_code == 403):
            header += '403 Forbidden'
            body = "<html><body><h1>403 Forbidden</h1><p>Localhost on ANDREJ'S MACHINE</p></body></html>"
        elif(response_code==400):
            header += '400 Bad Request'
            body = "<html><body><h1>400 Bad Request</h1><p>Localhost on ANDREJ'S MACHINE</p></body></html>"
        elif(response_code==0):
            header += '500 Internal Server Error'
            body = "<html><body><h1>500 Internal Server Error</h1><p>Localhost on ANDREJ'S MACHINE</p></body></html>"
        header+=f"\nContent-Type: text/html\nContent-Length:{len(body)}\nConnection: Closed"
        answer = header+"\r\n\r\n"+body
        client.send(answer.encode())
        client.close()
    server.close()



    #EXAMPLE OF HTTP REQUEST
    #GET /indsex.html HTTP/1.0
    #Host: localhost

if __name__ == '__main__':
    if (len(sys.argv) != 2):
        sys.stderr.write("Arguments not correct.")
        sys.exit(1)
    simpleserver(sys.argv[1])
    sys.exit(0)