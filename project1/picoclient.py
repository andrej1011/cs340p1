import socket
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(sys.argv[1])
client.connect(('localhost', port))
request = f'''GET /webpage1.html HTTP/1.1
Host: localhost:1025
User-Agent: homemade/8.13.0
Accept: */*'''
client.send(request.encode())
print(client.recv(1024).decode())
client.close()
sys.exit(0)