import sys
import socket
import re #REGEX to find status-code and content-type

redirect_hell = 0
def clientf(url):
    protocol, host, port, path = urlparser(url)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # TCP Connection with server
    client.connect((host, int(port)))

    simple_client(client, path,host)

    # EXIT THE CONNECTION
    client.close()

def simple_client(client, path, host):

    # GET REQUEST
    request = f"GET /{path} HTTP/1.0\r\nHost: {host}\r\n\r\n"
    client.sendall(request.encode())

    # RECEIVE DATA
    response = b""
    while True:
        chunk = client.recv(4096)
        if not chunk:
            break
        response += chunk
    try:
        response = response.decode('utf-8')
    except UnicodeDecodeError:
        response = response.decode('latin-1')
    except Exception as e:
        sys.stderr.write(f"Error at decoding: {e}")
        client.close()
        sys.exit(1)

    index = response.find("\r\n\r\n")


    #NOW WE WORK WITH HEADDATA
    bodydata = response[index + 4:]
    headdata = response[:index]
    stcode=status_code_getter(headdata)
    if(stcode == 200):
        if(content_type(headdata))=="text/html":
            print(f"{bodydata}")
            client.close()
            sys.exit(0)
        else:
            print(content_type(headdata))
            sys.stderr.write("Content-Type is NOT text/html")
            client.close()
            sys.exit(1)
    if(stcode >=400):
        sys.stderr.write("Error code: "+str(stcode))
        print(f"{bodydata}")
        client.close()
        sys.exit(1)
    if(stcode ==301 or stcode ==302):
        global redirect_hell
        redirect_hell+=1
        if(redirect_hell>10):
            sys.stderr.write("Too many redirects")
            client.close()
            sys.exit(1)
        else:
            newurl =redirected_to(headdata)
            print(f"REDIRECTED TO: {newurl}")
            clientf(newurl)


    else:
        sys.stderr.write("Error code: " + str(stcode))
        client.close()
        sys.exit(1)



def urlparser(url):

    #PROTOCOL DRILLING
    protocol_index = url.find("://")
    if protocol_index == -1:
        sys.stderr.write("URL has to start with http://.\n")
        sys.exit(1)
    protocolused = url[:protocol_index]
    if (protocolused == "https"):
        sys.stderr.write("Can't work with HTTPS.\n")
        sys.exit(1)
    if(protocolused != "http"):
        sys.stderr.write("Protocol has to be HTTP\n")
        sys.exit(1)

    #PATH DRILLS
    path_index = url.find("/", protocol_index+3)
    if path_index == -1:
        path = ""
        path_index = len(url)-1
    else:
        path = url[path_index+1:]

    portindex = url.find(":", protocol_index+3, path_index-1)

    if(portindex == -1):
        port = 80
        portindex = path_index

    else:
        port = url[portindex+1:path_index]
    host = url[protocol_index+3:portindex]
#
#    print("Protocol: "+protocolused)
#    print("Port: "+str(port))
#    print("Host: "+str(host))
#    print("Path: "+str(path))
    return protocolused, host, port, path
def status_code_getter(headdata):
    match = re.search(r"HTTP/\d\.\d\s(\d{3})\s", headdata)
    if match:
        return int(match.group(1))
    else:
        sys.stderr.write("Can't get HTTP response code\n.")
        sys.exit(1)
def redirected_to(headdata):
    match = re.search(r"Location: (\S+)", headdata)

    if match:
        location_url = match.group(1)
        return location_url
    return None
def content_type(headdata):
    match = re.search(r"Content-Type:\s*([^;\s]+)(?:;\s*(.*))?", headdata, re.IGNORECASE)

    if match:
        location_url = match.group(1)
        return location_url
    return "fakeredirect"
if __name__ == '__main__':
    # Check if sysargv is done correctly
    if (len(sys.argv) != 2):
        sys.stderr.write("Arguments not correct.")
        sys.exit(1)
    clientf(sys.argv[1])
    sys.exit(0)
