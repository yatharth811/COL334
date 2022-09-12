from multiprocessing import Lock
from socket import *
import threading
import pickle


def splitwise(s, split_sz):
    a = []
    for i in range(0, len(s), split_sz):
        a.append(s[i:i+split_sz])

    return a

def ceil(a, b):
    return (a+b-1)//b



IP = gethostbyname(gethostname())
PORT = 5050
ADDR = (IP, PORT)
HEADER = 2048
FORMAT = 'utf-8'
COUNT = 2
CACHE = []
CLIENTS = [None]*COUNT

server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)

lock = threading.Lock()


sw = "abcdefghij"
chunk = splitwise(sw, 2)
# print(chunk, len(chunk))
chunks = splitwise(chunk, ceil(len(chunk), COUNT))
# print(chunks)


def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')
    connected = True
    while(connected):

        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if (msg[0:2] == '#R'):
                chunkid = int(msg[2:])
                data = pickle.dumps(chunk[chunkid])
                conn.send(data)

            elif (msg[0] == '#'):
                clientid = int(msg[1:])
                data = pickle.dumps([len(chunk), chunks[clientid]])
                conn.send(data)
                CLIENTS[clientid] = conn

            if (msg == '!DISCONNECT'):
                connected = False
    
    conn.close()

def start():
    server.listen() 
    print(f'[LISTENING] Server is listening on {IP}:{PORT}')
    while(True):
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        # print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}') 
        # print(CLIENTS)
        

print('Server is starting..')
start()



